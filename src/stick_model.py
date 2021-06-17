import mysql.connector

def connection():
  mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="hdq001@@",
  database="smart-graph"
  )
  return mydb

def insert_stick(new_stick):
  mydb = connection()
  cursor = mydb.cursor()
  sql = f"""
  INSERT INTO candle_sticks (coin, frequency, datetime, open, low, high, close) 
  VALUES {new_stick}
  """
  cursor.execute(sql)
  mydb.commit()
  print(cursor.rowcount, "record inserted.")
  