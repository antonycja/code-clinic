from sys import argv
from api_connection import get_calendar_results


def main():
    while True:
        calendar = input(
            "Which calendar would you like to view? Enter the number \n (1) Personal\n (2) WethinkCode\nEnter your option here: ")
        if calendar.strip() not in ["1", "2"]:
            print("?????* Invalid option for calendar. *?????\n")
            continue
        break
    while True:
        max_results = input(
            "\nHow many days would you like to view?\nEnter a number here: ")
        if not max_results.isdigit():
            print("?????* Please enter a valid integer. *?????\n")
            continue
        break

    print("------------------------------------------------------------------------------------------")
    get_calendar_results(int(calendar), int(max_results))


if __name__ == "__main__":
    # system arguments
    options = argv[1:]
    if len(options) == 0:
        main()
    elif len(options) > 1:
        if options[0].lower() == "wethinkcode" and options[1].isdigit():
            print("showing Wethinkcode calender")
            get_calendar_results(2, options[1])
        elif options[0].lower() == "personal" and options[1].isdigit():
            print("showing code clinics personal calender")
            get_calendar_results(1, options[1])
    else:
        main()
