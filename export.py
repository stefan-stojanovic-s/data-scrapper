import pandas as pd
import sqlite3

conn=sqlite3.connect('members.db')
df=pd.read_sql_query('SELECT * from members',conn)
df.to_csv('reports.csv')
conn.close()
print("report created")