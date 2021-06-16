import time
from datetime import datetime

def save_stick(stick, delay, coin):
    while True:
        time.sleep(delay)
        print(stick)

        candle = (
                  coin, # Moeda
                  delay/60, # Periodicidade
                  datetime.now(), # Datetime
                  stick[0], # Open
                  min(stick), # Low
                  max(stick), # High
                  stick[-1] # Close
                  )
        print(candle)        
        stick.clear()
