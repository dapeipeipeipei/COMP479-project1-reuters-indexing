# Subproject III (extra): run the six sample queries on the compressed index only.
# Query terms go through the same compression steps as the documents. Prints to the console.

from src.compression import (
    build_compressed_documents,
    compress_query_terms
)

from src.naive_indexer import build_naive_index
from src.query_processor import single_term_query, and_query


def main():
    
    print("Building compress index ...")
    
    documents,stopwords_150 = build_compressed_documents()
    compressed_index =build_naive_index(documents)
    
    single_queries = [
        "cocoa",
        "bahia",
        "review"
        
    ]
    
    and_queries = [
        ["cocoa", "bahia"],
        ["cocoa", "review"],
        ["bahia", "review"],
    ]
    
    
    for term in single_queries:
        processed_terms = compress_query_terms(
            [term],
            stopwords_150
        )
        
        if not processed_terms:
            result = []
            
        else:
            
            result = single_term_query(
                compressed_index,
                processed_terms[0]
            )
        print(f"\nQuery:{term}")
        print(f"Processed query:{processed_terms}")  
        print(f"Number of results:{len(result)}")   
        print(f"DocsIDs:{result}")   
    print("\n ---Compressed AND queries ---")    
    for terms in and_queries:
        
        processed_terms = compress_query_terms(
            terms,
            stopwords_150
        )
        
        result = and_query(
            compressed_index,
            processed_terms
        )
        print(f"\nQuery:{' AND '.join(terms)}")
        print(f"Processed query:{processed_terms}")  
        print(f"Number of results:{len(result)}")   
        print(f"DocsIDs:{result}")  






if __name__ == "__main__":
    main()    
        
        