from src.preprocessing import iter_documents
from src.spimi_indexer import build_spimi_index



def main():
    print("Building SPIMI index...")
    documents = iter_documents(
        
    )
    
    index = build_spimi_index(documents)
    
    print(f"Number of terms: {len(index)}")
    print(f"cocoa:{index.get('cocoa',[])}")
    print(f"bahia:{index.get('bahia',[])}")
    print(f"review:{index.get('review',[])}")


if __name__ == "__main__":
    main()
