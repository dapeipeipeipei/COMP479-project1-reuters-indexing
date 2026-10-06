from src.query_processor import single_term_query

index = {
    "apple":[1,4,5],
    "banana":[2,3,4],
    "carrot":[2,9],
}

print(single_term_query(index, "apple"))
print(single_term_query(index, "BANANA"))
print(single_term_query(index, "orange"))