# -*- coding: utf-8 -*- env: Pydroid
""" portfolio.py |50 ✓ DO NOT ALTER
    *31072025
    - accommodates two methods.
"""
def portfolio(T, D, I):
	""" receives 29,14,16 (int 0-28, 0-13, 0-15).
	    returns (str, int, str)."""
	symbol, days, interval = ('ATOM-USD',
        'BTC-USD','DASH-USD','ETH-BTC',
        'ETH-USD','KAVA-USD',
	    'MKR-USD','OP-USD','SAND-USD',
	    'XLM-USD','SOL-USD',
	    'FONE-USD'),(30,
	    1,2,3,5,7,
	    10,20,30,45,60,
        90,120,180),(86400,
        60,120,300,900,1800,
        3600,5400,86400
    )
    #] #,['1d',
    #'1m','2m','5m','15m','30m',
    #'60m','90m','1d','5d','1wk',
    #'1mo','3mo','6mo','1yr','1y']
	return (
	    symbol[T], days[D], interval[I]
	)


def folio(T, D, I):
	# 12 e.g.,0->11
	symbol = ('ATOM-USD',
        'BTC-USD','DASH-USD','ETH-USD',
        'GRT-USD','KAVA-USD',
	    'MKR-USD','OP-USD','SAND-USD',
	    'SOL-USD','XLM-USD',
	    'XRP-USD'
	) # 300 days max.!
	days = (45,
	    1,2,3,5,7,
	    10,20,30,45,60,
	    90,120,180,240
	) # 1D, 1m 2m 5m 15m 30m, 1h 90m 2h 4h 1D
	interval = (86400,
	    60,120,300,900,1800,
	    3600,5400,7200,14400,86400
	) # returns lengths
	#len(symbol),#len(days),#len(interval) # 0->10
	return symbol[T], days[D], interval[I]
