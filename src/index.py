from time import sleep
import websocket
import json
import threading 
from requests import get
from tick_service import save_tick, live_graph_plot

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
                                        args=(tick_5_min_data, 600, coin["name"]))

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

def is_any_thread_alive(threads):
    return threads.is_alive()

def start(currency_pair, real_time_graph = False, frequency = 1 ):
  try:

    all_tickers = get("https://poloniex.com/public?command=returnTicker")
    currency = json.loads(all_tickers.text)[currency_pair]
    
    monitoring_thread = threading.Thread(target = start_monitoring, 
                                        args = ({ "id": currency["id"], "name": currency_pair }, ),
                                        daemon = True)
    monitoring_thread.start()
    
    if real_time_graph:
      if frequency == 1 or frequency == 5 or frequency == 10:
        live_graph_plot(currency_pair, frequency)
      else:
        raise ValueError('Valor de intervalo incorreto. Valores validos: 1, 5, 10')

    while is_any_thread_alive(monitoring_thread):
      sleep(1)

  except KeyError: 
    print("Moeda invalida ou inexistente")
  except KeyboardInterrupt:
    print("programa encerrado")