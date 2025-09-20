

# Website Grammar Checker

This project uses **web scraping** (Selenium + BeautifulSoup) and **NLP techniques** (spaCy + LanguageTool)  
to identify spelling and grammatical mistakes from webpages.

## Features
- Extracts text from target web pages using Selenium
- Detects grammar & spelling issues with LanguageTool
- Dynamically identifies proper nouns (names, cities, acronyms) using spaCy to reduce false positives
- Exports results to CSV with error, suggestion, and entity type

## Files
- `grammar_checker.py` → Python script for scraping and analysis
- `grammar_spelling_report.csv` → Sample output report

## Example Output
CSV report includes:
- Page URL
- Error text
- Suggested correction(s)
- Grammar/Spelling message
- Entity type (if detected)

## Requirements
- Python 3.8+
- Selenium
- BeautifulSoup
- spaCy (`en_core_web_sm` model)
- LanguageTool

Install dependencies:
```bash
pip install -r requirements.txt
````

Run the script:

```bash
python grammar_checker.py
```

## Note

This project was originally built as part of a coding assignment.







