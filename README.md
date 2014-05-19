mellon-grants
=============
To quote Yusuke Shinyama, developer of PDFMiner, ["PDF is evil."](http://www.unixuser.org/~euske/python/pdfminer/programming) This is true, because unlike a Microsoft Word document or HTML file, there is no preserved data structure in a PDF. Rather, PDF contents typically only contain instructions that say where to position certain items on a page. This means PDF data is best extracted by preserving some type of layout that matches the original document, as there is no other hierarchical structure to extract the information you need. 

For this project, I used [Xpdf](http://www.foolabs.com/xpdf/) to preserve the document layout while converting [grants PDFs](http://www.mellon.org/news_publications/annual-reports-essays/grants/) from the Andrew W. Mellon Foundation into text files, before running the pdftocsv.py script.


As of 05.18, contents include:

(1) **pdftocsv.py**: script that parses grants data into readable csv files, ready for analysis.
