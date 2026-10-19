from src import preprocessing

from src.preprocessing import (
    split_articles,
    get_doc_id,
    extract_article_text,
    tokenize_text,
    iter_documents,
)



def test_split_articles(tmp_path,monkeypatch):
    
    content = """
    <REUTERS NEWID="1">
        <TEXT>
            <TITLE>Apple Market</TITLE>
            <BODY>Apple prices rose.</BODY>
        </TEXT>
    </REUTERS>

    <REUTERS NEWID="2">
        <TEXT>
            <TITLE>Banana Market</TITLE>
            <BODY>Banana prices fell.</BODY>
        </TEXT>
    </REUTERS>
    """
    
    
    file_path = tmp_path / "sample.sgm"
    
    file_path.write_text(content,encoding = "latin-1")
    
    monkeypatch.setattr(
        preprocessing,
        "DATA_DIR",
        tmp_path
    )
    
    result = split_articles("sample.sgm")
    
    assert len(result) ==2
    assert 'NEWID="1"' in result [0]
    assert 'NEWID="2"' in result [1]
    
def test_get_doc_id():
    
    article = '<REUTERS NEWID="123">Test</REUTERS>'
    result = get_doc_id(article)
    
    assert result == 123
    
def test_extract_article_text():
    article = """
    <REUTERS NEWID="1">
        <TEXT>
            <TITLE>Apple Market</TITLE>
            <BODY>Prices rose today.</BODY>
        </TEXT>
    </REUTERS>
    """   
    
    result = extract_article_text(article)
    
    assert result == "Apple Market Prices rose today."
    
def test_tokenize_text():
    text =    "Apple prices rose 10%."
    
    result = tokenize_text(text)
    
    assert result == [
        "apple",
        "prices",
        "rose",
        "10"
    ]
    
def test_iter_documents(tmp_path,monkeypatch):
    content = """
    <REUTERS NEWID="1">
        <TEXT>
            <TITLE>Apple Market</TITLE>
            <BODY>Prices rose.</BODY>
        </TEXT>
    </REUTERS>

    <REUTERS NEWID="2">
        <TEXT>
            <TITLE>Banana Market</TITLE>
            <BODY>Prices fell.</BODY>
        </TEXT>
    </REUTERS>
    """
    file_path = tmp_path /"reut2-000.sgm"
    file_path.write_text(content,encoding ="latin-1")
    
    monkeypatch.setattr(
        preprocessing,
        "DATA_DIR",
        tmp_path 
    )
    
    result = list(iter_documents())
    assert len(result) ==2 
    
    assert result [0]== (
                1,
        ["apple", "market", "prices", "rose"]
    )
    
    assert result[1] == (
                2,
        ["banana", "market", "prices", "fell"]
        
    )
    