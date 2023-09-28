import requests

def fetchAllScooters():
    pass
def fetchAllReportedScooters():
    response = requests.get("http://localhost:5000/scooters/maintenance", timeout=5)
    return response.json()
def updateScooterStatus(scooterID):
    response = requests.get(f"http://localhost:5000/scooters/{scooterID}", timeout=5)
    user = response.json();
    user["status"] = "available"
    response = requests.put(f"http://localhost:5000/scooters/{scooterID}",json=user)
    return user

def fetchEngineerData(request, options):
    if request == "locations":
       return fetchAllReportedScooters() 
    elif request  == "repair-fixed":
        print(options)
        return updateScooterStatus(options["id"])
    elif request == 'scooters-info':
        print("Fetching all scooter information") 