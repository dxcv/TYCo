"""
Copyright (C) 2018 Interactive Brokers LLC. All rights reserved. This code is subject to the terms
and conditions of the IB API Non-Commercial License or the IB API Commercial License, as applicable.
"""

import sys
import argparse
import datetime
import collections
import inspect

import logging
import time
import os.path
import TYCoAlgo

from ibapi import wrapper
from ibapi.client import EClient
from ibapi.utils import iswrapper

# types
from ibapi.common import *
from ibapi.order_condition import *
from ibapi.contract import *
from ibapi.order import *
from ibapi.order_state import *
from ibapi.execution import Execution
from ibapi.execution import ExecutionFilter
from ibapi.commission_report import CommissionReport
from ibapi.scanner import ScannerSubscription
from ibapi.ticktype import *

from ibapi.account_summary_tags import *


from AvailableAlgoParams import AvailableAlgoParams
from TYCoContracts import TYCoContracts
from TYCoOrders import TYCoOrders


def SetupLogger():
    if not os.path.exists("log"):
        os.makedirs("log")

    time.strftime("pyibapi.%Y%m%d_%H%M%S.log")

    recfmt = '(%(threadName)s) %(asctime)s.%(msecs)03d %(levelname)s %(filename)s:%(lineno)d %(message)s'

    timefmt = '%y%m%d_%H:%M:%S'

    # logging.basicConfig( level=logging.DEBUG,
    #                    format=recfmt, datefmt=timefmt)
    logging.basicConfig(filename=time.strftime("log/pyibapi.%y%m%d_%H%M%S.log"),
                        filemode="w",
                        level=logging.INFO,
                        format=recfmt, datefmt=timefmt)
    logger = logging.getLogger()
    console = logging.StreamHandler()
    console.setLevel(logging.ERROR)
    logger.addHandler(console)


def printWhenExecuting(fn):
    def fn2(self):
        print("   doing", fn.__name__)
        fn(self)
        print("   done w/", fn.__name__)

    return fn2


def printinstance(inst: Object):
    attrs = vars(inst)
    print(', '.join("%s: %s" % item for item in attrs.items()))


class Activity(Object):
    def __init__(self, reqMsgId, ansMsgId, ansEndMsgId, reqId):
        self.reqMsdId = reqMsgId
        self.ansMsgId = ansMsgId
        self.ansEndMsgId = ansEndMsgId
        self.reqId = reqId


class RequestMgr(Object):
    def __init__(self):
        # I will keep this simple even if slower for now: only one list of
        # requests finding will be done by linear search
        self.requests = []

    def addReq(self, req):
        self.requests.append(req)

    def receivedMsg(self, msg):
        pass


# ! [socket_declare]
class TestClient(EClient):
    def __init__(self, wrapper):
        EClient.__init__(self, wrapper)
        # ! [socket_declare]

        # how many times a method is called to see test coverage
        self.clntMeth2callCount = collections.defaultdict(int)
        self.clntMeth2reqIdIdx = collections.defaultdict(lambda: -1)
        self.reqId2nReq = collections.defaultdict(int)
        self.setupDetectReqId()

    def countReqId(self, methName, fn):
        def countReqId_(*args, **kwargs):
            self.clntMeth2callCount[methName] += 1
            idx = self.clntMeth2reqIdIdx[methName]
            if idx >= 0:
                sign = -1 if 'cancel' in methName else 1
                self.reqId2nReq[sign * args[idx]] += 1
            return fn(*args, **kwargs)

        return countReqId_

    def setupDetectReqId(self):

        methods = inspect.getmembers(EClient, inspect.isfunction)
        for (methName, meth) in methods:
            if methName != "send_msg":
                # don't screw up the nice automated logging in the send_msg()
                self.clntMeth2callCount[methName] = 0
                # logging.debug("meth %s", name)
                sig = inspect.signature(meth)
                for (idx, pnameNparam) in enumerate(sig.parameters.items()):
                    (paramName, param) = pnameNparam
                    if paramName == "reqId":
                        self.clntMeth2reqIdIdx[methName] = idx

                setattr(TestClient, methName, self.countReqId(methName, meth))

                # print("TestClient.clntMeth2reqIdIdx", self.clntMeth2reqIdIdx)


# ! [ewrapperimpl]
class TestWrapper(wrapper.EWrapper):
    # ! [ewrapperimpl]
    def __init__(self):
        wrapper.EWrapper.__init__(self)

        self.wrapMeth2callCount = collections.defaultdict(int)
        self.wrapMeth2reqIdIdx = collections.defaultdict(lambda: -1)
        self.reqId2nAns = collections.defaultdict(int)
        self.setupDetectWrapperReqId()

    # TODO: see how to factor this out !!

    def countWrapReqId(self, methName, fn):
        def countWrapReqId_(*args, **kwargs):
            self.wrapMeth2callCount[methName] += 1
            idx = self.wrapMeth2reqIdIdx[methName]
            if idx >= 0:
                self.reqId2nAns[args[idx]] += 1
            return fn(*args, **kwargs)

        return countWrapReqId_

    def setupDetectWrapperReqId(self):

        methods = inspect.getmembers(wrapper.EWrapper, inspect.isfunction)
        for (methName, meth) in methods:
            self.wrapMeth2callCount[methName] = 0
            # logging.debug("meth %s", name)
            sig = inspect.signature(meth)
            for (idx, pnameNparam) in enumerate(sig.parameters.items()):
                (paramName, param) = pnameNparam
                # we want to count the errors as 'error' not 'answer'
                if 'error' not in methName and paramName == "reqId":
                    self.wrapMeth2reqIdIdx[methName] = idx

            setattr(TestWrapper, methName, self.countWrapReqId(methName, meth))

            # print("TestClient.wrapMeth2reqIdIdx", self.wrapMeth2reqIdIdx)


