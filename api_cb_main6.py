#-*-utf-8-*-: env: Python Pydroid
# REFERENCE DO NOT ALTER
""" api_cb_main6.py |203✓✓✓
    EA_BCWrx.py |175 redux w/notes.

    - An all-in-one Pydroid mobile script
      for daily Coinbase quote and volume

    - Bollinger Bands,
      Commodity Channel Index,
      Williams Percentage Range.
SD
gitgub/vedisys ©2025
"""
from __future__ import absolute_import

import matplotlib.pyplot as plt
from   matplotlib.widgets import Cursor
import mplfinance as mpf
import numpy as np

from portfolio import folio
from autosize_cb import obtain_df as autosize

from bollinger_bands import (
    upper_BB_band as bb_up,
    middle_BB_band as bb_mid,
    lower_BB_band as bb_low
)
from laguerre import LaGuerre
from commodity_channel import CCI as cci
from williams_range import WPR as wpr

from themestyle import \
    Theme, Chart_Type, style_dict



# parameters.
CURR, PREV = -1, -2
cci_d, cci_m       = 1000, 1 #(100, 1)
BB_P, CCI_P, WPR_P = 17, 8, 13 #(20, 14||31, 14)
GAMMA, THETA       = 0.25, 0.75


_t, _d, _i = folio(1,11,0)
t_len, d_len, i_len = 11,14,10 #12,15,11
DEC = 2 # decimal places in USD

# obtain smoothed data file.
df = autosize(_t, _d, _i, DEC)

# alias allocated data items via '.iloc[:]'.
df_o, df_h, df_l, df_c, df_v = (
    df['Open'].iloc[:], df['High'].iloc[:],
    df['Low'].iloc[:], df['Close'].iloc[:],
    df['Volume'].iloc[:]
)
last_o, last_h, last_l, last_c, last_v = (
    df['Open'].iloc[CURR],
    df['High'].iloc[CURR],
    df['Low'].iloc[CURR],
    df['Close'].iloc[CURR],
    df['Volume'].iloc[CURR]
)
last, lastr_c , prev_h, prev_c = (
    df.iloc[CURR][:], #?! necessary ??
    str(
        df['Close'].iloc[CURR]),
    df['High'].iloc[PREV],
    df['Close'].iloc[PREV]
) # for/in axes annotation.
ticker_close, ticker_str = (
    _t+' $'+lastr_c,
    str(_d)+' days of '+_t+'  $'+str(lastr_c)
) # bollinger bands.--------------------|
bb_u, bb_m, bb_l = (bb_up(df_c,BB_P),
    bb_mid(df_c,BB_P), bb_low(df_c,BB_P)
)
last_bb_up, last_bb_mid, last_bb_low = (
    np.round(bb_u[CURR],DEC),
	np.round(bb_m[CURR],DEC),
	np.round(bb_l[CURR],DEC)
)
bbu_panel, bbm_panel, bbl_panel = (
	mpf.make_addplot(bb_u,color='b',linestyle='-'),
	mpf.make_addplot(bb_m,color='g',linestyle='-'),
	mpf.make_addplot(bb_l,color='r',linestyle='-')
)
# lag 1
laga, lagb = (
    LaGuerre(df,GAMMA), LaGuerre(df,THETA)
)
curr_laga, curr_lagb = (
    np.round(laga[CURR],DEC),
    np.round(lagb[CURR],DEC)
)
# commodity channel index.
CCI = cci(df_c, df_h, df_l, CCI_P)
CCI = np.round(CCI /cci_d, DEC)
#(CCI[-1] *cci_m, DEC) #cci_r, DEC)
last_cci = np.round(CCI[CURR] /cci_d, DEC)
# williams percentage range.
WPR = wpr(df_c, df_h, df_l, WPR_P)

last_wpr = np.round(WPR[CURR], DEC)

