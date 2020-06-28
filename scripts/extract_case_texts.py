#!/usr/bin/env python
# # Script to extract full texts for Court of Justice of the European Union (CJEU) judgements
# GNU AGPLv3 - https://choosealicense.com/licenses/agpl-3.0/
# # Input: a CSV file named 'input_celex_numbers.csv' with exactly one column with no header. The file should contain a list of CELEX numbers (https://eur-lex.europa.eu/content/help/faq/celex-number.html), one on each line, representing the desired input cases.
# # NB: Each CELEX number should occur on a separate line. The input file should be located in the same directory as this script file.
# # Output: 
# # 1. The full texts of cases in .txt text files in the directory 'fulltexts/'. Each case text will be in separate file and will be named with the CELEX number of that case e.g. 62016CJ0295.txt
# # 2. Optional: 'extracted_texts_failed.csv' a CSV file with exactly one column containing a list of CELEX numbers (one on each line). These numbers represent cases for which the script could not successfully extract the full text.
# # Usage:
# # python extract_case_texts.py

import sys
import getopt
import re
import requests
from bs4 import BeautifulSoup
import os
from os import path

def get_parsed_html_text(page):
    soup = BeautifulSoup(page.content, 'html.parser')
    text = soup.find('div', {'id': 'text'})
    if text is not None:
        return text.text
    else:
        return False

def get_celex_numbers(file):
    result = []
    with open(file, 'r') as fh:
        for line in fh:
            line = line.rstrip('\n')
            result.append(line)
    return result

def get_html_page_from_url(url):
    try:
        page = requests.get(url)
    except Exception as e:
        print('Request has failed for this URL:')
        print(url)
        print()
        raise(e)
    return page

def remove_unwanted_artefacts(text):
    text = text.replace(u'\xa0', ' ')
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\n\d+\n', '\n', text)
    text = re.sub(r'\d+\s+', '', text)
    return text

base_url = 'https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:'
celexnumbers = get_celex_numbers('input_celex_numbers.csv')
errors = []
index = 1
length = len(celexnumbers)

textspath = "fulltexts/"
if not path.exists(textspath):
    try:
        os.mkdir(textspath)
    except OSError:
        print ("Creation of the directory %s failed" % textspath)
    #else:
        #print ("Successfully created the directory %s " % processedtextpath)
print()
print("Extracting texts...")
print()
for celexnumber in celexnumbers:
    print(index,"/",length)
    index += 1
    url = base_url + celexnumber
    page = get_html_page_from_url(url)
    case_text = get_parsed_html_text(page)
    if case_text:
        case_text = remove_unwanted_artefacts(case_text)
        file_name = 'fulltexts/' + celexnumber + '.txt'
        with open(file_name, 'w', encoding='utf-8') as out:
            out.write(case_text)
    else:
        errors.append(celexnumber)

if len(errors) > 0:
    print('Failed to extract ', len(errors), ' cases')
    with open('extracted_texts_failed.csv', 'w') as out:
        for error in errors:
            out.write(error + '\n')
    out.close()

print()
print('Done!')
