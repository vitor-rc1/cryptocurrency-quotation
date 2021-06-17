import time
from datetime import datetime
from stick_model import insert_stick

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
      print(f"Ultimo candle de {candle[1]} adicionado:")
      print(candle)
      stick.clear()
    except Exception as exc:
      print(exc)
