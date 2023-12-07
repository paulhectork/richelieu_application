import click

from app.app import app
from app.utils.io import maketmp, deltmp, write_credfile, read_credfile


@click.command()
@click.option("--database", "-d"
              , type=click.Choice(["local", "remote"])
              , help="a key pointing to the credentials and database to use"
              , required=True)
def run(database:str) -> None:
    """
    run the app
    """
    maketmp()
    write_credfile(database)
    app.run(port=5000, debug=True)


if __name__ == "__main__":
    run()

