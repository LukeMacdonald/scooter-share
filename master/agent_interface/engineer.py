def fetchAllScooters():
    pass
def fetchAllReportedScooters():
    return {"data": "Looking for locations of all reported scooters"}
def updateScooterStatus():
    pass

def fetchEngineerData(request, options):
    if request == "locations":
       return fetchAllReportedScooters() 
    elif request  == "report-repair":
        print("Engineering is reporting repair")
    elif request == 'scooters-info':
        print("Fetching all scooter information") 