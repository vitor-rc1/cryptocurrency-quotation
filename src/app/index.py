import json
from requests import get
from tick_service import start_monitoring
from tick_model import create_table

# def is_any_thread_alive(threads):
#     return threads.is_alive()

def getId(currency_pair, currencies):
  return {
    "currency_pair": currency_pair,
    "id": currencies[currency_pair]["id"],
    "data": []
  }

def start(currency_pair):
  try:
    create_table()

    all_currencies_pair = get("https://poloniex.com/public?command=returnTicker")
    currencies_pair_json = json.loads(all_currencies_pair.text)

    filtered_currencies_pair = [getId(currency_pair, currencies_pair_json) for currency_pair in currency_pair]

    print(currency_pair)

    start_monitoring(filtered_currencies_pair)

  except KeyError: 
    print("Uma das moedas passada é invalida ou inexistente")
  except KeyboardInterrupt:
    print("programa encerrado")
  except Exception as exc:
    print(exc)