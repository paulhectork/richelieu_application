import atexit
import click

from app.utils.io import maketmp, deltmp, write_credfile, read_credfile
from app.tests.load_tests import load_tests

@click.command()
@click.option( "--database", "-d"
             , type=click.Choice(["local", "server"])
             , help="a key pointing to the credentials and database to use"
             , required=True)
@click.option( "--test", "-t"
             , is_flag=True
             , default=False
             , help="run test")

def run(database:str, test:bool) -> None:
    """
    configure and run  the backend app
    """
    try:
        maketmp()                       # create necessary files/dirs
        write_credfile(database)        # write the credential file to use

        if test:
            print("hiii")
            load_tests().run()

        from app.app import app         # avoid import errors
        app.run(port=5000, debug=True)  # run the app
    finally:
        atexit.register(deltmp)         # delete temp files at exit, or exception

    return


if __name__ == "__main__":
    run()

