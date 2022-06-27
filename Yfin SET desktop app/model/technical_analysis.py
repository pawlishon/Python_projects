import yfinance as yf
import talib
import finplot as fplt
import numpy as np


def plot_patterns(df, ax, ms: bool = True, es: bool = True, eng: bool = True, hm: bool = True):
    min_price = df['Low'].min()
    max_price = df['High'].max()
    if ms:
        morning_star = talib.CDLMORNINGSTAR(df['Open'], df['High'], df['Low'], df['Close'])
        df['Morning Star'] = morning_star
        morning_star_dates = df[df['Morning Star'] == 100].index
        for pattern_date in morning_star_dates:
            fplt.add_line((pattern_date, min_price), (pattern_date, max_price), color='#2ECC71', ax=ax)
    if es:
        evening_star = talib.CDLEVENINGSTAR(df['Open'], df['High'], df['Low'], df['Close'])
        df['Evening Star'] = evening_star
        evening_star_dates = df[df['Evening Star'] == -100].index
        for pattern_date in evening_star_dates:
            fplt.add_line((pattern_date, min_price), (pattern_date, max_price), color='#E74C3C', ax=ax)
    if eng:
        engulfing = talib.CDLENGULFING(df['Open'], df['High'], df['Low'], df['Close'])
        df['Engulfing'] = engulfing
        bullish_engulfing_dates = df[df['Engulfing'] == 100].index
        bearish_engulfing_dates = df[df['Engulfing'] == -100].index
        for pattern_date in bullish_engulfing_dates:
            fplt.add_line((pattern_date, min_price), (pattern_date, max_price), color='#5DADE2', ax=ax)
        for pattern_date in bearish_engulfing_dates:
            fplt.add_line((pattern_date, min_price), (pattern_date, max_price), color='#F4D03F', ax=ax)
    if hm:
        hanging_man = talib.CDLHANGINGMAN(df['Open'], df['High'], df['Low'], df['Close'])
        df['Hanging man'] = hanging_man
        hanging_dates = df[df['Hanging man'] == -100].index
        for pattern_date in hanging_dates:
            fplt.add_line((pattern_date, min_price), (pattern_date, max_price), color='#F5B041', ax=ax)


def plot_moving_average(df, ax, short: int, long: int):
    df['ma10'] = df.Close.rolling(short).mean()
    df['ma50'] = df.Close.rolling(long).mean()
    fplt.plot(df.ma10, legend='MA10', ax=ax)
    fplt.plot(df.ma50, legend='MA50', ax=ax)


def plot_bollinger_bands(df, ax):
    mean = df.Close.rolling(20).mean()
    stddev = df.Close.rolling(20).std()
    df['boll_hi'] = mean + 2.5*stddev
    df['boll_lo'] = mean - 2.5*stddev
    p0 = df.boll_hi.plot(color='#808080', legend='BB', ax=ax)
    p1 = df.boll_lo.plot(color='#808080', ax=ax)
    fplt.fill_between(p0, p1, color='#bbb')


def plot_rsi(df, ax):
    diff = df.Close.diff().values
    gains = diff
    losses = -diff
    with np.errstate(invalid='ignore'):
        gains[(gains<0)|np.isnan(gains)] = 0.0
        losses[(losses<=0)|np.isnan(losses)] = 1e-10 # we don't want divide by zero/NaN
    n = 14
    m = (n-1) / n
    ni = 1 / n
    g = gains[n] = np.nanmean(gains[:n])
    l = losses[n] = np.nanmean(losses[:n])
    gains[:n] = losses[:n] = np.nan
    for i, v in enumerate(gains[n:],n):
        g = gains[i] = ni*v + m*g
    for i, v in enumerate(losses[n:],n):
        l = losses[i] = ni*v + m*l
    rs = gains / losses
    df['rsi'] = 100 - (100/(1+rs))
    df.rsi.plot(ax=ax, legend='RSI')
    fplt.set_y_range(0, 100, ax=ax)
    fplt.add_band(30, 70, ax=ax)


def plot_vol_hist(df, ax):
    fplt.add_legend('Volume', ax=ax)
    fplt.bar(df.Volume, ax=ax)


def plot_ta(ticker, start_date, end_date, bb:bool = True, rsi: bool = True, ma: bool = True, vol: bool = True, patterns:bool = True, short: int = 10, long: int = 50):
    # today = date.today().strftime('%Y-%m-%d')
    rows = 1
    if vol:
        rows += 1
    if rsi:
        rows +=1
    df = yf.download(ticker, start=start_date, end=end_date)
    if rows == 1:
        ax = fplt.create_plot(f'Technical Analysis for {ticker}', rows=rows)
    elif rows ==2:
        ax, ax2 = fplt.create_plot(f'Technical Analysis for {ticker}', rows=rows)
    else:
        ax, ax2, ax3 = fplt.create_plot(f'Technical Analysis for {ticker}', rows=rows)
    fplt.candlestick_ochl(df[['Open', 'Close', 'High', 'Low']], ax=ax)
    if bb:
        plot_bollinger_bands(df, ax)
    if rsi:
        plot_rsi(df, ax2)
    if ma:
        plot_moving_average(df, ax, short, long)
    if vol and rsi:
        plot_vol_hist(df, ax3)
    if vol and not rsi:
        plot_vol_hist(df, ax2)
    if patterns:
        plot_patterns(df, ax)
    fplt.show()


