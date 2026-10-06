# index = {"apple":[1,4,5],"banana":[2,3,4],"carrot":[2,9]}...
def single_term_query(index,term):
    term = term.lower()
    return index.get(term,[])


# Two-pointer intersection:
# postings lists are sorted.
# Compare current docIDs:
# - equal -> add to result, move both pointers
# - left smaller -> move left pointer
# - right smaller -> move right pointer
# Stop when either list reaches the end.
def intersect_postings(postings1,postings2):
    result = []
    i,j =0,0
    
    while i <len(postings1) and j<len(postings2):
        if postings1[i] == postings2[j]:
            result.append(postings1[i])
            i += 1
            j += 1
            
        elif postings1[i] < postings2[j]:
            i += 1
            
        else:
            j += 1
            
    return result            




# Multi-term AND query:
# - use the first term's postings list as the initial result
# - for every remaining term, get its postings list
# - intersect it with the current result
# - replace result with the new intersection
# - if result becomes empty, stop early
# - return the docIDs containing ALL query terms


def and_query(index,terms):
    if not terms:
        return []
    
    result = single_term_query(index,terms[0])
    
    
    for term in terms[1:]:
        postings = single_term_query(index,term)
        result = intersect_postings(result,postings)
        
        
        if not result:
            break
        
        
    return result    
    
