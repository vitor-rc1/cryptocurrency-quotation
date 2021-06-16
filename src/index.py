import websocket
import json
import threading 
from save_stick import save_stick

stick_1_min_data = []
stick_5_min_data = []
stick_10_min_data = []

sttick_1_min_thread = threading.Thread(
                                      target=save_stick, 
                                      args=(stick_1_min_data, 60, "BTC"))

sttick_5_min_thread = threading.Thread(
                                      target=save_stick, 
                                      args=(stick_5_min_data, 300, "BTC"))      

sttick_10_min_thread = threading.Thread(
                                      target=save_stick, 
                                      args=(stick_5_min_data, 600, "BTC"))                                                                       

def on_message(ws, message):
  _, _, data = json.loads(message)
  pair_id, last_price, *_ = data
  if pair_id == 121:
    stick_1_min_data.append(last_price)
    stick_5_min_data.append(last_price)
    stick_10_min_data.append(last_price)
    print(last_price)


def on_error(ws, error):
  print(error)

def on_close(ws, close_status_code, close_msg):
  print("### programa encerrado ###")

def on_open(ws):
  ws.send(json.dumps({ "command": "subscribe", "channel": 1002 }))
  sttick_1_min_thread.daemon = True
  sttick_1_min_thread.start()
  sttick_5_min_thread.daemon = True
  sttick_5_min_thread.start()
  sttick_10_min_thread.daemon = True
  sttick_10_min_thread.start()
  print("Começou")


ws = websocket.WebSocketApp("wss://api2.poloniex.com",
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)
ws.run_forever()