import csv

def write_to_csv_file(data_list):
    field_names = [name.capitalize() for name in data_list[0].keys()]
    filename = "calendar_data.csv"
    with open(filename, "a") as csvfile:
        writer = csv.DictWriter(csvfile, filenames=field_names)
        
        writer.writeheader()
        writer.writerows(data_list)
        pass