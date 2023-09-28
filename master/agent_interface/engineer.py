import requests
from requests.exceptions import RequestException
from master.web.database.models import ScooterStatus

def fetchAllReportedScooters():
    try:
        url = "http://localhost:5000/scooters/maintenance"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return {"data": response.json()}
    except RequestException as req_error:
        return {"error": f"Request error while fetching reported scooters: {req_error}" }
    except ValueError as json_error:
        return {"error": f"JSON decoding error while processing response: {json_error}" }
    except Exception as error:
        return {"error": f"An unexpected error occurred: {error}" }

def updateScooterStatus(scooterID):
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

def fetchEngineerData(request, options):
    if request == "locations":
        return fetchAllReportedScooters()
    elif request == "repair-fixed":
        return updateScooterStatus(options["id"])
        