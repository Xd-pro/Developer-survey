from scarletdb import ScarletDB

db = ScarletDB([])
db.replit("answers")

db.remove({"choice": "Python"})