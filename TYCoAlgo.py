import statistics
import numpy as np
import pandas_datareader.data as web
import pandas as pd
import math
import scipy.optimize as sco
from datetime import datetime
from datetime import timedelta
from datetime import date
import time
#import matplotlib.pyplot as plt

class stockData(object):
    def __init__(self,ticker):
        self.ticker = ticker
        self.close = 0
        self.monthEndPrice = np.zeros(5)
        self.monthAveragePrice = np.zeros(5)

VOOph = stockData('VOO')
VEAph = stockData('VEA')
VWOph = stockData('VWO')
BNDph = stockData('BND')
VEUph = stockData('VEU')
SCZph = stockData('SCZ')
BILph = stockData('BIL')
SHYph = stockData('SHY')
IEFph = stockData('IEF')
LQDph = stockData('LQD')
RWXph = stockData('RWX')
EWJph = stockData('EWJ')
EEMph = stockData('EEM')
VNQph = stockData('VNQ')
TLTph = stockData('TLT')
DBCph = stockData('DBC')
GLDph = stockData('GLD')
EZUph = stockData('EZU')

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

def K13612W(close):
    momentum = (((close[12]/close[11]-1)*12) + ((close[12]/close[9]-1)*4) +
                ((close[12]/close[6]-1)*2) + ((close[12]/close[0]-1)*1))/4
    return momentum

def ADM136W(close):
    momentum = ((close[12]/close[11]-1) + (close[12]/close[9]-1) +
                (close[12]/close[6]-1) )/3
    return momentum

def K6M(close):
    momentum = (close[12]/close[6]-1)
    return momentum 

def GEM12M(close):
    momentum = (close[12]/close[0]-1)
    return momentum

def get_stock_data(stock):
    stock.close = get_12_month_close_price(stock.ticker)
    stock.monthEndPrice = get_12_month_price_endofmonth(stock.close)
    stock.monthAveragePrice = get_12_month_price_average(stock.close)
    return stock

def get_12_month_close_price(ticker):
    start = datetime.today() - timedelta(days=365)
    start = start.replace(day=1)
    end = datetime.today()
    #print (" data start at ", start)
    #print (" data end at ", end)
    prices = web.DataReader(ticker, 'iex', start, end)
    close = prices['close']
    close.index = pd.to_datetime(close.index)
    return close

def get_12_month_price_average(close):
    monthAverage = close.resample('M').mean()
    return monthAverage

def get_12_month_price_endofmonth(close):
    start = date.today() - timedelta(days=365)
    start = start.replace(day=1)
    eom = pd.date_range(start, periods=13 , freq='BM')
    #print (eom)
    monthly = close
    monthly = monthly.reindex(eom)
    #print (monthly)
    for idx in monthly.index:
        if( math.isnan(monthly.loc[idx]) ) : 
            #print ( "no value ", idx)
            newidx = idx - timedelta(days=1)
            while( True ):
                try:
                    close.loc[newidx]
                    monthly.loc[idx] = close.loc[newidx]
                    #print( " new idx ", newidx, " new value ",monthly.loc[idx])
                    break;
                except:
                    newidx = newidx - timedelta(days=1)
        else:
            #print( idx, " value is not NaN ", monthly.loc[idx] )
            pass
    #print ('\n',"End of month price")
    #print (monthly)
    #print ('\n')        
    return monthly

class ReturnList(object):
    def __init__(self,ticker,WR):
        self.ticker = ticker
        self.WR = WR

class ReturnListwithClose(object):
    def __init__(self,ticker,WR,close):
        self.ticker = ticker
        self.WR = WR
        self.close = close


def getWR(Riskon):
    return Riskon.WR


