import statistics
import numpy as np


def round_to_base(x, base=5):
    return int(base * round(float(x)/base))


def round_to_nth_digits_after_decimal_point_with_base_m(x, n=5, m=5):
    x = x*(10**(n+1))
    x = round_to_base(x, 10)
    x = x/10
    x = round_to_base(x, m)
    x = x/float(10**n)
    return x


def cal_ATR14(high, low, close):
    TR = 0
    for x in range(14):
        TR = TR + max((high[x]-low[x]), abs(high[x] -
                                            close[x+1]), abs(low[x]-close[x+1]))
    ATR = TR/14
    print(" ATR14 is ", ATR)
    return ATR


def isNarrowDay(high, low, N):
    print ("Today     high-low = ",  (high[0]-low[0]))
    current = high[0]-low[0]
    for x in range(N):
        if current >= (high[x+1]-low[x+1]):
            print ("Nth day ", x+1, " high-low = ",  (high[x+1]-low[x+1]))
            return 0
    return 1


def isInsideDay(high, low):
    print ("Today     high-low = ",  (high[0]-low[0]))
    print ("Yesterday high-low = ",  (high[1]-low[1]))
    if (high[0]-low[0]) < (high[1]-low[1]):
        return 1
    else:
        return 0


def isReversalBullBear(high, low, close, length):
    if (low[0] < low[0]) and (close[0] > low[1]):
        return 1
    elif (high[0] > high[1]) and (close[0] < low[1]):
        return -1
    else:
        return 0


def isMission1_bull(close, sma, stdev):
    for x in range(1, 10):
        if(close[x] >= (sma[x]-stdev[x])):
            print (" Not mission1 bull ", x, " close ",
                   close[x], " SMA-STDEV line ",  (sma[x]-stdev[x]))
            return 0
    if(close[0] > (sma[0]-stdev[0])):
        return 1
    print (" Not mission1 bull now close is ",
           close[0],  " SMA-STDEV line ",  (sma[0]-stdev[0]))
    return 0


def isMission1_bear(close, sma, stdev):
    for x in range(1, 10):
        if(close[x] <= (sma[x]+stdev[x])):
            print (" Not mission1 bear ", x, " close  ",
                   close[x], " SMA+STDEV line ",  (sma[x]+stdev[x]))
            return 0
    if(close[0] < (sma[0]+stdev[0])):
        return 1
    print (" Not mission1 bear now close is ",
           close[0],  " SMA+STDEV line ",  (sma[0]+stdev[0]))
    return 0


def SMA(close, offset, length):
    headclose = close[offset: (offset+length)]
    sma = statistics.mean(headclose)
    stdev = statistics.stdev(headclose)
    return sma, stdev
