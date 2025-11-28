# -*- coding: utf-8 -*- env: Pydroid
""" api_cb_main.py |<400✓✓
    - base_architecture:  *23122023
    - last edit: 17092024, 10102025
      w/development notes.

    - All-in-one Python Pydroid periodic
      market monitor script using the
      Coinbase API with indicators,
      data acquisition, portfolio
      and theme scripts.

    - displays a window of axes panels
      in a figure with Bollinger Bands,
      dual LaGuerre and Volume,
      triple Parabolic Stop and Reverse,
      dual Relative Strength Index and
      MACD.
_________________________________________________.
@github/vedisys ©2023-2025 ARR
coffee?; send: BTC coinbase mainnet:
	3MZm5HF7USTC1RcNk2pTduHoZ6oBdw9pUs
#""
def price_diff(_df): #, period=pf[2]):
    #"" Intraday price change marker.""
    up_mark, dn_mark = [],[]
    for idx, row in _df.iterrows(): #for row in _df.iterrows():
        diff = _df['Open'].iloc[row] -_df['Close'].iloc[row]
        diff_pct = diff /_df['Open'].iloc[row]
        if diff_pct > 0.05:
            up_mark.append(row['Close'])
            dn_mark.append(np.nan)
        elif diff_pct < -0.05:
            dn_mark.append(row['Close'])
            up_mark.append(np.nan)
        else:
            up_mark.append(np.nan)
            dn_mark.append(np.nan)
    return np.array(up_mark, dn_mark)""
""def save_png(_df, _t, _i):
    "" ---.""
    #_T, _I = (str(spin1.get()), str(spin3.get()))
    #fig, _ax = mpf.plot(_df,savefig=FILENAME+_t+'_'+_i+'.png')
    return None
"""

# req'd (in sequence)
#import tkinter as tk
#import urllib
import sys
import time as tm
import numpy as np
#import pandas
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
import mplfinance as mpf
# custom scripts (11)
from autosize_cb import obtain_df
from portfolio import folio
# main panel indicators#from intraday_pricechange import price_diff
from bollinger_bands import (
    upper_BB_band  as bb_up,
    middle_BB_band as bb_mid,
    lower_BB_band  as bb_low)
from parabolic_sar3 import parabolic
# subplot panel indicators sequence
from laguerre          import LaGuerre
from relative_strength import relative
from macd_signal       import Macd
from commodity_channel import CCI #*-
from williams_range    import WPR
# decisi logicum plurare, prix
from indicator_calcs import \
    bb_calcs, laguerre_calcs, priceline_calcs
# output theme and style
from themestyle import \
    Theme, Chart_Type, style_dict


FILENAME = "api_tk_main.py"
# T: 0-11, D: 0-13, I: 0-12
Ticker, Days, Interval = folio(1, 0, 0)
#len(Ticker), len(Days), len(Interval)
T_len, D_len, I_len = (11, 9, 1) #len(Ticker), len(Days), len(Interval))

# application, indicator parameters.
DEC = 2                       # default: 4
GAMMA, THETA = 0.25, 0.75     # default: 0.75
CURR, PREV, LAST = -1, -2, -3 # sets flow
#up_mark, dn_mark = [],[]
# default: BB: 20, RSI: 14, 8, WPR: 14
bb_p, rsia_p, rsib_p, wpr_p = 17, 5, 8,14
fast, slow, ema = 11,17, 5 # 12,26,9 # macd default: 

af1, af2, af3, am1, am2, am3 = ( # Parabolic SAR
    0.01, 0.02, 0.05, # :.., 0.03,
    0.1,  0.2,  0.5)  # :.., 0.3)

ccia_p, ccib_p = 8, 17 # dual CCI (a,b) orig17,23
CCI_RND = 10000000     # 10M cci rounding factor
# colours (0-12); in specific idx order!
i_clr = ['g', #'lime', #'dodgerblue', #,'lime' -g maroon
	'g', #'lime',
	'g', #'lime', #'khaki','orangered',
	'dodgerblue','khaki','orangered',
	'aquamarine','salmon', #'royalblue','plum',
	'dodgerblue','orangered','khaki',
	'chartreuse','c','orangered','darkslategrey','white']