def get_VAA_allocations(method='0'):
    # Keller and Butler’s Vigilant Asset Allocation – G4
    global VOOph
    global VEAph
    global VWOph
    global BNDph
    global SHYph
    global IEFph
    global LQDph
  
    print ('\n',"=== start of VAA ===")
    if(VOOph.monthEndPrice[0]==0):
        VOOph = get_stock_data(VOOph)
    VOO13612Wa = K13612W(VOOph.monthAveragePrice)
    print ('\n'," VOO month average 13612W is ",VOO13612Wa)
    VOO13612We = K13612W(VOOph.monthEndPrice)
    print ('\n'," VOO end of month 13612W is ",VOO13612We)

    if(VEAph.monthEndPrice[0]==0):
        VEAph = get_stock_data(VEAph)
    VEA13612Wa = K13612W(VEAph.monthAveragePrice)
    print ('\n'," VEA month average 13612W is ",VEA13612Wa)
    VEA13612We = K13612W(VEAph.monthEndPrice)
    print ('\n'," VEA end of month 13612W is ",VEA13612We)

    if(VWOph.monthEndPrice[0]==0):
        VWOph = get_stock_data(VWOph)
    VWO13612Wa = K13612W(VWOph.monthAveragePrice)
    print ('\n'," VWO month average 13612W is ",VWO13612Wa)
    VWO13612We = K13612W(VWOph.monthEndPrice)
    print ('\n'," VWO end of month 13612W is ",VWO13612We)

    if(BNDph.monthEndPrice[0]==0):
        BNDph = get_stock_data(BNDph)
    BND13612Wa = K13612W(BNDph.monthAveragePrice)
    print ('\n'," BND month average 13612W is ",BND13612Wa)
    BND13612We = K13612W(BNDph.monthEndPrice)
    print ('\n'," BND end of month 13612W is ",BND13612We)

    if(SHYph.monthEndPrice[0]==0):
        SHYph = get_stock_data(SHYph)
    SHY13612Wa = K13612W(SHYph.monthAveragePrice)
    print ('\n'," SHY month average 13612W is ",SHY13612Wa)
    SHY13612We = K13612W(SHYph.monthEndPrice)
    print ('\n'," SHY end of month 13612W is ",SHY13612We)

    if(IEFph.monthEndPrice[0]==0):
        IEFph = get_stock_data(IEFph)
    IEF13612Wa = K13612W(IEFph.monthAveragePrice)
    print ('\n'," IEF month average 13612W is ",IEF13612Wa)
    IEF13612We = K13612W(IEFph.monthEndPrice)
    print ('\n'," IEF end of month 13612W is ",IEF13612We)

    if(LQDph.monthEndPrice[0]==0):
        LQDph = get_stock_data(LQDph)
    LQD13612Wa = K13612W(LQDph.monthAveragePrice)
    print ('\n'," LQD month average 13612W is ",LQD13612Wa)
    LQD13612We = K13612W(LQDph.monthEndPrice)
    print ('\n'," LQD end of month 13612W is ",LQD13612We)


    if method == '0' :
        print( '\n'" Choose end of month price to calculate 13612W ")
        RiskonG4 = [ ReturnList( "VOO" , VOO13612Wa ) , ReturnList( "VEA" , VEA13612Wa ) ,ReturnList( "VWO" , VWO13612Wa ) ,ReturnList( "BND" , BND13612Wa ) ]
        Riskoff = [ ReturnList( "SHY" , SHY13612Wa ) , ReturnList( "IEF" , IEF13612Wa ) ,ReturnList( "LQD" , LQD13612Wa ) ]
    elif method == '1' :
        print( '\n'" Choose month's month average price to calculate 13612W ")
        RiskonG4 = [ ReturnList( "VOO" , VOO13612We ) , ReturnList( "VEA" , VEA13612We ) ,ReturnList( "VWO" , VWO13612We ) ,ReturnList( "BND" , BND13612We ) ]
        Riskoff = [ ReturnList( "SHY" , SHY13612We ) , ReturnList( "IEF" , IEF13612We ) ,ReturnList( "LQD" , LQD13612We ) ]

    VAAVOO = 0
    VAAVEA = 0
    VAAVWO = 0
    VAABND = 0
    VAASHY = 0
    VAAIEF = 0
    VAALQD = 0

    if( RiskonG4[0].WR > 0 and RiskonG4[1].WR > 0  and  RiskonG4[2].WR > 0  and  RiskonG4[3].WR > 0 ):
        print ( '\n'," Makret is not Risky for VAA.  Sorting Riskon G4... ")
        RiskonG4 = sorted( RiskonG4 , key=getWR , reverse = True )
        for i in RiskonG4:
            print ( i.ticker, " Weight Return is ", i.WR )

        if( RiskonG4[0].ticker == "VOO" ):
            VAAVOO = 1
        elif (RiskonG4[0].ticker == "VEA" ):
            VAAVEA = 1
        elif (RiskonG4[0].ticker == "VWO" ):
            VAAVWO = 1
        elif (RiskonG4[0].ticker == "BND" ):
            VAABND = 1     
    else:
        print ( '\n'," Makret is risky for VAA.  Try Rick off asset ",'\n')
        Riskoff = sorted( Riskoff , key=getWR , reverse = True )
        for i in Riskoff:
            print ( i.ticker, " Weight Return is ", i.WR ) 

        if( Riskoff[0].WR > 0 ):    
            if (Riskoff[0].ticker == "SHY" ):
                VAASHY = 1
            elif (Riskoff[0].ticker == "IEF" ):
                VAAIEF = 1
            elif (Riskoff[0].ticker == "LQD" ):
                VAALQD = 1  
    print ( '\n'," Allocation for VAA is ", " VOO ", VAAVOO," VEA ",VAAVEA," VWO ",VAAVWO," BND ",VAABND," SHY ",VAASHY," IEF ",VAAIEF," LQD ",VAALQD, '\n' )
    return VAAVOO,VAAVEA,VAAVWO,VAABND,VAASHY,VAAIEF,VAALQD


