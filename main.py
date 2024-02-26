from view_calendar.view_calendar import get_calendar_results


def get_user_input() -> tuple[int, int]:
    """get user input to optimize the viewing experience of the user by only displaying what the user chooses to output.

    Returns:
        tuple[int,int]: the calendar option to be viewed and the number of days to view.
    """
    while True:
        calendar = input(
            "Which calendar would you like to view? \n(0). All Calendars.\n(1). Personal Calendar Only.\n(2). Code Clinics Calendar Only.\nEnter the number of the calendar here: ")
        print()
        if len(calendar) == 0:
            break
        if calendar.isdigit():
            calendar = int(calendar)
            break

    while True:
        days = input(
            "Enter the number of days you would like to view, leave empty for (default = 7).\nEnter a number here: ")
        print()
        if len(days) == 0:
            days = 0
            break
        if days.isdigit():
            days = int(days)
            break

    # TODO: Make filter function to do the functionality below
    
    while True:
        filter_evt = input("Would you like to filter the events/calendar? (leave blank if NOT).\nEnter the filter ',' separated keyword(s) here : ")
        print()
        if not filter_evt:
            filter_keyword_list = None
            break
        
        filter_keyword_list = filter_evt.split(",")
        break

        
    # while True:
    #     filter_evt = input("Would you like to filter the events/calendar? (leave blank if NOT).\n(0). Available Times.\n(1). NOT BOOKED.\nEnter the filter number here: ")
    #     print()
    #     if len(filter_evt) == 0:
    #         filter_evt = None
    #         break
    #     if filter_evt.isdigit():
    #         filter_evt = int(filter_evt)
    #         break

    return calendar, days, filter_keyword_list


def run_view_calendars() -> None:
    """Run the view calendars 
    """
    calendar, days, filter_keyword_list = get_user_input()

    if days != 0:
        get_calendar_results(filter_keyword_list, calendar, days)
    else:
        get_calendar_results(filter_keyword_list, calendar)

# get_calendar_results(0, 7)


if __name__ == "__main__":
    run_view_calendars()
