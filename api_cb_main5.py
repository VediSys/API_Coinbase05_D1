# -*- coding: utf-8 -*-: *26072025
# REFERENCE do not alter
""" api_cb_main5.py |<250 ✓✓✓  :nov2425
    cb02_BPL_idx.py
    api_cb01_chatGPT.py

    - mobile networks and devices only.

    - Bollinger Bands(3),
      LaGuerre(4/5),
      Parabolic(2/3)

    _t = symbol = 16 portfolio items
    _d = 300    = daily interval maximum
    _i = 86400  = seconds in a day

    Meiner kleiner Düßenjäger*,
    ist daß ja nicht?

//-vedNOTES-----------------------------|
class Algorithmic_financial_decision:
    "" cyclical trading implementation ""
    #def __init__(self):

    def indicators # for the calculations
    def indicator_calcs
    def auto_trade
    
class Visual_financial_psychology:
    "" oversight via colour simplification ""
    #def __init__(self):

    def indicators # for the chart values
    def display_chart

def obtain_quotes, ...
if name ==__main__: , ...
//-NOTES--------------------------------|
days = [30,
    1,2,3,5,7,          # 5
    10,20,30,45,60,     #10
    90,120,180,240,     #15
    300]                #0+16
"""

# on first build prerequisite installs
from __future__ import absolute_import

#import time as tm
import math # req'd
import numpy as np
import matplotlib.pyplot as plt # req'd
from   matplotlib.widgets import Cursor
import mplfinance as mpf

from portfolio   import folio
from autosize_cb import obtain_df

from bollinger_bands import (
    upper_BB_band  as bb_up,
    middle_BB_band as bb_mid,
    lower_BB_band  as bb_low
)
from parabolic_sar3 import parabolic
from laguerre       import LaGuerre

from themestyle import \
    Theme, Chart_Type, style_dict


#file_name = "api_cb02_BPL_idx.py" # ----|
file_name = "api_cb_main5.py"
# 16
symbol = ('ATOM-USD', "BAT-USD",
    'BTC-USD','DASH-USD','ETH-USD',
    'GRT-USD','KAVA-USD',
	'MKR-USD','OP-USD','SAND-USD',
	'SOL-USD','XLM-USD',
	'XRP-USD')
# settings -----------------------------|
# _symbol, days to view, interval seconds
#-?_t, _d, _i = symbol[0], 11, 0 #60, 86400 # raw_input
_t, _d, _i = folio(1, 11, 0) #, 0) #11:XRP
_dec = 3 # decimal places in USD

curr, prev, pr3v = -1, -2, -3 # indexing
bb_p = np.abs(16.18) #17,20   # bollinger
# parabolic
af1, af2, af3, am1, am2, am3 = (
    0.01, 0.02, 0.03,
    0.1, 0.2, 0.3
) # laGuerre ranges (.25, .75)
gamma, delta, theta, epsilon, kappa = (
     0.25, 0.33, 0.5, 0.66, 0.75
)


def data_columns(df):
    """ Extract data columns.
          0   1   2   3   4   5
      || _u, _o, _h, _l, _c, _v  orig."""
    _o, _h, _l, _c = (
        df['Open'], df['High'],
        df['Low'], df['Close']
    )
    ohlc = _o, _h, _l, _c

    return ohlc


def tint_interpolations(
    laga, lagb, lagd, lage):
	ftint = ['royalblue',
	    'coral','cyan','lightblue',
	    'teal','salmon']
	# laguerre in panel 1
	#fb_up1, fb_dn1 = (
	#    dict(y1=laga,y2=lagb,where=lagb<=laga,color="#e06666",alpha=0.4,interpolate=True),
	#    dict(y1=laga,y2=lagb,where=lagb >laga,color="#93c47d",alpha=0.4,interpolate=True))
	#fb_up1['panel'], fb_dn1['panel'] = 1, 1
	# lagA, lagB in panel 1
	fb_up2, fb_dn2 = (
	    dict(y1=laga,y2=lagb,where=lagb >laga,color="#93c47d",alpha=0.4,interpolate=True),
	    dict(y1=laga,y2=lagb,where=lagb<=laga,color="#e06666",alpha=0.4,interpolate=True)
	)
	fb_up2['panel'], fb_dn2['panel'] = 1, 1 #2, 2
	# lagD, lagE in panel 1 also logic switched!
	fb_up4, fb_dn4 = (
	    dict(y1=lagd,y2=lage,where=lage >lagd,color="#e06666",alpha=0.5,interpolate=True),
	    dict(y1=lagd,y2=lage,where=lage<=lagd,color="#93c47d",alpha=0.5,interpolate=True)
	)
	fb_up4['panel'], fb_dn4['panel'] = 1, 1 #4, 4

	return [ #fb_up1, fb_dn1,
	    fb_up2, fb_dn2,
	    fb_up4, fb_dn4]

