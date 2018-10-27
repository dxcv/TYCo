"""
Copyright (C) 2018 Interactive Brokers LLC. All rights reserved. This code is subject to the terms
and conditions of the IB API Non-Commercial License or the IB API Commercial License, as applicable.
"""

import sys

from ibapi.contract import *


class TYCoContracts:

    """ Usually, the easiest way to define a Stock/CASH contract is through 
    these four attributes.  """

    # Forex contracts

    @staticmethod
    def EurUsdFx():
        #! [cashcontract]
        contract = Contract()
        contract.symbol = "EUR"
        contract.secType = "CASH"
        contract.currency = "USD"
        contract.exchange = "IDEALPRO"
        #! [cashcontract]
        return contract

    @staticmethod
    def EurAudFx():
        #! [cashcontract]
        contract = Contract()
        contract.symbol = "EUR"
        contract.secType = "CASH"
        contract.currency = "AUD"
        contract.exchange = "IDEALPRO"
        #! [cashcontract]
        return contract

    @staticmethod
    def EurCadFx():
        #! [cashcontract]
        contract = Contract()
        contract.symbol = "EUR"
        contract.secType = "CASH"
        contract.currency = "CAD"
        contract.exchange = "IDEALPRO"
        #! [cashcontract]
        return contract

    @staticmethod
    def EurJpyFx():
        #! [cashcontract]
        contract = Contract()
        contract.symbol = "EUR"
        contract.secType = "CASH"
        contract.currency = "JPY"
        contract.exchange = "IDEALPRO"
        #! [cashcontract]
        return contract

    @staticmethod
    def EurGbpFx():
        #! [cashcontract]
        contract = Contract()
        contract.symbol = "EUR"
        contract.secType = "CASH"
        contract.currency = "GBP"
        contract.exchange = "IDEALPRO"
        #! [cashcontract]
        return contract

    @staticmethod
    def EurChfFx():
        #! [cashcontract]
        contract = Contract()
        contract.symbol = "EUR"
        contract.secType = "CASH"
        contract.currency = "CHF"
        contract.exchange = "IDEALPRO"
        #! [cashcontract]
        return contract

    @staticmethod
    def EurNzdFx():
        #! [cashcontract]
        contract = Contract()
        contract.symbol = "EUR"
        contract.secType = "CASH"
        contract.currency = "NZD"
        contract.exchange = "IDEALPRO"
        #! [cashcontract]
        return contract

    @staticmethod
    def UsdCadFx():
        #! [cashcontract]
        contract = Contract()
        contract.symbol = "USD"
        contract.secType = "CASH"
        contract.currency = "CAD"
        contract.exchange = "IDEALPRO"
        #! [cashcontract]
        return contract

    @staticmethod
    def UsdJpyFx():
        #! [cashcontract]
        contract = Contract()
        contract.symbol = "USD"
        contract.secType = "CASH"
        contract.currency = "JPY"
        contract.exchange = "IDEALPRO"
        #! [cashcontract]
        return contract

    @staticmethod
    def UsdChfFx():
        #! [cashcontract]
        contract = Contract()
        contract.symbol = "USD"
        contract.secType = "CASH"
        contract.currency = "CHF"
        contract.exchange = "IDEALPRO"
        #! [cashcontract]
        return contract

    @staticmethod
    def GbpCadFx():
        #! [cashcontract]
        contract = Contract()
        contract.symbol = "GBP"
        contract.secType = "CASH"
        contract.currency = "CAD"
        contract.exchange = "IDEALPRO"
        #! [cashcontract]
        return contract

    @staticmethod
    def GbpJpyFx():
        #! [cashcontract]
        contract = Contract()
        contract.symbol = "GBP"
        contract.secType = "CASH"
        contract.currency = "JPY"
        contract.exchange = "IDEALPRO"
        #! [cashcontract]
        return contract

    @staticmethod
    def GbpUsdFx():
        #! [cashcontract]
        contract = Contract()
        contract.symbol = "GBP"
        contract.secType = "CASH"
        contract.currency = "USD"
        contract.exchange = "IDEALPRO"
        #! [cashcontract]
        return contract

    @staticmethod
    def GbpChfFx():
        #! [cashcontract]
        contract = Contract()
        contract.symbol = "GBP"
        contract.secType = "CASH"
        contract.currency = "CHF"
        contract.exchange = "IDEALPRO"
        #! [cashcontract]
        return contract

    @staticmethod
    def GbpAudFx():
        #! [cashcontract]
        contract = Contract()
        contract.symbol = "GBP"
        contract.secType = "CASH"
        contract.currency = "AUD"
        contract.exchange = "IDEALPRO"
        #! [cashcontract]
        return contract

    @staticmethod
    def GbpNzdFx():
        #! [cashcontract]
        contract = Contract()
        contract.symbol = "GBP"
        contract.secType = "CASH"
        contract.currency = "NZD"
        contract.exchange = "IDEALPRO"
        #! [cashcontract]
        return contract

    @staticmethod
    def AudUsdFx():
        #! [cashcontract]
        contract = Contract()
        contract.symbol = "AUD"
        contract.secType = "CASH"
        contract.currency = "USD"
        contract.exchange = "IDEALPRO"
        #! [cashcontract]
        return contract

    @staticmethod
    def AudChfFx():
        #! [cashcontract]
        contract = Contract()
        contract.symbol = "AUD"
        contract.secType = "CASH"
        contract.currency = "CHF"
        contract.exchange = "IDEALPRO"
        #! [cashcontract]
        return contract

    @staticmethod
    def NzdJpyFx():
        #! [cashcontract]
        contract = Contract()
        contract.symbol = "NZD"
        contract.secType = "CASH"
        contract.currency = "JPY"
        contract.exchange = "IDEALPRO"
        #! [cashcontract]
        return contract

    @staticmethod
    def NzdCadFx():
        #! [cashcontract]
        contract = Contract()
        contract.symbol = "NZD"
        contract.secType = "CASH"
        contract.currency = "CAD"
        contract.exchange = "IDEALPRO"
        #! [cashcontract]
        return contract

    @staticmethod
    def CadJpyFx():
        #! [cashcontract]
        contract = Contract()
        contract.symbol = "CAD"
        contract.secType = "CASH"
        contract.currency = "JPY"
        contract.exchange = "IDEALPRO"
        #! [cashcontract]
        return contract

    @staticmethod
    def CadChfFx():
        #! [cashcontract]
        contract = Contract()
        contract.symbol = "CAD"
        contract.secType = "CASH"
        contract.currency = "CHF"
        contract.exchange = "IDEALPRO"
        #! [cashcontract]
        return contract

    @staticmethod
    def ChfJpyFx():
        #! [cashcontract]
        contract = Contract()
        contract.symbol = "CHF"
        contract.secType = "CASH"
        contract.currency = "JPY"
        contract.exchange = "IDEALPRO"
        #! [cashcontract]
        return contract

    @staticmethod
    def Index():
        #! [indcontract]
        contract = Contract()
        contract.symbol = "DAX"
        contract.secType = "IND"
        contract.currency = "EUR"
        contract.exchange = "DTB"
        #! [indcontract]
        return contract

    @staticmethod
    def CFD():
        #! [cfdcontract]
        contract = Contract()
        contract.symbol = "IBDE30"
        contract.secType = "CFD"
        contract.currency = "EUR"
        contract.exchange = "SMART"
        #! [cfdcontract]
        return contract

    @staticmethod
    def EuropeanStock():
        contract = Contract()
        contract.symbol = "SIE"
        contract.secType = "STK"
        contract.currency = "EUR"
        contract.exchange = "SMART"
        return contract

    @staticmethod
    def OptionAtIse():
        contract = Contract()
        contract.symbol = "BPX"
        contract.secType = "OPT"
        contract.currency = "USD"
        contract.exchange = "ISE"
        contract.lastTradeDateOrContractMonth = "20160916"
        contract.right = "C"
        contract.strike = 65
        contract.multiplier = "100"
        return contract

    @staticmethod
    def BondWithCusip():
        #! [bondwithcusip]
        contract = Contract()
        # enter CUSIP as symbol
        contract.symbol = "912828C57"
        contract.secType = "BOND"
        contract.exchange = "SMART"
        contract.currency = "USD"
        #! [bondwithcusip]
        return contract

    @staticmethod
    def Bond():
        #! [bond]
        contract = Contract()
        contract.conId = 15960357
        contract.exchange = "SMART"
        #! [bond]
        return contract

    @staticmethod
    def MutualFund():
        #! [fundcontract]
        contract = Contract()
        contract.symbol = "VINIX"
        contract.secType = "FUND"
        contract.exchange = "FUNDSERV"
        contract.currency = "USD"
        #! [fundcontract]
        return contract

    @staticmethod
    def MutualFund_VINEX():
        #! [fundcontract]
        contract = Contract()
        contract.symbol = "VINEX"
        contract.secType = "FUND"
        contract.exchange = "FUNDSERV"
        contract.currency = "USD"
        #! [fundcontract]
        return contract

    @staticmethod
    def MutualFund_VFINX():
        #! [fundcontract]
        contract = Contract()
        contract.symbol = "VFINX"
        contract.secType = "FUND"
        contract.exchange = "FUNDSERV"
        contract.currency = "USD"
        #! [fundcontract]
        return contract

    @staticmethod
    def Commodity():
        #! [commoditycontract]
        contract = Contract()
        contract.symbol = "XAUUSD"
        contract.secType = "CMDTY"
        contract.exchange = "SMART"
        contract.currency = "USD"
        #! [commoditycontract]
        return contract

    @staticmethod
    def USDBCAtSmart():
        contract = Contract()
        contract.symbol = "DBC"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        return contract

    @staticmethod
    def USStock():
        #! [stkcontract]
        contract = Contract()
        contract.symbol = "IBKR"
        contract.secType = "STK"
        contract.currency = "USD"
        # In the API side, NASDAQ is always defined as ISLAND in the exchange field
        contract.exchange = "ISLAND"
        #! [stkcontract]
        return contract

    @staticmethod
    def USStockWithPrimaryExch():
        #! [stkcontractwithprimary]
        contract = Contract()
        contract.symbol = "MSFT"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        # Specify the Primary Exchange attribute to avoid contract ambiguity
        # (there is an ambiguity because there is also a MSFT contract with primary exchange = "AEB")
        contract.primaryExchange = "ISLAND"
        #! [stkcontractwithprimary]
        return contract

    @staticmethod
    def USStockAtSmart():
        contract = Contract()
        contract.symbol = "QCOM"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        return contract

    @staticmethod
    def USSPYAtSmart():
        contract = Contract()
        contract.symbol = "SPY"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        return contract

    @staticmethod
    def USSCZAtSmart():
        contract = Contract()
        contract.symbol = "SCZ"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        return contract

    @staticmethod
    def USVOOAtSmart():
        contract = Contract()
        contract.symbol = "VOO"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        return contract

    @staticmethod
    def USVOOAtNYSE():
        contract = Contract()
        contract.symbol = "VOO"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "NYSE"
        return contract

    @staticmethod
    def USQQQAtSmart():
        contract = Contract()
        contract.symbol = "QQQ"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        return contract

    @staticmethod
    def USEFAAtSmart():
        contract = Contract()
        contract.symbol = "EFA"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        return contract

    @staticmethod
    def USEEMAtSmart():
        contract = Contract()
        contract.symbol = "EEM"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        return contract

    @staticmethod
    def USEWJAtSmart():
        contract = Contract()
        contract.symbol = "EWJ"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        return contract

    @staticmethod
    def USIEFAtSmart():
        contract = Contract()
        contract.symbol = "IEF"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        return contract

    @staticmethod
    def USHYGAtSmart():
        contract = Contract()
        contract.symbol = "HYG"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        return contract

    @staticmethod
    def USGLDAtSmart():
        contract = Contract()
        contract.symbol = "GLD"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "ISLAND"
        return contract

    @staticmethod
    def USTLTAtSmart():
        contract = Contract()
        contract.symbol = "TLT"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        return contract

    @staticmethod
    def USVNQAtSmart():
        contract = Contract()
        contract.symbol = "VNQ"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        return contract

    @staticmethod
    def USVEUAtSmart():
        contract = Contract()
        contract.symbol = "VEU"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        return contract

    @staticmethod
    def USVEAAtSmart():
        contract = Contract()
        contract.symbol = "VEA"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        return contract

    @staticmethod
    def USVWOAtSmart():
        contract = Contract()
        contract.symbol = "VWO"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        return contract

    @staticmethod
    def USSHYAtSmart():
        contract = Contract()
        contract.symbol = "SHY"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        return contract

    @staticmethod
    def USLQDAtSmart():
        contract = Contract()
        contract.symbol = "LQD"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        return contract

    @staticmethod
    def USEZUAtSmart():
        contract = Contract()
        contract.symbol = "EZU"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        return contract

    @staticmethod
    def USRWXAtSmart():
        contract = Contract()
        contract.symbol = "RWX"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        return contract


    @staticmethod
    def USBNDAtNYSE():
        contract = Contract()
        contract.symbol = "BND"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "NYSE"
        return contract

    @staticmethod
    def USBNDAtSmart():
        contract = Contract()
        contract.symbol = "BND"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        return contract

    @staticmethod
    def USOptionContract():
        #! [optcontract_us]
        contract = Contract()
        contract.symbol = "GOOG"
        contract.secType = "OPT"
        contract.exchange = "SMART"
        contract.currency = "USD"
        contract.lastTradeDateOrContractMonth = "20170120"
        contract.strike = 615
        contract.right = "C"
        contract.multiplier = "100"
        #! [optcontract_us]
        return contract

    @staticmethod
    def OptionAtBOX():
        #! [optcontract]
        contract = Contract()
        contract.symbol = "GOOG"
        contract.secType = "OPT"
        contract.exchange = "BOX"
        contract.currency = "USD"
        contract.lastTradeDateOrContractMonth = "20170120"
        contract.strike = 615
        contract.right = "C"
        contract.multiplier = "100"
        #! [optcontract]
        return contract

    """ Option contracts require far more information since there are many 
    contracts having the exact same attributes such as symbol, currency, 
    strike, etc. This can be overcome by adding more details such as the 
    trading class"""

    @staticmethod
    def OptionWithTradingClass():
        #! [optcontract_tradingclass]
        contract = Contract()
        contract.symbol = "SANT"
        contract.secType = "OPT"
        contract.exchange = "MEFFRV"
        contract.currency = "EUR"
        contract.lastTradeDateOrContractMonth = "20190621"
        contract.strike = 7.5
        contract.right = "C"
        contract.multiplier = "100"
        contract.tradingClass = "SANEU"
        #! [optcontract_tradingclass]
        return contract

    """ Using the contract's own symbol (localSymbol) can greatly simplify a
    contract description """

    @staticmethod
    def OptionWithLocalSymbol():
        #! [optcontract_localsymbol]
        contract = Contract()
        # Watch out for the spaces within the local symbol!
        contract.localSymbol = "C DBK  DEC 20  1600"
        contract.secType = "OPT"
        contract.exchange = "DTB"
        contract.currency = "EUR"
        #! [optcontract_localsymbol]
        return contract

    """ Dutch Warrants (IOPTs) can be defined using the local symbol or conid 
    """

    @staticmethod
    def DutchWarrant():
        #! [ioptcontract]
        contract = Contract()
        contract.localSymbol = "B881G"
        contract.secType = "IOPT"
        contract.exchange = "SBF"
        contract.currency = "EUR"
        #! [ioptcontract]
        return contract

    """ Future contracts also require an expiration date but are less
    complicated than options."""

    @staticmethod
    def SimpleFuture():
        #! [futcontract]
        contract = Contract()
        contract.symbol = "ES"
        contract.secType = "FUT"
        contract.exchange = "GLOBEX"
        contract.currency = "USD"
        contract.lastTradeDateOrContractMonth = "201803"
        #! [futcontract]
        return contract

    """Rather than giving expiration dates we can also provide the local symbol
    attributes such as symbol, currency, strike, etc. """

    @staticmethod
    def FutureWithLocalSymbol():
        #! [futcontract_local_symbol]
        contract = Contract()
        contract.secType = "FUT"
        contract.exchange = "GLOBEX"
        contract.currency = "USD"
        contract.localSymbol = "ESU6"
        #! [futcontract_local_symbol]
        return contract

    @staticmethod
    def FutureWithMultiplier():
        #! [futcontract_multiplier]
        contract = Contract()
        contract.symbol = "DAX"
        contract.secType = "FUT"
        contract.exchange = "DTB"
        contract.currency = "EUR"
        contract.lastTradeDateOrContractMonth = "201609"
        contract.multiplier = "5"
        #! [futcontract_multiplier]
        return contract

    """ Note the space in the symbol! """

    @staticmethod
    def WrongContract():
        contract = Contract()
        contract.symbol = " IJR "
        contract.conId = 9579976
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"
        return contract

    @staticmethod
    def FuturesOnOptions():
        #! [fopcontract]
        contract = Contract()
        contract.symbol = "SPX"
        contract.secType = "FOP"
        contract.exchange = "GLOBEX"
        contract.currency = "USD"
        contract.lastTradeDateOrContractMonth = "20180315"
        contract.strike = 1025
        contract.right = "C"
        contract.multiplier = "250"
        #! [fopcontract]
        return contract

    """ It is also possible to define contracts based on their ISIN (IBKR STK
    sample). """

    @staticmethod
    def ByISIN():
        contract = Contract()
        contract.secIdType = "ISIN"
        contract.secId = "US45841N1072"
        contract.exchange = "SMART"
        contract.currency = "USD"
        contract.secType = "STK"
        return contract

    """ Or their conId (EUR.uSD sample).
    Note: passing a contract containing the conId can cause problems if one of 
    the other provided attributes does not match 100% with what is in IB's 
    database. This is particularly important for contracts such as Bonds which 
    may change their description from one day to another.
    If the conId is provided, it is best not to give too much information as
    in the example below. """

    @staticmethod
    def ByConId():
        contract = Contract()
        contract.secType = "CASH"
        contract.conId = 12087792
        contract.exchange = "IDEALPRO"
        return contract

    """ Ambiguous contracts are great to use with reqContractDetails. This way
    you can query the whole option chain for an underlying. Bear in mind that
    there are pacing mechanisms in place which will delay any further responses
    from the TWS to prevent abuse. """

    @staticmethod
    def OptionForQuery():
        #! [optionforquery]
        contract = Contract()
        contract.symbol = "FISV"
        contract.secType = "OPT"
        contract.exchange = "SMART"
        contract.currency = "USD"
        #! [optionforquery]
        return contract

    @staticmethod
    def OptionComboContract():
        #! [bagoptcontract]
        contract = Contract()
        contract.symbol = "DBK"
        contract.secType = "BAG"
        contract.currency = "EUR"
        contract.exchange = "DTB"

        leg1 = ComboLeg()
        leg1.conId = 197397509  # DBK JUN 15 2018 C
        leg1.ratio = 1
        leg1.action = "BUY"
        leg1.exchange = "DTB"

        leg2 = ComboLeg()
        leg2.conId = 197397584  # DBK JUN 15 2018 P
        leg2.ratio = 1
        leg2.action = "SELL"
        leg2.exchange = "DTB"

        contract.comboLegs = []
        contract.comboLegs.append(leg1)
        contract.comboLegs.append(leg2)
        #! [bagoptcontract]
        return contract

    """ STK Combo contract
    Leg 1: 43645865 - IBKR's STK
    Leg 2: 9408 - McDonald's STK """

    @staticmethod
    def StockComboContract():
        #! [bagstkcontract]
        contract = Contract()
        contract.symbol = "IBKR,MCD"
        contract.secType = "BAG"
        contract.currency = "USD"
        contract.exchange = "SMART"

        leg1 = ComboLeg()
        leg1.conId = 43645865  # IBKR STK
        leg1.ratio = 1
        leg1.action = "BUY"
        leg1.exchange = "SMART"

        leg2 = ComboLeg()
        leg2.conId = 9408  # MCD STK
        leg2.ratio = 1
        leg2.action = "SELL"
        leg2.exchange = "SMART"

        contract.comboLegs = []
        contract.comboLegs.append(leg1)
        contract.comboLegs.append(leg2)
        #! [bagstkcontract]
        return contract

    """ CBOE Volatility Index Future combo contract """

    @staticmethod
    def FutureComboContract():
        #! [bagfutcontract]
        contract = Contract()
        contract.symbol = "VIX"
        contract.secType = "BAG"
        contract.currency = "USD"
        contract.exchange = "CFE"

        leg1 = ComboLeg()
        leg1.conId = 256038899  # VIX FUT 201708
        leg1.ratio = 1
        leg1.action = "BUY"
        leg1.exchange = "CFE"

        leg2 = ComboLeg()
        leg2.conId = 260564703  # VIX FUT 201709
        leg2.ratio = 1
        leg2.action = "SELL"
        leg2.exchange = "CFE"

        contract.comboLegs = []
        contract.comboLegs.append(leg1)
        contract.comboLegs.append(leg2)
        #! [bagfutcontract]
        return contract

    @staticmethod
    def SmartFutureComboContract():
        #! [smartfuturespread]
        contract = Contract()
        # WTI,COIL spread. Symbol can be defined as first leg symbol ("WTI") or currency ("USD")
        contract.symbol = "WTI"
        contract.secType = "BAG"
        contract.currency = "USD"
        contract.exchange = "SMART"

        leg1 = ComboLeg()
        leg1.conId = 55928698  # WTI future June 2017
        leg1.ratio = 1
        leg1.action = "BUY"
        leg1.exchange = "IPE"

        leg2 = ComboLeg()
        leg2.conId = 55850663  # COIL future June 2017
        leg2.ratio = 1
        leg2.action = "SELL"
        leg2.exchange = "IPE"

        contract.comboLegs = []
        contract.comboLegs.append(leg1)
        contract.comboLegs.append(leg2)
        #! [smartfuturespread]
        return contract

    @staticmethod
    def InterCmdtyFuturesContract():
        #! [intcmdfutcontract]
        contract = Contract()
        # symbol is 'local symbol' of intercommodity spread.
        contract.symbol = "CL.BZ"
        contract.secType = "BAG"
        contract.currency = "USD"
        contract.exchange = "NYMEX"

        leg1 = ComboLeg()
        leg1.conId = 47207310  # CL Dec'16 @NYMEX
        leg1.ratio = 1
        leg1.action = "BUY"
        leg1.exchange = "NYMEX"

        leg2 = ComboLeg()
        leg2.conId = 47195961  # BZ Dec'16 @NYMEX
        leg2.ratio = 1
        leg2.action = "SELL"
        leg2.exchange = "NYMEX"

        contract.comboLegs = []
        contract.comboLegs.append(leg1)
        contract.comboLegs.append(leg2)
        #! [intcmdfutcontract]
        return contract

    @staticmethod
    def NewsFeedForQuery():
        #! [newsfeedforquery]
        contract = Contract()
        contract.secType = "NEWS"
        contract.exchange = "BT"  # Briefing Trader
        #! [newsfeedforquery]
        return contract

    @staticmethod
    def BTbroadtapeNewsFeed():
        #! [newscontractbt]
        contract = Contract()
        contract.symbol = "BT:BT_ALL"  # BroadTape All News
        contract.secType = "NEWS"
        contract.exchange = "BT"  # Briefing Trader
        #! [newscontractbt]
        return contract

    @staticmethod
    def BZbroadtapeNewsFeed():
        #! [newscontractbz]
        contract = Contract()
        contract.symbol = "BZ:BZ_ALL"  # BroadTape All News
        contract.secType = "NEWS"
        contract.exchange = "BZ"  # Benzinga Pro
        #! [newscontractbz]
        return contract

    @staticmethod
    def FLYbroadtapeNewsFeed():
        #! [newscontractfly]
        contract = Contract()
        contract.symbol = "FLY:FLY_ALL"  # BroadTape All News
        contract.secType = "NEWS"
        contract.exchange = "FLY"  # Fly on the Wall
       #! [newscontractfly]
        return contract

    @staticmethod
    def MTbroadtapeNewsFeed():
        #! [newscontractmt]
        contract = Contract()
        contract.symbol = "MT:MT_ALL"  # BroadTape All News
        contract.secType = "NEWS"
        contract.exchange = "MT"  # Midnight Trader
        #! [newscontractmt]
        return contract

    @staticmethod
    def ContFut():
        #! [continuousfuturescontract]
        contract = Contract()
        contract.symbol = "ES"
        contract.secType = "CONTFUT"
        contract.exchange = "GLOBEX"
        #! [continuousfuturescontract]
        return contract

    @staticmethod
    def ContAndExpiringFut():
        #! [contandexpiringfut]
        contract = Contract()
        contract.symbol = "ES"
        contract.secType = "FUT+CONTFUT"
        contract.exchange = "GLOBEX"
        #! [contandexpiringfut]
        return contract

    @staticmethod
    def JefferiesContract():
        #! [jefferies_contract]
        contract = Contract()
        contract.symbol = "AAPL"
        contract.secType = "STK"
        contract.exchange = "JEFFALGO"
        contract.currency = "USD"
        #! [jefferies_contract]
        return contract

    @staticmethod
    def CSFBContract():
        #! [csfb_contract]
        contract = Contract()
        contract.symbol = "IBKR"
        contract.secType = "STK"
        contract.exchange = "CSFBALGO"
        contract.currency = "USD"
        #! [csfb_contract]
        return contract


def Test():
    from ibapi.utils import ExerciseStaticMethods
    ExerciseStaticMethods(TYCoContracts)


if "__main__" == __name__:
    Test()
