# -*-utf-8-*-: Pydroid
""" themestyle.py | 60 ✓✓
    - *05022023, **26072023 ✓✓✓30072025
"""

import mplfinance as mpf


BG_CLR, LN_CLR, TXT_CLR = ('k','lime','y')

style_dict = {
    'figure.facecolor':'#252525', #darkslategrey',
    'text.color':'khaki',
    'xtick.color': LN_CLR,
    'ytick.color': LN_CLR,
    'xtick.labelcolor': TXT_CLR,
    'ytick.labelcolor': TXT_CLR,
    'axes.labelcolor': LN_CLR,
    'axes.spines.top': False,
    'axes.spines.right': False}


def Theme(index):
	""" choose setting: 0-13."""
	themes = ['binance',
	    'blueskies', 'brasil', 'charles',
	    'checkers', 'classic',
	    'default', 'ibd', 'kenan',
	    'mike', 'nightclouds',
	    'sas', 'starsandstripes',
	    'yahoo']

	return themes[index % len(themes)]


def Chart_Type(index):
    """ default: 3."""
    types = ['line',
        'ohlc','hollow','candle']

    return types[index % len(types)]


def _style():
    Style = mpf.make_mpf_style(
        base_mpf_style=Theme(3),
        marketcolors=_chart,
        gridcolor='g',facecolor='k',
	    rc={#'figure.facecolor':'yellow',
	        'text.color':'khaki',
	        'xtick.labelcolor':'lime',
	        'ytick.labelcolor':TXT_CLR} #'yellow'}
	    ) #; return Style


def _chart():
    Chart = mpf.make_marketcolors(
        up='dodgerblue',down='tomato',edge='k',
        wick={'up':'aqua','down':'orange'},
        volume='in',ohlc='gold'
        )
    #return Chart