def get_ADM_allocations(method='0'):
    # Engineered Portfolios' Accelerating Dual Momentum Investing 
    global VOOph
    global SCZph
    global TLTph


    print ('\n',"=== start of ADM ===")
    if(VOOph.monthEndPrice[0]==0):
        VOOph = get_stock_data(VOOph)
    VOO136Wa = ADM136W(VOOph.monthAveragePrice)
    print ('\n',"VOO month average ADM136W is ",VOO136Wa)
    VOO136We = ADM136W(VOOph.monthEndPrice)
    print ('\n'," VOO end of month ADM136W is ",VOO136We) 

    if(SCZph.monthEndPrice[0]==0):
        SCZph = get_stock_data(SCZph)
    SCZ136Wa = ADM136W(SCZph.monthAveragePrice)
    print ('\n',"SCZ month average ADM136W is ",SCZ136Wa)
    SCZ136We = ADM136W(SCZph.monthEndPrice)
    print ('\n'," SCZ end of month ADM136W is ",SCZ136We) 

    if(TLTph.monthEndPrice[0]==0):
        TLTph = get_stock_data(TLTph)
    TLT136Wa = ADM136W(TLTph.monthAveragePrice)
    print ('\n',"TLT month average ADM136W is ",TLT136Wa)
    TLT136We = ADM136W(TLTph.monthEndPrice)
    print ('\n'," TLT end of month ADM136W is ",TLT136We) 

    if method == '0' :
        VOO136W = VOO136We
        SCZ136W = SCZ136We
        TLT136W = TLT136We
    elif method == '1':
        VOO136W = VOO136Wa
        SCZ136W = SCZ136Wa 
        TLT136W = TLT136Wa             

    ADMVOO=0
    ADMSCZ=0
    ADMTLT=0

    if(VOO136W>SCZ136W):
        if(VOO136W > 0):
            ADMVOO = 1
        else:
            if(TLT136W>0):
                ADMTLT = 1
    elif(SCZ136W>0):
        ADMSCZ=1
    else:
        if(TLT136W>0):
            ADMTLT=1

    print ( '\n'," Allocation for ADM is ", " VOO ", ADMVOO," SCZ ",ADMSCZ, " TLT ",ADMTLT , '\n' )
    return ADMVOO,ADMSCZ,ADMTLT


