import rtml_core.Document

obj = rtml_core.Document.document("./files/kan-input.txt")

res = obj.search_document(search_type=["subtag"], search_term="ಉಳಿದ")

print(res)
