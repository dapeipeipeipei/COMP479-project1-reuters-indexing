import nltk
from nltk.stem import PorterStemmer
from collections import Counter

from src.preprocessing import split_articles,get_doc_id,extract_article_text,DATA_DIR

stemmer = PorterStemmer()



# Tokenize text while keeping numbers and original letter case.
def tokenize_unfiltered(text):
    tokens = nltk.word_tokenize(text)
    clean_tokens = []
    
    for token in tokens:
        if any(char.isalnum() for char in token):
            clean_tokens.append(token)
            
    return clean_tokens

# Remove tokens that contain only numbers.        
def remove_numbers(tokens):
    clean_tokens = []
    
    
    for token in tokens:
        normalized = token.replace(",","")
        if normalized.endswith("%"):
            normalized = normalized[:-1]
            
        try:
            float(normalized)
        except ValueError:
            clean_tokens.append(token)        
        

    return clean_tokens


# Convert all tokens to lowercase.
def case_fold(tokens):
    return [token.lower() for token in tokens]


# Remove tokens that appear in the given stopword set.
def remove_stopwords(tokens, stopwords):
    clean_tokens = []
    
    for token in tokens:
        if token not in stopwords:
            clean_tokens.append(token)
    return clean_tokens



# Reduce each token to its Porter stem.
def stem_tokens(tokens):
    
    stemmed_tokens = []
    
    for token in tokens:
        stemmed_tokens.append(stemmer.stem(token))
    return stemmed_tokens



# Count unique terms and total non-positional postings.
def compute_stats(documents):
    vocabulary = set()
    posting_count = 0
    
    
    for doc_id,tokens in documents:
        
        vocabulary.update(tokens)
        
        unique_terms_in_document = set(tokens)
        posting_count += len(unique_terms_in_document)
    return len(vocabulary), posting_count



# Find the n most frequent terms in the whole collection.
def get_most_common_terms(documents,n):
    
    frequencies = Counter()
    
    for doc_id,tokens in documents:
        frequencies.update(tokens)
        
    most_common = frequencies.most_common(n)
        
    return {term for term, count in most_common}    


# Load Reuters documents without applying lossy compression.   
def load_unfiltered_documents():
    
    documents = []
    
    for file_path in sorted(DATA_DIR.glob("reut2-*.sgm")):
        articles = split_articles(file_path.name)
        for article in articles:
            doc_id = get_doc_id(article)
            
            if doc_id is None:
                continue
            
            text = extract_article_text(article)
            tokens = tokenize_unfiltered(text)
            
            documents.append((doc_id,tokens))
            
    return documents        


# Apply one token-processing function to every document.
def transform_documents(documents,transform):
    transform_documents = []
    
    for doc_id,tokens in documents:
        new_tokens = transform(tokens)
        transform_documents.append((doc_id,new_tokens))
        
    return transform_documents    



# Run all compression stages and collect statistics for each stage.
def run_compression_experiment():
    
    results = []
    
    
    #1.
    documents = load_unfiltered_documents()
    terms,postings = compute_stats(documents)
    results.append(("unfiltered",terms,postings))
    
    #2
    no_numbers = transform_documents(documents,remove_numbers)
    terms,postings = compute_stats(no_numbers)
    results.append(("no numbers",terms,postings))
    
    #3
    case_folded = transform_documents(no_numbers,case_fold)
    terms,postings = compute_stats(case_folded)
    results.append(("case folding",terms,postings))
    
    #4
    stopwords_30 = get_most_common_terms(case_folded,30)
    
    stopwords_30_docs = []
    
    for doc_id,tokens in case_folded:
        new_tokens = remove_stopwords(tokens,stopwords_30)
        stopwords_30_docs.append((doc_id,new_tokens))
    terms,postings = compute_stats(stopwords_30_docs)
    results.append(("30 stopwords",terms,postings))    
    
    #5
    stopwords_150 = get_most_common_terms(case_folded,150)
    
    stopwords_150_docs = []
    
    for doc_id,tokens in case_folded:
        new_tokens = remove_stopwords(tokens,stopwords_150)
        stopwords_150_docs.append((doc_id,new_tokens))
    terms,postings = compute_stats(stopwords_150_docs)
    results.append(("150 stopwords",terms,postings))   
    
    #6 stemming
    
    stemmed = transform_documents(stopwords_150_docs,stem_tokens)
    terms,postings = compute_stats(stemmed)
    results.append(("stemming",terms,postings))  
    
    return results 



#build the final compressed doc

def build_compressed_documents():
    
    documents = load_unfiltered_documents()
    
    no_numbers = transform_documents(documents,remove_numbers)
    
    case_folded = transform_documents(no_numbers,case_fold)
    
    stopwords_150 = get_most_common_terms(case_folded,150)
    
    stopwords_removed = []
    
    for doc_id,tokens in case_folded:
        new_tokens = remove_stopwords(tokens,stopwords_150)
        stopwords_removed.append((doc_id,new_tokens))
        
    stemmed_documents = transform_documents(
        stopwords_removed,
        stem_tokens
    ) 
    
    return stemmed_documents,stopwords_150   


#apply the same compression steps to query terms 
def compress_query_terms(terms,stopwords_150):
    terms = remove_numbers(terms)
    terms = case_fold( terms)
    terms = remove_stopwords(terms,stopwords_150)
    terms = stem_tokens(terms)
    
    
    
    return terms