# this is here for documentation generation
"""
#! [ereader]
        # You don't need to run this in your code!
        self.reader = reader.EReader(self.conn, self.msg_queue)
        self.reader.start()   # start thread
#! [ereader]
"""


class TAA_struct(object):
    def __init__(self, VOO, VOOp, QQQ, QQQp, EFA, EFAp, EEM, EEMp, EWJ, EWJp, IEF, IEFp, HYG, HYGp, GLD, GLDp, TLT, TLTp, VNQ, VNQp, VEU, VEUp, BND, BNDp, trading):
        self.VOO = VOO
        self.VOOp = VOOp
        self.QQQ = QQQ
        self.QQQp = QQQp
        self.EFA = EFA
        self.EFAp = EFAp
        self.EEM = EEM
        self.EEMp = EEMp
        self.EWJ = EWJ
        self.EWJp = EWJp
        self.IEF = IEF
        self.IEFp = IEFp
        self.HYG = HYG
        self.HYGp = HYGp
        self.GLD = GLD
        self.GLDp = GLDp
        self.TLT = TLT
        self.TLTp = TLTp
        self.VNQ = VNQ
        self.VNQp = VNQp
        self.VEU = VEU
        self.VEUp = VEUp
        self.BND = BND
        self.BNDp = BNDp
        self.trading = trading

# Dick Stoken’s Active Combined Asset (ACA)
# S&P 500 (VOO) vs Intermediate-term US Treasuries (IEF)
# Gold (GLD) vs Long-term US Treasuries (TLT)
# US Real Estate (VNQ) vs Intermediate-term US Treasuries (IEF)

# ! [socket_init]


