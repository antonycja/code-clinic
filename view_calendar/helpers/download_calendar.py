import csv
def calendar_data_changed(data_list, filename):
    try:
        with open(filename, "r") as cal_data:
            csv_file = csv.reader(cal_data)
            print(csv_file)
            pass
        pass
        
    except FileNotFoundError:
        pass
    pass

def write_to_csv_file(data_list, filename):
    fields = [name for name in data_list[0].keys()]
    with open(filename, "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        
        writer.writeheader()
        writer.writerows(data_list)
        pass