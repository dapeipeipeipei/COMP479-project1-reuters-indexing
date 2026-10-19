# To test:
# - single-term query, term in the index
# - single-term query, term not in the index
# - intersection of two postings lists
# - AND query with an empty result
from src.query_processor import (
    single_term_query,
    intersect_postings,
    and_query,
)

def test_single_term_query_found():
    index = {
        "apple": [1, 3],
        "banana": [1, 2],
    }
    
    result = single_term_query(index,"apple")
    
    assert result ==[1,3]
    
    
def test_single_term_query_not_found():
    index = {
        "apple": [1, 3],
        "banana": [1, 2],
    }    
    
    result = single_term_query(index,"carrot")
    
    
    assert result == []
    
    
def test_intersect_postings():
    
    
    postings1 = [1, 3, 5, 7]
    postings2 = [2, 3, 5, 8]
    
    result = intersect_postings(postings1,postings2)
    
    assert result ==[3,5]
    
def test_and_query_empty_result():
     index = {
         "apple": [1, 3],
        "banana": [2, 4],
         
     }  
     
     
     result = and_query(
        index,
        ["apple", "banana"]
     )  
     
     
     assert result == []