# panels, interpolations.
laga_panel, lagb_panel, cci_panel, wpr_panel = (
    mpf.make_addplot(laga,
        color="dodgerblue",
        linestyle='-', panel=1,
        secondary_y=True),
    mpf.make_addplot(lagb,
        color="plum",
        linestyle='-', panel=1,
        secondary_y=True),
    mpf.make_addplot(CCI,
        color='chartreuse',
        linestyle='-', panel=1),
    mpf.make_addplot(WPR,
        color='orchid',
        linestyle='-', panel=1)
)
indicator_panels = [
    bbu_panel, bbm_panel, bbl_panel,
    laga_panel, lagb_panel,
    cci_panel,
    wpr_panel
    ]
fb_a0, fb_b0 = (
    dict(y1=CCI, y2=WPR,
        where=CCI <=WPR, color='coral',
        alpha=0.5, interpolate=True),
    dict(y1=CCI, y2=WPR,
        where=CCI >WPR, color='royalblue',
        alpha=0.6, interpolate=True)
)
fb_a0['panel'], fb_b0['panel'] = (1, 1)
interpolation = [fb_a0, fb_b0]
# priceline colour quasi-logic.------------------|
if ((last_c > prev_c)
and (last_o > prev_h)):
    calc_clr='aqua'
else:
	calc_clr='r'
# ---.
if last_o <= last_c:
	price_clr='lightskyblue'
else:
	price_clr='salmon'
# output_to_ax0. (amalgamated mpf_style)---------|
cvals, leg_fnt = {}, 16 # for calcs.
fig, ax0 = mpf.plot(df,
    fill_between=interpolation,
    type=Chart_Type(3),
    style=mpf.make_mpf_style(
        base_mpf_style=Theme(3),
        marketcolors=mpf.make_marketcolors(
            up='dodgerblue', down='tomato',
            edge=price_clr, wick='w',
            volume='in', ohlc='i'),
        gridcolor='dimgray', facecolor='k',
        rc=style_dict),
    addplot=indicator_panels,
    hlines=dict(hlines=last_c, colors=price_clr,
        linestyle='-', linewidths=2.2, alpha=0.4),
    panel_ratios=(5, 2, 1),
    return_calculated_values=cvals,
    volume=True, volume_panel=2,
    returnfig=True, figsize=(10.3, 20.5)
) # text ON priceline in chart.
ax0[0].annotate(lastr_c,(_d,last_c),
    fontsize=leg_fnt, xytext=(_d,last_c),
    transform=ax0[0].transAxes,
    color=price_clr, alpha=0.7
) # text IN box on chart.
ax0[0].annotate(f"{_d:} days {_t:}" # [{_i:}]"
    +f"\n{last.name.date().strftime('%b/%e/%Y'):}"
    +f"\n\nO: ${last_o:.2f}\nH: ${last_h:.2f}"
    +f"\nL: ${last_l:.2f}\nC: ${last_c:.2f}" #+f"\n\nV: {last_v:}"
    +f"\n\nBB  up ({ BB_P:}): {last_bb_up:.2f}"
	+f"\nBBmid ({ BB_P:}): {last_bb_mid:.2f}"
	+f"\nBB low ({ BB_P:}): {last_bb_low:.2f}"
	+f"\n\n.CCI ({CCI_P:}): {last_cci:.2f}"
    +f"\nW% ({WPR_P:}): {abs(last_wpr):.2f}",
    xy=(len(df),last_c), transform=ax0[0].transAxes,
    textcoords='axes fraction', xytext=(0.02, 0.67),
    fontsize=leg_fnt, color='khaki',
    bbox=dict(boxstyle='square',
        #fc="k",
        fc=price_clr,
        alpha=0.35) # 17)
) # text IN box in ax[].
ax0[4].annotate( #ticker_str,[#str(_d)+' days of '+
    _t+'  $'+str(lastr_c),
    xy=(len(df)-1,last_c),
    transform=ax0[4].transAxes,
    textcoords='axes fraction',
    xytext=(0.02, 0.67),
    fontsize=leg_fnt,
    color=price_clr, #'khaki',
    bbox=dict(boxstyle='square',
        fc=price_clr, #calc_clr,
        alpha=0.17)
)
cursor = (Cursor(ax0[0], useblit=True,
    color='w', linewidth=2)
)
#cursor1 = (Cursor(_ax[4], useblit=True,
#    color='w', linewidth=2)
#)
# run GUI.
plt.show()
