import datetime
from tabulate import tabulate
from collections import defaultdict
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from auth.auth import authenticate_user

from .helpers.download_calendar import write_to_csv_file, calendar_data_changed


def get_events(service: object, calender: str, days: int) -> list:
    """get the events on the specified period from the google calendars api.

    Args:
        service (object): the google calendar api response.
        calender (str): the calendar ID of the calendar to be viewed.
        days (int): the number of days to check.

    Returns:
        list: a list of events for the specified period.
    """
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    end = (datetime.datetime.utcnow() + datetime.timedelta(days=days)
           ).isoformat() + "Z"  # Get the date in <days> amount of days
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


def determine_calendar(calendar: int) -> tuple:
    """determine which calendar to get the data from depending on which calendar option the user chose.

    Args:
        calendar (int): the number option of the calendar.

    Returns:
        tuple: a tuple containing the calendars, cal_type and cal_type_list.
    """
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

    return calendars, cal_type, cal_type_list


def get_data_from_calendar_api(service: object, calendar: int, days: int) -> list:
    """get the data from the calendar api and return a list containing the calendar data.

    Args:
        service (object): the google calendar api response.
        calendar (int): the calendar ID of the calendar to be viewed.
        days (int): the number of days to check.

    Returns:
        list: a list containing dictionaries of events.
    """
    calendars, cal_type, cal_type_list = determine_calendar(calendar)
    # Calling the Calendar API
    print(
        f"Getting the upcoming event for the next {days} for {cal_type}...\n")

    event_list = []
    selected_events_info_list = []
    # Get each calendar from the list of calendars
    for calendar_id in calendars:
        events = get_events(service, calendar_id, days)
        event_list.append(events)

    for index, events in enumerate(event_list):
        if calendar != 1 and calendar != 2:
            cal_name = cal_type_list[index].upper()
        else:
            cal_name = cal_type.upper()

        # Check if there is are events or not on each calendar, if there are no events on the specified time period, let the user know.
        if events:
            if isinstance(events, str):
                print(events)
            else:
                # print(events)
                event_info = create_event_info(events, cal_name)
                [selected_events_info_list.append(
                    event) for event in event_info]

    return selected_events_info_list


def display_events(events: list) -> None:
    """print out the results on the terminal.

    Args:
        events (list): a list containing the event data to be shown to the user.
    """
    # get the current terminal size
    terminal_size = os.get_terminal_size()

    # Prevent a keyerror by defaulting to a list if the value still needs to be generated.
    calendar_events = defaultdict(list)
    for event in events:
        calendar_events[event['Calendar']].append(event)

    # Print each calendar's events
    for calendar, events in calendar_events.items():
        table_events = []
        print(f"{calendar}:")
        for event in events:
            event_details = {"Date": event["date"], "Time": f'{event["start time"]} - {event["end time"]}',
                             "Summary": event["summary"], "Location": event["location"], "Organizer": event["organizer"], "Attendees": ', '.join(event["attendees"])}
            table_events.append(event_details)

        # the max row span of each row in the table
        row_span = [(terminal_size.columns-10) // len(event_details.keys())
                    for _ in event_details.keys()]

        # the max row span of the organizer -> [-2] row in the table
        row_span[-2] = row_span[-2]+5

        # Create the table using table events list created above
        table = tabulate(table_events, headers="keys", tablefmt="fancy_grid",
                         colalign=("center"), maxcolwidths=row_span)

        # Display the table and add spaces after
        print(table)
        print()
        print()


def create_event_info(events: list, cal_name: str) -> list:
    """create a list of dictionaries containing the relevant data to be used and stored by other functions.

    Args:
        events (list): the list of all events unfiltered.
        cal_name (str): the name of the calendar being created currently.

    Returns:
        list: a list containing dictionaries of relevant data.
    """
    event_info_list = []
    for event in events:
        date_time = event["start"].get("dateTime").split("T")
        date = date_time[0]
        start_time = date_time[1][:5]
        end_time = event["end"].get("dateTime").split("T")[1][:5]
        summary = event["summary"]
        try:
            location = event["location"]
        except KeyError:
            location = "TBC"
        organizer = event["creator"].get("email")
        attendees = []
        
        # First try to check the number of attendees if attendees is a key in event other handles keyerror
        try:
            if len(event["attendees"]) > 1:
                for index, attendee in enumerate(event["attendees"]):
                    if index == 0:
                        if event["creator"].get("email") != event["organizer"].get("email"):
                            attendees.append(attendee.get(
                                "email", "TBC").split("@")[0])
                        continue
                    else:
                        attendees.append(attendee.get(
                            "displayName", attendee.get("email", "TBC").split("@")[0]))
            else:
                attendees.append("NOT BOOKED")
        except KeyError:  # Error handling for when no attendees are setup, which can only be caused by a manual entry.
            attendees.append("TBC")

        # Finally adding the relevant data to the event info list once we have handled the errors if any occurred
        event_info_list.append({"Calendar": cal_name, "date": date, "start time": start_time, "end time": end_time,
                               "summary": summary, "location": location, "organizer": organizer, "attendees": attendees})
    return event_info_list


def get_calendar_results(calendar: int = 1, days:int = 7) -> None:
    """Print the calendar data for the selected calendar.

    Args:
        calendar (int, optional): the calendar ID of the calendar to be viewed. Defaults to 1.
        days (int, optional): the number of days to check. Defaults to 7 days.
    """
    user_credentials = authenticate_user()

    try:
        filename = "calendar_data.csv"
        service = build("calendar", "v3", credentials=user_credentials)
        selected_events_info_list = get_data_from_calendar_api(
            service, calendar, max_results)
        # print(selected_events_info_list)
        if calendar_data_changed(selected_events_info_list, filename):
            write_to_csv_file(selected_events_info_list, filename)

        display_events(selected_events_info_list)
    except HttpError as error:
        print(f"An error occurred: {error}")
