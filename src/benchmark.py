"""
Timing of the naive indexer vs the SPIMI-inspired indexer.

Both indexers are timed on the same input, stopping after the first
10,000 term-docID pairs.
"""

import time

from src.naive_indexer import build_naive_index
from src.spimi_indexer import build_spimi_index


def limit_documents(documents,limit):
    limited_documents = []
    count = 0
    
    for doc_id,tokens in documents: 
        remaining = limit - count
        
        if remaining <= 0:
            break
        
        selected_tokens = tokens[:remaining]
        
        limited_documents.append(
            (doc_id,selected_tokens)
        )
        
        count += len(selected_tokens)
    return limited_documents    


def benchmark_indexers(documents):
    
    #naive
    start = time.perf_counter(
        
    )
    
    naive_index = build_naive_index(documents)
    
    naive_time = time.perf_counter() - start
    
    
    start = time.perf_counter()
    
    spimi_index = build_spimi_index(documents)
    
    spimi_time = time.perf_counter() - start
    
    
    return naive_time,spimi_time,naive_index == spimi_index
