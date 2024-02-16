import csv

def write_to_csv_file(data_list):
    fields = [name for name in data_list[0].keys()]
    filename = "calendar_data.csv"
    with open(filename, "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        
        writer.writeheader()
        writer.writerows(data_list)
        pass