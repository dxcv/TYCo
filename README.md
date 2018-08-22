# TY&Co.

Python code for executing Tactical asset allocation on Interactive Brokers

Note:

* This is modified from Interactive Brokers sample code.
* Code is not pretty but workable.
* Use VOO to replace SPY for lower expense ratio 

Usage:

1.
Modify the following value in TAA.py according to current Tactical asset allocation

        # Keller and Butler’s Elastic Asset Allocation – Defensive
        kellerAllocation = 1000   // Total amount in Keller and Butler’s Elastic Asset Allocation – Defensive
        kellerVOO = 0.15          // the VOO's decimal fraction
        kellerQQQ = 0.281
        kellerEFA = 0
        kellerEEM = 0
        kellerEWJ = 0
        kellerIEF = 0.429
        kellerHYG = 0.14

        # Dick Stoken’s Active Combined Asset (ACA)
        StokenAllocation = 1000
        StokenVOO = 0.333
        StokenIEF = 0
        StokenGLD = 0
        StokenTLT = 0.333
        StokenVNQ = 0.333

        # GEM
        GEMAllocation = 1000
        GEMVOO = 1
        GEMVEU = 0
        GEMBND = 0


2. 
Execute

python3 TAA.py
