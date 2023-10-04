from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from googleapiclient.discovery import build
import pytz
from tzlocal import get_localzone
from google.auth.transport.requests import Request

from google.oauth2.credentials import Credentials
import datetime


class GoogleCalendar:

    def __init__(self):
        # Assuming you have the user's credentials

       
        SCOPES = "https://www.googleapis.com/auth/calendar"
        
        store = file.Storage("token.json")
        creds = store.get()
        if(not creds or creds.invalid):
            flow = client.flow_from_clientsecrets("agent/web/google_api/credentials.json", SCOPES)
            creds = tools.run_flow(flow, store)
        self.service = build("calendar", "v3", http=creds.authorize(Http()))


    def insert(self, event_info):
        local_timezone = get_localzone()
        event = {
            "summary": event_info["summary"],
            "description": event_info["description"],
            "start": {
                "dateTime": event_info["time_start"].isoformat(),
                "timeZone": str(local_timezone),
            },
            "end": {
                "dateTime": event_info["time_end"].isoformat(),
                "timeZone": str(local_timezone),
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
            return event["id"]
        except Exception as error:
            print(f"Error inserting event: {error}")

    def remove(self, event_id):
        try:
            self.service.events().delete(calendarId="primary", eventId=event_id).execute()
            print(f'Event {event_id} deleted successfully.')
        except Exception as e:
            print(f'Error deleting event: {str(e)}')