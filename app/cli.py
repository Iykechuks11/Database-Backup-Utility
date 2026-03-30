import click
from app.engines.postgres import PostgresEngine

@click.group()
def cli():
    """Database Backup Utility CLI"""
    pass

@cli.command()
@click.option('--host', default='127.0.0.1', help='Database host')
@click.option('--port', default=5432, help='Database port')
@click.option('--user', required=True, help='Database username')
@click.option('--password', required=True, help='Database password', hide_input=True)
@click.option('--dbname', required=True, help='Database name')

def check(host, port, dbname, user, password):
    """Test the connection to the database."""
    click.echo(f"Checking connection to {dbname} on {host}...")

    engine = PostgresEngine(host, port, user, password, dbname)
    success, message = engine.test_connection()
    
    if success:
        click.secho(f"Success: {message}", fg='green')
    else:
        click.secho(f"Failed: {message}", fg='red')

if __name__ == '__main__':
    cli()