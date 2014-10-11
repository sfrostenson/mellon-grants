import csv
import re

# read a csv file and return it
def read_one_csv(filename):
    data = []
    with open(filename, 'rU') as f:
        f = csv.reader(f)
        for row in f:
            data.append(row)

    return data

def is_a_university(s):
	if 'University' in s or 'College' in s:
 		return True
 	else:
 		return False

def is_an_association(s):
    if 'Associated' in s or 'Association' in s:
        return True
    else:
        return False

def is_a_foundation_or_incorporated(s):
    if 'Foundation' in s or 'Inc.' in s:
        return True
    else:
        return False

def write(data, filename):
    with open(filename, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(data)


rows = read_one_csv('unmatched.csv')

schools = []

for row in rows:
    is_an_assocition_or_not = is_an_association(row[0])
    if is_an_assocition_or_not:
        continue
    is_a_foundation_or_incorporated_or_not = is_a_foundation_or_incorporated(row[0])
    if is_a_foundation_or_incorporated_or_not:
        continue
    is_university_or_not = is_a_university(row[0])
    if is_university_or_not:
        schools.append(row)
    else:
        continue

write(schools, 'unmatched_schools.csv')
