import typer

from .main import check as m_check
from .main import showtime as m_showtime

app = typer.Typer()


@app.command()
def check(filename: str) -> bool:
    """Check whether a KOMIS-FILE is readable and all frame types are available."""
    return m_check(filename)


@app.command()
def showtime(filename: str, out_dir_name: str = "out"):
    """Go. Generate the comic."""
    m_showtime(filename, out_dir_name)
