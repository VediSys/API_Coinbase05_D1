# -*- coding: utf-8 -*- env: Pydroid
""" indicator_value.py |51 ✓ *04092025
"""

import matplotlib.pyplot # req'd
# main panel
from bollinger_bands import (
    upper_BB_band  as bb_up,
    middle_BB_band as bb_mid,
    lower_BB_band  as bb_low)
from parabolic_sar3 import parabolic
# subpanel
from laguerre import LaGuerre


# bollinger bands deviation
bb_p = 20
# parabolic parameters
af1, af2, af3, am1, am2, am3 = (
    0.01, 0.02, 0.03,
    0.1, 0.2, 0.3
)
# laGuerre ranges
gamma, theta, kappa = 0.25, 0.5, 0.75


def indicator_values(df, ohlc):
    """ Extract data columns and list
        indicator values."""
    _o, _h, _l, _c = ohlc
    # Bollinger Bands
    bb_u, bb_m, bb_l = (
        bb_up( _c,bb_p),
        bb_mid(_c,bb_p),
        bb_low(_c,bb_p))
    # Parabolic SAR
    sar1, sar2, sar3 = (
	    parabolic(_h,_l,af1,am1),
	    parabolic(_h,_l,af2,am2),
	    parabolic(_h,_l,af3,am3))
    # la Guerre
    laga, lagb, lagc = (
        LaGuerre(df, gamma),
        LaGuerre(df, theta),
        LaGuerre(df, kappa))
    # int_vals = [
    boll = bb_u, bb_m, bb_l
    psar = sar1, sar2, sar3
    lag  = laga, lagb, lagc #]

    return boll, psar, lag #int_vals
