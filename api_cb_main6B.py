#-*-utf-8-*-: env: Python Pydroid
"""
    api_tk_main6B.py |186 ✓✓ :api tk main6

 --- ALTERED REFERENCE ---: PROVISIONAL
    MULTI-CURSOR FIRST BUILD LOADS SLOWLY

    - An all-in-one Pydroid mobile script
      of daily Coinbase quotes and volume
      using publicly available tick data.

    - A template for educational purposes
      in trading bot design architecture.

    - Bollinger Bands
      Commodity Channel Index
      Williams Percentage Range

github/vedisys ©2012-2026 S.Dzubïella ARR®™
"""

from __future__ import absolute_import
# standard library
from os import system
import sys
import time as tm
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import \
    MultiCursor
import mplfinance as mpf
# github/vedisys repository extensions
from portfolio import folio
from autosize_cb import \
    obtain_df as autosize
from bollinger_bands import (
    upper_BB_band  as bb_up,
    middle_BB_band as bb_mid,
    lower_BB_band  as bb_low)
from laguerre import LaGuerre
from commodity_channel import \
    CCI as cci
from williams_range import \
    WPR as wpr
from themestyle import \
    Theme, Chart_Type, style_dict


# -SETTINGS------------------------------
_dec = 2 # decimal places
curr, prev = -1, -2 # indexing
# parameters
CCI_D, CCI_M       = 10000, 1   #(100, 1)
BB_P, CCI_P, WPR_P = 17, 17, 17 #(20, 13|14||31, 14)
GAMMA, THETA       = 0.25, 0.75 #33, 0.66
# portfolio symbol spacers(13);future idx
_s = ('',' ',' ','',' ',' ','',' ','  ','','','','')
index, step, seconds = 0, 1, 110
# ---------------------------------------
#for index in range(0, len(_s), step):
#while index <= len(_s):


