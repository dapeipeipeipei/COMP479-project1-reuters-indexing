# To test (small hand-made documents):
# - F contains every term-docID pair
# - F is sorted
# - duplicate pairs are removed
# - postings lists are sorted and have no duplicates
from src.naive_indexer import (
    build_pair_list,
    sort_and_deduplicate,
    build_inverted_index,
    build_naive_index,
)



def test_build_pair_list():
    
    documents  = [
        (1,["apple","banana","apple"]),
        (2,["banana","carrot"])
        
    ]
    
    result = build_pair_list(documents)
    
    
    expected = [
        ("apple",1),
        ("banana",1),
        ("apple",1),
        ("banana",2),
        ("carrot",2),
        
    ]
    
    assert result == expected
    
    
    
def test_sort_and_deduplicate():
    pairs = [
        ("banana", 2),
        ("apple", 1),
        ("banana", 1),
        ("apple", 1),    
    ]
    
    result = sort_and_deduplicate(pairs)
    expected = [
        ("apple",1),
        ("banana",1),
        ("banana",2),
    ]
    assert result == expected
    
def test_build_inverted_index():
    
    unique_pairs = [
        ("apple", 1),
        ("apple", 3),
        ("banana", 1),
        ("banana", 2),
        ("carrot", 2),
        ("carrot", 3),  
    ]   
    
    result = build_inverted_index(unique_pairs)
    
    expected = {
        "apple": [1, 3],
        "banana": [1, 2],
        "carrot": [2, 3],  
    } 
    
    
    assert result == expected
    
    
def test_build_naive_index():
    documents = [
        (1, ["apple", "banana", "apple"]),
        (2, ["banana", "carrot"]),
        (3, ["apple", "carrot"]),
        
    ] 
    
    result = build_naive_index (documents)
    
    expected = {
         "apple": [1, 3],
        "banana": [1, 2],
        "carrot": [2, 3],
    }   
    
    assert result == expected