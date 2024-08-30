import json
import os
import warnings
from typing import Any, Dict, Optional

from invoke import task

from ..utils import _get_file_hash, _get_file_size


def _get_data_dir(data_dir: Optional[str] = None) -> str:
    """Get tha path to a data dir and check if it has the right subfolders"""
    if data_dir is None:
        data_dir = os.path.join(os.getcwd(), "data")
        if not os.path.exists(data_dir):
            data_dir = os.getenv("DATA_DIR")
            if data_dir is None:
                raise FileNotFoundError(
                    "cannot find data directory; pass explicitly with -d/--data_dir"
                )
    elif not os.path.exists(data_dir):
        raise FileNotFoundError(f"cannot find directory {data_dir}")

    _data_dir_files = os.listdir(data_dir)
    if "raw" not in _data_dir_files:
        raise FileNotFoundError("raw directory not found in data_dir")
    if "curated" not in _data_dir_files:
        raise FileNotFoundError("curated directory not found in data_dir")
    if "ml_ready" not in _data_dir_files:
        raise FileNotFoundError("ml_ready directory not found in data_dir")

    return data_dir


def _get_raw_data_dir(data_dir: str) -> str:
    """Get the path to the raw data dir"""
    return os.path.join(data_dir, "raw")


def _get_curated_data_dir(data_dir: str) -> str:
    """Get the path to the curated data dir"""
    return os.path.join(data_dir, "curated")


def _get_ml_data_data_dir(data_dir: str) -> str:
    """Get the path to the ml_ready data dir"""
    return os.path.join(data_dir, "ml_ready")


def _lock_dir(dirpath: str) -> Dict[str, Dict[str, Any]]:
    """Given a data dir, generate its lock info"""
    files = [
        os.path.join(dirpath, f)
        for f in os.listdir(dirpath)
        if os.path.isfile(os.path.join(dirpath, f)) and not f.endswith(".lock")
    ]
    _lock: Dict[str, Dict[str, Any]] = dict()
    for file in files:
        _lock[os.path.basename(file)] = {
            "hash": _get_file_hash(os.path.join(dirpath, file)),
            "size": _get_file_size(os.path.join(dirpath, file)),
        }
    return _lock


@task
def lock_raw_data(ctx, data_dir: Optional[str] = None) -> None:
    """
    Lock the raw data directory

    Notes
    -----
    Lock file will be a json with a single element: "raw" that
    encodes the lock dictionary for the raw directory

    data_dir is optional. If you don't pass a specific data_dir it will
    look for in the CWD for a valid `data` folder (has all three subfolders)
    and then look in the @DATA_DIR environment variable

    Parameters
    ----------
    ctx:
        invoke context
    data_dir:
        path to data directory
        if None will look for it in CWD and then $DATA_DIR
    """
    data_dir = _get_data_dir(data_dir)

    dirpath = _get_raw_data_dir(data_dir)

    _lock = {
        "raw": _lock_dir(dirpath),
    }
    _lock_file = os.path.join(dirpath, "raw.lock")
    json.dump(_lock, open(_lock_file, "w"))
    print(f"saved lock file to {_lock_file}")


@task
def lock_curated_data(ctx, data_dir: Optional[str] = None) -> None:
    """
    Lock the curated data directory

    Notes
    -----
    Lock file will be a json with two elements:
    - "raw"; curated files are generated from raw files, so need to make sure these
             have not changed
    - "curated"; the lock dictionary for the curated directory

    data_dir is optional. If you don't pass a specific data_dir it will
    look for in the CWD for a valid `data` folder (has all three subfolders)
    and then look in the @DATA_DIR environment variable

    Parameters
    ----------
    ctx:
        invoke context
    data_dir:
        path to data directory
        if None will look for it in CWD and then $DATA_DIR
    """
    data_dir = _get_data_dir(data_dir)

    raw_dirpath = _get_raw_data_dir(data_dir)
    curated_dirpath = _get_curated_data_dir(data_dir)

    _lock = {
        "raw": _lock_dir(raw_dirpath),
        "curated": _lock_dir(curated_dirpath),
    }
    _lock_file = os.path.join(curated_dirpath, "curated.lock")
    json.dump(_lock, open(_lock_file, "w"))
    print(f"saved lock file to {_lock_file}")


@task
def lock_ml_ready_data(ctx, data_dir: Optional[str] = None) -> None:
    """
    Lock the ml_ready data directory

    Notes
    -----
    Lock file will be a json with two elements:
    - "curated"; ml_ready files are generated from curated files,
                 so need to make sure these have not changed
    - "ml_ready"; the lock dictionary for the curated directory

    data_dir is optional. If you don't pass a specific data_dir it will
    look for in the CWD for a valid `data` folder (has all three subfolders)
    and then look in the @DATA_DIR environment variable

    Parameters
    ----------
    ctx:
        invoke context
    data_dir:
        path to data directory
        if None will look for it in CWD and then $DATA_DIR
    """
    data_dir = _get_data_dir(data_dir)

    curated_dirpath = _get_curated_data_dir(data_dir)
    ml_ready_dirpath = _get_ml_data_data_dir(data_dir)

    _lock = {
        "curated": _lock_dir(curated_dirpath),
        "ml_ready": _lock_dir(ml_ready_dirpath),
    }
    _lock_file = os.path.join(ml_ready_dirpath, "ml_ready.lock")
    json.dump(_lock, open(_lock_file, "w"))
    print(f"saved lock file to {_lock_file}")


@task()
def lock_data(ctx, data_dir: Optional[str] = None) -> None:
    """
    Lock all data sub directories

    Parameters
    ----------
    ctx:
        invoke context
    data_dir:
        path to data directory
        if None will look for it in CWD and then $DATA_DIR
    """
    lock_raw_data(ctx, data_dir)
    lock_curated_data(ctx, data_dir)
    lock_ml_ready_data(ctx, data_dir)


