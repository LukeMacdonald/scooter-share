from comms.client import Client

import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


def message_scooter(scooter_id, message):

    host = os.getenv(f"SCOOTER_HOST_{scooter_id}", "192.168.1.108")
    port = int(os.getenv("SCOOTER_PORT"))

    client = Client(host=host, port=port)

    return client.send_message(message)
