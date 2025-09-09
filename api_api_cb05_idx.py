# -*- coding: utf-8 -*- env: Pydroid
""" api_cb05_idx.py |75 ✓ *07092025
"""

#import matplotlib.pyplot # req'd 1x
from portfolio   import folio
from autosize_cb import obtain_df
# ---.
from indicator_value import \
    indicator_values
from indicator_logic import (
    boll_logic,
    psar_logic,
    laguerre_logic)
from indicator_panel import \
    indicator_panels
from display_quotes import \
    display_chart


#symbol, days to view, interval seconds
_t, _d, _i = folio(11, 0, 0) #11:XRP
_dec = 3 # decimal places


def data_columns(_t, _d, df):
    """ Extract data columns."""
    # || _u, _o, _h, _l, _c, _v
    _o, _h, _l, _c = (
        df['Open'], df['High'],
        df['Low'], df['Close']
    )
    ohlc = _o, _h, _l, _c

    return ohlc


def main():
    """ obtain and display OHLC data
        with indicators."""
    # symbol, days, interval, decimal.
    df = obtain_df(_t, _d, _i, _dec)

    # OHLC via ticker, days, datafile.
    ohlc = data_columns(_t, _d, df)

    # ind_values via OHLC, datafile.
    boll, psar, lag = indicator_values(df,ohlc)

    # indicator logic determinations
    bb_u_i, bb_m_i, bb_l_i = boll_logic(boll)
    sar1_i, sar2_i, sar3_i = psar_logic(psar)
    laga_i, lagb_i, lagc_i = laguerre_logic(lag) #,curr,prev)

    # LaG 'conclusions / recommendations' HAQ
    if (bb_u_i == '↓'
    and bb_m_i == '↓'
    and bb_l_i == '↓'):
    	boll_adv = 'Bollinger : Sell'
    else:
    	boll_adv = 'Bollinger : Buy'

    # LaG 'conclusions / recommendations' HAQ
    if (laga_i == '↓'
    and lagb_i == '↓'
    and lagc_i == '↓'):
    	lag_adv = 'LaGuerre : Sell'
    else:
    	lag_adv = 'LaGuerre : Buy'

    all_ind = (
        bb_u_i, bb_m_i, bb_l_i,
        sar1_i, sar2_i, sar3_i,
        laga_i, lagb_i, lagc_i,
        boll_adv, lag_adv)

    # assign indicator panels.
    ind_panels = indicator_panels(
       boll, psar, lag)

    # display daily cryptocurrency
    # candlestick chart with
    # trending indications, (5).
    display_chart(_t, #_d,
        df, ohlc, #ind_vals, #lag, psar,
        all_ind, ind_panels)


if __name__ == '__main__':
	main()
	exit()
