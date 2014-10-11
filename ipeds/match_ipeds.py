from difflib import SequenceMatcher
import csv

# read a csv file and return it
def read_one_tsv(filename):
    data = []
    with open(filename, 'rU') as f:
        f = csv.reader(f, dialect ='excel-tab')
        for row in f:
            data.append(row)

    return data

def read_one_csv(filename):
    data = []
    with open(filename, 'rU') as f:
        f = csv.reader(f)
        for row in f:
            data.append(row)

    return data

def is_a_university(s):
    if 'private' in s or 'public' in s or 'for profit' in s or 'ivy' in s:
        return True
    else:
        return False

def get_match_ratio(a, b):
    s = SequenceMatcher(lambda x: x == ' ', a, b)
    return round(s.ratio(), 3)

def get_top_matches(string_to_match, list_to_match_against):
    s = string_to_match
    l = list_to_match_against

    threshold = 0.8
    ratios = []

    for index, item in enumerate(l):
        ratio = get_match_ratio(s, item)
        if ratio >= threshold:
            return index
        else:
            ratios.append({"ratio": ratio, "index": index})
    return sorted(ratios, key=lambda x: x["ratio"], reverse=True)[0:10]

def write(data, filename):
    with open(filename, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(data)


master_file = read_one_tsv('grants_master.tsv')
h0 = master_file.pop(0)

ipeds = read_one_csv('ipeds_ids.csv')
h1 = ipeds.pop(0)


# create a list of the master file
master_list = []
for row in master_file:
    university = is_a_university(row[9])
    if not university:
        continue
    else:
        master_list.append(row[2])

# get unique orgs from master_list by converting to a dict, then back to a list
unique_names = list(set(master_list))

# define threshold here - you can tune this variable later if it's giving you too many or not enough matches
threshold = 0.8
unmatched = []
matched = []

for name in unique_names:
    matches_over_threshold = []
    for ids in ipeds:
        if name == ids[1]:
            matches_over_threshold.append({'id': ids[0], 'name': ids[1]})
        else:
            #sequence match
            match_ratio = get_match_ratio(name.lower(), ids[1].lower())
            #now 2 outcomes: skip, perfect match, made match based on threshold conditions.
            # skip those organizations beneath the threshold.
            if match_ratio < threshold:
                continue
            # if it's not a perfect match but reaches our threshold, save it and continue the loop
            else:
                matches_over_threshold.append({'id': ids[0], 'name': ids[1]})
    
    #sort our matches
    sorted_matches = sorted(matches_over_threshold, key=lambda x: x['ratio'], reverse=True)

    ### here we figure out what to do with the matches
    # no matches - continue and append to unmatched []
    if not sorted_matches:
        print '\nNo matches found for %s' % name
        unmatched.append([name])
        continue

    # the top match is a perfect match!
    #if the first sorted_match has a ratio of 1, perfect match and append to matched []
    elif sorted_matches[0]['ratio'] == 1:
        match = sorted_matches[0]
        print '\nFound a perfect match: %s and %s' % (name, match['name'])
        matched.append([name, match['type']])
        # go back into types and remove the index as we no longer need it.
        print 'Deleting %s from %s.csv' % (types[ match['type'] ][ match['index'] ], match['type'])
        del types[ match['type'] ][ match['index'] ]
        continue

    # show the top matches and decide which one to go with
    else:
        num_matches_to_show = len(sorted_matches)

        # if there are fewer then 10 matches, show them all
        # otherwise just show the top 10
        if num_matches_to_show > 10:
            num_matches_to_show = 10

        # print the matches
        print '\n\n\nLet\'s look at the top %s matches for %s\n' % (num_matches_to_show, name)
        for index, match in enumerate(sorted_matches[0 : num_matches_to_show]):
            print '%s %s ------- %s' % (index, match['type'], match['name'])

        # using a while loop here so we don't break the program if we accidentally enter something wrong
        not_selected = True
        while not_selected:
            sel = raw_input('\nEnter the best match, or -1 if nothing matches: ')
            try:
                sel = int(sel)
            except:
                continue
            # if the selection is -1, put the row in unsorted and break the loop
            if sel == -1:
                print '\nPutting %s in unmatched.csv\n\n' % name
                unmatched.append([name])
                not_selected = False
            # if the selection is within range, accept the answer and break the loop
            elif sel < num_matches_to_show:
                print '\nWriting %s as type %s\n\n' % (name, sorted_matches[sel]['type'])
                matched.append([name, sorted_matches[sel]['type']])
                not_selected = False
            # if the selection isn't in range and isn't -1, ask the question again
            else:
                continue

write(unmatched, 'unmatched.csv')
write(matched, 'matches.csv')