def get_GEM_allocations(method='0'):
    global VOOph
    global BILph
    global VEUph

    print ('\n',"=== start of GEM ===")

    if(VOOph.monthEndPrice[0]==0):
        VOOph = get_stock_data(VOOph)
    VOO12Wa = GEM12M(VOOph.monthAveragePrice)
    print ('\n',"VOO month average 12W is ",VOO12Wa)
    VOO12We = GEM12M(VOOph.monthEndPrice)
    print ('\n',"VOO end of month 12W is ",VOO12We)

    if(BILph.monthEndPrice[0]==0):
        BILph = get_stock_data(BILph)
    BIL12Wa = GEM12M(BILph.monthAveragePrice)
    print ('\n',"BIL month average 12W is ",BIL12Wa)
    BIL12We = GEM12M(BILph.monthEndPrice)
    print ('\n',"BIL end of month 12W is ",BIL12We)

    if(VEUph.monthEndPrice[0]==0):
        VEUph = get_stock_data(VEUph)
    VEU12Wa = GEM12M(VEUph.monthAveragePrice)
    print ('\n',"VEU month average 12W is ",VEU12Wa)
    VEU12We = GEM12M(VEUph.monthEndPrice)
    print ('\n',"VEU end of month 12W is ",VEU12We)

    if method == '0' :
        VOO12W = VOO12Wa
        BIL12W = BIL12Wa
        VEU12W = VEU12Wa
    elif method == '1':
        VOO12W = VOO12We
        BIL12W = BIL12We
        VEU12W = VEU12We

    GEMVOO=0
    GEMVEU=0
    GEMBND=0

    if(VOO12W>BIL12W):
        if(VOO12W>VEU12W):
            GEMVOO=1
        else:
            GEMVEU=1
    else:
        GEMBND=1
    

    print ( '\n'," Allocation for GEM is ", " VOO ", GEMVOO," VEU ",GEMVEU, " BND ", GEMBND  , '\n')
    return GEMVOO,GEMVEU,GEMBND

# Following is copy from http://www.bradfordlynch.com/blog/2015/12/04/InvestmentPortfolioOptimization.html
def findMaxSharpeRatioPortfolio(meanReturns, covMatrix, riskFreeRate):
    '''
    Finds the portfolio of assets providing the maximum Sharpe Ratio

    INPUT
    meanReturns: mean values of each asset's returns
    covMatrix: covariance of each asset in the portfolio
    riskFreeRate: time value of money
    '''
    numAssets = len(meanReturns)
    args = (meanReturns, covMatrix, riskFreeRate)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple( (0,1) for asset in range(numAssets))

    opts = sco.minimize(negSharpeRatio, numAssets*[1./numAssets,], args=args,
                        method='SLSQP', bounds=bounds, constraints=constraints)

    return opts

def findMinVariancePortfolio(meanReturns, covMatrix):
    '''
    Finds the portfolio of assets providing the lowest volatility

    INPUT
    meanReturns: mean values of each asset's returns
    covMatrix: covariance of each asset in the portfolio
    '''
    numAssets = len(meanReturns)
    args = (meanReturns, covMatrix)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple( (0,1) for asset in range(numAssets))

    opts = sco.minimize(getPortfolioVol, numAssets*[1./numAssets,], args=args,
                        method='SLSQP', bounds=bounds, constraints=constraints)

    return opts

def getPortfolioVol(weights, meanReturns, covMatrix):
    '''
    Returns the volatility of the specified portfolio of assets
    
    INPUT
    weights: array specifying the weight of each asset in the portfolio
    meanReturns: mean values of each asset's returns
    covMatrix: covariance of each asset in the portfolio
    
    OUTPUT
    The portfolio's volatility
    '''
    return calcPortfolioPerf(weights, meanReturns, covMatrix)[1]

