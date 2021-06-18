import time
import websocket
import threading 
import json
from datetime import datetime
import mplfinance as mpf
import pandas as pd
import matplotlib.animation as animation
from tick_model import insert_tick, get_ticks_data

def save_tick(tick, delay, coin):
  while True:
    time.sleep(delay)
    candle = (
              coin, # coin
              delay/60, # frequency
              datetime.now().strftime('%Y-%m-%d %H:%M:%S'), # datetime
              float(tick[0]), # open
              float(min(tick)), # low
              float(max(tick)), # high
              float(tick[-1]) # close
              )
    try:
      insert_tick(candle)
      print(f'Ultimo candle de {candle[1]} min(s) adicionado:')
      print(candle)
      tick.clear()
    except Exception as exc:
      print(exc)

def start_monitoring(coin):
  tick_1_min_data = []
  tick_5_min_data = []
  tick_10_min_data = []

  sttick_1_min_thread = threading.Thread(
                                        target=save_tick, 
                                        args=(tick_1_min_data, 60, coin["name"]))

  sttick_5_min_thread = threading.Thread(
                                        target=save_tick, 
                                        args=(tick_5_min_data, 300, coin["name"]))      

  sttick_10_min_thread = threading.Thread(
                                        target=save_tick, 
                                        args=(tick_10_min_data, 600, coin["name"]))

  def on_message(ws, message):
    _, _, data = json.loads(message)
    pair_id, last_price, *_ = data
    if pair_id == coin["id"]:
      tick_1_min_data.append(last_price)
      tick_5_min_data.append(last_price)
      tick_10_min_data.append(last_price)


  def on_error(ws, error):
    print(error)

  def on_close():
    print("programa encerrado")

  def on_open(ws):
    ws.send(json.dumps({ "command": "subscribe", "channel": 1002 }))

    sttick_1_min_thread.daemon = True
    sttick_1_min_thread.start()
    sttick_5_min_thread.daemon = True
    sttick_5_min_thread.start()
    sttick_10_min_thread.daemon = True
    sttick_10_min_thread.start()
    print("Monitoramento iniciado")


  ws = websocket.WebSocketApp("wss://api2.poloniex.com",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)
  
  ws.run_forever()
  print("programa encerrado")

def live_graph_plot(currency_pair, frequency):
  mc = mpf.make_marketcolors(up='g',down='r',
                            wick={'up':'blue','down':'orange'})
  style = mpf.make_mpf_style(marketcolors=mc, base_mpl_style='seaborn')
  fig = mpf.figure(style=style, figsize=(9,7))
  ax = fig.subplot()
  fig.suptitle(f'{currency_pair} VS Tempo')
  ax.set(xlabel='Tempo (hh:mm)', ylabel=f'{currency_pair} USD')

  def animate(i):
    data = get_ticks_data(frequency)
    data.index = pd.DatetimeIndex(data['datetime'])
    ax.clear()
    ax.set(xlabel='Tempo (hh:mm)', ylabel=f'{currency_pair} USD')
    mpf.plot(data, ax=ax, type='candle')

  _ = animation.FuncAnimation(fig, animate, interval=5000)
  mpf.show()