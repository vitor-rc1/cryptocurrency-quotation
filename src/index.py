import websocket
import json
import threading 
from requests import get
from stick_service import save_stick

def start_monitoring(coin):
  stick_1_min_data = []
  stick_5_min_data = []
  stick_10_min_data = []

  sttick_1_min_thread = threading.Thread(
                                        target=save_stick, 
                                        args=(stick_1_min_data, 60, coin["name"]))

  sttick_5_min_thread = threading.Thread(
                                        target=save_stick, 
                                        args=(stick_5_min_data, 300, coin["name"]))      

  sttick_10_min_thread = threading.Thread(
                                        target=save_stick, 
                                        args=(stick_5_min_data, 600, coin["name"]))                                                                       

  def on_message(ws, message):
    _, _, data = json.loads(message)
    pair_id, last_price, *_ = data
    if pair_id == coin["id"]:
      stick_1_min_data.append(last_price)
      stick_5_min_data.append(last_price)
      stick_10_min_data.append(last_price)


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

def start(currency_pair, real_time_graph = False, interval = 1 ):
  try:
    all_tickers = get("https://poloniex.com/public?command=returnTicker")
    currency = json.loads(all_tickers.text)[currency_pair]
    start_monitoring({ "id": currency["id"], "name": currency_pair })

  except KeyError: 
    print("Moeda invalida ou inexistente")