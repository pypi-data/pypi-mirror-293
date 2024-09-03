import click
from streamlit import config as _config
from streamlit.web.bootstrap import run


@click.command("app")
def start_app():
    """
    Start the app

    """

    _config.set_option("server.headless", True)
    run("./src/mlinvitrotox/app/Results.py", args=[], flag_options={}, is_hello=False)


if __name__ == "__main__":
    start_app()
