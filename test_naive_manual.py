from src.preprocessing import iter_documents
from src.naive_indexer import build_naive_index


documents = iter_documents()

index = build_naive_index(documents)

print("Number of terms:", len(index))

print("cocoa:", index.get("cocoa"))
print("bahia:", index.get("bahia"))
print("the:", index.get("the"))