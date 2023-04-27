from database import Database


db = Database()


db.open()
print(len(db.get_all_data()))
print(db.get_all_data())

db.close()