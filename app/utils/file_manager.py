import os
from datetime import datetime

def get_backup_path(db_name, extension="sql.gz"):
    """Generates a timestamped path: backups/db_name_20260309_143005.sql.gz"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{db_name}_{timestamp}.{extension}"
    
    # Ensure the 'backups' directory exists
    os.makedirs("backups", exist_ok=True)
    
    return os.path.join("backups", filename)