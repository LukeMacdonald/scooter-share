from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from googleapiclient.discovery import build
import pytz
import json


class GoogleCalendar:

    def __init__(self):
        SCOPES = "https://www.googleapis.com/auth/calendar"
        store = file.Storage("token.json")
        creds = store.get()
        if(not creds or creds.invalid):
            flow = client.flow_from_clientsecrets("/assignment-2-scooter-share-application-team-7/agent/web/google_api/credentials.json", SCOPES)
            creds = tools.run_flow(flow, store)
        self.service = build("calendar", "v3", http=creds.authorize(Http()))


    def insert(self, eventInfo):
        current_timezone = pytz.timezone('Etc/GMT+0')
        current_timezone_str = current_timezone.zone
        event = {
            "summary": eventInfo["summary"],
            "description": eventInfo["description"],
            "start": {
                "dateTime": eventInfo["time_start"].isoformat(),
                "timeZone": current_timezone_str,
            },
            "end": {
                "dateTime": eventInfo["time_end"].isoformat(),
                "timeZone": current_timezone_str,
            },
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "email", "minutes": 30},
                    {"method": "popup", "minutes": 30},
                ],
            }
        }

        try:
            event = self.service.events().insert(calendarId="primary", body=event).execute()
        except self.service.errors.HttpError as error:
            print(f"Error inserting event: {error}")