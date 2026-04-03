import click
from app.engines import SUPPORTED_ENGINES
from app.utils.file_manager import get_backup_path
from app.utils.logger import logger
from app.storage.s3 import S3Storage
from app.utils.notifier import send_slack_notification
from dotenv import load_dotenv

# 1. Load environment variables from .env file
load_dotenv()

@click.group()
def cli():
    """Database Backup Utility CLI"""
    pass

@cli.command()
@click.option('--host', envvar='DB_HOST', show_envvar=True, help='Database host')
@click.option('--port', envvar='DB_PORT', show_envvar=True, help='Database port')
@click.option('--user', envvar='DB_USER', show_envvar=True, required=True, help='Database username')
@click.option('--password', envvar='DB_PASSWORD', show_envvar=True, required=True, help='Database password', hide_input=True)
@click.option('--dbname', envvar='DB_NAME', show_envvar=True, required=True, help='Database name')
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
@click.option('--host', envvar='DB_HOST', default='127.0.0.1', help='Database host')
@click.option('--port', envvar='DB_PORT', default=5432, help='Database port')
@click.option('--user', envvar='DB_USER', required=True, help='DB User')
@click.option('--password', envvar='DB_PASSWORD', required=True, help='Database password', hide_input=True)
@click.option('--dbname', envvar='DB_NAME', required=True, help='Database name')
@click.option('--s3-bucket', envvar='AWS_S3_BUCKET', show_envvar=True, help='S3 Bucket')
@click.option('--aws-key', envvar='AWS_ACCESS_KEY', show_envvar=True, help='AWS Key')
@click.option('--aws-secret', envvar='AWS_SECRET_KEY', show_envvar=True, help='AWS Secret')
@click.option('--aws_region', envvar='AWS_REGION', default='eu-north-1')
def backup(host, port, user, password, dbname, s3_bucket, aws_key, aws_secret, aws_region):
    """Run a backup using .env defaults or manual flags."""
    output_path = get_backup_path(dbname)

    # Validation: Ensure we have the basics
    if not all([user, password, dbname]):
        click.secho("❌ Error: Missing DB credentials. Set them in .env or use flags.", fg='red')
        return

    # Log the start of the operation
    logger.info(f"Initiating backup for database: {dbname} (Host: {host})")
    click.echo(f"📦 Starting compressed backup for '{dbname}'...")
    
    # Database backup logic
    engine_class = SUPPORTED_ENGINES.get("postgres")
    engine = engine_class(host, port, user, password, dbname)
    success, message = engine.backup(output_path)

    if not success:
        logger.error(f"Backup Failed: {message}")
        click.secho(f"❌ {message}", fg='red')
        return
    
    logger.info(f"Backup successful: {message}")
    click.secho(f"✅ Local backup completed: {output_path}", fg='green')

    # S3 Upload logic
    if s3_bucket and aws_key and aws_secret:
        click.echo(f"☁️  Uploading to S3 bucket '{s3_bucket}'...")
        s3 = S3Storage(s3_bucket, aws_key, aws_secret, aws_region)
        s3_success, s3_message = s3.upload_file(output_path)    

        if s3_success:
            logger.info(f"S3 Upload Success: {s3_message}")
            click.secho(f"🚀 Cloud Upload Complete: {s3_message}", fg='cyan')
        else:
            logger.error(f"S3 Upload Failed: {s3_message}")
            click.secho(f"⚠️  Cloud Upload Failed: {s3_message}", fg='yellow')

        # Send Slack notification
        if s3_success:
            msg = f"Backup successful: {dbname}\nS3: {s3_message if s3_bucket else 'Local only'}"
            send_slack_notification(msg, success=True)
            click.secho("🔔 Slack notification sent.", fg='green')
        else:
            msg = f"Backup failed for {dbname}\nError: {s3_message}"
            send_slack_notification(msg, success=False)
            click.secho(f"🔔 {message}.", fg='red')

if __name__ == '__main__':
    cli()