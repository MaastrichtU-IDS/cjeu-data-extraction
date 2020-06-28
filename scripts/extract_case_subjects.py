#!/usr/bin/env python
# # Script to extract subjects (topics) for Court of Justice of the European Union (CJEU) judgements
# GNU AGPLv3 - https://choosealicense.com/licenses/agpl-3.0/
# # Input: a CSV file named 'input_celex_numbers.csv' with exactly one column with no header. The file should contain a list of CELEX numbers (https://eur-lex.europa.eu/content/help/faq/celex-number.html), one on each line, representing the desired input cases.
# # NB: Each CELEX number should occur on a separate line. The input file should be located in the same directory as this script file.
# # Output: 
# # 1. 'extracted_subjects.csv' a file containing the extracted subjects. There are exactly two columns in this CSV file with headers 'source' and 'subject' respectively. The 'source' column indicates the input case, the 'subject' column indicates the topic for that case. Note that there may be multiple subjects per case.
# # 2. Optional: 'extracted_subjects_failed.csv' a CSV file with exactly one column containing a list of CELEX numbers (one on each line). These numbers represent cases for which the script could not successfully extract subjects.
# # Usage:
# # python extract_case_subjects.py

import sys
import getopt
import re
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv

def get_celex_numbers(file):
    result = []
    with open(file, 'r') as fh:
        for line in fh:
            line = line.rstrip('\n')
            result.append(line)
    return result

def get_html_page_from_url(url):
    try:
        page = urlopen(url)
    except Exception as e:
        print('Request has failed for this URL:')
        print(url)
        print()
        raise(e)
    soup = BeautifulSoup(page, "html.parser")
    return soup

# Extract citations for the case given the BeautifulSoup format of it's HTML page
def extractSubjects(soup_judgement_page, celexNumber):
    # Citations array
    subjects = []
    # Get all list items in this web page (the citations are in one of the list items in the HTML source)
    li_results = soup_judgement_page.find_all("dl", class_="NMetadata")

    # loop through items until you find the citation list item
    for result in li_results:
        dts = result.find_all('dt',string="Subject matter: ")
        if len(dts) == 1:
            dds = result.find_all('dd')
            if len(dds) > 0:
                anchors = dds[0].find_all('li')
                if len(anchors) > 0:
                    for anchor in anchors:
                        currentrow = []
                        currentrow.append(celexNumber)
                        tmpStr = anchor.text
                        tmpStr = tmpStr.rstrip()
                        tmpStr = tmpStr.lstrip()
                        currentrow.append(tmpStr)
                        subjects.append(currentrow)
    return subjects

base_url = 'https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:'
celexnumbers = get_celex_numbers('input_celex_numbers.csv')
errors = []

all_subjects = []
length = len(celexnumbers)
index = 1
print()
print("Extracting subjects...")
print()
for celexnumber in celexnumbers:
    print(index,"/",length)
    index+=1
    url = base_url + celexnumber
    try:
        page = get_html_page_from_url(url)
        subjects = extractSubjects(page, celexnumber)
        if (len(subjects) == 0):
            item = []
            item.append(celexnumber)
            errors.append(item)
        all_subjects.extend(subjects)
    except Exception as e:
        item = []
        item.append(celexnumber)
        errors.append(item)

with open('extracted_subjects_failed.csv', 'a', newline='') as outfile:
    writer = csv.writer(outfile, delimiter=',')
    writer.writerows(errors)
    
all_subjects.insert(0,['source','subject'])
with open('extracted_subjects.csv', 'w', newline='') as outfile:
    writer = csv.writer(outfile, delimiter=',')
    writer.writerows(all_subjects)

print()
print('Done!')
