from database import Database

db = Database()
db.open()
print(db.get_devices())
db.close()