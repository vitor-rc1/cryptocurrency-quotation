import websocket
import json
import multiprocessing 
from timerWhile import conta_tempo


stick_1_min = []
stick_5_min = []
stick_10_min = []

stop_process = False

start_time = multiprocessing.Process(target=conta_tempo)
# start_time2 = threading.Timer(20, print("asa2"))
# start_time3 = threading.Timer(30, print("asa3"))

def on_message(ws, message):
  _, _, data = json.loads(message)
  pair_id, last_price, *_ = data
  if pair_id == 121:
    stick_1_min.append(last_price)
    # stick_5_min.append(last_price)
    # stick_10_min.append(last_price)
    print(last_price)


def on_error(ws, error):
  print(error)

def on_close(ws, close_status_code, close_msg):
  start_time.terminate()
  # start_time2.cancel()
  # start_time3.cancel()
  print("### closed ###")

def on_open(ws):
  ws.send(json.dumps({ "command": "subscribe", "channel": 1002 }))
  start_time.start()
  # start_time2.start()
  # start_time3.start()
  print("Começou")


ws = websocket.WebSocketApp("wss://api2.poloniex.com",
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)
ws.run_forever()