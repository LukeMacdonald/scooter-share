import requests
from requests.exceptions import RequestException
from database.models import ScooterStatus, RepairStatus

def fetch_reported_scooters():
    """
    Fetch a list of scooters reported for repair.

    Returns:
        dict: A dictionary containing the fetched data or an error message.
    """
    try:
        url = "http://localhost:5000/scooters/awaiting-repairs"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return {"data": response.json()}
    except RequestException as req_error:
        return {"error": f"{req_error}" }
    except ValueError as json_error:
        return {"error": f"JSON decoding error while processing response: {json_error}" }
    except Exception as error:
        return {"error": f"An unexpected error occurred: {error}" }

def update_scooter_status(scooter_id, repair_id):
    """
    Mark scooter as repaired by updating its status as available.

    Args:
        scooter_id (int): The ID of the scooter to update.
        repair_id (int): The ID of the repair associated with the scooter.

    Returns:
        dict: A dictionary containing the response data or an error message.
    """
    try:
        fixed_url = f"http://localhost:5000/scooters/fixed/{scooter_id}/{repair_id}"
        response = requests.put(fixed_url, timeout=5)

        if response.status_code == 200:
            return {"message": "Scooter status updated successfully"}
        else:
            return {"error": f"Failed to update scooter status. Status code: {response.status_code}"}
    
    except RequestException as req_error:
        return {"error": f"Request error while updating scooter status: {req_error}"}
    except Exception as error:
        return {"error": f"An unexpected error occurred: {error}"}

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
        return update_scooter_status(options["id"],options["repair_id"])
        