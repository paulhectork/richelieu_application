import atexit
import click

from app.utils.io import maketmp, deltmp, write_credfile, read_credfile


@click.command()
@click.option("--database", "-d"
              , type=click.Choice(["local", "remote"])
              , help="a key pointing to the credentials and database to use"
              , required=True)
def run(database:str) -> None:
    """
    configure and run  the backend app
    """
    try:
        maketmp()                       # create necessary files/dirs
        write_credfile(database)        # write the credential file to use
        from app.app import app         # avoid import errors
        app.run(port=5000, debug=True)  # run the app
    finally:
        atexit.register(deltmp)         # delete temp files at exit, or exception

    return


if __name__ == "__main__":
    run()

