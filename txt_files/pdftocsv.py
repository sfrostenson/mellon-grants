import csv
import re


def should_skip(line):
    if not line:
        # Blanks
        return True
    if '(continued)' in line and 'appropriated' in line.lower():
        return True
    if line == 'The Andrew W. Mellon Foundation':
        # No need for this header
        return True
    if line == 'Classification of Grants':
        # No need for this header, either
        return True
    if re.search(r'^_+$', line):
        # Nothing but underscores
        return True
    if line == previous_line:
        # Duplicates
        return True
    if re.search(r'^\d{1,3}$', line):
        # Page numbers--any line with three or fewer digits on it and nothing
        # else
        return True

    # If it isn't one of the above kinds of line, we shouldn't skip it.
    return False


def is_amount(line):
    return re.search(r'^\$? *[,\d]+$', line) is not None


def is_total_header(line):
    return unicode(line, 'utf-8', 'ignore') == u'Total\u2014'


# Read in all the lines of the input file at once. We could do this a bit
# differently, but then we'd have even more nesting going on--and these files
# aren't terribly large.
with open('content2000.txt', 'r') as input_file:
    input_lines = input_file.readlines()

# Remosve whitespace characters (including '\n') at beginning and end of the
# line.
input_lines = [line.strip().replace('$','') for line in input_lines]

# Find where the table ends using the string 'Classification of Grants'
# Since it seems to denote the data we're looking for.
#Enumerate iterates through a list, returns values and corresponding positions.
#In case Classification of Grants does not exist, start at 0. If it does exist,
#index is whatever line Classification of Grants is on + 1
start = -1
for index, line in enumerate(input_lines):
    if 'Classification of Grants' in line:
        start = index
        break
    continue
input_lines = input_lines[start+1:]

# Start building the rows of our CSV.
rows = []

#things to use in for loop that I need to remember outside of the for loop.
previous_line = ''
current_category = []
#allows us to use a category that spans two lines
last_category_index = -1

current_recipient = []
programs_so_far = []
amounts_so_far = []
#need a mechanism to look back up the list
#everytime I don't find a flag, keep a running list in stack.
stack = []

for index, line in enumerate(input_lines):

    # Skip lines that are useless to us.
    if should_skip(line):
        continue

    # Get out of here altogether if we're getting to the last totals section.
    # It works differently from the others, and frankly we don't care.
    if is_total_header(line) and line.endswith('Contributions'):
        break

    # Remove the weird trailing periods and underscores.
    # Nothing that we care about is an empty space followed by a period.
    # The combination of split and join allows us to replace a variable in split with
    # a delimiters specified in join.
    line = line.split(' .')
    line = (' ').join(line)
    line = line.split('_')
    line = (' ').join(line)

    # Remove appropriated
    if 'Appropriated' in line:
        line = line.replace('Appropriated', '')

    if '(continued)' in line:
        line = line.replace('continued', '')

    # Remove excess whitespace and replace it with one space btn. words and leave it as a list.
    # all the content of a line as a list.
    split_line = line.split()
    #join always converts a list to a string
    join_line = (' ').join(split_line).strip()


    # If we're dealing with part of a category name, add it to a list so we can
    # keep track of the whole thing later. This also resets everything else
    # we're keeping track of, since a recipient and its programs aren't going
    # to carry over from one category to the next.
    if join_line.upper() == join_line and not is_amount(join_line):

        # last line was also a category, these are usually 2 lines so append the
        # name to current_category
        if index - last_category_index <= 3:
            current_category.append(line)

        # we haven't seen a category for a while, this is a new category; reset
        else:
            current_category = [join_line]
            current_recipient = ''
            programs_so_far = []
            amounts_so_far = []
            stack = []

        last_category_index = index
        continue

    # If the last word in the list is a number, and there are things saved in
    # the stack, assume we've found the end of a contribution amount and start
    # start counting backwards up the stack
    elif is_amount(split_line[-1]):

        amounts_so_far.append(split_line[-1])
        # 0:-1 says to take all the words except the last word
        programs_so_far = split_line[0:-1] 

        #while loop helps you look backward more easily than a for loop.
        while len(stack):
            last_line = ' '.join(stack[-1])
            if last_line[-1] == ':':
                stack = []
            elif last_line.upper() == last_line and not is_amount(last_line):
                stack = []
            else:
                programs_so_far = stack.pop(-1) + programs_so_far

        new_row = []
        new_row.append((' ').join(current_category))
        new_row += current_recipient
        new_row.append((' ').join(programs_so_far))
        new_row.append((' ').join(amounts_so_far))

        rows.append(new_row)

        amounts_so_far = []
        programs_so_far = []

    elif join_line.endswith(':') and not 'book' in line and not 'entitled' in line:
        #will remove any characters specified in quotes; no need to separate out characters.
        recepient_line = join_line.rstrip(':,')
        current_recipient = [recepient_line]
        while len(stack):
            #the last word of the last line of stack (in this case; could be vice versa)
            #nested index
            if is_amount(stack[-1][-1]):
                stack = []
            else:
                current_recipient = [(' ').join(stack.pop(-1)).rstrip(':,'), recepient_line]

    else:
        stack.append(split_line)

    previous_line = line


with open('grants2000.csv', 'w') as output_file:
    writer = csv.writer(output_file)
    writer.writerows(rows)
