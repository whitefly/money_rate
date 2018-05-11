from modules.database import Database
from pymongo import cursor

Database.inti()

collection_name = "demo"

# Database.insert(collection_name, {"name": "周昂", "age": 18})
# Database.insert(collection_name, {"name": "周扬元", "age": 24})

cur = Database.find_one(collection_name, query={"name": "周昂"})
print(type(cur))
print(cur['age'])
