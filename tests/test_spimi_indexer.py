from src.spimi_indexer import build_spimi_index
from src.naive_indexer import build_naive_index


def test_build_spimi_index():
    
    documenets = [
        (1, ["apple", "banana", "apple"]),
        (2, ["banana", "carrot"]),
        (3, ["apple", "carrot"]),
        
    ]
    
    
    result = build_spimi_index(documenets)
    
    expected = {
         "apple": [1, 3],
        "banana": [1, 2],
        "carrot": [2, 3],   
        
    }
    
    assert result == expected
    
def test_spimi_matches_naive():
    
    documents = [
        (1, ["apple", "banana", "apple"]),
        (2, ["banana", "carrot"]),
        (3, ["apple", "carrot"]),  
        
    ] 
    
    
    spimi_index =build_spimi_index(documents)
    naive_index = build_naive_index(documents)
    
    assert spimi_index == naive_index
    
     