import ccxt
import pandas as pd
import matplotlib
matplotlib.use('TkAgg') # TkAgg Qt5Agg
import matplotlib.pyplot as plt

testnet = False

bitmex = ccxt.bitmex()

if testnet:
    bitmex.set_sandbox_mode(True)

def fetch_ohlcv(symbol, timeframe, limit):
    global bitmex

    result = bitmex.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(result, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    return df

def main():
    symbol = "BTC/USDT"
    timeframe = "1d"
    limit = 55

    smaller_limit = 5
    larger_limit = 30

    data = fetch_ohlcv(symbol, timeframe, limit)
    data[f'SMA_{smaller_limit}'] = data['close'].rolling(window=3).mean()
    data[f'SMA_{larger_limit}'] = data['close'].rolling(window=7).mean()



    
    print(data)

    fig, ax = plt.subplots()

    timestamps = data['timestamp']
    SMA_smaller_points = data[f'SMA_{smaller_limit}']
    SMA_larger_points = data[f'SMA_{larger_limit}']

    line_smaller = ax.plot(timestamps, SMA_smaller_points, marker='o', linestyle='-', color='b', label=f'{smaller_limit} period')

    line_larger = ax.plot(timestamps, SMA_larger_points, marker='o', linestyle='-', color='g', label=f'{larger_limit} period')


    ax.set_xlabel('Time')
    ax.set_ylabel('Average Price')
    ax.set_title('Moving Averages')
    ax.grid(True)
    ax.legend()

    plt.show()
main()


