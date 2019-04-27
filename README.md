# TY&Co.

# Gap between 3-month and 10-year U.S. yields vanishes Friday (March 22, 2019)
The gap between the three-month and 10-year yields vanished as a surge of buying pushed the latter to a 14-month low of 2.416 percent. Inversion is considered a reliable harbinger of recession in the U.S., within roughly the next 18 months.
https://www.bloomberg.com/news/articles/2019-03-22/u-s-treasury-yield-curve-inverts-for-first-time-since-2007?fbclid=IwAR3hW-milqCV9K-FuJY8GomPTjkmk9L0Eq6Hh2-BqxRValKrXlznpvHlEKY

Python code for executing Tactical asset allocation on Interactive Brokers

*Disclaimer

TYCo does not make any guarantee or other promise as to any results that may be obtained from using our content. No one should make any investment decision without first consulting his or her own financial advisor and conducting his or her own research and due diligence. To the maximum extent permitted by law, TYCo disclaims any and all liability in the event any information, commentary, analysis, opinions, advice and/or recommendations prove to be inaccurate, incomplete or unreliable, or result in any investment or other losses.


Note:

* This is modified from Interactive Brokers sample code.
* Code is not pretty but workable.
* Use VOO to replace SPY for the lower expense ratio.
* Suggest testing with a paper trading account first.
* GLD doesn't support IB algo order, so here it uses Market order.
* Please be cautious when using auto calculated distribution for VAA, ADM, AAA, and GEM.
* Adaptive Asset Allocation's calculation accuracy is limited due to using scipy.optimize with Python 
* End of month price is easy to be affected by short-term volatility. So it also shows the calculation result with the monthly average price for reference.
* When executing before 15th of the month, it will use the price closest to today as the end price of last month. 
  If you execute after 15th, it will use price closest to today as the end price of this month. 
* For the monthly average price, it will always try to average the current month's price regardless of the date unless there is no price available for the current month.  
* Add one option T which allow you to diverified allocation for VAA during turbulent time. 

Usage:

1.
Decide the each strategy's allocation value in TAA.py 

        # Keller and Butler’s Vigilant Asset Allocation – G4 (VAA)
        VAAAllocation = 1000 // Total amount invest in Keller and Butler’s Vigilant Asset Allocation – G4
        
        # Accelerating Dual Momentum (ADM)
        ADMAllocation = 1000

        # Adaptive Asset Allocation: A Primer (AAA)
        AAAAllocation = 1000

        # Ray Dalio’s All-Weather ( Fixed allocation )
        RDAWAllocation = 0

        # GLOBAL EQUITIES MOMENTUM (GEM)
        GEMAllocation = 0
        
        # Keller and Butler’s Elastic Asset Allocation – Defensive
        kellerAllocation = 0   


2.
Decide each strategy's distribution in TAA.py 

We could use auto calculation for VAA, ADM, AAA, and GEM.
Or manually update strategy's distribution by modifing following values in TAA.py and run with option "-manual 1"


        VAAAllocation = 10000
        if ( self.manual_update == '1' ):
            VAAVOO = 0
            VAAVEA = 0
            VAAVWO = 0
            VAABND = 0
            VAASHY = 1
            VAAIEF = 0
            VAALQD = 0




3. 
*Execute following for seeing the calculation result

python3 TAA.py -real 0

*Execute following to do actually trading

python3 TAA.py -real 1

*Execute following to use cash for crash protection instead of each stratey's default

python3 TAA.py -real 1 -cash 1 


P.S.
For actual trading account, you need to specify port number with option "-p"


