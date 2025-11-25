# -*- coding: utf-8 -*-:
""" api_cb_BLPredux.py |<140✓nov252025
    Coinbase public API version.(D1 only)

    - Bollinger Bands(3),
      LaGuerre(4/5),
      Parabolic(2/3)

    _t = symbol = 16 portfolio items
    _d = 300    = daily interval maximum
    _i = 86400  = seconds in a day

symbol = ('ATOM-USD',
    'BTC-USD','DASH-USD','ETH-USD',
    'GRT-USD','KAVA-USD',
	'MKR-USD','OP-USD','SAND-USD',
	'SOL-USD','XLM-USD',
	'XRP-USD')

days = [30,             # 0
    1,2,3,5,7,          # 5
    10,20,30,45,60,     #10
    90,120,180,240,     #15
    300]                #0+16 = max.300
"""

# on first build prerequisite installs
import math # req'd
import numpy as np
import matplotlib.pyplot # req'd
import mplfinance as mpf

from portfolio       import folio
from autosize_cb     import obtain_df
from bollinger_bands import (
    upper_BB_band    as bb_up,
    middle_BB_band   as bb_mid,
    lower_BB_band    as bb_low)
from parabolic_sar3  import parabolic
from laguerre        import LaGuerre
from themestyle      import \
    Theme, Chart_Type, style_dict


# -- settings -----------------------------

#symbol, days to view, interval seconds
# ex.: "_t, _d, _i = symbol[1],60,86400" == 60 days BTCUSD
_t, _d, _i = folio(5, 11, 0)
# --------------------------------------------------------
_dec = 3                      # decimal places
curr, prev, pr3v = -1, -2, -3 # indexing
bb_p = np.abs(16.18) #17 #20  # Bollinger
af1, af2, af3, am1, am2, am3 = ( # Parabolic
    0.01,0.02,0.03, 0.1, 0.2, 0.3) # laGuerre
gamma, delta, theta, epsilon, kappa = (
     0.25, 0.33, 0.5, 0.66, 0.75)


def data_columns(df):
    _o, _h, _l, _c = df['Open'],df['High'],df['Low'],df['Close']
    ohlc = _o, _h, _l, _c

    return ohlc


def display_chart(df, _t, _d):
    """ indicator and chart elements."""
    #_o, _h, _l, _c = ohlc = data_columns(df)
    _o, _h, _l, _c = data_columns(df)
    _style, _chart = 3, 3
    _title = (f"{_t} | {len(df)} Days | $ "+str(_c[curr]))
    # Bollinger Bands ----------------|
    bb_u, bb_m, bb_l = bb_up( _c,bb_p),bb_mid(_c,bb_p),bb_low(_c,bb_p)
    bbu_panel, bbm_panel, bbl_panel = (
	    mpf.make_addplot(bb_u, color='g', linestyle='-'),
	    mpf.make_addplot(bb_m, color='g', linestyle='-'),
	    mpf.make_addplot(bb_l, color='g', linestyle='-')
	) # Parabolic SAR (hobbled)---------|
    (sar1, #sar2,
    sar3) = (
	    parabolic(_h,_l,af1,am1),
	    #parabolic(_h,_l,af2,am2),
	    parabolic(_h,_l,af3,am3)
	)
    (sar1_panel, #sar2_panel,
    sar3_panel) = (
	    mpf.make_addplot(sar1, color="tomato", type='scatter'),
	    #mpf.make_addplot(sar2, color="beige", type='scatter'),
	    mpf.make_addplot(sar3, color="cadetblue", type='scatter')
	) # La Guerre abcde (hobbled)-------|
    laga, lagb = LaGuerre(df, gamma), LaGuerre(df, delta)
    #lagc = LaGuerre(df, theta)
    lagd, lage = LaGuerre(df, epsilon), LaGuerre(df, kappa)

    laga_panel = mpf.make_addplot(laga,color="dodgerblue",linestyle='-',panel=1)
    lagb_panel = mpf.make_addplot(lagb,color="y",linestyle='-',panel=1)
    #lagc_panel = (mpf.make_addplot(lagc,
    #    color="gold",linestyle='-',panel=1))
    lagd_panel = mpf.make_addplot(lagd,color="salmon",linestyle='-',panel=1)
    lage_panel = mpf.make_addplot(lage,color="orangered",linestyle='-',panel=1)
    # uml, abcde -> edcba overlay sequence
    ind_panels = [
        bbu_panel, bbm_panel, bbl_panel,
        sar1_panel,sar3_panel, #sar3_panel,
        laga_panel,lagb_panel, #lagc_panel,
        lagd_panel, lage_panel
    ]
    x_label = (f"{_t} | {len(df)} Days"
        +f"\n   kappa({kappa}) {np.abs(lage[curr]):.2f}"
        +f"\n epsilon({epsilon}) {np.abs(lagd[curr]):.2f}"
        #+f"\n theta({theta}) {np.abs(lagc[curr]):.2f}"
        +f"\n    delta({delta}) {np.abs(lagb[curr]):.2f}"
        +f"\n gamma({gamma}) {np.abs(laga[curr]):.2f}"
    )
    mpf_style = mpf.make_mpf_style(
        base_mpf_style=Theme(_style),
        marketcolors=mpf.make_marketcolors(up='dodgerblue', down='tomato',
            edge='w', wick={'up':'w', 'down':'w'}, volume='in', ohlc='in'),
        gridcolor='dimgrey', facecolor='k', edgecolor='w', rc=style_dict
    )
    fig, ax = mpf.plot(df, type=Chart_Type(_chart),
        addplot=ind_panels, style=mpf_style, title=_title,
        hlines=dict(hlines=[_c[curr], _c[prev]], colors=['cyan','pink'],
	        linestyle='-.', linewidths=[2.2, 1.7], alpha=0.7),
        panel_ratios=(5, 2, 1), xlabel=x_label,
        mav=(8, 5, 3), mavcolors=('y','r','b'),
        volume=True, volume_panel=2,
        figratio=(12, 8), figscale=1.75, figsize =(10.3, 20.5),
        tight_layout=False
    )


if __name__ == '__main__':
    _df = obtain_df(_t, _d, _i, _dec)
    display_chart(_df, _t, _d)
    exit()
