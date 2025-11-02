#-*-utf-8-*-: Pydroid python
""" macd_signal.py |22 ✓"""
import numpy as np


def Macd( #app_0.
    df_c,
    fast, slow, ema):
	""" MACD as an external function."""
	expa = df_c.ewm(span=fast, adjust=False).mean()
	expb = df_c.ewm(span=slow, adjust=False).mean()
	macd = expa -expb
	# ---.
	signal = macd.ewm(span=ema, adjust=False).mean()
	histogram = macd -signal
	
	macd = np.round(macd.dropna(),2)
	signal = np.round(signal.dropna(),2)
	histogram = np.round(histogram.dropna(),2)

	return macd, signal, histogram
