import datetime

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from auth.auth import authenticate_user


def get_events(service, calender, max_results):
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    events_result = (
        service.events()
        .list(
            calendarId=calender,
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
        print("No upcoming events found.")
        return
    return events


def get_data_from_calendar_api(service, calendar=1, max_results=7):
    calendars = {"personal": "primary",
                 "clinic": "c_7f60d63097ebf921579ca266668826f490dc72478a9d37d17ad62046836f598a@group.calendar.google.com"}
    
    if calendar == 1:
        calendar = calendars["personal"]
        cal_type = "PERSONAL calendar"
    elif calendar == 2:
        calendar = calendars["clinic"]
        cal_type = "CODE CLINIC calendar"
    else:
        calendar = [calendar for calendar in calendars.values]
        cal_type = "ALL calendars"
        

    # Calling the Calendar API
    print(
        f"Getting the upcoming {max_results} events for {cal_type}.")

    events = get_events(service, calendar, max_results)

    # Prints the start and name of the next max_events events
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        start = start.replace("T", " at ")
        start = start[:19]
        print(start, "->", event["summary"])


def get_calendar_results(calendar, max_results):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    user_credentials = authenticate_user()

    try:
        service = build("calendar", "v3", credentials=user_credentials)
        get_data_from_calendar_api(service, calendar, max_results)

    except HttpError as error:
        print(f"An error occurred: {error}")
