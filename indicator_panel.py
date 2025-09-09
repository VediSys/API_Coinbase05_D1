# -*- coding: utf-8 -*- env: Pydroid
""" indicator_panel.py |40 ✓ *04092025
"""
import matplotlib.pyplot as mpl # req'd
import mplfinance        as mpf


def indicator_panels(boll, psar, lag):
    """ Plot indicator panels from
        listed indicator values."""
    bb_u, bb_m, bb_l = boll
    sar1, sar2, sar3 = psar
    laga, lagb, lagc = lag

    bb_u_panel, bb_m_panel, bb_l_panel = (
	    mpf.make_addplot(bb_u,
	        color='khaki', linestyle='-'),
	    mpf.make_addplot(bb_m,
	        color='gold', linestyle='-'),
	    mpf.make_addplot(bb_l,
	        color='khaki', linestyle='-')
	)
    sar1_panel, sar2_panel, sar3_panel = (
	    mpf.make_addplot(sar1,
	        color="r",type='scatter'),
	    mpf.make_addplot(sar2,
	        color="beige",type='scatter'),
	    mpf.make_addplot(sar3,
	        color="cadetblue",type='scatter')
	)
    laga_panel, lagb_panel, lagc_panel = (
        mpf.make_addplot(laga,
            color="c",linestyle='-',
            panel=1),
        mpf.make_addplot(lagb,
            color="y",linestyle='-',
            panel=1),
        mpf.make_addplot(lagc,
            color="r",linestyle='-',
            panel=1)
    )
    # transfer panels into array
    ind_panels = [
        bb_u_panel, bb_m_panel, bb_l_panel,
        sar1_panel, sar2_panel, sar3_panel,
        laga_panel, lagb_panel, lagc_panel
        ]

    return ind_panels
