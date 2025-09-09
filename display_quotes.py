# -*- coding: utf-8 -*- env: Pydroid
""" display_quotes.py |95 ✓ *04092025
"""
#import matplotlib # req'd 1x
import mplfinance as mpf
from portfolio import folio
from themestyle import \
    Theme, Chart_Type, style_dict


# settings
file_name = "api_cb05_idx.py"
#symbol, days to view, interval seconds
_t, _d, _i = folio(1, 0, 0)
# decimal places and indexing
_dec = 3
curr, prev, pr3v = -1, -2, -3

# parabolic parameters
af1, af2, af3, am1, am2, am3 = (
    0.01, 0.02, 0.03,
    0.1, 0.2, 0.3
) # laGuerre ranges
gamma, theta, kappa = 0.25, 0.5, 0.75


def display_chart(_t, #_d,
    df, ohlc, # ind_vals, #lag, psar,
    all_ind, ind_panels):
    """ display quote chart w/ indicators."""
    _o, _h, _l, _c = ohlc

    (bb_u_i, bb_m_i, bb_l_i,
        sar1_i, sar2_i, sar3_i,
        laga_i, lagb_i, lagc_i,
        boll_adv, lag_adv
        ) = all_ind

    _style, _chart = 3, 3
    _title = (f"\n\n{_t} ({len(df)} Days)"
        +f"  $ {_c.iloc[curr]:.2f}"
        #+f"\nc({gamma}): {laga[curr]:.2f}"
        #+f", y({theta}): {lagb[curr]:.2f}"
        #+f", r({kappa}): {lagc[curr]:.2f}"
        #+f"\nsar1:{sar1[curr]:.2f}"
        #+f", sar2: {sar2[curr]:.2f}"
        #+f", sar3: {sar3[curr]:.2f}"
        +f"\n  bb: {bb_u_i} , {bb_m_i} , {bb_l_i}"
        +f" {boll_adv}"
        +f"\n lag: {laga_i} , {lagb_i} , {lagc_i}"
        +f" {lag_adv}"
        +f"\nsar: {sar1_i} , {sar2_i} , {sar3_i}"
    )
    ohlc_label = (
        f"> {_t} ({str(len(df))} Days)"
        "\n"
        +" O: "+str(_o[curr])
        +" H: "+str(_h[curr])
        +" L: "+str(_l[curr])
        +" C: "+str(_c[curr])
        +"*\n"
        +" O: "+str(_o[prev])
        +" H: "+str(_h[prev])
        +" L: "+str(_l[prev])
        +" C: "+str(_c[prev])
        +"\n"
        +" O: "+str(_o[pr3v])
        +" H: "+str(_h[pr3v])
        +" L: "+str(_l[pr3v])
        +" C: "+str(_c[pr3v])
    )
    x_label = "<"+file_name+ohlc_label
    # y_label = f"Price ($ {_c.iloc[curr]:.2f})"
    mpf_style = mpf.make_mpf_style(
        base_mpf_style=Theme(_style),
        marketcolors=mpf.make_marketcolors(
            up='dodgerblue',
            down='tomato', edge='w',
            wick={'up': 'w', 'down': 'w'},
            volume='in', ohlc='in'),
        gridcolor='dimgrey', facecolor='k',
        edgecolor='w', rc=style_dict
    ) #fig, ax =
    mpf.plot(df,
        type=Chart_Type(_chart),
        addplot=ind_panels,
        style=mpf_style,
        title=_title,
        hlines=dict(hlines=[
            _c.iloc[curr], _c.iloc[prev]],
            colors=['cyan','pink'],
	        linestyle='-.',
	        linewidths=[2.2, 1.7],
	        alpha=0.4),
        panel_ratios=(5, 2, 1),
        xlabel=x_label, #ylabel=y_label,
        mav=(8, 5, 3),
        mavcolors=('orangered','cadetblue','lime'),
        volume=True, volume_panel=2,
        figratio=(12, 8), figscale=1.75,
        #figsize =(10.3, 20.5) ,
        tight_layout=False #True
    )
    mpf.show()
