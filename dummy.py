# from view_calendar.view_calendar import display_events, selected_events_info_list
# from tabulate import tabulate


# def main():
#     # h = ["table 1", "table 2"]
#     t = [display_events, display_events]

#     # print(tabulate(t, headers=h, showindex="always", tablefmt="plain"))
#     # display_events()
    
#     for i in range(2):
#         t[i]()
#         print()


import curses

# Sample data
data = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5", "Item 6", "Item 7", "Item 8", "Item 9", "Item 10"]

def display_data(stdscr, data):
    page_size = curses.LINES - 2  # Height of the terminal window excluding borders
    num_pages = (len(data) + page_size - 1) // page_size
    current_page = 0

    while True:
        stdscr.clear()

        start_index = current_page * page_size
        end_index = min(start_index + page_size, len(data))

        for i in range(start_index, end_index):
            stdscr.addstr(i - start_index, 0, data[i])

        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_DOWN:
            current_page = (current_page + 1) % num_pages
        elif key == curses.KEY_UP:
            current_page = (current_page - 1) % num_pages
        elif key == ord('q'):
            break

if __name__ == "__main__":
    curses.wrapper(display_data, data)


# if __name__ == "__main__":
#     main()
