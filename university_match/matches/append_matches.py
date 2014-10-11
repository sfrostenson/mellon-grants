import csv

# read a csv file and return it
def read(filename):
    data = []
    with open(filename, 'rU') as f:
        f = csv.reader(f)
        for row in f:
            data.append(row)

    return data

def write(data, filename):
    with open(filename, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(data)


master_file = read('merged_work.csv')
h0 = master_file.pop(0)

matches = read('matches.csv')
#use list comprehnesion to create a list of just university names from matches.
uni_names = [row[0] for row in matches]

append_list = []

for row in master_file:
    #recip is where the university name is positioned in master_file
    recip = row[2]
    if recip:
        # must use try because if recip doesn't exist, truncates
        try:
            #index says find using the index of the list uni_names,
            #returns the index of the first time the recipient appears in the other list
            index = uni_names.index(recip)
            row.append(matches[index][1])
        except:
            a = 1
        # append_list.append(row)
        #having found the instances, append university type

        append_list.append(row)


write(append_list, 'new_merged_file.csv')
