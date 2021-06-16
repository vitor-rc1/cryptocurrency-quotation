from logging import error
import time
from datetime import datetime
from connection import insert_stick

def save_stick(stick, delay, coin):
    while True:
        time.sleep(delay)
        candle = (
                  coin, # coin
                  delay/60, # frequency
                  datetime.now().strftime('%Y-%m-%d %H:%M:%S'), # datetime
                  float(stick[0]), # open
                  float(min(stick)), # low
                  float(max(stick)), # high
                  float(stick[-1]) # close
                  )
        try:
          insert_stick(candle)
          stick.clear()
        except Exception:
          print(Exception)