def main(argv):
	_t, _d, _i = folio(2, 12, 0); df = autosize(_t, _d, _i, _dec)
	_o, _h, _l, _c = df['Open'].iloc[:],df['High'].iloc[:],df['Low'].iloc[:],df['Close'].iloc[:]
	# current or last known ohlc value.#, last_v
	this, lastr_c = df.iloc[curr][:], str(df['Close'].iloc[curr]),
	curr_o, curr_c = df['Open'].iloc[curr], df['Close'].iloc[curr]
	prev_o, prev_c = df['Open'].iloc[prev], df['Close'].iloc[prev]
	# Bollinger bands
	bb_u, bb_m, bb_l = bb_up(_c,BB_P), bb_mid(_c,BB_P), bb_low(_c,BB_P)
	last_bb_up, last_bb_mid, last_bb_low = (
	    np.round(bb_u[curr],_dec),np.round(bb_m[curr],_dec),np.round(bb_l[curr],_dec))
	bbu_panel, bbm_panel, bbl_panel = (
	    mpf.make_addplot(bb_u,color='y',linestyle='-'),
		mpf.make_addplot(bb_m,color='y',linestyle='-'),
		mpf.make_addplot(bb_l,color='y',linestyle='-'))
	# La Guerre indicator
	laga, lagb = LaGuerre(df,GAMMA), LaGuerre(df,THETA)
	last_laga, last_lagb = np.round(laga[curr],_dec), np.round(lagb[curr],_dec)
	# Commodity Channel index
	CCI = cci(_c, _h, _l, CCI_P); CCI = np.round(CCI /CCI_D, _dec)
	last_cci = np.round(CCI[curr], _dec)
	# Williams Percentage range
	WPR = wpr(_c, _h, _l, WPR_P)
	last_wpr = np.round(WPR[curr], _dec)
	# panels, interpolations
	(laga_panel, lagb_panel,
	    cci_panel, wpr_panel
	) = (
	    mpf.make_addplot(laga, color='c', linestyle='-', panel=1, secondary_y=True),
	    mpf.make_addplot(lagb, color='orangered', linestyle='-', panel=1, secondary_y=True),
	    mpf.make_addplot(CCI, color='chartreuse', linestyle='-', panel=2),
	    mpf.make_addplot(WPR, color='violet', linestyle='-', panel=2)
	)
	# panels
	indicator_panels = [
	    bbu_panel, bbm_panel, bbl_panel,
	    laga_panel, lagb_panel,
	    cci_panel, wpr_panel]
	# interpolations
	fb_a0, fb_b0 = (
	    dict(y1=CCI, y2=WPR, where=CCI<=WPR, color='coral', alpha=0.5, interpolate=True),
	    dict(y1=CCI, y2=WPR, where=CCI >WPR, color='royalblue', alpha=0.6, interpolate=True)
	); fb_a0['panel'], fb_b0['panel'] = 2, 2
	"""fb_a1, fb_b1 = (
	    dict(y1=laga*100, y2=lagb*100, where=lagb>=laga, color='salmon', alpha=0.4, interpolate=True),
	    dict(y1=laga*100, y2=lagb*100, where=lagb <laga, color='cadetblue', alpha=0.3, interpolate=True)
	); fb_a1['panel'], fb_b1['panel'] = 3, 3"""
	interpolation = [fb_a0, fb_b0]#, fb_a1, fb_b1
	# calc, priceline colour quasi-logic
	#if ((curr_c > prev_c) and (curr_o > prev_h)): calc_clr='aqua'#else: calc_clr='r'
	if prev_c <= curr_c or prev_o <= curr_o :
		price_clr='lightskyblue'
	else:
		price_clr='salmon'
	# ---.
	if ((laga[curr] > lagb[curr])
	or (laga[curr] >0 or laga[prev] >0)
	#and (laga[curr]==0 or lagb[prev]==0)
	):
		char = 'Buy' #+'\033[1;33;40m^∆^'
	else:
		char = 'Sell' #+'\033[1;34;40mvVv'
	# output
	cvals, leg_fnt = {}, 16
	fig, ax = mpf.plot(df, fill_between=interpolation, type=Chart_Type(3),
	    style=mpf.make_mpf_style(base_mpf_style=Theme(3),
	        marketcolors=mpf.make_marketcolors(up='c', down='r',
	        edge='y', wick='w', volume='in', ohlc='i'),
	        gridcolor='dimgray', facecolor='k', rc=style_dict),
	    addplot=indicator_panels,
	    hlines=dict(hlines=curr_c, colors=price_clr,
	    linestyle='-', linewidths=2.2, alpha=0.4),
	    panel_ratios=(5, 2, 2, 2), return_calculated_values=cvals,
	    volume=True, volume_panel=3, returnfig=True, figsize=(10.3, 20.5)
	) # line ON chart priceline #'\033[1;37;40m',lastr_c)
	ax[0].annotate(_t+"\n"+lastr_c,(_d-2,curr_c),
	    fontsize=leg_fnt, xytext=(_d-2,curr_c),
	    transform=ax[0].transAxes, color='lime', alpha=0.8
	) # legend IN box on chart
	#ax[0].annotate(f"{index:}|{_d:} days of {_t:}" # [{_i:}]" etc.
	ax[0].annotate(f"{_d:} days of {_t:}" #[{_i:}]"
	    +f"\n{this.name.date().strftime('%b.%e, %Y'):}  ${curr_c:.2f}"
	    #+f"\nO: ${curr_o:.2f}\nH: ${curr_h:.2f}"+f"\nL: ${curr_l:.2f}\nC: ${curr_c:.2f}"
	    +f"\n\nBB  up ({ BB_P:}): {last_bb_up:.2f}"
	    +f"\nBBmid ({ BB_P:}): {last_bb_mid:.2f}"
		+f"\nBB low ({ BB_P:}): {last_bb_low:.2f}"
		+f"\n\n.CCI ({CCI_P:}): {last_cci:.2f}"
	    +f"\nW% ({WPR_P:}): {abs(last_wpr):.2f}",
	    xy=(len(df), curr_c),
	    transform=ax[0].transAxes, textcoords='axes fraction',
	    xytext=(0.02, 0.67), fontsize=leg_fnt, color='chartreuse',
	    bbox=dict(boxstyle='square', fc=price_clr, alpha=0.35)
	)
	ax[0].annotate(char, xy=(len(df)-10, curr_c),
	    transform=ax[0].transAxes, textcoords='axes fraction',
	    xytext=(0.3, 0.04), fontsize=leg_fnt+2 #, color='w' #,
	    #bbox=dict(boxstyle='square', fc=price_clr, alpha=0.17)
	)
	# laguerre IN box in ax[n]
	ax[0].annotate(f"lagA: {abs(last_laga):.2f}", xy=(len(df)-1, curr_c),
	    transform=ax[0].transAxes, textcoords='axes fraction',
	    xytext=(0.03, 0.15), fontsize=leg_fnt+2, color='lightskyblue',
	    bbox=dict(boxstyle='square', fc='k', alpha=0.17)
	)
	ax[0].annotate(f"lagB: {abs(last_lagb):.2f}", xy=(len(df)-1, curr_c),
	    transform=ax[0].transAxes, textcoords='axes fraction',
	    xytext=(0.03, 0.04), fontsize=leg_fnt+2, color='coral',
	    bbox=dict(boxstyle='square', fc='k', alpha=0.17)
	)
	# multi-panel cursor
	cursor = MultiCursor(fig.canvas,(ax[1],ax[2],ax[4],ax[6]),color='lime',lw=2,horizOn=False,vertOn=True)
	plt.show(mpf.show(), cursor) # run GUI
	#index = index +1  # increment symbol#tm.sleep(seconds) # display timer#system('clear')#
	return


if __name__ == '__main__':
	#main() #; tm.sleep(seconds); exit()
	main(sys.argv[1:])
else:
    sys.stdout.flush() #system('clear'); 
    sys.exit(2)
