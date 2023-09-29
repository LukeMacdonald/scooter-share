"""
Module for loading environment variables from a .env file.
"""
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Define variables with the loaded environment variables
HOST = os.getenv("DB_HOST")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
NAME = os.getenv("DB_NAME")
