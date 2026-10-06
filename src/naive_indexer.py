


# TODO: build F from the token stream

def build_pair_list(documents):
    pairs = []
    
    for doc_id,tokens in documents:
        for term in tokens :
            pairs.append((term,doc_id))
            
    return pairs        
            

def sort_and_deduplicate(pairs):
    pairs.sort()
    
    unique_pairs = []
    
    previous_pair = None
    
    for pair in pairs:
        if pair != previous_pair:
            unique_pairs.append(pair)
            previous_pair = pair
    return unique_pairs        
    

def build_inverted_index(unique_pairs):
    index = {}
    
    for term,doc_id in unique_pairs:
        if term not in index:
            index[term] = []
            
        index[term].append(doc_id)
    return index        


def build_naive_index(documents):
    pairs = build_pair_list(documents)
    unique_pairs = sort_and_deduplicate(pairs)
    index = build_inverted_index(unique_pairs)
    
    return index
    