# CJEU Data Extraction

Python scripts for extracting citations, topics and full texts of cases by the Court of Justice of the European Union (CJEU). Data is publicly available and sourced from the [EURLEX](https://eur-lex.europa.eu/homepage.html) website which provides access to EU legislation and court decisions.

## Running the scripts

##### Requirements:

+ [Python 3.7+](https://www.python.org/downloads/)
+ [Git](https://git-scm.com/) **or** an archive extractor like [7-Zip](https://www.7-zip.org/)
+ A list of [CELEX](https://eur-lex.europa.eu/content/help/faq/celex-number.html) numbers of cases for which you would like to extract citations, full texts or topics. This has to be specified in a single CSV file called `input_celex_numbers.csv` with exactly one column. Each celex number (e.g. `62016CJ0295`) should be specified on a separate line in the file. For instructions on how to obtain a list of all CELEX numbers from the Court of Justice of the EU, please consult the [wiki](https://github.com/MaastrichtU-IDS/cjeu-data-extraction/wiki) of this repository.

##### Instructions
    
1. If you are using Git, type this command in your commandline tool: `https://github.com/MaastrichtU-IDS/cjeu-data-extraction.git`
2. If you are using an archive extractor, download this repository's code archive from [here](https://github.com/MaastrichtU-IDS/cjeu-data-extraction/archive/master.zip) and extract it to the desired folder on your file system
3. Place your `input_celex_numbers.csv` file in `scripts/` in the same directory as the Python scripts
4. In your commandline tool, change into the **root** directory of your local copy of the repository
5. **Important:** create a fresh [virtual environment](https://docs.python.org/3/tutorial/venv.html) with a default or base installation of Python 3.7+  
6. Run the command `pip install -r requirements.txt` which will install all required libraries for the scripts in your fresh Python virtual environment
7. On installation completion of the required libraries in the previous step, change into the `scripts/` directory of your local copy of the code (this directory contains all `.py` code files)
8. For extracting citations, run the command `python extract_case_citations.py`. For extracting [official topics](https://op.europa.eu/en/web/eu-vocabularies/at-dataset/-/resource/dataset/subject-matter/version-20200318-0), run the command `python extract_case_subjects.py`. For extracting full texts of cases, run the command `python extract_case_texts.py`

## License
Copyright (C) 2020, Kody Moodley

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.