def negSharpeRatio(weights, meanReturns, covMatrix, riskFreeRate):
    '''
    Returns the negated Sharpe Ratio for the speicified portfolio of assets
    
    INPUT
    weights: array specifying the weight of each asset in the portfolio
    meanReturns: mean values of each asset's returns
    covMatrix: covariance of each asset in the portfolio
    riskFreeRate: time value of money
    '''
    p_ret, p_var = calcPortfolioPerf(weights, meanReturns, covMatrix)
    
    return -(p_ret - riskFreeRate) / p_var

def calcPortfolioPerf(weights, meanReturns, covMatrix):
    '''
    Calculates the expected mean of returns and volatility for a portolio of
    assets, each carrying the weight specified by weights

    INPUT
    weights: array specifying the weight of each asset in the portfolio
    meanReturns: mean values of each asset's returns
    covMatrix: covariance of each asset in the portfolio

    OUTPUT
    tuple containing the portfolio return and volatility
    '''    
    #Calculate return and variance

    portReturn = np.sum( meanReturns*weights )
    portStdDev = np.sqrt(np.dot(weights.T, np.dot(covMatrix, weights)))

    return portReturn, portStdDev

# This monte_carlo method is copy from https://medium.com/python-data/efficient-frontier-portfolio-optimization-with-python-part-2-2-2fe23413ad94
def MTP_by_monte_carlo( returns_6months, cov_6months):
    # empty lists to store returns, volatility and weights of imiginary portfolios
    port_returns = []
    port_volatility = []
    sharpe_ratio = []
    stock_weights = []
    selected = ['top1', 'top2', 'top3', 'top4', 'top5']
    # set the number of combinations for imaginary portfolios
    num_assets = 5
    num_portfolios = 80000

    #set random seed for reproduction's sake
    np.random.seed(seed=int(time.time()))

    # populate the empty lists with each portfolios returns,risk and weights
    for single_portfolio in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights /= np.sum(weights)
        returns = np.dot(weights, returns_6months)
        volatility = np.sqrt(np.dot(weights.T, np.dot(cov_6months, weights)))
        sharpe = returns / volatility
        sharpe_ratio.append(sharpe)
        port_returns.append(returns)
        port_volatility.append(volatility)
        stock_weights.append(weights)

    # a dictionary for Returns and Risk values of each portfolio
    portfolio = {'Returns': port_returns,
             'Volatility': port_volatility,
             'Sharpe Ratio': sharpe_ratio}

    # extend original dictionary to accomodate each ticker and weight in the portfolio
    for counter,symbol in enumerate(selected):
        portfolio[ symbol+' Weight'] = [Weight[counter] for Weight in stock_weights]

    # make a nice dataframe of the extended dictionary
    df = pd.DataFrame(portfolio)

    min_volatility = df['Volatility'].min()
    max_sharpe = df['Sharpe Ratio'].max()

    # use the min, max values to locate and create the two special portfolios
    sharpe_portfolio = df.loc[df['Sharpe Ratio'] == max_sharpe]
    min_variance_port = df.loc[df['Volatility'] == min_volatility]

    '''
    # plot frontier, max sharpe & min Volatility values with a scatterplot
    plt.style.use('seaborn-dark')
    df.plot.scatter(x='Volatility', y='Returns', c='Sharpe Ratio',
                cmap='RdYlGn', edgecolors='black', figsize=(10, 8), grid=True)
    plt.scatter(x=sharpe_portfolio['Volatility'], y=sharpe_portfolio['Returns'], c='red', marker='D', s=200)
    plt.scatter(x=min_variance_port['Volatility'], y=min_variance_port['Returns'], c='blue', marker='D', s=200 )
    plt.xlabel('Volatility (Std. Deviation)')
    plt.ylabel('Expected Returns')
    plt.title('Efficient Frontier')
    plt.show()
    '''
    print(sharpe_portfolio.T)
    print(min_variance_port.T)

    return sharpe_portfolio, min_variance_port

def close_to_percentage_change(close):
    close = np.diff(close) / close[:-1] * 100
    return close


