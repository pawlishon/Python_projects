import yfinance as yf
import talib
from datetime import date
import finplot as fplt

today = date.today().strftime('%Y-%m-%d')
ticker = '^GSPC'

df = yf.download(ticker, start='2022-01-01', end=today)

morning_star = talib.CDLMORNINGSTAR(df['Open'], df['High'], df['Low'], df['Close'])
evening_star = talib.CDLEVENINGSTAR(df['Open'], df['High'], df['Low'], df['Close'])
engulfing = talib.CDLENGULFING(df['Open'], df['High'], df['Low'], df['Close'])
hanging_man = talib.CDLHANGINGMAN(df['Open'], df['High'], df['Low'], df['Close'])
df['Morning Star'] = morning_star
df['Evening Star'] = evening_star
df['Engulfing'] = engulfing
df['Hanging man'] = hanging_man

min_price = df['Low'].min()
max_price = df['High'].max()

bullish_engulfing_dates = df[df['Engulfing'] == 100].index
bearish_engulfing_dates = df[df['Engulfing'] == -100].index
morning_star_dates = df[df['Morning Star'] == 100].index
evening_star_dates = df[df['Evening Star'] == -100].index
hanging_dates = df[df['Hanging man'] == -100].index


fplt.candlestick_ochl(df[['Open', 'Close', 'High', 'Low']])
for pattern_date in bullish_engulfing_dates:
    fplt.add_line((pattern_date, min_price), (pattern_date, max_price), color='#5DADE2')
for pattern_date in bearish_engulfing_dates:
    fplt.add_line((pattern_date, min_price), (pattern_date, max_price), color='#F4D03F')
for pattern_date in morning_star_dates:
    fplt.add_line((pattern_date, min_price), (pattern_date, max_price), color='#2ECC71')
for pattern_date in evening_star_dates:
    fplt.add_line((pattern_date, min_price), (pattern_date, max_price), color='#E74C3C')
for pattern_date in hanging_dates:
    fplt.add_line((pattern_date, min_price), (pattern_date, max_price), color='#F5B041')
fplt.show()

