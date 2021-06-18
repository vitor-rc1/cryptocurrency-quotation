from time import sleep
import json
import threading 
from requests import get
from tick_service import start_monitoring, live_graph_plot
from tick_model import create_table

def is_any_thread_alive(threads):
    return threads.is_alive()

def start(currency_pair, real_time_graph = False, frequency = 1 ):
  try:
    create_table()
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
  except Exception as exc:
    print(exc)