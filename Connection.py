######################################################
# Exemplos de uso do sqlobject
######################################################
import sqlobject

from sqlobject.mysql import builder
conn = 'mysql://dbuser:dbpassword@localhost/sqlobject_demo?debug=1'

"""
Database Connections Examples:

    MySQL
    conn = MySQLConnection(user='test', passwd='pwd', db='testdb') 
           [this method is now deprecated. Use the URI method below]
    conn = 'mysql://test:pwd@localhost/testdb'
    conn = 'mysql://test:pwd@localhost/testdb?debug=1'
           [To allow debugging, shows sql queries]
    
    PostgreSQL
    conn = PostgresConnection('user=test passwd=pwd dbname=testdb') 
           [this method is now deprecated. Use the URI method below]
    conn = 'postgres://test:pwd@localhost/testdb'

    SQLite
    conn = SQLiteConnect('database.db')
    conn = 'sqlite://path/to/database.db'

    DBM
    conn = DBMConnection('database/')
    conn = 'dbm://path/to/database/'

... (then assign using:)

    class Person(SQLObject):
         _connection = conn
"""
