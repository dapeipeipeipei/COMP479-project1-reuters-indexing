# SPIMI-inspired indexer (Subproject IV):
# same document stream as the naive indexer, but no list F.
# Each docID is appended directly to the postings list of its term (hash table).


# Build postings lists directly from the document token stream.
def build_spimi_index(documents):


    index = {

    }

    for doc_id,tokens in documents :


        # a term can appear many times in one document,
        # but the docID should be added only once
        unique_terms = set(tokens)

        for term in unique_terms:

            # new term -> create an empty postings list
            if term not in index:
                index[term] = []

            # documents are read in increasing NEWID order,
            # so the postings list stays sorted without sorting it
            index[term].append(doc_id)
            
            
    index = sort_index_terms(index)        
            
    return index



# Sort dictionary terms alphabetically (only the terms, postings are not changed).
def sort_index_terms(index):
    return dict(sorted(index.items()))
