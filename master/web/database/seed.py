from master.web.database.models import Scooter, db  # Import Scooter locally

def seedData():
    scooterData()

def scooterData():
    if not Scooter.query.first():

        # Create and add scooters to the database session
        scooter1 = Scooter(
            Make="Scooter Make 1",
            Longitude=123.456789,
            Latitude=45.678901,
            RemainingPower=75.5,
            CostPerTime=10.99,
            Status="available"
        )

        scooter2 = Scooter(
            Make="Scooter Make 2",
            Longitude=123.789012,
            Latitude=45.123456,
            RemainingPower=85.0,
            CostPerTime=9.99,
            Status="occupying"
        )

        scooter3 = Scooter(
            Make="Scooter Make 3",
            Longitude=124.567890,
            Latitude=46.789012,
            RemainingPower=50.25,
            CostPerTime=12.50,
            Status="maintenance"
        )

        # Add the scooters to the session and commit the changes to the database
        db.session.add(scooter1)
        db.session.add(scooter2)
        db.session.add(scooter3)
        db.session.commit()