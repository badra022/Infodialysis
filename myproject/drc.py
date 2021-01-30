from apiclient.discovery import build
import pickle
from datetime import datetime, timedelta
import datefinder
credentials = pickle.load(open("myproject/token.pkl", "rb"))
service = build("calendar", "v3", credentials=credentials)
result = service.calendarList().list().execute()

calendar_id = result['items'][1]['id']
# print(calendar_id)
def create_event(start_time_str , attendees):
    matches = list(datefinder.find_dates(start_time_str))
    if len(matches):
        start_time = matches[0]
        end_time = start_time + timedelta(hours=1)

    event = {
        'summary': 'Hemodialysis',
        'location': 'SBME hosbital',
        'description': '',
        'start': {
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'Africa/Cairo',
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'Africa/Cairo',
        },

        'attendees': attendees ,

        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},

            ],
        },
    }
    return service.events().insert(calendarId = 'ahmedelbadawy9999@gmail.com', body=event ).execute()
