import click
from lum0x.handlers.credential_handler import authenticate_api_key
from lum0x.handlers.deploy_handler import deploy_lambda_function

@click.group()
def cli():
    pass

@cli.command()
def credential():
    """Authenticate API key."""
    authenticate_api_key()

@cli.command()
@click.argument('user_code_zip')
@click.argument('trigger_conf', required=False)
@click.option('--overwrite', is_flag=True, default=False, help="Flag to allow file overwrite.")
@click.option('--ondemand', is_flag=True, default=False, help="Deploy as on-demand function.")
def deploy(user_code_zip, trigger_conf, overwrite, ondemand):
    """Deploy user code with a Lambda handler."""
    deploy_lambda_function(user_code_zip, trigger_conf, overwrite, ondemand)

if __name__ == '__main__':
    cli()
