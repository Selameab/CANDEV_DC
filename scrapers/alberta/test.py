from tinydb import TinyDB, Query

db = TinyDB('./alberta.json')

for i in range(10000):
    db.insert({'here': i})
    if len(db) > 100:
        print(db['1'])
    print(len(db))

