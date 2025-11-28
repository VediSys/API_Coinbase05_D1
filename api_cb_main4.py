#--utf-8-- *26072025 REFERENCE
""" api_cb_main4.py |<306 ✓✓

    - Parabolic SAR(3) [.01,.02,.03]+*10 inc.
    - LaGuerre(3) [.25,.5,.75]
      Moving Average(3) [5, 8, 11]

    - Eine kleine Focke-Wulf.

//------------------------------
//---- concept architecture ----
Class algorithmic_financial_decision
    def indicators # for the calculation
    def indicator_calcs
    def auto_trade
    
*Class visual_financial_psychology
    def indicators # for the chart values
    def display_chart

def obtain_quotes

if name ==__main__
//------------------------------
"""
from __future__ import absolute_import

import matplotlib.pyplot  as plt
from   matplotlib.widgets import Cursor
import mplfinance   as mpf

from portfolio      import folio
from autosize_cb    import obtain_df
from laguerre       import LaGuerre
from parabolic_sar3 import parabolic
from themestyle     import \
    Theme, Chart_Type, style_dict


file_name = "api_tk_main4.py"
symbol = ['ATOM-USD', 'BAT-USD', #12 portfolio items
    'BTC-USD','DASH-USD','ETH-USD',
    'GRT-USD','KAVA-USD',
	'MKR-USD','OP-USD','SAND-USD',
	'SOL-USD','XLM-USD',
	'XRP-USD'
    ]
days = [300, # days[0] == max.: 300.
    1,2,3,5,7,
    10,20,30,45,60,
    90,120,150,180,240
    ]
#_t = symbol[1] # 0-11: 12 symbols
#_d =  days[10] # [11] 16 daily quote types
#_i =     86400 # seconds per one(1) day
_t, _d, _i = folio(4, 11, 0)
# USD decimal places and tensor indexing
_dec, curr, prev, pr3v = 2, -1, -2, -3
# la_guerre ranges
gamma, theta, kappa = 0.25, 0.5, 0.75
# parabolic stop and reverse
af1, af2, af3, am1, am2, am3 = (
    0.01,0.02,0.03,
    0.1, 0.2, 0.3
)


"""def wireless():
	while True:
		try:
			main() #urllib.error
			#exit()
		except : # urllib2.URLError
		    urllib.error
		    exit()
			
	return
"""

def tint_interpolations( #laga,lagb,
    rsia,rsib,ccia,ccib,macd,signal):
	ftint = ['royalblue','coral','cyan',
	    'lightblue','teal','salmon'
	    ]
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

	return [ #fb_up1, fb_dn1,
	    fb_up2, fb_dn2,
	    fb_up4, fb_dn4,
	    fb_up5, fb_dn5
	    ]


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

def interpolate_laguerre(laga,lagb):
	fb_up1, fb_dn1 = (
	    dict(y1=laga,y2=lagb,
	        where=lagb<=laga,color="#93c47d",
	        alpha=0.4,interpolate=True),
	    dict(y1=laga,y2=lagb,
	        where=lagb >laga,color="#e06666",
	        alpha=0.4,interpolate=True)
	)
	fb_up1['panel'], fb_dn1['panel'] = 1, 1
	return fb_up1, fb_dn1


def indicator_panels(
    sar1, sar2, sar3, laga, lagb, lagc):
    # ---.
    sar1_panel, sar2_panel, sar3_panel = (
	    mpf.make_addplot(sar1,
	        color="r", type='scatter'),
	    mpf.make_addplot(sar2,
	        color="beige", type='scatter'),
	    mpf.make_addplot(sar3,
	        color="dodgerblue", type='scatter')
	)
    laga_panel, lagb_panel, lagc_panel = (
        mpf.make_addplot(laga,
            color="c", linestyle='-',
            panel=1),
        mpf.make_addplot(lagb,
            color="y", linestyle='-',
            panel=1),
        mpf.make_addplot(lagc,
            color="darkred", linestyle='-',
            panel=1)
    )
    ind_panels = [
        laga_panel,lagb_panel,lagc_panel,
        sar1_panel,sar2_panel,sar3_panel
        ]

    return ind_panels


