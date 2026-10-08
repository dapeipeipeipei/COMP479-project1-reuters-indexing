# Build postings lists directly from the document token stream.
def build_spimi_index(documents):
    
    
    index = {
        
    }
    
    for doc_id,tokens in documents :
        
        
        unique_terms = set(tokens)
        
        for term in unique_terms:
            
            if term not in index:
                index[term] = []
                
            index[term].append(doc_id)
            
            
    index = sort_index_terms(index)        
            
    return index



# Sort dictionary terms alphabetically.            
def sort_index_terms(index):
    return dict(sorted(index.items()))