def get_AAA_allocations(method='0', val20days='1' ):
    # Keller and Butler’s Vigilant Asset Allocation – G4
    global VOOph
    global EZUph
    global EWJph
    global EEMph
    global VNQph
    global RWXph
    global IEFph
    global TLTph
    global DBCph
    global GLDph


    print ('\n',"=== start of AAA ===")

    if(VOOph.monthEndPrice[0]==0):    
        VOOph = get_stock_data(VOOph)
    VOO126D = K6M(VOOph.monthEndPrice)
    print ('\n'," VOO 126D is ", VOO126D )

    if(EZUph.monthEndPrice[0]==0):    
        EZUph = get_stock_data(EZUph)
    EZU126D = K6M(EZUph.monthEndPrice)
    print ('\n'," EZU 126D is ", EZU126D )

    if(EWJph.monthEndPrice[0]==0):    
        EWJph = get_stock_data(EWJph)
    EWJ126D = K6M(EWJph.monthEndPrice)
    print ('\n'," EWJ 126D is ", EWJ126D )

    if(EEMph.monthEndPrice[0]==0):    
        EEMph = get_stock_data(EEMph)
    EEM126D = K6M(EEMph.monthEndPrice)
    print ('\n'," EEM 126D is ", EEM126D )

    if(VNQph.monthEndPrice[0]==0):    
        VNQph = get_stock_data(VNQph)
    VNQ126D = K6M(VNQph.monthEndPrice)
    print ('\n'," VNQ 126D is ", VNQ126D )

    if(RWXph.monthEndPrice[0]==0):    
        RWXph = get_stock_data(RWXph)
    RWX126D = K6M(RWXph.monthEndPrice)
    print ('\n'," RWX 126D is ", RWX126D )

    if(IEFph.monthEndPrice[0]==0):    
        IEFph = get_stock_data(IEFph)
    IEF126D = K6M(IEFph.monthEndPrice)
    print ('\n'," IEF 126D is ", IEF126D )

    if(TLTph.monthEndPrice[0]==0):    
        TLTph = get_stock_data(TLTph)
    TLT126D = K6M(TLTph.monthEndPrice)
    print ('\n'," TLT 126D is ", TLT126D )

    if(DBCph.monthEndPrice[0]==0):    
        DBCph = get_stock_data(DBCph)
    DBC126D = K6M(DBCph.monthEndPrice)
    print ('\n'," DBC 126D is ", DBC126D )

    if(GLDph.monthEndPrice[0]==0):    
        GLDph = get_stock_data(GLDph)
    GLD126D = K6M(GLDph.monthEndPrice)
    print ('\n'," GLD 126D is ", GLD126D )


    AAAUniverse = [ ReturnListwithClose( "VOO" , VOO126D ,VOOph.close ) , ReturnListwithClose( "EZU" , EZU126D ,EZUph.close) , ReturnListwithClose( "EWJ" , EWJ126D , EWJph.close )\
                   ,ReturnListwithClose( "EEM" , EEM126D, EEMph.close ), ReturnListwithClose( "VNQ" , VNQ126D, VNQph.close ), ReturnListwithClose( "RWX" , RWX126D, RWXph.close )\
                   ,ReturnListwithClose( "IEF" , IEF126D, IEFph.close ),ReturnListwithClose( "TLT" , TLT126D, TLTph.close ),ReturnListwithClose( "DBC" , DBC126D, DBCph.close ),\
                    ReturnListwithClose( "GLD" , GLD126D, GLDph.close ) ]

    AAAUniverse = sorted( AAAUniverse , key=getWR , reverse = True )

    print ('\n'," After sorting ", '\n' )
    for i in AAAUniverse:
        print ( i.ticker, " Return is ", i.WR )


    closeArray = close_to_percentage_change( np.array( AAAUniverse[0].close ) )
    top5returns = closeArray[ (len(closeArray)-126) :len(closeArray) ]
    for i in range(4):
        closeArray = close_to_percentage_change (np.array( AAAUniverse[i+1].close ))
        closeArray = closeArray[ (len(closeArray)-126) :len(closeArray) ]
        top5returns = np.vstack( ( top5returns , closeArray ))
    


    if val20days=='1' :
        # 126-day correlations ρ(i,j) with 20-day volatilities σ(i) and σ(j) for covariance
        covMatrix = np.corrcoef(top5returns)
        stds = np.std(top5returns[:,:20], axis=1)  # 20-day volatilities for five products
        print (stds)
        for row in range(5):
            for column in range(5):
                covMatrix[row][column] = (covMatrix[row][column]*stds[row]*stds[column])
        print ( "Using 20 day volatilities version ")
        print (covMatrix)        
        print ( "126 day volatilities version is")
        print (np.cov(top5returns))
    else:
        covMatrix = np.cov(top5returns)
    
    meanReturns = np.mean(top5returns, axis=1)    

    # method 1 scipy.optimize 

    
    maxSharpe = findMaxSharpeRatioPortfolio( meanReturns, covMatrix, 0 )
    print ('\n'," Best weights for max sharpe with scipy solver", '\n' )
    print (maxSharpe)
    print (maxSharpe['x'])
    minVar = findMinVariancePortfolio( meanReturns, covMatrix )
    print ('\n'," Best weights for min variance with scipy solver ", '\n' )
    print (minVar)
    print (minVar['x'])

    # method 2 monte carlo #
    maxSharpe2, minVar2 = MTP_by_monte_carlo( meanReturns , covMatrix )
    

    # TODO test whether to scale return and cov to 126D
    if method == '0' :
        print ("use scipy solver ")
        weights = maxSharpe['x']
    else:
        print (" monte carlo ")
        weights = maxSharpe2.ix[:,3:]
        weights = weights.values
        weights = weights[0]

    #return maxSharpe, maxSharpe2
    
    AAAVOO=0
    AAAEZU=0 
    AAAEWJ=0
    AAAEEM=0
    AAAVNQ=0
    AAARWX=0 
    AAAIEF=0
    AAATLT=0
    AAADBC=0
    AAAGLD=0

    for i in range(5):
        str = AAAUniverse[i].ticker
        if( str == 'VOO'):
            AAAVOO = weights[i]
            if AAAVOO < 0.02 :
                AAAVOO = 0
        if( str == 'EZU'):
            AAAEZU = weights[i]
            if AAAEZU < 0.02 :
                AAAEZU = 0
        if( str == 'EWJ'):
            AAAEWJ = weights[i]
            if AAAEWJ < 0.02 :
                AAAEWJ = 0
        if( str == 'EEM'):
            AAAEEM = weights[i]
            if AAAEEM < 0.02 :
                AAAEEM = 0
        if( str == 'VNQ'):
            AAAVNQ = weights[i]
            if AAAVNQ < 0.02 :
                AAAVNQ= 0
        if( str == 'RWX'):
            AAARWX = weights[i]
            if AAARWX < 0.02 :
                AAARWX = 0
        if( str == 'IEF'):
            AAAIEF = weights[i]
            if AAAIEF < 0.02 :
                AAAIEF = 0
        if( str == 'TLT'):
            AAATLT = weights[i]
            if AAATLT < 0.02 :
                AAATLT = 0
        if( str == 'DBC'):
            AAADBC = weights[i]
            if AAADBC < 0.02 :
                AAADBC = 0
        if( str == 'GLD'):
            AAAGLD = weights[i]
            if AAAGLD < 0.02 :
                AAAGLD = 0
    

    print ( '\n'," Allocation for AAA is ", " VOO ", AAAVOO," EZU ",AAAEZU, " EWJ ", AAAEWJ  ," EEM ", AAAEEM, " VNQ ", AAAVNQ  , " RWX ", AAARWX  , " IEF ", AAAIEF  , " TLT ", AAATLT  , " DBC ", AAADBC  , " GLD ", AAAGLD,   '\n')
    return AAAVOO,AAAEZU,AAAEWJ,AAAEEM,AAAVNQ,AAARWX,AAAIEF,AAATLT,AAADBC,AAAGLD
    