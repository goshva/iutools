from tinydb import TinyDB

ldb = TinyDB('db/lessons.db') # db with parsings
ldb.default_table_name = '_lessons'

tdb = TinyDB('db/tworks.db') # db with ykl testworks
tdb.default_table_name = '_tworks'

pdb = TinyDB('db/paper.db') # db with paperworks
pdb.default_table_name = '_paper'
# hi pasha

def search(id, _type):
	if _type == "parsing":
		if ldb.contains(doc_id=int(id)):
			return ldb.get(doc_id=int(id))["links"]

	if _type == "twork":
		if tdb.contains(doc_id=int(id)):
			return tdb.get(doc_id=int(id))["links"]

	if _type == "paper":
		if pdb.contains(doc_id=int(id)):
			return pdb.get(doc_id=int(id))["links"]

	return False # return False if something wasn't found