class TestApp(TestWrapper, TestClient):
    def __init__(self):
        TestWrapper.__init__(self)
        TestClient.__init__(self, wrapper=self)
        # ! [socket_init]
        self.nKeybInt = 0
        self.started = False
        self.nextValidOrderId = None
        self.permId2ord = {}
        self.reqId2nErr = collections.defaultdict(int)
        self.globalCancelOnly = False
        self.simplePlaceOid = None
        self.TAA = TAA_struct(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    def dumpTestCoverageSituation(self):
        for clntMeth in sorted(self.clntMeth2callCount.keys()):
            logging.debug("ClntMeth: %-30s %6d" % (clntMeth,
                                                   self.clntMeth2callCount[clntMeth]))

        for wrapMeth in sorted(self.wrapMeth2callCount.keys()):
            logging.debug("WrapMeth: %-30s %6d" % (wrapMeth,
                                                   self.wrapMeth2callCount[wrapMeth]))

    def dumpReqAnsErrSituation(self):
        logging.debug("%s\t%s\t%s\t%s" % ("ReqId", "#Req", "#Ans", "#Err"))
        for reqId in sorted(self.reqId2nReq.keys()):
            nReq = self.reqId2nReq.get(reqId, 0)
            nAns = self.reqId2nAns.get(reqId, 0)
            nErr = self.reqId2nErr.get(reqId, 0)
            logging.debug("%d\t%d\t%s\t%d" % (reqId, nReq, nAns, nErr))

    @iswrapper
    # ! [connectack]
    def connectAck(self):
        if self.async:
            self.startApi()

    # ! [connectack]

    @iswrapper
    # ! [nextvalidid]
    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)

        logging.debug("setting nextValidOrderId: %d", orderId)
        self.nextValidOrderId = orderId
        # ! [nextvalidid]

        # we can start now
        self.start()

    def start(self):
        if self.started:
            return

        self.started = True

        if self.globalCancelOnly:
            print("Executing GlobalCancel only")
            self.reqGlobalCancel()
        else:
            print("Executing requests")
            self.marketDataType_req()
            self.TAA_req()
            self.request_update_portfolio()
            print("Executing requests ... finished")

    def keyboardInterrupt(self):
        self.nKeybInt += 1
        if self.nKeybInt == 1:
            self.stop()
        else:
            print("Finishing test")
            self.done = True

    def stop(self):
        print("Executing cancels")
        self.orderOperations_cancel()
        self.accountOperations_cancel()
        self.tickDataOperations_cancel()
        print("Executing cancels ... finished")

    def nextOrderId(self):
        oid = self.nextValidOrderId
        self.nextValidOrderId += 1
        return oid

    @iswrapper
    # ! [error]
    def error(self, reqId: TickerId, errorCode: int, errorString: str):
        super().error(reqId, errorCode, errorString)
        print("Error. Id: ", reqId, " Code: ",
              errorCode, " Msg: ", errorString)

    # ! [error] self.reqId2nErr[reqId] += 1

    @iswrapper
    def winError(self, text: str, lastError: int):
        super().winError(text, lastError)

    @iswrapper
    # ! [openorder]
    def openOrder(self, orderId: OrderId, contract: Contract, order: Order,
                  orderState: OrderState):
        super().openOrder(orderId, contract, order, orderState)
        print("OpenOrder. ID:", orderId, contract.symbol, contract.secType,
              "@", contract.exchange, ":", order.action, order.orderType,
              order.totalQuantity, orderState.status)
        # ! [openorder]

        if order.whatIf:
            print("WhatIf: ", orderId, "initMarginBefore: ", orderState.initMarginBefore, " maintMarginBefore: ", orderState.maintMarginBefore,
                  "equityWithLoanBefore ", orderState.equityWithLoanBefore, " initMarginChange ", orderState.initMarginChange, " maintMarginChange: ", orderState.maintMarginChange,
                  " equityWithLoanChange: ", orderState.equityWithLoanChange, " initMarginAfter: ", orderState.initMarginAfter, " maintMarginAfter: ", orderState.maintMarginAfter,
                  " equityWithLoanAfter: ", orderState.equityWithLoanAfter)

        order.contract = contract
        self.permId2ord[order.permId] = order

    @iswrapper
    # ! [openorderend]
    def openOrderEnd(self):
        super().openOrderEnd()
        print("OpenOrderEnd")
        # ! [openorderend]

        logging.debug("Received %d openOrders", len(self.permId2ord))

    @iswrapper
    # ! [orderstatus]
    def orderStatus(self, orderId: OrderId, status: str, filled: float,
                    remaining: float, avgFillPrice: float, permId: int,
                    parentId: int, lastFillPrice: float, clientId: int,
                    whyHeld: str, mktCapPrice: float):
        super().orderStatus(orderId, status, filled, remaining,
                            avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)
        print("OrderStatus. Id: ", orderId, ", Status: ", status, ", Filled: ", filled,
              ", Remaining: ", remaining, ", AvgFillPrice: ", avgFillPrice,
              ", PermId: ", permId, ", ParentId: ", parentId, ", LastFillPrice: ",
              lastFillPrice, ", ClientId: ", clientId, ", WhyHeld: ",
              whyHeld, ", MktCapPrice: ", mktCapPrice)

    # ! [orderstatus]
    @iswrapper
    # ! [managedaccounts]
    def managedAccounts(self, accountsList: str):
        super().managedAccounts(accountsList)
        print("Account list: ", accountsList)
        # ! [managedaccounts]

        self.account = accountsList.split(",")[0]

    @printWhenExecuting
    def request_update_portfolio(self):
        self.reqAccountUpdates(True, self.account)
        self.reqPositions()

    @iswrapper
    # ! [updateportfolio]
    def updatePortfolio(self, contract: Contract, position: float,
                        marketPrice: float, marketValue: float,
                        averageCost: float, unrealizedPNL: float,
                        realizedPNL: float, accountName: str):
        super().updatePortfolio(contract, position, marketPrice, marketValue,
                                averageCost, unrealizedPNL, realizedPNL, accountName)
        print("UpdatePortfolio.", contract.symbol, "", contract.secType, "@",
              contract.exchange, "Position:", position, "MarketPrice:", marketPrice,
              "MarketValue:", marketValue, "AverageCost:", averageCost,
              "UnrealizedPNL:", unrealizedPNL, "RealizedPNL:", realizedPNL,
              "AccountName:", accountName)

        if(contract.symbol == "VOO"):
            self.TAA.VOO = position
        if(contract.symbol == "QQQ"):
            self.TAA.QQQ = position
        if(contract.symbol == "EFA"):
            self.TAA.EFA = position
        if(contract.symbol == "EEM"):
            self.TAA.EEM = position
        if(contract.symbol == "EWJ"):
            self.TAA.EWJ = position
        if(contract.symbol == "IEF"):
            self.TAA.IEF = position
        if(contract.symbol == "HYG"):
            self.TAA.HYG = position
        if(contract.symbol == "GLD"):
            self.TAA.GLD = position
        if(contract.symbol == "TLT"):
            self.TAA.TLT = position
        if(contract.symbol == "VNQ"):
            self.TAA.VNQ = position
        if(contract.symbol == "VEU"):
            self.TAA.VEU = position
        if(contract.symbol == "BND"):
            self.TAA.BND = position
    # ! [updateportfolio]

    @iswrapper
    # ! [updateaccounttime]
    def updateAccountTime(self, timeStamp: str):
        super().updateAccountTime(timeStamp)
        print("UpdateAccountTime. Time:", timeStamp)

    # ! [updateaccounttime]
    # ! [accountdownloadend]

    @iswrapper
    # ! [accountdownloadend]
    def accountDownloadEnd(self, accountName: str):
        super().accountDownloadEnd(accountName)
        print("Account download finished:", accountName)

    # ! [accountdownloadend]

    @iswrapper
    # ! [position]
    def position(self, account: str, contract: Contract, position: float,
                 avgCost: float):
        super().position(account, contract, position, avgCost)
        print("Position.", account, "Symbol:", contract.symbol, "SecType:",
              contract.secType, "Currency:", contract.currency,
              "Position:", position, "Avg cost:", avgCost)

    # ! [position]

    @iswrapper
    # ! [positionend]
    def positionEnd(self):
        super().positionEnd()
        print("PositionEnd")

    # ! [positionend]

    def marketDataType_req(self):
        # ! [reqmarketdatatype]
        # Switch to live (1) frozen (2) delayed (3) delayed frozen (4).
        self.reqMarketDataType(MarketDataTypeEnum.DELAYED)
        # ! [reqmarketdatatype]

    @iswrapper
    # ! [marketdatatype]
    def marketDataType(self, reqId: TickerId, marketDataType: int):
        super().marketDataType(reqId, marketDataType)
        print("MarketDataType. ", reqId, "Type:", marketDataType)

    # ! [marketdatatype]

    @printWhenExecuting
    def TAA_req(self):
        self.reqMktData(1000, TYCoContracts.USVOOAtSmart(),
                        "", False, False, [])
        self.reqMktData(1001, TYCoContracts.USQQQAtSmart(),
                        "", False, False, [])
        self.reqMktData(1002, TYCoContracts.USEFAAtSmart(),
                        "", False, False, [])
        self.reqMktData(1003, TYCoContracts.USEEMAtSmart(),
                        "", False, False, [])
        self.reqMktData(1004, TYCoContracts.USEWJAtSmart(),
                        "", False, False, [])

        self.reqMktData(1005, TYCoContracts.USIEFAtSmart(),
                        "", False, False, [])
        self.reqMktData(1006, TYCoContracts.USHYGAtSmart(),
                        "", False, False, [])
        self.reqMktData(1007, TYCoContracts.USGLDAtSmart(),
                        "", False, False, [])
        self.reqMktData(1008, TYCoContracts.USTLTAtSmart(),
                        "", False, False, [])
        self.reqMktData(1009, TYCoContracts.USVNQAtSmart(),
                        "", False, False, [])
        self.reqMktData(1010, TYCoContracts.USVEUAtSmart(),
                        "", False, False, [])
        self.reqMktData(1011, TYCoContracts.USBNDAtSmart(),
                        "", False, False, [])

    @iswrapper
    # ! [tickprice]
    def tickPrice(self, reqId: TickerId, tickType: TickType, price: float,
                  attrib: TickAttrib):
        super().tickPrice(reqId, tickType, price, attrib)
        print("Tick Price. Ticker Id:", reqId, "tickType:", tickType,
              "Price:", price, "CanAutoExecute:", attrib.canAutoExecute,
              "PastLimit:", attrib.pastLimit, end=' ')
        if tickType == TickTypeEnum.BID or tickType == TickTypeEnum.ASK:
            print("PreOpen:", attrib.preOpen)
        else:
            print()

        if(reqId == 1000 and tickType == 66):
            self.TAA.VOOp = price
        if(reqId == 1001 and tickType == 66):
            self.TAA.QQQp = price
        if(reqId == 1002 and tickType == 66):
            self.TAA.EFAp = price
        if(reqId == 1003 and tickType == 66):
            self.TAA.EEMp = price
        if(reqId == 1004 and tickType == 66):
            self.TAA.EWJp = price
        if(reqId == 1005 and tickType == 66):
            self.TAA.IEFp = price
        if(reqId == 1006 and tickType == 66):
            self.TAA.HYGp = price
        if(reqId == 1007 and tickType == 66):
            self.TAA.GLDp = price
        if(reqId == 1008 and tickType == 66):
            self.TAA.TLTp = price
        if(reqId == 1009 and tickType == 66):
            self.TAA.VNQp = price
        if(reqId == 1010 and tickType == 66):
            self.TAA.VEUp = price
        if(reqId == 1011 and tickType == 66):
            self.TAA.BNDp = price

        if(self.TAA.VOOp != 0 and
                self.TAA.QQQp != 0 and
                self.TAA.EFAp != 0 and
                self.TAA.EEMp != 0 and
                self.TAA.EWJp != 0 and
                self.TAA.IEFp != 0 and
                self.TAA.HYGp != 0 and
                self.TAA.GLDp != 0 and
                self.TAA.TLTp != 0 and
                self.TAA.VNQp != 0 and
                self.TAA.VEUp != 0 and
                self.TAA.BNDp != 0 and
                self.TAA.trading == 0
           ):
            self.TAA.trading = 1
            self.trade_TAA()
    # ! [tickprice]

    @iswrapper
    # ! [ticksize]
    def tickSize(self, reqId: TickerId, tickType: TickType, size: int):
        super().tickSize(reqId, tickType, size)
        print("Tick Size. Ticker Id:", reqId,
              "tickType:", tickType, "Size:", size)

    # ! [ticksize]

    @iswrapper
    # ! [tickgeneric]
    def tickGeneric(self, reqId: TickerId, tickType: TickType, value: float):
        super().tickGeneric(reqId, tickType, value)
        print("Tick Generic. Ticker Id:", reqId,
              "tickType:", tickType, "Value:", value)

    # ! [tickgeneric]

    @iswrapper
    # ! [tickstring]
    def tickString(self, reqId: TickerId, tickType: TickType, value: str):
        super().tickString(reqId, tickType, value)
        print("Tick string. Ticker Id:", reqId,
              "Type:", tickType, "Value:", value)

    # ! [tickstring]

    @iswrapper
    # ! [ticksnapshotend]
    def tickSnapshotEnd(self, reqId: int):
        super().tickSnapshotEnd(reqId)
        print("TickSnapshotEnd:", reqId)

    # ! [ticksnapshotend]

    @iswrapper
    # ! [headTimestamp]
    def headTimestamp(self, reqId: int, headTimestamp: str):
        print("HeadTimestamp: ", reqId, " ", headTimestamp)
    # ! [headTimestamp]

    @iswrapper
    # ! [historicaldata]
    def historicalData(self, reqId: int, bar: BarData):
        print("HistoricalData. ", reqId, " Date:", bar.date, "Open:", bar.open,
              "High:", bar.high, "Low:", bar.low, "Close:", bar.close, "Volume:", bar.volume,
              "Count:", bar.barCount, "WAP:", bar.average)
    # ! [historicaldata]

    @iswrapper
    # ! [historicaldataend]
    def historicalDataEnd(self, reqId: int, start: str, end: str):
        super().historicalDataEnd(reqId, start, end)
        print("HistoricalDataEnd ", reqId, "from", start, "to", end)
    # ! [historicaldataend]

    @iswrapper
    # ! [historicalDataUpdate]
    def historicalDataUpdate(self, reqId: int, bar: BarData):
        print("HistoricalDataUpdate. ", reqId, " Date:", bar.date, "Open:", bar.open,
              "High:", bar.high, "Low:", bar.low, "Close:", bar.close, "Volume:", bar.volume,
              "Count:", bar.barCount, "WAP:", bar.average)
    # ! [historicalDataUpdate]

    @iswrapper
    # ! [historicalticks]
    def historicalTicks(self, reqId: int, ticks: ListOfHistoricalTick, done: bool):
        for tick in ticks:
            print("Historical Tick. Req Id: ", reqId, ", time: ", tick.time,
                  ", price: ", tick.price, ", size: ", tick.size)
    # ! [historicalticks]

    @iswrapper
    # ! [historicalticksbidask]
    def historicalTicksBidAsk(self, reqId: int, ticks: ListOfHistoricalTickBidAsk,
                              done: bool):
        for tick in ticks:
            print("Historical Tick Bid/Ask. Req Id: ", reqId, ", time: ", tick.time,
                  ", bid price: ", tick.priceBid, ", ask price: ", tick.priceAsk,
                  ", bid size: ", tick.sizeBid, ", ask size: ", tick.sizeAsk)
    # ! [historicalticksbidask]

    @iswrapper
    # ! [historicaltickslast]
    def historicalTicksLast(self, reqId: int, ticks: ListOfHistoricalTickLast,
                            done: bool):
        for tick in ticks:
            print("Historical Tick Last. Req Id: ", reqId, ", time: ", tick.time,
                  ", price: ", tick.price, ", size: ", tick.size, ", exchange: ", tick.exchange,
                  ", special conditions:", tick.specialConditions)
    # ! [historicaltickslast]

    @iswrapper
    # ! [contractdetails]
    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        super().contractDetails(reqId, contractDetails)
        printinstance(contractDetails.contract)

    # ! [contractdetails]

    @iswrapper
    # ! [contractdetailsend]
    def contractDetailsEnd(self, reqId: int):
        super().contractDetailsEnd(reqId)
        print("ContractDetailsEnd. ", reqId, "\n")

    # ! [contractdetailsend]

    @iswrapper
    # ! [smartcomponents]
    def smartComponents(self, reqId: int, map: SmartComponentMap):
        super().smartComponents(reqId, map)
        print("smartComponents: ")
        for exch in map:
            print(exch.bitNumber, ", Exchange Name: ", exch.exchange,
                  ", Letter: ", exch.exchangeLetter)
    # ! [smartcomponents]

    @iswrapper
    # ! [tickReqParams]
    def tickReqParams(self, tickerId: int, minTick: float,
                      bboExchange: str, snapshotPermissions: int):
        super().tickReqParams(tickerId, minTick, bboExchange, snapshotPermissions)
        print("tickReqParams: ", tickerId, " minTick: ", minTick,
              " bboExchange: ", bboExchange, " snapshotPermissions: ", snapshotPermissions)
    # ! [tickReqParams]

    def adaptive_order_buy(self, contract, position, price):
        # ! [adaptive]
        print(" going to BUY ", contract.symbol, " position ", position, "at ",
              TYCoAlgo.round_to_nth_digits_after_decimal_point_with_base_m(price, 2, 1))
        baseOrder = TYCoOrders.LimitOrder(
            "BUY", position, TYCoAlgo.round_to_nth_digits_after_decimal_point_with_base_m(price, 2, 1))
        AvailableAlgoParams.FillAdaptiveParams(baseOrder, "Patient")
        self.placeOrder(self.nextOrderId(), contract, baseOrder)
        # ! [adaptive]

    def adaptive_order_sell(self, contract, position, price):
        # ! [adaptive]
        print(" going to SELL ", contract.symbol, " position ", position, "at ",
              TYCoAlgo.round_to_nth_digits_after_decimal_point_with_base_m(price, 2, 1))
        baseOrder = TYCoOrders.LimitOrder(
            "SELL", abs(position), TYCoAlgo.round_to_nth_digits_after_decimal_point_with_base_m(price, 2, 1))
        AvailableAlgoParams.FillAdaptiveParams(baseOrder, "Patient")
        self.placeOrder(self.nextOrderId(), contract, baseOrder)
        # ! [adaptive]

    @printWhenExecuting
    def trade_TAA(self):
        # make sure we have the current position data
        self.cancelMktData(1000)
        self.cancelMktData(1001)
        self.cancelMktData(1002)
        self.cancelMktData(1003)
        self.cancelMktData(1004)
        self.cancelMktData(1005)
        self.cancelMktData(1006)
        self.cancelMktData(1007)
        self.cancelMktData(1008)
        self.cancelMktData(1009)
        self.cancelMktData(1010)
        self.cancelMktData(1011)
        time.sleep(5)
        # predefine allocation

        # Keller and Butler’s Elastic Asset Allocation – Defensive
        kellerAllocation = 0
        kellerVOO = 0
        kellerQQQ = 0
        kellerEFA = 0
        kellerEEM = 0
        kellerEWJ = 0
        kellerIEF = 0
        kellerHYG = 0

        # Dick Stoken’s Active Combined Asset (ACA)
        StokenAllocation = 0
        StokenVOO = 0
        StokenIEF = 0
        StokenGLD = 0
        StokenTLT = 0
        StokenVNQ = 0

        # GEM
        GEMAllocation = 0
        GEMVOO = 0
        GEMVEU = 0
        GEMBND = 0

        targetVOO = (kellerAllocation * kellerVOO) + \
            (StokenAllocation*StokenVOO) + (GEMAllocation*GEMVOO)
        diffVOO = targetVOO - (self.TAA.VOO*self.TAA.VOOp)
        print("VOO diff is ", diffVOO)
        if(abs(diffVOO) >= self.TAA.VOOp and self.TAA.VOOp != 0 and abs(diffVOO) > 100):
            print("VOO diff is ", diffVOO, "going to do trade with ",
                  (round(diffVOO/self.TAA.VOOp)*self.TAA.VOOp))
            if(diffVOO > 0):
                self.adaptive_order_buy(TYCoContracts.USVOOAtSmart(),  round(
                    diffVOO/self.TAA.VOOp), (self.TAA.VOOp*1.01))
            else:
                self.adaptive_order_sell(TYCoContracts.USVOOAtSmart(),  round(
                    diffVOO/self.TAA.VOOp), (self.TAA.VOOp*0.99))

        targetQQQ = kellerAllocation*kellerQQQ
        diffQQQ = targetQQQ - (self.TAA.QQQ*self.TAA.QQQp)
        print("QQQ diff is ", diffQQQ)
        if(abs(diffQQQ) >= self.TAA.QQQp and self.TAA.QQQp != 0 and abs(diffQQQ) > 100):
            print("QQQ diff is ", diffQQQ, "going to do trade with ",
                  (round(diffQQQ/self.TAA.QQQp)*self.TAA.QQQp))
            if(diffQQQ > 0):
                self.adaptive_order_buy(TYCoContracts.USQQQAtSmart(),  round(
                    diffQQQ/self.TAA.QQQp), (self.TAA.QQQp*1.01))
            else:
                self.adaptive_order_sell(TYCoContracts.USQQQAtSmart(),  round(
                    diffQQQ/self.TAA.QQQp), (self.TAA.QQQp*0.99))

        targetEFA = kellerAllocation*kellerEFA
        diffEFA = targetEFA - (self.TAA.EFA*self.TAA.EFAp)
        print("EFA diff is ", diffEFA)
        if(abs(diffEFA) >= self.TAA.EFAp and self.TAA.EFAp != 0 and abs(diffEFA) > 100):
            print("EFA diff is ", diffEFA, "going to do trade with ",
                  (round(diffEFA/self.TAA.EFAp)*self.TAA.EFAp))
            if(diffEFA > 0):
                self.adaptive_order_buy(TYCoContracts.USEFAAtSmart(),  round(
                    diffEFA/self.TAA.EFAp), (self.TAA.EFAp*1.01))
            else:
                self.adaptive_order_sell(TYCoContracts.USEFAAtSmart(),  round(
                    diffEFA/self.TAA.EFAp), (self.TAA.EFAp*0.99))

        targetEEM = kellerAllocation*kellerEEM
        diffEEM = targetEEM - (self.TAA.EEM*self.TAA.EEMp)
        print("EEM diff is ", diffEEM)
        if(abs(diffEEM) >= self.TAA.EEMp and self.TAA.EEMp != 0 and abs(diffEEM) > 100):
            print("EEM diff is ", diffEEM, "going to do trade with ",
                  (round(diffEEM/self.TAA.EEMp)*self.TAA.EEMp))
            if(diffEEM > 0):
                self.adaptive_order_buy(TYCoContracts.USEEMAtSmart(),  round(
                    diffEEM/self.TAA.EEMp), (self.TAA.EEMp*1.01))
            else:
                self.adaptive_order_sell(TYCoContracts.USEEMAtSmart(),  round(
                    diffEEM/self.TAA.EEMp), (self.TAA.EEMp*0.99))

        targetEWJ = kellerAllocation*kellerEWJ
        diffEWJ = targetEWJ - (self.TAA.EWJ*self.TAA.EWJp)
        print("EWJ diff is ", diffEWJ)
        if(abs(diffEWJ) >= self.TAA.EWJp and self.TAA.EWJp != 0 and abs(diffEWJ) > 100):
            print("EWJ diff is ", diffEWJ, "going to do trade with ",
                  (round(diffEWJ/self.TAA.EWJp)*self.TAA.EWJp))
            if(diffEWJ > 0):
                self.adaptive_order_buy(TYCoContracts.USEWJAtSmart(),  round(
                    diffEWJ/self.TAA.EWJp), (self.TAA.EWJp*1.01))
            else:
                self.adaptive_order_sell(TYCoContracts.USEWJAtSmart(),  round(
                    diffEWJ/self.TAA.EWJp), (self.TAA.EWJp*0.99))

        targetIEF = (kellerAllocation*kellerIEF) + (StokenAllocation*StokenIEF)
        diffIEF = targetIEF - (self.TAA.IEF*self.TAA.IEFp)
        print("IEF diff is ", diffIEF)
        if(abs(diffIEF) >= self.TAA.IEFp and self.TAA.IEFp != 0 and abs(diffIEF) > 100):
            print("IEF diff is ", diffIEF, "going to do trade with ",
                  (round(diffIEF/self.TAA.IEFp)*self.TAA.IEFp))
            if(diffIEF > 0):
                self.adaptive_order_buy(TYCoContracts.USIEFAtSmart(),  round(
                    diffIEF/self.TAA.IEFp), (self.TAA.IEFp*1.01))
            else:
                self.adaptive_order_sell(TYCoContracts.USIEFAtSmart(),  round(
                    diffIEF/self.TAA.IEFp), (self.TAA.IEFp*0.99))

        targetHYG = kellerAllocation*kellerHYG
        diffHYG = targetHYG - (self.TAA.HYG*self.TAA.HYGp)
        print("HYG diff is ", diffHYG)
        if(abs(diffHYG) >= self.TAA.HYGp and self.TAA.HYGp != 0 and abs(diffHYG) > 100):
            print("HYG diff is ", diffHYG, "going to do trade with ",
                  (round(diffHYG/self.TAA.HYGp)*self.TAA.HYGp))
            if(diffHYG > 0):
                self.adaptive_order_buy(TYCoContracts.USHYGAtSmart(),  round(
                    diffHYG/self.TAA.HYGp), (self.TAA.HYGp*1.01))
            else:
                self.adaptive_order_sell(TYCoContracts.USHYGAtSmart(),  round(
                    diffHYG/self.TAA.HYGp), (self.TAA.HYGp*0.99))

        targetGLD = StokenAllocation*StokenGLD
        diffGLD = targetGLD - (self.TAA.GLD*self.TAA.GLDp)
        print("GLD diff is ", diffGLD)
        if(abs(diffGLD) >= self.TAA.GLDp and self.TAA.GLDp != 0 and abs(diffGLD) > 100):
            print("GLD diff is ", diffGLD, "going to do trade with ",
                  (round(diffGLD/self.TAA.GLDp)*self.TAA.GLDp))
            if(diffGLD > 0):
                self.adaptive_order_buy(TYCoContracts.USGLDAtSmart(),  round(
                    diffGLD/self.TAA.GLDp), (self.TAA.GLDp*1.01))
            else:
                self.adaptive_order_sell(TYCoContracts.USGLDAtSmart(),  round(
                    diffGLD/self.TAA.GLDp), (self.TAA.GLDp*0.99))

        targetTLT = StokenAllocation*StokenTLT
        diffTLT = targetTLT - (self.TAA.TLT*self.TAA.TLTp)
        print("TLT diff is ", diffTLT)
        if(abs(diffTLT) >= self.TAA.TLTp and self.TAA.TLTp != 0 and abs(diffTLT) > 100):
            print("TLT diff is ", diffTLT, "going to do trade with ",
                  (round(diffTLT/self.TAA.TLTp)*self.TAA.TLTp))
            if(diffTLT > 0):
                self.adaptive_order_buy(TYCoContracts.USTLTAtSmart(),  round(
                    diffTLT/self.TAA.TLTp), (self.TAA.TLTp*1.01))
            else:
                self.adaptive_order_sell(TYCoContracts.USTLTAtSmart(),  round(
                    diffTLT/self.TAA.TLTp), (self.TAA.TLTp*0.99))

        targetVNQ = StokenAllocation*StokenVNQ
        diffVNQ = targetVNQ - (self.TAA.VNQ*self.TAA.VNQp)
        print("VNQ diff is ", diffVNQ)
        if(abs(diffVNQ) >= self.TAA.VNQp and self.TAA.VNQp != 0 and abs(diffVNQ) > 100):
            print("VNQ diff is ", diffVNQ, "going to do trade with ",
                  (round(diffVNQ/self.TAA.VNQp)*self.TAA.VNQp))
            if(diffVNQ > 0):
                self.adaptive_order_buy(TYCoContracts.USVNQAtSmart(),  round(
                    diffVNQ/self.TAA.VNQp), (self.TAA.VNQp*1.01))
            else:
                self.adaptive_order_sell(TYCoContracts.USVNQAtSmart(),  round(
                    diffVNQ/self.TAA.VNQp), (self.TAA.VNQp*0.99))

        targetVEU = GEMAllocation*GEMVEU
        diffVEU = targetVEU - (self.TAA.VEU*self.TAA.VEUp)
        print("VEU diff is ", diffVEU)
        if(abs(diffVEU) >= self.TAA.VEUp and self.TAA.VEUp != 0 and abs(diffVEU) > 100):
            print("VEU diff is ", diffVEU, "going to do trade with ",
                  (round(diffVEU/self.TAA.VEUp)*self.TAA.VEUp))
            if(diffVEU > 0):
                self.adaptive_order_buy(TYCoContracts.USVEUAtSmart(),  round(
                    diffVEU/self.TAA.VEUp), (self.TAA.VEUp*1.01))
            else:
                self.adaptive_order_sell(TYCoContracts.USVEUAtSmart(),  round(
                    diffVEU/self.TAA.VEUp), (self.TAA.VEUp*0.99))

        targetBND = GEMAllocation*GEMBND
        diffBND = targetBND - (self.TAA.BND*self.TAA.BNDp)
        print("BND diff is ", diffBND)
        if(abs(diffBND) >= self.TAA.BNDp and self.TAA.BNDp != 0 and abs(diffBND) > 100):
            print("BND diff is ", diffBND, "going to do trade with ",
                  (round(diffBND/self.TAA.BNDp)*self.TAA.BNDp))
            if(diffBND > 0):
                self.adaptive_order_buy(TYCoContracts.USBNDAtSmart(),  round(
                    diffBND/self.TAA.BNDp), (self.TAA.BNDp*1.01))
            else:
                self.adaptive_order_sell(TYCoContracts.USBNDAtSmart(),  round(
                    diffBND/self.TAA.BNDp), (self.TAA.BNDp*0.99))

    def orderOperations_cancel(self):
        if self.simplePlaceOid is not None:
            # ! [cancelorder]
            self.cancelOrder(self.simplePlaceOid)
            # ! [cancelorder]

    @iswrapper
    # ! [execdetails]
    def execDetails(self, reqId: int, contract: Contract, execution: Execution):
        super().execDetails(reqId, contract, execution)
        print("ExecDetails. ", reqId, contract.symbol, contract.secType, contract.currency,
              execution.execId, execution.orderId, execution.shares, execution.lastLiquidity)

    # ! [execdetails]

    @iswrapper
    # ! [execdetailsend]
    def execDetailsEnd(self, reqId: int):
        super().execDetailsEnd(reqId)
        print("ExecDetailsEnd. ", reqId)

    # ! [execdetailsend]

    @iswrapper
    # ! [commissionreport]
    def commissionReport(self, commissionReport: CommissionReport):
        super().commissionReport(commissionReport)
        print("CommissionReport. ", commissionReport.execId, commissionReport.commission,
              commissionReport.currency, commissionReport.realizedPNL)
        # ! [commissionreport]