F_CLR = i_clr[13] #'#505050'


"""def wireless():
	while True:
		try:
			main() #urllib.error
			#exit()
		except : # urllib2.URLError
		    urllib.error
		    exit()
			
	return"""

def tint_interpolations( #laga,lagb,
    rsia,rsib,ccia,ccib,macd,signal):
	ftint = ['royalblue',
	    'coral','cyan','lightblue',
	    'teal','salmon']
	# laguerre in panel 1
	#fb_up1, fb_dn1 = (
	#    dict(y1=laga,y2=lagb,where=lagb<=laga,color="#e06666",alpha=0.4,interpolate=True),
	#    dict(y1=laga,y2=lagb,where=lagb >laga,color="#93c47d",alpha=0.4,interpolate=True))
	#fb_up1['panel'], fb_dn1['panel'] = 1, 1
	# rsiA, rsiB in panel 2
	fb_up2, fb_dn2 = (
	    dict(y1=rsia,y2=rsib,where=rsib<=rsia,color="#93c47d",alpha=0.4,interpolate=True),
	    dict(y1=rsia,y2=rsib,where=rsib >rsia,color="#e06666",alpha=0.4,interpolate=True)
	)
	fb_up2['panel'], fb_dn2['panel'] = 2, 2
	# cciA, cciB in panel 4
	fb_up4, fb_dn4 = (
	    dict(y1=ccia,y2=ccib,where=ccib<=ccia,color=ftint[0],alpha=0.5,interpolate=True),
	    dict(y1=ccia,y2=ccib,where=ccib >ccia,color=ftint[1],alpha=0.5,interpolate=True)
	)
	fb_up4['panel'], fb_dn4['panel'] = 4, 4
	# macd in panel 5
	fb_up5, fb_dn5 = (
	    dict(y1=macd.values,y2=signal.values,
	        where=signal<=macd,color="#93c47d",alpha=0.5,interpolate=True),
	    dict(y1=macd.values,y2=signal.values,
	        where=signal >macd,color="#e06666",alpha=0.5,interpolate=True)
	)
	fb_up5['panel'], fb_dn5['panel'] = 5, 5
	return [fb_up2, fb_dn2, #\\fb_up1, fb_dn1,
	    fb_up4, fb_dn4, fb_up5, fb_dn5]


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


