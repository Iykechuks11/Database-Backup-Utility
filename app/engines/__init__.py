# app/engines/__init__.py

# from .base import BaseEngine 
from .postgres import PostgresEngine

SUPPORTED_ENGINES = {
    "postgres": PostgresEngine,
}