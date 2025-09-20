# Import required libraries

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
import spacy
import csv
import language_tool_python


nlp = spacy.load("en_core_web_sm")


tool = language_tool_python.LanguageTool("en-US")

main_pages = [
    "https://sheetal.net/",
    "https://sheetal.net/packers-and-movers-bangalore.php",
    "https://sheetal.net/Best-Packers-Movers.php",
    "https://sheetal.net/advertise-with-us.php",
    "https://sheetal.net/packers-movers.php",
    "https://www.skywingcargopackers.in/packer-movers-hyderabad.php",
    "https://sheetal.net/contactus.php"
]

def extract_entities(text):
    """
    Extract proper nouns, city names, organizations, people, and acronyms.
    - Uses spaCy NER for structured entities
    - Adds custom rule for acronyms (short words in uppercase like AC, TV, etc.)
    """
    doc = nlp(text)
    entities = set()

    
    for ent in doc.ents:
        if ent.label_ in ["PERSON", "ORG", "GPE", "PRODUCT"]: 
            entities.add(ent.text.lower())

    for token in text.split():
        if token.isupper() and 2 <= len(token) <= 5:
            entities.add(token.lower())

    return entities

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)


with open("grammar_spelling_report.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow(["Page URL", "Error Text", "Suggestion(s)", "Message", "Entity Type"])

   
    for url in main_pages:
        print(f"\n--- Checking page: {url} ---\n")
        driver.get(url)
        time.sleep(5) 

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        texts = [
            t.get_text(separator=" ", strip=True)
            for t in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li'])
        ]
        site_text = "\n".join(texts)
 
        entities = extract_entities(site_text)

        
        matches = tool.check(site_text)
        if not matches:
            print("No spelling or grammar errors found.")

        for match in matches:
            error_text = site_text[match.offset:match.offset + match.errorLength].strip()
            suggestion = ', '.join(match.replacements) if match.replacements else "No suggestion"
            message = match.message

      
            if error_text.lower() in entities:
                continue
            entity_type = None
            for ent in nlp(error_text).ents:
                entity_type = ent.label_

            print(f"Error: {error_text}")
            print(f"Suggestion: {suggestion}")
            print(f"Message: {message}")
            print(f"Entity Type: {entity_type}")

            writer.writerow([url, error_text, suggestion, message, entity_type])


driver.quit()
print("\n✅ Done! Report saved as grammar_spelling_report.csv")
