import subprocess
import os
import psycopg2 
from psycopg2 import OperationalError

class PostgresEngine:
    def __init__(self, host, port, user, password, db_name):
        self.config = {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'dbname': db_name
        }

    def test_connection(self):
        """Attempts to connect. Returns (True, None) if success, (False, Error) if fail."""
        try:
            # We add a 5-second timeout so it doesn't hang forever
            conn = psycopg2.connect(**self.config, connect_timeout=5)
            conn.close()
            return True, "Connection successful!"
        except OperationalError as e:
            return False, str(e)
        
    def backup(self, destination_path: str):
        """Executes pg_dump and saves the output to destination_path."""
        try:
            # Prepare the environment variable for the password
            env = os.environ.copy()
            env["PGPASSWORD"] = self.config['password']

            # Construct the command
            # -Fc: Custom archive format (compressed and flexible)
            command = [
                "pg_dump",
                "-h", self.config['host'],
                "-p", str(self.config['port']),
                "-U", self.config['user'],
                "-Fc",                   
                "-f", destination_path,  # Output file path
                self.config['dbname']
            ]

            # Run the command
            result = subprocess.run(
                command, 
                env=env, 
                capture_output=True, 
                text=True
            )

            if result.returncode == 0:
                return True, f"Backup created: {destination_path}"
            else:
                return False, f"pg_dump error: {result.stderr}"

        except Exception as e:
            return False, f"Unexpected error: {str(e)}"