def main(df, _t, _d):
    """ chart elements."""
    _o, _h, _l, _c = (
        df['Open'], df['High'],
        df['Low'], df['Close']
    )
    #def indicator_values():
    sar1, sar2, sar3 = (
	    parabolic(_h,_l,af1,am1),
	    parabolic(_h,_l,af2,am2),
	    parabolic(_h,_l,af3,am3)
	); sar = sar1, sar2, sar3

    laga, lagb, lagc = (
        LaGuerre(df, gamma),
        LaGuerre(df, theta),
        LaGuerre(df, kappa)
    ); lag = laga, lagb, lagc
    #return ( # lag, sar
    #    sar1, sar2, sar3,
    #    laga, lagb, lagc
    #)
    #//fill_between=interpolate_laguerre,
    fb_up, fb_dn = (
	    dict(y1=laga,y2=lagb,
	        where=lagb<=laga,color="#93c47d",
	        alpha=0.4,interpolate=True),
	    dict(y1=laga,y2=lagb,
	        where=lagb >laga,color="#e06666",
	        alpha=0.4,interpolate=True)
	); fb_up['panel'],fb_dn['panel']=1,1

    # display output information
    _style, _chart = 3, 3

    _title = (
        f"\n\n{_t} ({len(df)} Days)"
        +f"  $ {_c[curr]:.2f}"
        +f"\nb({gamma}): {laga[curr]:.2f}"
        +f"\ny({theta}0): {lagb[curr]:.2f}"
        +f"\nr({kappa}): {lagc[curr]:.2f}"
    )
    """
    ohlc_label = ("\n*"
        +" O: "+str(_o[curr])
        +", H: "+str(_h[curr])
        +" L: "+str(_l[curr])
        +", C: "+str(_c[curr])
        +"\n"
        +" O: "+str(_o[prev])
        +", H: "+str(_h[prev])
        +" L: "+str(_l[prev])
        +", C: "+str(_c[prev])
        +"\n"
        +" O: "+str(_o[pr3v])
        +", H: "+str(_h[pr3v])
        +" L: "+str(_l[pr3v])
        +", C: "+str(_c[pr3v])
    )""
    x_label, y_label = (
        file_name, #+ohlc_label,
        f"Price (${_c[curr]:.2f})"
    )
    """
    mpf_style = mpf.make_mpf_style(
        base_mpf_style=Theme(_style),
        marketcolors=mpf.make_marketcolors(
            up='dodgerblue',
            down='tomato',
            edge='w',
            wick={'up': 'w',
                'down': 'w'},
            volume='in',
            ohlc='in'),
        gridcolor='dimgrey',
        facecolor='k',
        edgecolor='w',
        rc=style_dict
    )
    cvals = {}
    leg_fnt = 16
    ind_panels = indicator_panels(
        sar1, sar2, sar3,
        laga, lagb, lagc
    )
    fig, _ax = mpf.plot(df,
        #fill_between=lag_int, #[fb_up1, fb_dn1],
        type   =Chart_Type(_chart),
        addplot=ind_panels,
        style  =mpf_style,
        title  =_title,
        hlines =dict(hlines=[_c[curr],_c[prev]],
            colors    =['cyan','pink'],
	        linestyle ='-.',
	        linewidths=[2.2, 1.7],
	        alpha=0.4
	    ),
        panel_ratios=(5, 2, 1),
        return_calculated_values=cvals,
        #xlabel=x_label, ylabel=y_label,
        mav=(11, 8, 5), mavcolors=('r','y','c'),
        volume=True, volume_panel=2,
        figratio=(12, 8), figscale=1.75,
        #figsize=(10.3, 20.5) ,
        tight_layout=False #True
    )
    # current quote on priceline in chart ||+curr_str!-
    """_ax[0].annotate(_t+'\n',
	    (_t, _d, _c[curr]),
	    fontsize=leg_fnt, color="w",
	    xytext=(_d, _c[curr]), alpha=0.7
	)"""
    # text ON priceline in chart.
    _ax[0].annotate(
        (_d-1, _c[curr]),
        fontsize =leg_fnt, color="w",
        xytext   =_c[curr],
        transform=_ax[0].transAxes,
        alpha=0.7
    )
    cursor = (Cursor(_ax[0], useblit=True,
        color='w', linewidth=2)
    )
    #cursor1 = (Cursor(_ax[4], useblit=True,
    #    color='w', linewidth=2)
    #)
    plt.show(mpf.show())
    return


if __name__ == '__main__':
    df = obtain_df(_t, _d, _i, _dec)
    main(df, _t, _d)
    exit()
