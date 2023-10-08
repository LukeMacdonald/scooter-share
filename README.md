# Scooter Share Application

This is an implementation of a scooter sharing application,
including a master server, agent web application and a scooter
control program. The scooter control program includes crash
detection, which records a scooter for repair when the scooter
experiences very high acceleration.

## Project Setup Instructions

First run `pip install -r requirements.txt` to install all
required dependencies, then run `python3 main.py` to start
the master and agent software. Connect to `https://localhost:5001`
to use the agent software (as customer or engineer) - note that
we use a self-signed certificate in order to get the location of
the user, which must be explicitly allowed in the web browser.
Connect to `http://localhost:5000` to use the master software
(as administrator).

## User Accounts Details

- Administrator: admin@gmail.com / admin
- Engineer: Lukemacdonald21@gmail.com / password
- Customer: customer1@gmail.com / password

(See `master/database/seed.py`.)

## Trello Screenshots
![Trello usage 1](https://github.com/COSC2764-2755/assignment-2-scooter-share-application-team-7/blob/main/Images/Trello%201.png)

![Trello usage 2](https://github.com/COSC2764-2755/assignment-2-scooter-share-application-team-7/blob/main/Images/Trello%202.png)

![Trello usage 3](https://github.com/COSC2764-2755/assignment-2-scooter-share-application-team-7/blob/main/Images/Trello%203.png)

![Trello usage 4](https://github.com/COSC2764-2755/assignment-2-scooter-share-application-team-7/blob/main/Images/Trello%204.png)

![Trello usage 5](https://github.com/COSC2764-2755/assignment-2-scooter-share-application-team-7/blob/main/Images/Trello%205.png)

## Contributions

- Chloe Harvey: Master server, agent app
- Luke MacDonald: Master server, agent app, testing
- Damon O'Malley: Agent protocol, agent app, testing
- Bailey Vogt: Master server, scooter control software


## Enchancements

Crash Detection:
    Our Scooters utilize crash detection, it works by
    utilizing the accelorometer on the sensehat, if the
    accel detects a force greater then 5g, which is typically
    considered the limit a human can handle on one moment,
    after the Scooter detects a crash it locks up the scooter
    and requests repair from the engineers.

### Github Usage
![Github usage 1](https://github.com/COSC2764-2755/assignment-2-scooter-share-application-team-7/blob/main/Images/Github%20usage%201.png)

![Github usage 2](https://github.com/COSC2764-2755/assignment-2-scooter-share-application-team-7/blob/main/Images/Github%20usage%202.png)

![Github usage 3](https://github.com/COSC2764-2755/assignment-2-scooter-share-application-team-7/blob/main/Images/Github%20usage%203.png)

### Project Structure
![Project Structure](https://github.com/COSC2764-2755/assignment-2-scooter-share-application-team-7/blob/main/Images/Structure.png)
