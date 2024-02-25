import csv
def calendar_data_changed(data_list:list, filename:str) -> bool:
    """check whether the calendar data has changed compared to the data in the filename.

    Args:
        data_list (list): the new updated data.
        filename (str): the filename of the currently saved data.

    Returns:
        bool: true if the data has changed and false if it hasn't
    """
    try:
        with open(filename, "r") as cal_data:
            csv_file = csv.reader(cal_data)
            data_to_list = list(csv_file)
            keys = data_to_list[0]
            list_of_dict_data = [dict(zip(keys, data_list)) for data_list in data_to_list[1:]]
            
            for item in list_of_dict_data:
                item['attendees'] = eval(item['attendees'])
            
            if data_list == list_of_dict_data:
                return False
            else:
                return True
        
        
    except FileNotFoundError:
        return True

def write_to_csv_file(data_list, filename):
    fields = [name for name in data_list[0].keys()]
    with open(filename, "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        
        writer.writeheader()
        writer.writerows(data_list)
        pass