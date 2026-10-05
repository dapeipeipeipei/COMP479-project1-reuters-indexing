"""
Reading and preprocessing the Reuters-21578 collection.

- read the raw .sgm files from data/raw/
- split each file into articles and use NEWID as the docID
- extract the article text (title + body)
- tokenize the text into a list of tokens
"""
from pathlib import Path

DATA_DIR = Path("data/raw/reuters21578")


# TODO: read a .sgm file and split it into articles

# TODO: get the NEWID of an article

# TODO: extract the text of an article

# TODO: tokenize the text

# TODO: generator that yields (docID, tokens) for the whole collection
