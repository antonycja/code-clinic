import datetime

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from auth.auth import authenticate_user

from .helpers.download_calendar import write_to_csv_file

def get_events(service, calender, days):
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    end = (datetime.datetime.utcnow() + datetime.timedelta(days=days)
           ).isoformat() + "Z"  # 'Date in <days> amount of days
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
        if events:
            # print(events[0])
            if isinstance(events, str):
                print(events)
            else:
                event_info = create_event_info(events)
                write_to_csv_file(event_info)
                for event in events:
                    date_time = event["start"].get("dateTime").split("T")
                    date = date_time[0]
                    time = date_time[1][:5]
                    print(time)
                    start = event["start"].get(
                        "dateTime", event["start"].get("date"))
                    start = start.replace("T", " at ")
                    start = start[:19]
                    print(start, "->", event["summary"])
            print()


def create_event_info(events: list):
    event_info_list = []
    for event in events:
        date_time = event["start"].get("dateTime").split("T")
        date = date_time[0]
        start_time = date_time[1][:5]
        end_time = event["end"].get("dateTime").split("T")[1][:5]
        summary = event["summary"]
        location = event["location"]
        organizer = event["organizer"].get("email")
        attendees = []

        if len(event["attendees"]) > 1:
            for index, attendee in enumerate(event["attendees"]):
                if index == 0:
                    continue
                attendees.append(attendee["email"].split("@")[0])
        else:
            attendees.append(event["organizer"].split("@")[0])

        event_info_list.append({"date": date, "start time": start_time, "end time": end_time,
                               "summary": summary, "location": location, "organizer": organizer, "attendees": attendees})
    return event_info_list

def get_calendar_results(calendar: int, max_results=7):
    """Print the calendar data for the selected calendar.

    Args:
        calendar (int): the calendar number to be viewed.
        max_results (int)-> (optional): the number of days to view starting from today
    """
    user_credentials = authenticate_user()

    try:
        service = build("calendar", "v3", credentials=user_credentials)
        get_data_from_calendar_api(service, calendar, max_results)

    except HttpError as error:
        print(f"An error occurred: {error}")
