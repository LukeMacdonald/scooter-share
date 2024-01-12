import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
PUBLIC_HOST = os.getenv('PUBLIC_HOST', '0.0.0.0')
PRIVATE_HOST = os.getenv('PRIVATE_HOST', '127.0.0.1')
MASTER_PORT = int(os.getenv('MASTER_PORT', 5000))
AGENT_PORT = int(os.getenv('AGENT_PORT', 5001))
SOCKET_PORT = int(os.getenv('SOCKET_PORT', 63000))
