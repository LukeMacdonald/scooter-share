import requests

def fetchAllScooters():
    pass
def fetchAllReportedScooters():
    response = requests.get("http://localhost:5000/scooters/maintenance", timeout=5)
    return response.json()
def updateScooterStatus():
    pass

def fetchEngineerData(request, options):
    if request == "locations":
       return fetchAllReportedScooters() 
    elif request  == "report-repair":
        print("Engineering is reporting repair")
    elif request == 'scooters-info':
        print("Fetching all scooter information") 