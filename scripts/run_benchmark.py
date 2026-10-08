"""Compare naive vs SPIMI on 10,000 term-docID pairs, save timings to results/benchmarks/."""
from src.preprocessing import iter_documents
from src.benchmark import limit_documents, benchmark_indexers

def main():
    
    print("Preparing 10000 term-docID parings ...")
    
    
    documents = list(iter_documents())
    
    limited_documents = limit_documents(documents,10000)
    
    naive_time,spimi_time,same_index = benchmark_indexers(limited_documents)
    
    print(f"Naive time :{naive_time:.6F} seconds")
    print(f"Spimi_time :{spimi_time:.6F} seconds")
    print(f"Indexes indentical:{same_index}")




if __name__ == "__main__":
    main()
