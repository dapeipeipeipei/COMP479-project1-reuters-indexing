import nltk

from src.preprocessing import iter_documents


# Make sure the tokenizer data exists
nltk.download("punkt_tab")

documents = iter_documents()

doc_id, tokens = next(documents)

print("First docID:", doc_id)
print("First 30 tokens:", tokens[:30])
print("Total documents:", sum(1 for _ in iter_documents()))

doc_ids = [doc_id for doc_id, _ in iter_documents()]

print("Min docID:", min(doc_ids))
print("Max docID:", max(doc_ids))
print("Unique docIDs:", len(set(doc_ids)))