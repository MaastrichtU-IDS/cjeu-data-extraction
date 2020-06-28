#!/usr/bin/env python
# # Script to extract citations for Court of Justice of the European Union (CJEU) judgements
# GNU AGPLv3 - https://choosealicense.com/licenses/agpl-3.0/
# # Input: a CSV file named 'input_celex_numbers.csv' with exactly one column with no header. The file should contain a list of CELEX numbers (https://eur-lex.europa.eu/content/help/faq/celex-number.html), one on each line, representing the desired input cases.
# # NB: Each CELEX number should occur on a separate line. The input file should be located in the same directory as this script file.
# # Output: 
# # 1. 'extracted_citations.csv' a file containing the extracted citations. There are exactly two columns in this CSV file with headers 'source' and 'target' respectively. The 'source' column indicates the citing cases, the 'target' column indicates the cited cases.
# # 2. Optional: 'extracted_citations_failed.csv' a CSV file with exactly one column containing a list of CELEX numbers (one on each line). These numbers represent cases for which the script could not successfully extract citations.
# # Usage:
# # python extract_case_citations.py

import sys
import getopt
import re
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv
import os

def get_celex_numbers(file):
    candidates = []
    with open(file, 'r') as fh:
        for line in fh:
            line = line.rstrip('\n')
            candidates.append(line)

    result = candidates
    errors = []
    if os.path.exists("extracted_citations_failed.csv"):
        with open('extracted_citations_failed.csv', 'r') as ef:
            for line in ef:
                line = line.rstrip('\n')
                errors.append(line)
        result = list(set(candidates).difference(set(errors)))

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

def clean_celex_number(text):
    if ")" in text:
        result = text.split(")")
        result[0] += ")"
        return result[0]
    else:
        return text[:11]

def is_valid_celex(celex):
    alphabet_count = 0
    for i in range(len(celex)):
        if(celex[i].isalpha()):
            alphabet_count += 1            
    if ("CJ" in celex.upper() or "CO" in celex.upper()) and alphabet_count == 2:
        return True
    else:
        return False

# Extract citations for the case given the BeautifulSoup format of it's HTML page
def extractCitations(soup_judgement_page, celexNumber):
    # Citations array
    citations = []
    # Get all list items in this web page (the citations are in one of the list items in the HTML source)
    li_results = soup_judgement_page.find_all('li')
    # loop through items until you find the citation list item
    for result in li_results:
        for link in result.find_all('a',href=True):
            if "./../../../legal-content/EN/AUTO/?uri=CELEX:6" in link['href']:
                currentrow = []
                citedcelex = clean_celex_number(link.text)
                if is_valid_celex(citedcelex) and is_valid_celex(celexNumber):
                    currentrow.append(celexNumber)
                    currentrow.append(citedcelex)
                    citations.append(currentrow)
    return citations

base_url = 'https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:'
celexnumbers = get_celex_numbers('input_celex_numbers.csv')
errors = []

all_citations = []
length = len(celexnumbers)
index = 1

print()
print("Extracting citations...")
print()
for celexnumber in celexnumbers:
    print(index,"/",length)
    index+=1
    url = base_url + celexnumber
    try:
        page = get_html_page_from_url(url)
        citations = extractCitations(page, celexnumber)
        all_citations.extend(citations)
    except Exception as e:
        errors.append(celexnumber)
    
with open('failed_celex_numbers.csv', 'a', newline='') as outfile:
    writer = csv.writer(outfile, delimiter=',')
    writer.writerows(errors)

all_citations.insert(0,['source','target'])
with open('extracted_citations.csv', 'w', newline='') as outfile:
    writer = csv.writer(outfile, delimiter=',')
    writer.writerows(all_citations)

print()
print('Done!')
