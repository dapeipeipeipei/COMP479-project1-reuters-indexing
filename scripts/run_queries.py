from src.preprocessing import iter_documents
from src.naive_indexer import build_naive_index
from src.query_processor import single_term_query, and_query
import time

def main():
    print("Building index...")
    index = build_naive_index(iter_documents())
    
    
    
    single_queries = [
        "cocoa",
        "bahia",
        "review",
    ]
    
    and_queries = [
        ["cocoa", "bahia"],
        ["cocoa", "review"],
        ["bahia", "review"],
    ]
    
    
    
    print("\n--- Single-term queries ---")
    
    for term in single_queries:
        start = time.perf_counter()
        result = single_term_query(index,term)
        end = time.perf_counter()
        print(f"Naive index build time: {end - start:.4f} seconds")
        
        print(f"\nQuery:{term}")
        print(f"Number of results:{len(result)}")
        print(f"DocIDs:{result}")
        
        
    print("\n --- AND queris ---")
    
    for terms in and_queries:
        result = and_query(index,terms)
        
        print(f"\nQuery:{' AND ' .join(terms)}")
        print(f"Number of results: {len(result)}")
        print(f"DocIDs:{result}")    


if __name__ == "__main__":
    main()
