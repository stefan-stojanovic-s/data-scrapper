import sqlite3

sqlite3.connect('members.db').cursor().execute('DElete from members')