def main(df, _t, _d):
    """ indicator and chart elements."""
    #_o, _h, _l, _c = ohlc = data_columns(df)
    _o, _h, _l, _c = data_columns(df)
    #_o, _h, _l, _c = ohlc
    _style, _chart = 3, 3
    _title = (
        f"{_t} | {len(df)} Days"
        +" | $ "+str(_c[curr])
    ) # Bollinger Bands ----------------|
    bb_u, bb_m, bb_l = (
	    bb_up( _c, bb_p),
		bb_mid(_c, bb_p),
		bb_low(_c, bb_p)
	)
    bbu_panel, bbm_panel, bbl_panel = (
	    mpf.make_addplot(bb_u,
	        color='g',linestyle='-'),
	    mpf.make_addplot(bb_m,
	        color='g', linestyle='-'),
	    mpf.make_addplot(bb_l,
	        color='g',linestyle='-')
	) # Parabolic stop and reverse -----|
    (sar1, #sar2,
    sar3) = (
	    parabolic(_h,_l,af1,am1),
	    #parabolic(_h,_l,af2,am2),
	    parabolic(_h,_l,af3,am3)
	)
    (sar1_panel, #sar2_panel,
    sar3_panel) = (
	    mpf.make_addplot(sar1,
	        color="tomato", #i_clr[5],
	        type='scatter'),
	    #mpf.make_addplot(sar2,
	    #    color="beige", #i_clr[4],
	    #    type='scatter'),
	    mpf.make_addplot(sar3,
	        color="cadetblue", #i_clr[3],
	        type='scatter')
	) # La Guerre abcde ----------------|
    laga = LaGuerre(df, gamma)
    lagb = LaGuerre(df, delta)
    #lagc = LaGuerre(df, theta)
    lagd = LaGuerre(df, epsilon)
    lage = LaGuerre(df, kappa)

    laga_panel = (mpf.make_addplot(laga,
        color="dodgerblue",linestyle='-',panel=1))
    lagb_panel = (mpf.make_addplot(lagb,
        color="y",linestyle='-',panel=1))
    #lagc_panel = (mpf.make_addplot(lagc,
    #    color="gold",linestyle='-',panel=1))
    lagd_panel = (mpf.make_addplot(lagd,
        color="salmon",linestyle='-',panel=1))
    lage_panel = (mpf.make_addplot(lage,
        color="orangered",linestyle='-',panel=1))
    # uml, abcde -> edcba ! viewing order
    ind_panels = [
        bbu_panel, bbm_panel, bbl_panel,
        sar1_panel,sar3_panel, #sar3_panel,
        laga_panel,lagb_panel, #lagc_panel,
        lagd_panel, lage_panel
    ]
    x_label = ( #"\033[1;33;40m"+
        file_name
        +f"\n{_t} | {len(df)} Days"
        +f"\n  kappa({kappa}) {np.abs(lage[curr]*100):.2f}"
        +f"\nepsilon({epsilon}) {np.abs(lagd[curr]*100):.2f}"
        #+f"\n theta({theta}) {np.abs(lagc[curr]*100):.2f}"
        +f"\n     delta({delta}) {np.abs(lagb[curr]*100):.2f}"
        +f"\n  gamma({gamma}) {np.abs(laga[curr]*100):.2f}"
    )
    #interpolations = tint_interpolations(
	#    laga,lagb,lagd,lage)
	#    laga[:],lagb[:],lagd[:],lage[:])
	#calc_clr, price_clr, d_g = priceline_calcs(
	#    curr_o,curr_c,prev_h,prev_c,curr_rsi_a,curr_rsi_b,DEC)
	#c_vals, leg_fnt = {}, 16
    mpf_style = mpf.make_mpf_style(
        base_mpf_style=Theme(_style),
        marketcolors=mpf.make_marketcolors(
            up='dodgerblue',
            down='tomato',
            edge='w',
            wick={'up':'w', 'down':'w'},
            volume='in',
            ohlc='in'
        ),
        gridcolor='dimgrey',
        facecolor='k',
        edgecolor='w',
        rc=style_dict
    )
    fig, ax = mpf.plot(df, #fill_between=interpolations,
        type=Chart_Type(_chart),
        addplot=ind_panels,
        style=mpf_style,
        title=_title,
        hlines=dict(
            hlines=[_c[curr],_c[prev]],
            colors=['cyan','pink'],
	        linestyle='-.',
	        linewidths=[2.2, 1.7],
	        alpha=0.7
	    ),
        panel_ratios=(5, 2, 1),
        xlabel=x_label,
        mav=(8, 5, 3),
        mavcolors=( #'y','r','b'),
            'khaki','orangered','royalblue'),
        volume=True, volume_panel=2,
        figratio=(12, 8), figscale=1.75,
        figsize =(10.3, 20.5),
        tight_layout=False #, returnfig=True
    )
    ax[4].annotate(
        str(_d)+' days of '
        +_t+'  $'+str(_c[curr]),
        xy=(len(df)-1,_c[curr]),
        transform=ax[4].transAxes,
        textcoords='axes fraction',
        xytext=(0.02, 0.67),
        fontsize=14, #leg_fnt,
        color='w', #price_clr, #'khaki',
        bbox=dict(boxstyle='square',
        fc='w', #price_clr, #calc_clr,
        alpha=0.17)
    )
    cursor = (Cursor(ax[0], useblit=True,
        color='w', linewidth=2)
    )
    #cursor1 = (Cursor(ax[4],useblit=True,color='w',linewidth=2))
    #tm.sleep(11)
    plt.show(mpf.show())

    return

if __name__ == '__main__':
    """
    for i in ??:
    	_t, _d, _i = folio(i, 11, 0)
    	_df = obtain_df(_t, _d, _i, _dec)
    	display_chart(_df, _t, _d)
    	#tm.sleep(11)
    """
    _df = obtain_df(_t, _d, _i, _dec)

    main(_df, _t, _d)

    exit()