def main(argv):
	""" ---."""
	# reset parameters, obtain file via tkinter
	_t, _d, _i = Ticker, Days, Interval
	#_t, _d, _i = "BTC-USD", 90, 86400 # Ticker[1], Days[0], Interval[0]
    #_t, _d, _i = (str(spin1.get()), int(spin2.get()), int(spin3.get()))
	# obtain OHLC feed quotes
	_df = obtain_df(_t, _d, _i, DEC)
	_o, _h, _l, _c = data_columns(_df)
	curr_o, curr_c = _o[CURR], _c[CURR]
	prev_h, prev_c = _h[PREV], _c[PREV]
	#-u-last_c = df_c.iloc[LAST] #last_o, last_c = df_o.iloc[LAST],
	#up_mark, dn_mark = price_diff(_df)
	# main panel 0: bb
	bb_u, bb_m, bb_l = (
	    bb_up(_c,bb_p),
	    bb_mid(_c,bb_p),
	    bb_low(_c,bb_p))
	curr_bb_up, curr_bb_mid, curr_bb_low = (
	    np.round(bb_u[CURR],DEC),np.round(bb_m[CURR],DEC),np.round(bb_l[CURR],DEC))
	prev_bb_up, prev_bb_mid, prev_bb_low = (
	    np.round(bb_u[PREV],DEC),np.round(bb_m[PREV],DEC),np.round(bb_l[PREV],DEC))
	#last_bb_up, last_bb_mid, last_bb_low = (
	#    np.round(bb_u[LAST],DEC),np.round(bb_m[LAST],DEC),np.round(bb_l[LAST],DEC))
	last_bb_mid = np.round(bb_m[LAST])
	# Bollinger calcs
	bb_clr,bb_i,bb_ih_clr,bb_ih,bb_il_clr,bb_il = bb_calcs(
	    curr_bb_up, curr_bb_mid, curr_bb_low,
	    prev_bb_up, prev_bb_mid, prev_bb_low,
	    last_bb_mid) #last_bb_up, , last_bb_low)
	# psar 0
	sar1, sar2, sar3 = (
	    parabolic(_h,_l,af1,am1),
	    parabolic(_h,_l,af2,am2),
	    parabolic(_h,_l,af3,am3))
	curr_sar1, curr_sar2, curr_sar3 = (
	    np.round(sar1[CURR],DEC),np.round(sar2[CURR],DEC),np.round(sar3[CURR],DEC))
	# lag 1
	laga, lagb = LaGuerre(_df,GAMMA),LaGuerre(_df,THETA)
	curr_laga, curr_lagb = np.round(laga[CURR],DEC),np.round(lagb[CURR],DEC)
	# 'La Guerre' calcs
	laga_clr, laga_i, lagb_clr, lagb_i = laguerre_calcs(
	    laga,lagb,CURR,PREV)
	#    #laga_clr, laga_i, lagb_clr, lagb_i
	#l_c, l_i = 0, 0
	# rsi 2
	rsia, rsib = (relative(_c, rsia_p, DEC),
	    relative(_c, rsib_p, DEC)
	)
	curr_rsi_a, curr_rsi_b = np.round(rsia[CURR],DEC), np.round(rsib[CURR],DEC)
	# williams % range 3
	wpr = WPR(_c, _h, _l, wpr_p)
	curr_wpr = np.round(wpr[CURR],DEC) #-.iloc
	# subpanel 4: cci
	ccia, ccib = (
	    CCI(_c, _h, _l, ccia_p),
	    CCI(_c, _h, _l, ccib_p)
	    )
	curr_cci_a, curr_cci_b = np.round(ccia[CURR]/CCI_RND,DEC),np.round(ccib[CURR]/CCI_RND,DEC)
	# subpanel 5: macd
	macd, signal, histogram = Macd(_c,fast,slow,ema)
	curr_macd, curr_signal, curr_histogram = (np.round(macd.iloc[CURR],DEC),
	    np.round(signal.iloc[CURR],DEC),np.round(histogram.iloc[CURR],DEC))
	# panels
	#up_mark_panel, dn_mark_panel = (
	#    mpf.make_addplot(up_mark,color='orange',type='scatter',marker='v',markersize=100),
	#    mpf.make_addplot(dn_mark,color='lime',type='scatter',marker='^',markersize=100))
	bbu_panel, bbm_panel, bbl_panel = (
	    mpf.make_addplot(bb_u,color=i_clr[0],linestyle='-'), #orig: '-'
	    mpf.make_addplot(bb_m,color=i_clr[1],linestyle='-'), #orig: ':'
	    mpf.make_addplot(bb_l,color=i_clr[2],linestyle='-'))
	sar1_panel, sar2_panel, sar3_panel = (
	    mpf.make_addplot(sar1,color=i_clr[5],type='scatter'),
	    mpf.make_addplot(sar2,color=i_clr[4],type='scatter'),
	    mpf.make_addplot(sar3,color=i_clr[3],type='scatter'))
	laga_panel, lagb_panel = (
	    mpf.make_addplot(laga,color=i_clr[6],linestyle='-',panel=1,secondary_y=True),
	    mpf.make_addplot(lagb,color=i_clr[7],linestyle='-',panel=1,secondary_y=True))
	rsia_panel, rsib_panel = (
	    mpf.make_addplot(rsia,color=i_clr[8],linestyle='-',panel=2,secondary_y=False),
	    mpf.make_addplot(rsib,color=i_clr[9],linestyle='-',panel=2,secondary_y=False))
	wpr_panel = mpf.make_addplot(wpr,color=i_clr[11],linestyle='-',panel=3,secondary_y=False)
	ccia_panel, ccib_panel = (
	    mpf.make_addplot(ccia,color=i_clr[12],linestyle='-',panel=4,secondary_y=False),
	    mpf.make_addplot(ccib,color=i_clr[13],linestyle='-',panel=4,secondary_y=False))
	histogram_panel, macd_panel, signal_panel = (
	    mpf.make_addplot(histogram,
	        color=i_clr[1],panel=5,type='bar',width=0.5,alpha=0.6,secondary_y=True),
	    mpf.make_addplot(macd,color=i_clr[0],panel=5,secondary_y=False),
	    mpf.make_addplot(signal,color=i_clr[2],panel=5,secondary_y=False))
	# pool panels for mplfinance figure
	indicators = [ #up_mark_panel, dn_mark_panel,
	    bbu_panel, bbm_panel, bbl_panel,
	    sar1_panel,sar2_panel,sar3_panel,
	    laga_panel, lagb_panel,
	    rsia_panel, rsib_panel,
	    wpr_panel, ccia_panel, ccib_panel,
	    histogram_panel, signal_panel, macd_panel
	    ]
    # def output_to_ax_0()-------------------------|
	interpolations = tint_interpolations( #laga,lagb,
	    rsia,rsib,ccia,ccib,macd,signal)
	calc_clr, price_clr, d_g = priceline_calcs(
	    curr_o,curr_c,prev_h,prev_c,curr_rsi_a,curr_rsi_b,DEC)
	c_vals, leg_fnt = {}, 16
	# figure values
	fig, _ax = mpf.plot(_df,
	    fill_between=interpolations,
	    style=mpf.make_mpf_style(base_mpf_style=Theme(3),
	        marketcolors=mpf.make_marketcolors(up='dodgerblue',down='tomato',edge='w',
	            wick={'up':'w','down':'w'},volume='in',ohlc='in'),
	        gridcolor='dimgrey', facecolor='k', edgecolor='y', rc=style_dict),
	    type=Chart_Type(3), addplot=indicators,
	    hlines=dict(hlines=[curr_c, prev_c],colors=[price_clr, calc_clr],
	        linestyle='-.',linewidths=[2.2, 1.7],alpha=0.4),
	    xlabel=('•'+FILENAME+'•\n'+_t+' $'+str(curr_c)), #+'\n'+_tail),
	    panel_ratios=( 4, 1, 1, 1, 1, 1), volume=True,volume_panel=1, #05, #<--!
	    return_calculated_values=c_vals,show_nontrading=False,
	    figratio=(12, 8),returnfig=True,figscale=1.75,figsize=(10.3, 20.5))
	# remove window toolbar items; ignore 'item' error
	#for idx, item in enumerate(rpm, start=0):
	#	fig.canvas.manager.toolmanager.remove_tool(
	#	    rpm[item])
	# last quote details in window border
	#fig.canvas.manager.set_window_title(
	#    '%s    %i days of %s [%s]    $%s' % ( #FILENAME, #||
	#        curr_rec.name.date().strftime('%A, %b. %e/%Y'),
	#        _d, _t, _i, curr_str))
	# axes values
	_ax[0].grid(True) #False) # remove ax0 grid
	# trading density in chart right
	df_len, _y = len(_df), -1
	for _y in _c:
	    _ax[0].annotate('          '+str(_y),(df_len, _y),transform=_ax[0].transAxes,
	        fontsize=10,color=i_clr[11],alpha=0.25)
    # current quote on priceline in chart ||+curr_str!-
	_ax[0].annotate(str(_t)+'\n',(_d, curr_c),
	    fontsize=10,color=i_clr[15],xytext=(_d, curr_c),alpha=0.7)
    # (-)current date), ohlc in chart
	_ax[0].annotate( #f"{_d:} day(s) {_t:} [{_i:}]"
        #+f"\n{curr_rec.name.date().strftime('%A, %b/%e/%Y'):}"
	    f"\nO: ${_df['Open'].iloc[CURR]:.2f}\nH: ${_df['High'].iloc[CURR]:.2f}" #(-) +f"\n
	    +f"\nL: ${_df['Low'].iloc[CURR]:.2f}\nC: ${_df['Close'].iloc[CURR]:.2f}\n", #<<==!!
		xy=(len(_df), curr_c), textcoords='axes fraction',
	    fontsize=leg_fnt,color=i_clr[1],xytext=(0.01, 1.0)
	) #,alpha=0.85)
	_ax[0].annotate(
	    f"MACD ({fast:},{slow:},{ema:}): {curr_macd:.3f}"
	    +f"\n               Signal: {curr_signal:.3f}\n         Histogram: {curr_histogram:.3f}\n",
	    xy=(len(_df), curr_c), textcoords='axes fraction',
	    fontsize=leg_fnt, color='beige',
	    xytext=(0.5, 1.0)
	)
	# bb decision logic
	_ax[0].annotate(bb_ih+"|",
		xy=(len(_df), curr_c), textcoords='axes fraction',
	    fontsize=leg_fnt, color=bb_ih_clr,
	    xytext=(0.01, 0.96)
	) #,alpha=0.85)
	_ax[0].annotate(bb_i+"|",
		xy=(len(_df), curr_c), textcoords='axes fraction',
	    fontsize=leg_fnt, color=bb_clr,
	    xytext=(0.01, 0.90)
	) #,alpha=0.85)
	_ax[0].annotate(bb_il+"|",
		xy=(len(_df), curr_c), textcoords='axes fraction',
	    fontsize=leg_fnt, color=bb_il_clr,
	    xytext=(0.01, 0.84)
	) #,alpha=0.85)
    # laguerre decision logic type A
	_ax[0].annotate(laga_i,
	    xy=(len(_df), curr_c), textcoords='axes fraction',
	    fontsize=leg_fnt, color=laga_clr,
	    xytext=(0.04, 0.04)
	)
	# laguerre decision logic type B <--logic error
	_ax[0].annotate(lagb_i,
	    xy=(len(_df), curr_c), textcoords='axes fraction',
	    fontsize=leg_fnt, color=lagb_clr,
	    xytext=(0.24, 0.04)
	)
	# subpanel annotations
	legend_array = (
	    f"- BB  up ({ bb_p:}): {curr_bb_up:.2f}",
	    f"- BBmid ({ bb_p:}): {curr_bb_mid:.2f}",
	    f"- BB low ({ bb_p:}): {curr_bb_low:.2f}",
	    f"• psar({af3:}): {curr_sar3:.2f}",
	    f"• psar({af2:}): {curr_sar2:.2f}",
	    f"• psar({af1:}): {curr_sar1:.2f}",
	    f"- LaG A({GAMMA:}): {curr_laga*100:.2f}",
	    f"- LaG B({THETA:}): {curr_lagb*100:.2f}",
	    f"- RSI({rsia_p:}): {curr_rsi_a:}",
	    f"- RSI({rsib_p:}): {curr_rsi_b:}",
	    f"________±{d_g:}",
	    f"- WPR({wpr_p:}): {curr_wpr/10:.2f}",
	    f"- CCI({ccia_p:}): {curr_cci_a:.2f}",
	    f"- CCI({ccib_p:}): {curr_cci_b:.2f}"
	)
	xy_txt = (0.96,
	    0.90,0.84,0.77,0.71,0.65,
	    0.58,0.52,0.45,0.39,0.33,
	    0.26,0.19,0.13
	) #,0.07,0.0)
	for idx, item in enumerate(xy_txt, start=0):
		_ax[0].annotate(
		    legend_array[idx],
		    xy=(len(xy_txt), curr_c),
		    textcoords='axes fraction',
		    fontsize=leg_fnt,
		    color=i_clr[idx],
		    xytext=(0.05, xy_txt[idx]),
		    bbox=dict(boxstyle='square',
		        fc='k', alpha=0.6
		    )
		)
	# cursor on main axe (candlestick) panel
	cursor1 = Cursor(_ax[1], useblit=True, color='w', linewidth=2)
	cursor2 = Cursor(_ax[2], useblit=True, color='w', linewidth=2)
	cursor3 = Cursor(_ax[4], useblit=True, color='w', linewidth=2)
	cursor4 = Cursor(_ax[6], useblit=True, color='w', linewidth=2)
	cursor5 = Cursor(_ax[8], useblit=True, color='w', linewidth=2)
	cursor6 = Cursor(_ax[10], useblit=True, color='w', linewidth=2)

	plt.show()

	return


if __name__ == "__main__" :
    main(sys.argv[1:])
