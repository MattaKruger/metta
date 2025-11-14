import typer
from path import Path


app = typer.Typer()


@app.command()
def list_files(directory: str, limit: int = 0, offset=0):
    files = Path(directory)
    print(files)


if __name__ == "__main__":
    app()