def main():
    SetupLogger()
    logging.debug("now is %s", datetime.datetime.now())
    logging.getLogger().setLevel(logging.ERROR)

    cmdLineParser = argparse.ArgumentParser("api tests")
    # cmdLineParser.add_option("-c", action="store_True", dest="use_cache", default = False, help = "use the cache")
    # cmdLineParser.add_option("-f", action="store", type="string", dest="file", default="", help="the input file")
    cmdLineParser.add_argument("-p", "--port", action="store", type=int,
                               dest="port", default=7497, help="The TCP port to use")
    cmdLineParser.add_argument("-C", "--global-cancel", action="store_true",
                               dest="global_cancel", default=False,
                               help="whether to trigger a globalCancel req")
    args = cmdLineParser.parse_args()
    print("Using args", args)
    logging.debug("Using args %s", args)
    # print(args)

    # enable logging when member vars are assigned
    from ibapi import utils
    from ibapi.order import Order
    Order.__setattr__ = utils.setattr_log
    from ibapi.contract import Contract, DeltaNeutralContract
    Contract.__setattr__ = utils.setattr_log
    DeltaNeutralContract.__setattr__ = utils.setattr_log
    from ibapi.tag_value import TagValue
    TagValue.__setattr__ = utils.setattr_log
    TimeCondition.__setattr__ = utils.setattr_log
    ExecutionCondition.__setattr__ = utils.setattr_log
    MarginCondition.__setattr__ = utils.setattr_log
    PriceCondition.__setattr__ = utils.setattr_log
    PercentChangeCondition.__setattr__ = utils.setattr_log
    VolumeCondition.__setattr__ = utils.setattr_log

    # from inspect import signature as sig
    # import code code.interact(local=dict(globals(), **locals()))
    # sys.exit(1)

    # tc = TestClient(None)
    # tc.reqMktData(1101, TYCoContracts.USStockAtSmart(), "", False, None)
    # print(tc.reqId2nReq)
    # sys.exit(1)

    try:
        app = TestApp()
        if args.global_cancel:
            app.globalCancelOnly = True
        # ! [connect]
        app.connect("127.0.0.1", args.port, clientId=0)
        # ! [connect]
        print("serverVersion:%s connectionTime:%s" % (app.serverVersion(),
                                                      app.twsConnectionTime()))

        # ! [clientrun]
        app.run()
        # ! [clientrun]
    except:
        raise
    finally:
        app.dumpTestCoverageSituation()
        app.dumpReqAnsErrSituation()


if __name__ == "__main__":
    main()
