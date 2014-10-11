mellon-grants
=============
To quote Yusuke Shinyama, developer of PDFMiner, ["PDF is evil."](http://www.unixuser.org/~euske/python/pdfminer/programming) This is true, because unlike a Microsoft Word document or HTML file, there is no preserved data structure in a PDF. Rather, PDF contents typically only contain instructions that say where to position certain items on a page. This means PDF data is best extracted by preserving some type of layout that matches the original document, as there is no other hierarchical structure to extract the information you need. 

For this project, I used [Xpdf](http://www.foolabs.com/xpdf/) to preserve the document layout while converting [grants PDFs](http://www.mellon.org/news_publications/annual-reports-essays/grants/) from the Andrew W. Mellon Foundation into text files, before running the pdftocsv.py script and generating csvs for each year of grants in the output folder. I then used the read_csvs.py script to combine all of the csvs into one csv file--merged.csv--for import into our MySQL database. But because my script didn't capture every irregularity, I went through and manually cleaned the data as well. Modifications are in merged_work.csv in the university_match directory.

##Contents include:

(1) **[pdftocsv.py](https://github.com/sfrostenson/mellon-grants/blob/master/txt_files/pdftocsv.py)**: script that parses grants data into readable csv files, ready for analysis.

(2) **[read_csvs.py](https://github.com/sfrostenson/mellon-grants/blob/master/output/read_csvs.py)**: script that combines multiple csvs into one csv file.

(3) **[match.py](https://github.com/sfrostenson/mellon-grants/blob/master/university_match/match.py)**: script that generates a unique list of institutions and matches universities to university type using a name based association.

(4) **[unmatched_uni.py](https://github.com/sfrostenson/mellon-grants/blob/master/university_match/unmatched/unmatched_uni.py)**: script that pulled universities from the unmatched.csv that were not assigned a university type in match.py.

(5) **[append_matches.py](https://github.com/sfrostenson/mellon-grants/blob/master/university_match/matches/append_matches.py)**: script that appended university type of matches.csv and unmatched_schools_matched.csv to a new master file-- new_merged_file.csv.

(6) **[match_ipeds.py](PUT LINK HERE)**: needs to be updated.

##With no unique id, use SequenceMatcher to join datasets

Once the Mellon grants data was broken free from its PDF format, it was time to analyze what types of universities were grant recipients. Only one problem--no unique id for institutions. Which means I needed to perform matches based on an institution's name in order to determine if it was a private, public or ivy league university.

I should have first used the Python module SequenceMatcher to match universities with their respective IPEDS unit ids. Instead, I used lists of private, public, ivy and for-profit institutions for matching and later ran another script--match_ipeds.py--to assign universities their respective IPEDS unit ids so I could perform more nuanced analyses--i.e. how many grants went to elite private institutions.

With match.py, I generated a unique list of institutions and using a similiarity index of 0.8 as a threshold, I devised a program that using named based associations let me assign university types to my master list of institutions. This generated two types of output--matches.csv in the matches folder and unmatched.csv in the unmatched folder. 

But because SequenceMatcher uses similiar characters to assign matches and as result, couldn't capture every match because of spelling discrepancies, I wrote a separate script--unmatched_uni.py--in the unmatched folder to capture those institutions that were obviously universities but were not assigned in our initial match.py script. It's output is unmatched_schools.csv. I manually assigned their university type in unmatched_schools_matched.csv

From there, I appended the university type of matches.csv and unmatched_schools_matched.csv with append_matches.py to the master file--merged_work.csv--as a new file, new_merged_file.csv. 