import sqlobject
from Connection import conn

class PhoneNumber(sqlobject.SQLObject):
    _connection = conn
    number = sqlobject.StringCol(length=14, unique=True)
    owner = sqlobject.StringCol(length=255)
    lastCall = sqlobject.DateTimeCol(default=None)
PhoneNumber.createTable(ifNotExists=True)
