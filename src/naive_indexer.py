# Naive indexer (Subproject I):
# documents -> list F of (term, docID) pairs -> sort F -> remove duplicates
# -> postings lists


# Step 1: while there are still documents, read each document's tokens
# and append one (term, docID) pair per token to the list F.
# Duplicates are kept here, they are removed in step 2.
def build_pair_list(documents):
    pairs = []

    for doc_id,tokens in documents:
        for term in tokens :
            pairs.append((term,doc_id))

    return pairs


# Step 2: no more input -> sort F by term, then by docID.
# After sorting, equal pairs are next to each other,
# so a pair is kept only if it is different from the previous one.
def sort_and_deduplicate(pairs):
    pairs.sort()

    unique_pairs = []

    previous_pair = None

    for pair in pairs:
        if pair != previous_pair:
            unique_pairs.append(pair)
            previous_pair = pair
    return unique_pairs


# Step 3: turn the sorted F into the index.
# DocIDs paired with the same term become that term's postings list.
# F is already sorted, so every postings list is sorted too.
def build_inverted_index(unique_pairs):
    index = {}

    for term,doc_id in unique_pairs:
        if term not in index:
            index[term] = []

        index[term].append(doc_id)
    return index


# Run the three steps: {term: [docID1, docID2, ...]}
def build_naive_index(documents):
    pairs = build_pair_list(documents)
    unique_pairs = sort_and_deduplicate(pairs)
    index = build_inverted_index(unique_pairs)
    
    return index
    