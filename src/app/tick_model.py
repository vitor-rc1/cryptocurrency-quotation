import mysql.connector
import pandas as pd

def connection():
  mydb = mysql.connector.connect(
  host="cryptocurrency-quotation_db_1",
  # host="localhost",
  user="root",
  password="smartt",
  database="smartt-graph"
  )
  cursor = mydb.cursor()
  return mydb, cursor

def create_table():
  _, cursor = connection()
  cursor.execute("""
  CREATE TABLE IF NOT EXISTS `smartt-graph`.`candlesticks` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `coin` VARCHAR(45) NOT NULL,
  `frequency` INT NOT NULL,
  `datetime` DATETIME NOT NULL,
  `open` FLOAT NOT NULL,
  `low` FLOAT NOT NULL,
  `high` FLOAT NOT NULL,
  `close` FLOAT NOT NULL,
  PRIMARY KEY (`id`));
  """)

def insert_tick(candlesticks):
  mydb, cursor = connection()
  sql = """
  INSERT INTO candlesticks (coin, frequency, datetime, open, low, high, close) 
  VALUES (%s, %s, %s, %s, %s, %s, %s);
  """
  cursor.executemany(sql, candlesticks)
  mydb.commit()
  return(f"{cursor.rowcount} record inserted.")

def get_ticks_data(currency_pair, frequency):
  mydb, cursor = connection()
  sql = f"""
            SELECT datetime, open, high, low, close 
            FROM candlesticks WHERE frequency = {frequency} and coin = '{currency_pair}'
            ORDER BY id DESC
            LIMIT 10;
          """
  return pd.read_sql(sql, con=mydb).sort_values(by=['datetime'])
