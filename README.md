# TY&Co.

Python code for executing Tactical asset allocation on Interactive Brokers

Note:

* This is modified from Interactive Brokers sample code.
* Code is not pretty but workable.
* Use VOO to replace SPY for lower expense ratio.
* Suggest to test with paper trading account first.
* GLD don't support IB algo order, so here it use Market order

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

        # ADM
        ADMAllocation = 1000
        ADMVOO = 1    # Use VOO to replace VFINX
        ADMTLT = 0    # Use TLT to replace VUSTX; Long-term Tressury might hurted by interesetd rate. Could consider replace with IEF or BND.
        ADMSCZ = 0    # Use SCZ to replace VINEX; Other alternative : SCHC , VSS , GWX ; VINEX only works for US resident.

        # Ray Dalio’s All-Weather
        RDAWAllocation = 1000
        RDAWDBC = 0.075
        RDAWGLD = 0.075
        RDAWIEF = 0.15
        RDAWTLT = 0.4
        RDAWVOO = 0.3

2. 
Execute

python3 TAA.py



*Disclaimer

TYCo does not make any guarantee or other promise as to any results that may be obtained from using our content. No one should make any investment decision without first consulting his or her own financial advisor and conducting his or her own research and due diligence. To the maximum extent permitted by law, TYCo disclaims any and all liability in the event any information, commentary, analysis, opinions, advice and/or recommendations prove to be inaccurate, incomplete or unreliable, or result in any investment or other losses.


