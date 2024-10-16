import traceback
import atexit
import click

from app.app import config_app
from app.utils.io import maketmp, deltmp # , write_credfile, read_credfile
from app.tests.runner import runner

@click.command()
@click.option( "--mode", "-m"
             , type=click.Choice(["dev", "test", "prod"])
             , help="choose the app configuration: database connexion and other parameters. see `app/config.py`"
             , required=True)
def run(mode:str) -> None:
    """
    configure and run the backend app
    """
    maketmp()  # create necessary files/dirs

    app = config_app(mode)
    if mode == "test":
        runner()
    else:
        # the try...except + app.logger allows to display
        # errors in the production env's journals
        try:
            debug = True if mode != "prod" else False  # disable debug mode in prod 
            app.run(port=5001, debug=debug)
        except Exception as e:
            app.logger.error(traceback.format_exc())
            raise e  # so far, we want the site to crash so we can find possible exceptions

    return


if __name__ == "__main__":
    run()

