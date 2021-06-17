import time
from datetime import datetime
import mplfinance as mpf
import pandas as pd
import matplotlib.animation as animation
from tick_model import insert_tick
from tick_model import get_ticks_data

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

  ani = animation.FuncAnimation(fig, animate, interval=5000)
  mpf.show()