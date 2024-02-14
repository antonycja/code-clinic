import datetime

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from auth.auth import authenticate_user


def get_events(service, calender, days):
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    end = (datetime.datetime.utcnow() + datetime.timedelta(days=days)).isoformat() + "Z"  # 'Date in <days> amount of days
    events_result = (
        service.events()
        .list(
            calendarId=calender,
            timeMin=now,
            timeMax=end,
            maxResults=100,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
        return "No upcoming events found."
    return events


def get_data_from_calendar_api(service, calendar=1, days=7):
    calendar_dict = {"personal": "primary",
                 "clinic": "c_7f60d63097ebf921579ca266668826f490dc72478a9d37d17ad62046836f598a@group.calendar.google.com"}
    cal_type_list = ["PERSONAL calendar", "CODE CLINIC calendar"]
    if calendar == 1:
        calendars = [calendar_dict["personal"]]
        cal_type = cal_type_list[0]
    elif calendar == 2:
        calendars = [calendar_dict["clinic"]]
        cal_type = cal_type_list[1]
    else:
        calendars = [calendar for calendar in calendar_dict.values()]
        cal_type = "ALL calendars"
        

    # Calling the Calendar API
    print(
        f"Getting the upcoming event for the next {days} for {cal_type}...\n")
    
    event_list = []
    # Get each calendar from the list of calendars
    for calendar_id in calendars:
        events = get_events(service, calendar_id, days)
        event_list.append(events)


    for index, events in enumerate(event_list):
        if calendar != 1 and calendar != 2:
            print(f"{cal_type_list[index].upper()}: ")
        else:
            print(f"{cal_type.upper()}: ")
            
        # Prints the start and name of the next max_events events
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            start = start.replace("T", " at ")
            start = start[:19]
            print(start, "->", event["summary"])
        print()


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
