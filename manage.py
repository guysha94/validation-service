
import typer

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
def worker() -> None:
    from src.main import main

    main()


if __name__ == "__main__":
    import sys
    from pathlib import Path

    src_dir = Path.cwd() / "src"
    if str(src_dir) not in sys.path:
        sys.path.append(str(src_dir))
    cli()
