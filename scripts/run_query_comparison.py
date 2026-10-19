# Subproject III: run the six sample queries on the original and the compressed index
# and compare the number of results. Output: experiments/compression/query_comparison.tsv

from pathlib import Path

from src.preprocessing import iter_documents
from src.naive_indexer import build_naive_index

from src.compression import (
    build_compressed_documents,
    compress_query_terms
)

from src.query_processor import (
    single_term_query,
    and_query
)


def main():
    
    print("Building original index ...")
    original_index = build_naive_index(iter_documents())
    
    print("Building compressed index ...")
    compressed_documents,stopwords_150 = build_compressed_documents()
    
    
    compressed_index = build_naive_index(
        compressed_documents
    )
    
    queries = [
        ["cocoa"],
        ["bahia"],
        ["review"],
        ["cocoa", "bahia"],
        ["cocoa", "review"],
        ["bahia", "review"]
    ]

    lines = []

    header = (
        "Query\t"
        "Original Results\t"
        "Compressed Results\t"
        "Change"
    )
    
    lines.append(header)
    
    for terms in queries :
        
        
        if len(terms) == 1 :
            original_result = single_term_query(
                original_index,
                terms[0]
            )
            
        else :
            original_result = and_query(
                original_index,
                terms
            )    
        processed_terms = compress_query_terms(
            terms,
            stopwords_150
        )    
        
        if not processed_terms :
            compressed_result = []
            
        elif len(processed_terms) == 1 :
            compressed_result = single_term_query(
                compressed_index,
                processed_terms[0]
            )   
        else:
            compressed_result = and_query(
                compressed_index,
                processed_terms
            )    
        original_count = len(original_result)
        compressed_count = len(compressed_result)
        change = compressed_count - original_count
        
        query_text = " AND " . join(terms)
        line = (
            f"{query_text}\t"
            f"{original_count}\t"
            f"{compressed_count}\t"
            f"{change:+d}"
        )
        
        lines.append(line)
        
    table = "\n".join(lines)
    
    print("\n" + table)
    
    output_dir = Path("experiments/compression")
    output_dir.mkdir(parents=True,exist_ok=True)
    
    output_file = output_dir /  "query_comparison.tsv"
    
    with open (output_file,"w",encoding="utf-8") as file :
        file.write(table)
    print(f"\nSaved to:{ output_file}")
    
if __name__ =="__main__" :
    main()        
        
        
        
        
            
            
             