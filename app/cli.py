import click
from app.engines import SUPPORTED_ENGINES
from app.utils.file_manager import get_backup_path
from app.utils.logger import logger
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

    engine_class = SUPPORTED_ENGINES.get("postgres")
    engine = engine_class(host, port, user, password, dbname)
    success, message = engine.test_connection()
    
    if success:
        click.secho(f"Success: {message}", fg='green')
    else:
        click.secho(f"Failed: {message}", fg='red')

@cli.command()
@click.option('--host', default='127.0.0.1')
@click.option('--user', required=True)
@click.option('--password', required=True, hide_input=True)
@click.option('--dbname', required=True)
# @click.option('--output', default='backup.dump', help='Path to save the backup')
def backup(host, user, password, dbname):
    """Run a full backup of the PostgreSQL database."""
    # click.echo(f"Starting backup for {dbname}...")
    output_path = get_backup_path(dbname)

    # Log the start of the operation
    logger.info(f"Initiating backup for database: {dbname} (Host: {host})")
    click.echo(f"📦 Starting compressed backup for '{dbname}'...")
    
    engine_class = SUPPORTED_ENGINES.get("postgres")
    engine = engine_class(host, 5432, user, password, dbname)
    success, message = engine.backup(output_path)
    
    if success:
        click.secho(message, fg='green')
        logger.info(message)
    else:
        click.secho(message, fg='red')
        logger.info(message)

if __name__ == '__main__':
    cli()