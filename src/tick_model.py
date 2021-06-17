import mysql.connector
import pandas as pd

def connection():
  mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="hdq001@@",
  database="smart-graph"
  )
  cursor = mydb.cursor()
  return mydb, cursor

def insert_tick(new_tick):
  mydb, cursor = connection()
  sql = f"""
  INSERT INTO candlesticks (coin, frequency, datetime, open, low, high, close) 
  VALUES {new_tick}
  """
  cursor.execute(sql)
  mydb.commit()
  print(cursor.rowcount, "record inserted.")

def get_ticks_data(frequency):
  mydb, cursor = connection()
  sql = f"""
            SELECT datetime, open, high, low, close 
            FROM candlesticks WHERE frequency = {frequency}
            ORDER BY id DESC
            LIMIT 10"""
  return pd.read_sql(sql, con=mydb).sort_values(by=['datetime'])
