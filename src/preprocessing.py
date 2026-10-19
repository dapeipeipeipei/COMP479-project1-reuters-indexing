"""
Reading and preprocessing the Reuters-21578 collection.

- read the raw .sgm files from data/raw/
- split each file into articles and use NEWID as the docID
- extract the article text (title + body)
- tokenize the text into a list of tokens
"""
from pathlib import Path
from bs4 import BeautifulSoup
import re
import nltk


# Relative path -> run the scripts from the project root.
DATA_DIR = Path("data/raw/reuters21578")




# Read one .sgm file and return every <REUTERS> ... </REUTERS> block as one article.
# The files are not valid UTF-8, so latin-1 is used.
def split_articles(filename):
    file_path = DATA_DIR / filename
    
    with open(file_path,"r",encoding="latin-1") as file :
        content = file.read()
        
    articles = re.findall(
            r"<REUTERS\b.*?</REUTERS>",
            content,
            re.DOTALL
        )
    return articles

# Use the NEWID attribute as the docID.
def get_doc_id(article):
    match = re.search(r'NEWID="(\d+)"',article)
    
    if match is None :
        return None 
    return int(match.group(1))



# Keep only the TITLE and BODY text of the article.
# Other fields (TOPICS, PLACES, DATELINE ...) are not indexed.
def extract_article_text(article):
    soup = BeautifulSoup(article,"html.parser")
    title = soup.find("title")
    body = soup.find("body")
    
    parts = []
    
    if title is not None:
        parts.append(title.get_text(" ",strip = True))
    if body is not None :
        parts.append(body.get_text(" ",strip = True))
        
    return " ".join(parts)    



# Tokenize with NLTK, lowercase every token,
# and drop punctuation (tokens with no letter or digit).
def tokenize_text(text):
    tokens = nltk.word_tokenize(text)
    clean_tokens = []
    
    for token in tokens:
        token = token.lower()
        
        if any(char.isalnum() for char in token):
            clean_tokens.append(token)
            
    return clean_tokens        




# Document stream for both indexers: yields (docID, tokens) one document at a time.
# Files are read in name order (reut2-000 ... reut2-021), so NEWIDs come in increasing order.
def iter_documents():
    for file_path in sorted(DATA_DIR.glob("reut2-*.sgm")):
        articles = split_articles(file_path.name)
        
        for article in articles:
            doc_id = get_doc_id(article)
            
            if doc_id is None:
                continue
            
            text = extract_article_text(article)
            tokens = tokenize_text(text)
            
            yield doc_id,tokens

