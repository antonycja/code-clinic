from view_calendar.view_calendar import get_calendar_results


def get_user_input():
    while True:
        calendar = input("Which calendar would you like to view? \n(0). All Calendars.\n(1). Personal Calendar Only.\n(2). Code Clinics Calendar Only.\nEnter the number of the calendar here: ")
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
    return calendar, days

calendar, days = get_user_input()

if days != 0:
    get_calendar_results(calendar, days)
else:
    get_calendar_results(calendar)
    
# get_calendar_results(0, 7)

