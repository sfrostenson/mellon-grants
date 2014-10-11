import os
import csv

# read a csv file and return it
def read_one_csv(filename):
    data = []
    with open(filename, 'rU') as f:
        f = csv.reader(f)
        for row in f:
            data.append(row)

    return data


def read_all_csvs(path_to_csvs):
    # lists all the files in the directory you specified as path_to_csvs
    all_filenames = os.listdir(path_to_csvs)
    print all_filenames

    # get all csv filenames by using the last four characters of the filename and checking if it's .csv
    csv_names = [filename for filename in all_filenames if filename[-4:] == '.csv']

    all_csv_data = []
    for filename in csv_names:
        single_csv = read_one_csv(path_to_csvs + filename)
        headers = single_csv.pop(0)
        all_csv_data += single_csv

    # Put one copy of the headers back in
    return [headers] + all_csv_data


def write(data, filename):
    with open(filename, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(data)


all_data = read_all_csvs('./')
write(all_data, 'merged.csv')
