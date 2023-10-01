from __future__ import print_function
from datetime import datetime
from datetime import timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = "https://www.googleapis.com/auth/calendar"
store = file.Storage("token.json")
creds = store.get()
if(not creds or creds.invalid):
    flow = client.flow_from_clientsecrets("credentials.json", SCOPES)
    creds = tools.run_flow(flow, store)
service = build("calendar", "v3", http=creds.authorize(Http()))

def main():
    """
    Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user"s calendar.
    """

    # Call the Calendar API.
    now = datetime.utcnow().isoformat() + "Z" # "Z" indicates UTC time.
    print("Getting the upcoming 10 events.")
    events_result = service.events().list(calendarId = "primary", timeMin = now,
        maxResults = 10, singleEvents = True, orderBy = "startTime").execute()
    events = events_result.get("items", [])

    if(not events):
        print("No upcoming events found.")
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(start, event["summary"])

def insert(eventInfo):
    event = {
        "summary": eventInfo["summary"],
        "description": eventInfo["description"],
        "start": {
            "dateTime": eventInfo["time_start"],
            "timeZone": eventInfo["timezone"],
        },
        "end": {
            "dateTime": eventInfo["time_end"],
            "timeZone": eventInfo["timezone"],
        },
        "reminders": {
            "useDefault": False,
            "overrides": [
                { "method": "email", "minutes": 30 },
                { "method": "popup", "minutes": 30 },
            ],
        }
    }

    event = service.events().insert(calendarId = "primary", body = event).execute()
    print("Event created: {}".format(event.get("htmlLink")))

if __name__ == "__main__":
    main()
    insert()