from src.rtml_core import Document

obj = Document.document("./tests/test_files/perfect_file.txt")

print(obj.search_document(search_type=["text", "tag", "subtag"], search_term="lorem"))
