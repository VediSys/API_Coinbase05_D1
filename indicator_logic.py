# -*- coding: utf-8 -*- env: Pydroid
""" indicator_logic.py |125 *05092025
    - logic architecture '•↑BUY↑'
    - bb, lg, psar, rsi, prix
"""
import numpy as np


curr, prev, pr3v = -1, -2, -3


def boll_logic(boll):
    """ bb calcs temp logicus:
    	if -3 >= -2 & -2 > -1; & vice versa."""
    bb_u, bb_m, bb_l = boll
    # u -/^-.
    if bb_u[prev] >=bb_u[curr]:
    	bb_u_i = '↓'
    elif bb_u[prev] <bb_u[curr]:
    	bb_u_i = '↑'
    else: bb_u_i = '≈'
    # m ---.
    if (bb_m[pr3v] >=bb_m[prev]
    and bb_m[prev] >=bb_m[curr]):
    	bb_m_i = '↓'
    elif (bb_m[pr3v] <=bb_m[prev]
    and bb_m[prev] <bb_m[curr]):
        bb_m_i = '↑'
    else: bb_m_i = '≈'
    # l -\v-.
    if bb_l[prev] >=bb_l[curr]:
        bb_l_i = '↓'
    elif bb_l[prev] <bb_l[curr]:
        bb_l_i = '↑'
    else: bb_l_i = '≈'

    return bb_u_i, bb_m_i, bb_l_i


def laguerre_logic(lag): #, curr, prev):
	""" dual 'La Guerre' logic types"""
	laga, lagb, lagc = lag
    # logic for 'laga'
	if ((laga[curr] <=0.03
	and laga[prev] <=0.025)
	or ( laga[curr] >=laga[prev])):
	    laga_i = '↑'
	else:
		laga_i = '↓'
	# logic for 'lagb'
	if ((laga[curr] ==0.00
	and laga[prev] <=0.01)
	or ( lagb[curr] ==0.00
	and lagb[prev] <=0.01)):
	    lagb_i = '↑'
	else:
	    lagb_i = '↓'
    # logic for 'lagc'
	if ((lagc[curr] <=0.03
	and lagc[prev] <=0.025)
	or ( lagc[curr] >=lagc[prev])):
	    lagc_i = '↑'
	else:
		lagc_i = '↓'

	return laga_i, lagb_i, lagc_i


def psar_logic(psar):
	""" psar logic x3 """
	#- [D1]: when psar 1 or psar 2 doubles up,
	#        its time to buy or sell
	sar1, sar2, sar3 = psar

	if sar1[curr] ==sar1[prev]:
		sar1_i = '••'
	elif sar1[curr] >sar1[prev]:
		sar1_i = '↑'
	elif sar1[curr] <sar1[prev]:
	    sar1_i = '↓'
	else:
		sar1_i = '-'

	if sar2[curr] ==sar2[prev]:
		sar2_i = '••'
	elif sar2[curr] >sar2[prev]:
		sar2_i = '↑'
	elif sar2[curr] ==sar2[prev]:
	    sar2_i = '↓'
	else:
		sar2_i = '-'

	if sar3[curr] ==sar3[prev]:
		sar3_i = '••'
	elif sar3[curr] >sar3[prev]:
		sar3_i = '↑'
	elif sar2[curr] ==sar2[prev]:
	    sar3_i = '↓'
	else:
		sar3_i = '-'

	return sar1_i, sar2_i, sar3_i


"""
def rsi_calcs(rsia[curr], rsib[curr]):
	"" ---.""
	if rsib[curr] > rsia[curr]:
		dg_clr = 'lightskyblue' #'salmon'
	elif rsib[curr] < rsia[curr]:
		dg_clr = 'salmon' #'lightskyblue'
	else:
		dg_clr = '#c0c0c0'

	return dg_clr""


def priceline_calcs(
    _o[curr],
    _c[curr],
    _h[prev],
    _c[prev],
    rsia[curr],
    rsib[curr],
    _dec):
    "" temp calcs, priceline colours""
    if _c[curr] >_c[prev] and _o[curr] >_h[prev]:
    	calc_clr='aqua'
    else: calc_clr='orange'
    # ---.
    if _o[curr] <=_c[curr]:
    	price_clr='lightskyblue'
    else: price_clr='salmon'
    # rsi priceline calc
    if rsib[curr] <=rsia[curr]:
    	d_g, price_clr=np.round(
    	    rsia[curr] -rsib[curr], _dec),'hotpink'
    else: d_g, price_clr=np.round(
        rsib[curr] -rsia[curr], _dec),'royalblue'

    return calc_clr, price_clr, d_g
"""
