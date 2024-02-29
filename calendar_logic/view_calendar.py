import datetime
from tabulate import tabulate
from curses import newpad
from collections import defaultdict
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from helpers.download_calendar import write_to_csv_file, calendar_data_changed, convert_csv_to_dict


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
        return None
    return events


def determine_calendar(calendar: int, cal_type_list: list, calendar_dict: dict) -> tuple:
    """determine which calendar to get the data from depending on which calendar option the user chose.

    Args:
        calendar (int): the number option of the calendar.
        cal_type_list (list): a list with the names of the calendars.
        calendar_dict (dict): a dictionary with the calendar IDs.
        
    Returns:
        tuple: a tuple containing the cal_type, calendars.
    """

    if calendar == 1:
        calendars = [calendar_dict["personal"]]
        cal_type = cal_type_list[0]
    elif calendar == 2:
        calendars = [calendar_dict["clinic"]]
        cal_type = cal_type_list[1]
    else:
        calendars = [calendar for calendar in calendar_dict.values()]
        cal_type = "ALL calendars"
        

    return cal_type, calendars


def get_data_from_calendar_api(service: object, calendar: int, days: int, cal_type: str, calendars: list,  cal_type_list: list) -> list:
    """get the data from the calendar api and return a list containing the calendar data.

    Args:
        service (object): the google calendar api response.
        calendar (int): the calendar ID of the calendar to be viewed.
        days (int): the number of days to check.
        cal_type (str): the type of calendar.
        calendars (list): a list with the name(s) of the calendar(s).
        cal_type_list (list): a list with the calendar headers.
    Returns:
        list: a list containing dictionaries of events.
    """
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
            # print(events)
            event_info = create_event_info(events, cal_name)
            [selected_events_info_list.append(
                event) for event in event_info]
        else:
            print(tabulate(
                [[f"No upcoming events for this {cal_name} calendar."]], tablefmt="double_grid"))

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


def filter_calendar_events(filter_by: list, filename: str) -> list:
    """filter the events by looking for the given keywords and only return those events.

    Args:
        filter_by (list): the filter keywords you would like to search for in the calendar.
        filename (str): the name of the file the data is being stored in.

    Returns:
        list: a list containing only the events that meet the filter criteria.
    """
    file = convert_csv_to_dict(filename)
    if not filter_by:
        return file

    filtered_data_list = []
    for event in file:
        is_valid_for_filter = []
        for value in event.values():
            tmp_filter = []
            for filter_word in filter_by:
                if isinstance(value, list):
                    value = [value.lower() for value in value]
                    if filter_word.lower() not in value:
                        continue
                elif filter_word.lower() != value.lower() and filter_word.lower() not in value.lower().split(" "):
                    continue
                tmp_filter.append(True)

            if tmp_filter:
                is_valid_for_filter.append(True)
                if len(is_valid_for_filter) == len(filter_by):
                    filtered_data_list.append(event)
    if not filtered_data_list:
        print("No Data was found matching your Filter Criteria. Here is all the data.\n")
        return file

    return filtered_data_list


def get_calendar_results(user_credentials: object, filter_keywords: str, calendar: int = 1, days: int = 7) -> None:
    """Print the calendar data for the selected calendar.

    Args:
        user_credentials (object): an object containing the user credentials.
        filter_keywords (str): a string containing the keywords if any were given.
        calendar (int, optional): the calendar ID of the calendar to be viewed. Defaults to 1.
        days (int, optional): the number of days to check. Defaults to 7 days.
    """

    try:
        # The name of the file where the data should be stored.
        filename = "calendar_data.csv"
        calendar_dict = {"personal": "primary",
                     "clinic": "c_7f60d63097ebf921579ca266668826f490dc72478a9d37d17ad62046836f598a@group.calendar.google.com"}
        cal_type_list = ["PERSONAL calendar", "CODE CLINIC calendar"]
        
        days = int(days)
        
        service = build("calendar", "v3", credentials=user_credentials)
        cal_type, calendars = determine_calendar(calendar, cal_type_list, calendar_dict)
        
        print(
        f"Getting the upcoming event(s) for the next {days} day(s) for {cal_type}...\n")
        
        # get event in the specified 
        selected_events_info_list = get_data_from_calendar_api(
            service, calendar, days, cal_type, calendars, cal_type_list)
        
        # Get events in the next 7 days 
        all_calendar_ids = [calendar for calendar in calendar_dict.values()]
        next_7_days = get_data_from_calendar_api(service, 0, 7, cal_type, all_calendar_ids, cal_type_list)
        # checking if the current saved data is up to date, if not updating it.
        if calendar_data_changed(next_7_days, filename):
            write_to_csv_file(next_7_days, filename)

        # Check if filtering must be applied or not.
        if filter_keywords:
            filter_keywords = filter_keywords.split(",")
            selected_events_info_list = filter_calendar_events(
                filter_keywords, filename)

        display_events(selected_events_info_list)

    except HttpError as error:
        print(f"An error occurred: {error}")
