from typing import Annotated, Optional

import typer
from python_sdk.conf.logger import LogLevel

cli = typer.Typer(help="CLI tool", add_completion=True, no_args_is_help=True)


@cli.command(name="test", help="Run unit tests.")
def test() -> None:
    import pytest

    from src.conf import settings

    pytest.main([str(settings.base_dir / "tests"), "-vv", "--cov"])
    exit(0)



@cli.command(name="shell", help="Run the Python shell.")
def shell() -> None:
    import IPython

    IPython.start_ipython(argv=[])


@cli.command(name="run", help="Run the background worker.")
def run(
        host: Annotated[Optional[str], typer.Option("-h", "--host", help="Host to bind to.")] = "0.0.0.0",
        port: Annotated[Optional[int], typer.Option("-p", "--port", help="Port to bind to.")] = 3000,
        reload: Annotated[Optional[bool], typer.Option("-r", "--reload", is_flag=True, help="Enable "
                                                                                            "auto-reload.")] = False,
        workers: Annotated[int, typer.Option("-w", "--workers", help="Number of worker processes.")] = 1,
        log_level: Annotated[
            Optional[LogLevel], typer.Option("-l", "--log-level", help="Logging level.")] = LogLevel.INFO,

) -> None:
    from src.main import main

    main()


if __name__ == "__main__":
    import sys
    from pathlib import Path

    src_dir = Path.cwd() / "src"
    if str(src_dir) not in sys.path:
        sys.path.append(str(src_dir))
    cli()
