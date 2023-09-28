import requests
from requests.exceptions import RequestException
from database.models import ScooterStatus

def fetch_reported_scooters():
    """
    Fetch a list of scooters reported for repair.

    Returns:
        dict: A dictionary containing the fetched data or an error message.
    """
    try:
        url = "http://localhost:5000/scooters/maintenance"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return {"data": response.json()}
    except RequestException as req_error:
        return {"error": f"{req_error}" }
    except ValueError as json_error:
        return {"error": f"JSON decoding error while processing response: {json_error}" }
    except Exception as error:
        return {"error": f"An unexpected error occurred: {error}" }

def update_scooter_status(scooterID):
    """
    Mark scooter as repaired by update its status as available.

    Args:
        scooterID (int): The ID of the scooter to update.

    Returns:
        dict: A dictionary containing the updated data or an error message.
    """
    try:
        
        scooter_url = f"http://localhost:5000/scooters/{scooterID}"
        response = requests.get(scooter_url, timeout=5)
        response.raise_for_status()
        scooter_data = response.json()

        scooter_data["status"] = ScooterStatus.AVAILABLE.value

        response = requests.put(scooter_url, json=scooter_data, timeout=5)
        response.raise_for_status()

        return {"data": response.json()}
    except RequestException as error:
        return {"error": f"An error occurred while updating scooter status: {error}" }
    except Exception as error:
        return {"error": f"An unexpected error occurred: {error}" }

def fetch_engineer_data(request, options):
    """
    Fetch engineer-related data based on the request type.

    Args:
        request (str): The type of data request, e.g., "locations" or "repair-fixed".
        options (dict): Additional options or parameters for the request.

    Returns:
        dict: A dictionary containing the fetched data or an error message.
    """
    if request == "locations":
        return fetch_reported_scooters()
    elif request == "repair-fixed":
        return update_scooter_status(options["id"])
        