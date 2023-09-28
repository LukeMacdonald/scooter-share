from master.web.database.models import Scooter, db  # Import Scooter locally

def seedData():
    scooterData()

def scooterData():
    if not Scooter.query.first():
        scooter_data = [
            {
                "CostPerTime": 10.99,
                "Latitude": -37.8136,
                "Longitude": 144.963,
                "Make": "Scooter Make 1",
                "RemainingPower": 75.5,
                "Status": "available"
            },
            {
                "CostPerTime": 9.99,
                "Latitude": -37.815,
                "Longitude": 144.978,
                "Make": "Scooter Make 2",
                "RemainingPower": 85.0,
                "Status": "occupying"
            },
            {
                "CostPerTime": 12.5,
                "Latitude": -37.807,
                "Longitude": 144.981,
                "Make": "Scooter Make 3",
                "RemainingPower": 50.25,
                "Status": "maintenance"
            },
            {
                "CostPerTime": 10.99,
                "Latitude": -37.8078,
                "Longitude": 144.984,
                "Make": "Scooter Make 1",
                "RemainingPower": 75.5,
                "Status": "available"
            },
            {
                "CostPerTime": 9.99,
                "Latitude": -37.8183,
                "Longitude": 144.965,
                "Make": "Scooter Make 2",
                "RemainingPower": 85.0,
                "Status": "occupying"
            },
            {
                "CostPerTime": 12.5,
                "Latitude": -37.8072,
                "Longitude": 144.99,
                "Make": "Scooter Make 3",
                "RemainingPower": 50.25,
                "Status": "maintenance"
            }
        ]

        for data in scooter_data:
            scooter = Scooter(
                make=data["Make"],
                longitude=data["Longitude"],
                latitude=data["Latitude"],
                remaining_power=data["RemainingPower"],
                cost_per_time=data["CostPerTime"],
                status=data["Status"]
            )

            # Add the scooter to the session
            db.session.add(scooter)

        # Commit the changes to the database
        db.session.commit()
