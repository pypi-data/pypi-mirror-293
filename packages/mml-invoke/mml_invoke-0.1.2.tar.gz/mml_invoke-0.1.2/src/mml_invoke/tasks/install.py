from invoke import task


@task
def dev_install(ctx) -> None:
    """
    install dev, docs and test packages

    Parameters
    ----------
    ctx: invoke context
    """
    ctx.run("poetry install --with test,dev,docs")
