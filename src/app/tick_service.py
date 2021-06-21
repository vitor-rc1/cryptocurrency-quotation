import time
import websocket
import threading 
import json
import copy
from datetime import datetime
import mplfinance as mpf
import pandas as pd
from tabulate import tabulate
import matplotlib.animation as animation
from tick_model import insert_tick, get_ticks_data

def create_candle(currency, delay): 
  return (
          currency["currency_pair"], # coin
          round(delay/60), # frequency
          datetime.now().strftime('%Y-%m-%d %H:%M:%S'), # datetime
          float(currency["data"][0]), # open
          float(min(currency["data"])), # low
          float(max(currency["data"])), # high
          float(currency["data"][-1]) # close
        )

def save_tick(currencies, delay):
  while True:
    time.sleep(delay)
    candlesticks = [create_candle(currency, delay) for currency in currencies]
    for index in range(len(currencies)):
      currencies[index]["data"].clear()


    try:
      insert_tick(candlesticks)

      headers = ["Currency", "Frequency", "Datetime", "Open", "Low", "High", "Close"]
      print(tabulate(candlesticks, headers=headers))


    except Exception as exc:
      print(exc)

def start_monitoring(currencies):
  tick_1_min_data = copy.deepcopy(currencies)
  tick_5_min_data = copy.deepcopy(currencies)
  tick_10_min_data = copy.deepcopy(currencies)

  sttick_1_min_thread = threading.Thread(
                                        target=save_tick, 
                                        args=(tick_1_min_data, 60, ))

  sttick_5_min_thread = threading.Thread(
                                        target=save_tick, 
                                        args=(tick_5_min_data, 300, ))      

  sttick_10_min_thread = threading.Thread(
                                        target=save_tick, 
                                        args=(tick_10_min_data, 600, ))

  def on_message(ws, message):
    _, _, data = json.loads(message)
    pair_id, last_price, *_ = data

    for index in range(len(currencies)):
      if pair_id == currencies[index]["id"]:

        tick_1_min_data[index]["data"].append(last_price)
        tick_5_min_data[index]["data"].append(last_price)
        tick_10_min_data[index]["data"].append(last_price)

  def on_error(ws, error):
    print(error)

  def on_close():
    print("Programa encerrado")

  def on_open(ws):
    ws.send(json.dumps({ "command": "subscribe", "channel": 1002 }))

    sttick_1_min_thread.daemon = True
    sttick_1_min_thread.start()
    sttick_5_min_thread.daemon = True
    sttick_5_min_thread.start()
    sttick_10_min_thread.daemon = True
    sttick_10_min_thread.start()

    print("\nMonitoramento iniciado\n")


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
    data = get_ticks_data(currency_pair, frequency)
    if not data.empty:
      data.index = pd.DatetimeIndex(data['datetime'])
      ax.clear()
      ax.set(xlabel='Tempo (hh:mm)', ylabel=f'{currency_pair} USD')
      mpf.plot(data, ax=ax, type='candle')

  _ = animation.FuncAnimation(fig, animate, interval=5000)
  mpf.show()