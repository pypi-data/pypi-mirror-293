import click

from .apply.extractsiriusdata import extract_sirius_data
from .apply.loaduserdata import load_user_data
from .apply.runmodels import run_models

# from .apply.startapp import start_app
from .train.evaluatemodels import run_evaluation
from .train.providemodels import export_model


@click.group()
def main():
    """Check MLinvitroTox commands"""
    pass


main.add_command(extract_sirius_data)
main.add_command(load_user_data)
main.add_command(run_models)
# main.add_command(start_app)


@main.group("train")
def train():
    """Commands related to model training"""
    pass


train.add_command(run_evaluation)
train.add_command(export_model)

if __name__ == "__main__":
    main()
