# -*- coding: utf-8 -*- env: Pydroid
""" autosize_cb.py |50 ✓ DO NOT ALTER
    *30052025-02082025
    - obtains file and returns data OHLCV
"""
import time as tm
import http.client
import pandas as pd


def obtain_df(_t, _d, _i, _dec):
    """ Coinbase OHLCV to pd.DataFrame """
    end   = int(tm.time())
    start = end -(_i *_d)

    url = (f"/products/{_t}/candles?"
        +f"start={start}&end={end}"
        +f"&granularity={_i}"
    )
    headers = {
        "Content-Type": "application/json",
        "User-Agent": (
            "Mozilla/5.0 (Android 13; Mobile; rv:136.0)"
            " Gecko/136.0 Firefox/136.0"
        )
    }
    conn = http.client.HTTPSConnection(
        "api.exchange.coinbase.com")

    conn.request("GET", url, "", headers)
    # compile first build w/ matplotlib.
    df = pd.read_json(conn.getresponse())

    conn.close()
    # pd.DataFrame
    df.columns = ['Time',
        'Low','High','Open','Close',
        'Volume']
    # ensure data sequencing
    df = df.sort_values('Time')
    # Converts unixtime to datetime index
    df['Date'] = pd.to_datetime(
        df['Time'],unit='s')
    df.set_index('Date', inplace=True)
    # df = df[['Time',
    df = df[['Open','High','Low','Close',
        'Volume']].round(_dec)

    return df