class LockMismatch(Exception):
    """exception to be raised when a lock files doesn't match current files"""

    pass


def _check_lock(old_lock: Dict, new_lock: Dict) -> None:
    """
    Check to see if a lock file matches the new files

    Notes
    -----
    old_lock and new_lock should be for only a single sub_dir
    this is the output of _lock_dir
    lock files save locks for multiple dirs, make sure to extract them
    with `old_lock["raw"]`, for example.

    Parameters
    ----------
    old_lock: Dict
        the read lock file (for a single sub dir)
    new_lock: Dict
        a newly generated lock dict for the current file status

    Raises
    ------
    LockMismatch:
        when a old and new lock do not match

    Warnings
    --------
    UserWarning:
        if new files not in new lock are present, but lock is still valid
    """
    if old_lock != new_lock:
        old_files = set(old_lock.keys())
        new_files = set(new_lock.keys())

        if len(new_files - old_files) != 0:
            warnings.warn(
                f"found files not in current lock file: {new_files - old_files}\n"
                f"extra files should be locked or removed",
                stacklevel=1,
            )

        if len(old_files - new_files) != 0:
            raise LockMismatch(f"missing files found in lock file: {old_files - new_files}")

        for old_file in old_files:
            old_hash = old_lock[old_file]["hash"]
            new_hash = new_lock[old_file]["hash"]
            if old_hash != new_hash:
                raise LockMismatch(f"file {old_file} has different hash in lock file")
            old_size = old_lock[old_file]["size"]
            new_size = new_lock[old_file]["size"]
            if old_size != new_size:
                raise LockMismatch(f"file {old_file} has different size in lock file")


@task
def check_raw_data(ctx, data_dir: Optional[str] = None) -> None:
    """
    Checks the lock the raw data directory

    Parameters
    ----------
    ctx:
        invoke context
    data_dir:
        path to data directory
        if None will look for it in CWD and then $DATA_DIR

    Raises
    ------
    LockMismatch:
        when a old and new lock do not match

    Warnings
    --------
    UserWarning:
        if new files not in new lock are present, but lock is still valid
    """
    data_dir = _get_data_dir(data_dir)

    raw_dirpath = _get_raw_data_dir(data_dir)

    new_raw_lock = _lock_dir(raw_dirpath)

    old_raw_lock = json.load(open(os.path.join(raw_dirpath, "raw.lock"), "r"))

    _check_lock(old_raw_lock["raw"], new_raw_lock)
    print("raw data passed lock check")


@task
def check_curated_data(ctx, data_dir: Optional[str] = None) -> None:
    """
    Checks the lock the curated data directory

    Notes
    -----
    checks both the curated and raw data dirs, since curated data
    is generated by raw data. If there is a change in raw there should
    be a change in curated. Will fail if either mismatch

    Parameters
    ----------
    ctx:
        invoke context
    data_dir:
        path to data directory
        if None will look for it in CWD and then $DATA_DIR

    Raises
    ------
    LockMismatch:
        when a old and new lock do not match

    Warnings
    --------
    UserWarning:
        if new files not in new lock are present, but lock is still valid
    """
    data_dir = _get_data_dir(data_dir)

    raw_dirpath = _get_raw_data_dir(data_dir)
    curated_dirpath = _get_curated_data_dir(data_dir)

    new_raw_lock = _lock_dir(raw_dirpath)
    new_curated_lock = _lock_dir(curated_dirpath)

    old_curated_lock = json.load(open(os.path.join(curated_dirpath, "curated.lock"), "r"))

    _check_lock(old_curated_lock["raw"], new_raw_lock)
    _check_lock(old_curated_lock["curated"], new_curated_lock)
    print("curated data passed lock check")


@task
def check_ml_ready_data(ctx, data_dir: Optional[str] = None) -> None:
    """
    Checks the lock the ml_ready data directory

    Notes
    -----
    checks both the ml_ready and curated data dirs, since ml_ready data
    is generated by curated data. If there is a change in curated there should
    be a change in ml_ready. Will fail if either mismatch

    Parameters
    ----------
    ctx:
        invoke context
    data_dir:
        path to data directory
        if None will look for it in CWD and then $DATA_DIR

    Raises
    ------
    LockMismatch:
        when a old and new lock do not match

    Warnings
    --------
    UserWarning:
        if new files not in new lock are present, but lock is still valid
    """
    data_dir = _get_data_dir(data_dir)

    curated_dirpath = _get_curated_data_dir(data_dir)
    ml_ready_dirpath = _get_ml_data_data_dir(data_dir)

    new_curated_lock = _lock_dir(curated_dirpath)
    new_ml_ready_lock = _lock_dir(ml_ready_dirpath)

    old_ml_ready_lock = json.load(open(os.path.join(ml_ready_dirpath, "ml_ready.lock"), "r"))

    _check_lock(old_ml_ready_lock["curated"], new_curated_lock)
    _check_lock(old_ml_ready_lock["ml_ready"], new_ml_ready_lock)
    print("ml_ready data passed lock check")


@task()
def check_data(ctx, data_dir: Optional[str] = None) -> None:
    """
    Checks the lock the of all data directories

    Parameters
    ----------
    ctx:
        invoke context
    data_dir:
        path to data directory
        if None will look for it in CWD and then $DATA_DIR

    Raises
    ------
    LockMismatch:
        when a old and new lock do not match

    Warnings
    --------
    UserWarning:
        if new files not in new lock are present, but lock is still valid
    """
    check_raw_data(ctx, data_dir)
    check_curated_data(ctx, data_dir)
    check_ml_ready_data(ctx, data_dir)
