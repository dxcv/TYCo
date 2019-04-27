"""
Copyright (C) 2018 Interactive Brokers LLC. All rights reserved. This code is subject to the terms
and conditions of the IB API Non-Commercial License or the IB API Commercial License, as applicable.
"""

import sys
import argparse
import datetime
import collections
import inspect
import numpy as np

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
    def __init__(self):
        self.VOO = 0
        self.VOOp = 0
        self.QQQ = 0
        self.QQQp = 0
        self.EZU = 0
        self.EZUp = 0
        self.EFA = 0
        self.EFAp = 0
        self.EEM = 0
        self.EEMp = 0
        self.EWJ = 0
        self.EWJp = 0
        self.IEF = 0
        self.IEFp = 0
        self.HYG = 0
        self.HYGp = 0
        self.GLD = 0
        self.GLDp = 0
        self.TLT = 0
        self.TLTp = 0
        self.VNQ = 0
        self.VNQp = 0
        self.VEU = 0
        self.VEUp = 0
        self.VEA = 0
        self.VEAp = 0
        self.VWO = 0
        self.VWOp = 0
        self.BND = 0
        self.BNDp = 0
        self.SCZ = 0
        self.SCZp = 0
        self.DBC = 0
        self.DBCp = 0
        self.SHY = 0
        self.SHYp = 0
        self.LQD = 0
        self.LQDp = 0
        self.RWX = 0
        self.RWXp = 0
        self.trading = 0

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
        self.manual_update = 0
        self.price_method = 0
        self.real_trade = 0
        self.cash_overwrite = 0
        self.top_accests = 1
        self.TAA = TAA_struct()

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
    def historicalDataRequests_req(self):
        # Requesting historical data
        # ! [reqhistoricaldata]
        queryTime = datetime.datetime.today().strftime("%Y%m%d %H:%M:%S")
        print(" request VOO Historical Data ")
        self.reqHistoricalData(3000, TYCoContracts.USVOOAtNYSE(), queryTime,
                               "1 Y", "1 month", "MIDPOINT", 1, 1, False, [])
        self.reqHeadTimeStamp(
            4103, TYCoContracts.USVOOAtNYSE(), "TRADES", 0, 1)

    @printWhenExecuting
    def historicalDataRequests_cancel(self):
        # Canceling historical data requests
        self.cancelHistoricalData(3000)

    @iswrapper
    # ! [historicaldata]
    def historicalData(self, reqId: int, bar: BarData):
        print("HistoricalData. ", reqId, " Date:", bar.date, "Open:", bar.open,
              "High:", bar.high, "Low:", bar.low, "Close:", bar.close, "Volume:", bar.volume,
              "Count:", bar.barCount, "WAP:", bar.average)

    @iswrapper
    # ! [historicaldataend]
    def historicalDataEnd(self, reqId: int, start: str, end: str):
        super().historicalDataEnd(reqId, start, end)
        print("HistoricalDataEnd ", reqId, "from", start, "to", end)

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
        if(contract.symbol == "EZU"):
            self.TAA.EZU = position
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
        if(contract.symbol == "VEA"):
            self.TAA.VEA = position
        if(contract.symbol == "VWO"):
            self.TAA.VWO = position
        if(contract.symbol == "BND"):
            self.TAA.BND = position
        if(contract.symbol == "SCZ"):
            self.TAA.SCZ = position
        if(contract.symbol == "DBC"):
            self.TAA.DBC = position
        if(contract.symbol == "SHY"):
            self.TAA.SHY = position
        if(contract.symbol == "LQD"):
            self.TAA.LQD = position
        if(contract.symbol == "RWX"):
            self.TAA.RWX = position
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
        self.reqMktData(1012, TYCoContracts.USSCZAtSmart(),
                        "", False, False, [])
        self.reqMktData(1013, TYCoContracts.USDBCAtSmart(),
                        "", False, False, [])
        self.reqMktData(1014, TYCoContracts.USVEAAtSmart(),
                        "", False, False, [])
        self.reqMktData(1015, TYCoContracts.USVWOAtSmart(),
                        "", False, False, [])
        self.reqMktData(1016, TYCoContracts.USSHYAtSmart(),
                        "", False, False, [])
        self.reqMktData(1017, TYCoContracts.USLQDAtSmart(),
                        "", False, False, [])
        self.reqMktData(1018, TYCoContracts.USEZUAtSmart(),
                        "", False, False, [])
        self.reqMktData(1019, TYCoContracts.USRWXAtSmart(),
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
        if(reqId == 1012 and tickType == 66):
            self.TAA.SCZp = price
        if(reqId == 1013 and tickType == 66):
            self.TAA.DBCp = price
        if(reqId == 1014 and tickType == 66):
            self.TAA.VEAp = price
        if(reqId == 1015 and tickType == 66):
            self.TAA.VWOp = price
        if(reqId == 1016 and tickType == 66):
            self.TAA.SHYp = price
        if(reqId == 1017 and tickType == 66):
            self.TAA.LQDp = price
        if(reqId == 1018 and tickType == 66):
            self.TAA.EZUp = price
        if(reqId == 1019 and tickType == 66):
            self.TAA.RWXp = price

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
                self.TAA.SCZp != 0 and
                self.TAA.DBCp != 0 and
                self.TAA.VEAp != 0 and
                self.TAA.VWOp != 0 and
                self.TAA.SHYp != 0 and
                self.TAA.LQDp != 0 and
                self.TAA.EZUp != 0 and
                self.TAA.RWXp != 0 and
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

    def market_order_buy(self, contract, position, price):
        # ! [adaptive]

        print(" going to BUY ", contract.symbol, " position ", position, "at Market around ",
              TYCoAlgo.round_to_nth_digits_after_decimal_point_with_base_m(price, 2, 1))
        baseOrder = TYCoOrders.MarketOrder("BUY", position)
        if self.real_trade == '1':
            self.placeOrder(self.nextOrderId(), contract, baseOrder)
        # ! [adaptive]

    def market_order_sell(self, contract, position, price):
        # ! [adaptive]
        print(" going to SELL ", contract.symbol, " position ", position, "at Market around ",
              TYCoAlgo.round_to_nth_digits_after_decimal_point_with_base_m(price, 2, 1))
        baseOrder = TYCoOrders.MarketOrder("SELL", abs(position))
        if self.real_trade == '1':
            self.placeOrder(self.nextOrderId(), contract, baseOrder)
        # ! [adaptive]

    def adaptive_order_buy(self, contract, position, price):
        # ! [adaptive]
        print(" going to BUY ", contract.symbol, " position ", position, "at ",
              TYCoAlgo.round_to_nth_digits_after_decimal_point_with_base_m(price, 2, 1))
        baseOrder = TYCoOrders.LimitOrder(
            "BUY", position, TYCoAlgo.round_to_nth_digits_after_decimal_point_with_base_m(price, 2, 1))
        AvailableAlgoParams.FillAdaptiveParams(baseOrder, "Patient")
        if self.real_trade == '1':
            self.placeOrder(self.nextOrderId(), contract, baseOrder)
        # ! [adaptive]

    def adaptive_order_sell(self, contract, position, price):
        # ! [adaptive]
        print(" going to SELL ", contract.symbol, " position ", position, "at ",
              TYCoAlgo.round_to_nth_digits_after_decimal_point_with_base_m(price, 2, 1))
        baseOrder = TYCoOrders.LimitOrder(
            "SELL", abs(position), TYCoAlgo.round_to_nth_digits_after_decimal_point_with_base_m(price, 2, 1))
        AvailableAlgoParams.FillAdaptiveParams(baseOrder, "Patient")
        if self.real_trade == '1':
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
        self.cancelMktData(1012)
        self.cancelMktData(1013)
        self.cancelMktData(1014)
        self.cancelMktData(1015)
        self.cancelMktData(1016)
        self.cancelMktData(1017)
        self.cancelMktData(1018)
        self.cancelMktData(1019)
        time.sleep(5)
        # predefine allocation
        print('\n')
        print("manual update is ", self.manual_update)
        print("price method is ", self.price_method)
        print("real trade is ", self.real_trade)
        print("cash overwrite is ", self.cash_overwrite)
        '''
        # We could overwrite parameters here
        self.manual_update='0'
        self.price_method='0'
        self.real_trade='0'
        self.cash_overwrite='0'
        '''
        tradeThreshold = 666
        # Keller and Butler’s Vigilant Asset Allocation – G4 (VAA)
        VAAAllocation = 0
        if (self.manual_update == '1'):
            VAAVOO = 0
            VAAVEA = 0
            VAAVWO = 0
            VAABND = 0
            VAASHY = 0
            VAAIEF = 0
            VAALQD = 0
        else:
            VAA = TYCoAlgo.get_VAA_allocations(
                self.price_method, self.top_assets)
            VAAVOO = VAA[0]
            VAAVEA = VAA[1]
            VAAVWO = VAA[2]
            VAABND = VAA[3]
            if self.cash_overwrite == '1':
                VAASHY = 0
            else:
                VAASHY = VAA[4]
            VAAIEF = VAA[5]
            VAALQD = VAA[6]

        # Accelerating Dual Momentum (ADM)
        ADMAllocation = 0
        if (self.manual_update == '1'):
            ADMVOO = 0    # Use VOO to replace VFINX
            # Use SCZ to replace VINEX; Other alternative : SCHC , VSS , GWX ; VINEX only works for US resident.
            ADMSCZ = 0
            # Use TLT to replace VUSTX; Long-term Tressury might hurted by interesetd rate. Could consider replace with IEF or BND.
            ADMTLT = 0
        else:
            ADM = TYCoAlgo.get_ADM_allocations(self.price_method)
            ADMVOO = ADM[0]
            ADMSCZ = ADM[1]
            if self.cash_overwrite == '1':
                ADMTLT = 0
            else:
                ADMTLT = ADM[2]

        # Adaptive Asset Allocation: A Primer (AAA)
        AAAAllocation = 0
        if (self.manual_update == '1'):
            AAAVOO = 0
            AAAEZU = 0
            AAAEWJ = 0
            AAAEEM = 0
            AAAVNQ = 0
            AAARWX = 0
            AAAIEF = 0
            AAATLT = 0
            AAADBC = 0
            AAAGLD = 0
        else:
            AAA = TYCoAlgo.get_AAA_allocations()
            AAAVOO = AAA[0]
            AAAEZU = AAA[1]
            AAAEWJ = AAA[2]
            AAAEEM = AAA[3]
            AAAVNQ = AAA[4]
            AAARWX = AAA[5]
            AAAIEF = AAA[6]
            AAATLT = AAA[7]
            AAADBC = AAA[8]
            AAAGLD = AAA[9]

        # Ray Dalio’s All-Weather ( Fixed allocation )
        RDAWAllocation = 0
        # ( Fixed allocation )
        RDAWDBC = 0.075
        RDAWGLD = 0.075
        RDAWIEF = 0.15
        RDAWTLT = 0.4
        RDAWVOO = 0.3

        # GLOBAL EQUITIES MOMENTUM (GEM)
        GEMAllocation = 0
        if (self.manual_update == '1'):
            GEMVOO = 0
            GEMVEU = 0
            GEMBND = 0
        else:
            GEM = TYCoAlgo.get_GEM_allocations(self.price_method)
            GEMVOO = GEM[0]
            GEMVEU = GEM[1]
            if self.cash_overwrite == '1':
                GEMBND = 0
            else:
                GEMBND = GEM[2]

        # Only manual update available for "Keller and Butler’s Elastic Asset Allocation"
        # Keller and Butler’s Elastic Asset Allocation 
        kellerAllocation = 0
        kellerVOO = 0
        kellerQQQ = 0
        kellerEFA = 0
        kellerEEM = 0
        kellerEWJ = 0
        kellerIEF = 0
        kellerHYG = 0

        targetVOO = (kellerAllocation * kellerVOO) +
        (GEMAllocation*GEMVOO) + (ADMAllocation*ADMVOO) + (RDAWAllocation *
                                                           RDAWVOO) + (VAAAllocation*VAAVOO) + (AAAAllocation*AAAVOO)
        diffVOO = targetVOO - (self.TAA.VOO*self.TAA.VOOp)
        print("VOO diff is ", diffVOO)
        if(abs(diffVOO) >= self.TAA.VOOp and self.TAA.VOOp != 0 and abs(diffVOO) > tradeThreshold):
            print("VOO diff is ", diffVOO, "going to do trade with ",
                  (round(diffVOO/self.TAA.VOOp)*self.TAA.VOOp))
            if(diffVOO > 0):
                self.adaptive_order_buy(TYCoContracts.USVOOAtSmart(),  round(
                    diffVOO/self.TAA.VOOp), (self.TAA.VOOp*1.005))
            else:
                self.adaptive_order_sell(TYCoContracts.USVOOAtSmart(),  round(
                    diffVOO/self.TAA.VOOp), (self.TAA.VOOp*0.995))

        targetEZU = (AAAAllocation*AAAEZU)
        diffEZU = targetEZU - (self.TAA.EZU*self.TAA.EZUp)
        print("EZU diff is ", diffEZU)
        if(abs(diffEZU) >= self.TAA.EZUp and self.TAA.EZUp != 0 and abs(diffEZU) > tradeThreshold):
            print("EZU diff is ", diffEZU, "going to do trade with ",
                  (round(diffEZU/self.TAA.EZUp)*self.TAA.EZUp))
            if(diffEZU > 0):
                self.adaptive_order_buy(TYCoContracts.USEZUAtSmart(),  round(
                    diffEZU/self.TAA.EZUp), (self.TAA.EZUp*1.005))
            else:
                self.adaptive_order_sell(TYCoContracts.USEZUAtSmart(),  round(
                    diffEZU/self.TAA.EZUp), (self.TAA.EZUp*0.995))

        targetRWX = (AAAAllocation*AAARWX)
        diffRWX = targetRWX - (self.TAA.RWX*self.TAA.RWXp)
        print("RWX diff is ", diffRWX)
        if(abs(diffRWX) >= self.TAA.RWXp and self.TAA.RWXp != 0 and abs(diffRWX) > tradeThreshold):
            print("RWX diff is ", diffRWX, "going to do trade with ",
                  (round(diffRWX/self.TAA.RWXp)*self.TAA.RWXp))
            if(diffRWX > 0):
                self.adaptive_order_buy(TYCoContracts.USRWXAtSmart(),  round(
                    diffRWX/self.TAA.RWXp), (self.TAA.RWXp*1.005))
            else:
                self.adaptive_order_sell(TYCoContracts.USRWXAtSmart(),  round(
                    diffRWX/self.TAA.RWXp), (self.TAA.RWXp*0.995))

        targetQQQ = (kellerAllocation*kellerQQQ)
        diffQQQ = targetQQQ - (self.TAA.QQQ*self.TAA.QQQp)
        print("QQQ diff is ", diffQQQ)
        if(abs(diffQQQ) >= self.TAA.QQQp and self.TAA.QQQp != 0 and abs(diffQQQ) > tradeThreshold):
            print("QQQ diff is ", diffQQQ, "going to do trade with ",
                  (round(diffQQQ/self.TAA.QQQp)*self.TAA.QQQp))
            if(diffQQQ > 0):
                self.adaptive_order_buy(TYCoContracts.USQQQAtSmart(),  round(
                    diffQQQ/self.TAA.QQQp), (self.TAA.QQQp*1.005))
            else:
                self.adaptive_order_sell(TYCoContracts.USQQQAtSmart(),  round(
                    diffQQQ/self.TAA.QQQp), (self.TAA.QQQp*0.995))

        targetEFA = (kellerAllocation*kellerEFA)
        diffEFA = targetEFA - (self.TAA.EFA*self.TAA.EFAp)
        print("EFA diff is ", diffEFA)
        if(abs(diffEFA) >= self.TAA.EFAp and self.TAA.EFAp != 0 and abs(diffEFA) > tradeThreshold):
            print("EFA diff is ", diffEFA, "going to do trade with ",
                  (round(diffEFA/self.TAA.EFAp)*self.TAA.EFAp))
            if(diffEFA > 0):
                self.adaptive_order_buy(TYCoContracts.USEFAAtSmart(),  round(
                    diffEFA/self.TAA.EFAp), (self.TAA.EFAp*1.005))
            else:
                self.adaptive_order_sell(TYCoContracts.USEFAAtSmart(),  round(
                    diffEFA/self.TAA.EFAp), (self.TAA.EFAp*0.995))

        targetEEM = (kellerAllocation*kellerEEM)+(AAAAllocation*AAAEEM)
        diffEEM = targetEEM - (self.TAA.EEM*self.TAA.EEMp)
        print("EEM diff is ", diffEEM)
        if(abs(diffEEM) >= self.TAA.EEMp and self.TAA.EEMp != 0 and abs(diffEEM) > tradeThreshold):
            print("EEM diff is ", diffEEM, "going to do trade with ",
                  (round(diffEEM/self.TAA.EEMp)*self.TAA.EEMp))
            if(diffEEM > 0):
                self.adaptive_order_buy(TYCoContracts.USEEMAtSmart(),  round(
                    diffEEM/self.TAA.EEMp), (self.TAA.EEMp*1.005))
            else:
                self.adaptive_order_sell(TYCoContracts.USEEMAtSmart(),  round(
                    diffEEM/self.TAA.EEMp), (self.TAA.EEMp*0.995))

        targetEWJ = (kellerAllocation*kellerEWJ) + (AAAAllocation*AAAEWJ)
        diffEWJ = targetEWJ - (self.TAA.EWJ*self.TAA.EWJp)
        print("EWJ diff is ", diffEWJ)
        if(abs(diffEWJ) >= self.TAA.EWJp and self.TAA.EWJp != 0 and abs(diffEWJ) > tradeThreshold):
            print("EWJ diff is ", diffEWJ, "going to do trade with ",
                  (round(diffEWJ/self.TAA.EWJp)*self.TAA.EWJp))
            if(diffEWJ > 0):
                self.adaptive_order_buy(TYCoContracts.USEWJAtSmart(),  round(
                    diffEWJ/self.TAA.EWJp), (self.TAA.EWJp*1.005))
            else:
                self.adaptive_order_sell(TYCoContracts.USEWJAtSmart(),  round(
                    diffEWJ/self.TAA.EWJp), (self.TAA.EWJp*0.995))

        targetIEF = (kellerAllocation*kellerIEF) + (RDAWAllocation*RDAWIEF) + \
            (VAAAllocation*VAAIEF) + (AAAAllocation*AAAIEF)
        diffIEF = targetIEF - (self.TAA.IEF*self.TAA.IEFp)
        print("IEF diff is ", diffIEF)
        if(abs(diffIEF) >= self.TAA.IEFp and self.TAA.IEFp != 0 and abs(diffIEF) > tradeThreshold):
            print("IEF diff is ", diffIEF, "going to do trade with ",
                  (round(diffIEF/self.TAA.IEFp)*self.TAA.IEFp))
            if(diffIEF > 0):
                self.adaptive_order_buy(TYCoContracts.USIEFAtSmart(),  round(
                    diffIEF/self.TAA.IEFp), (self.TAA.IEFp*1.005))
            else:
                self.adaptive_order_sell(TYCoContracts.USIEFAtSmart(),  round(
                    diffIEF/self.TAA.IEFp), (self.TAA.IEFp*0.995))

        targetHYG = (kellerAllocation*kellerHYG)
        diffHYG = targetHYG - (self.TAA.HYG*self.TAA.HYGp)
        print("HYG diff is ", diffHYG)
        if(abs(diffHYG) >= self.TAA.HYGp and self.TAA.HYGp != 0 and abs(diffHYG) > tradeThreshold):
            print("HYG diff is ", diffHYG, "going to do trade with ",
                  (round(diffHYG/self.TAA.HYGp)*self.TAA.HYGp))
            if(diffHYG > 0):
                self.adaptive_order_buy(TYCoContracts.USHYGAtSmart(),  round(
                    diffHYG/self.TAA.HYGp), (self.TAA.HYGp*1.005))
            else:
                self.adaptive_order_sell(TYCoContracts.USHYGAtSmart(),  round(
                    diffHYG/self.TAA.HYGp), (self.TAA.HYGp*0.995))

        targetGLD = (RDAWGLD*RDAWAllocation) + (AAAAllocation*AAAGLD)
        diffGLD = targetGLD - (self.TAA.GLD*self.TAA.GLDp)
        print("GLD diff is ", diffGLD)
        if(abs(diffGLD) >= self.TAA.GLDp and self.TAA.GLDp != 0 and abs(diffGLD) > tradeThreshold):
            print("GLD diff is ", diffGLD, "going to do trade with ",
                  (round(diffGLD/self.TAA.GLDp)*self.TAA.GLDp))
            if(diffGLD > 0):
                self.market_order_buy(TYCoContracts.USGLDAtSmart(),  round(
                    diffGLD/self.TAA.GLDp), (self.TAA.GLDp*1.005))
            else:
                self.market_order_sell(TYCoContracts.USGLDAtSmart(),  round(
                    diffGLD/self.TAA.GLDp), (self.TAA.GLDp*0.995))

        targetTLT = (ADMAllocation*ADMTLT) + \
            (RDAWAllocation*RDAWTLT) + (AAAAllocation*AAATLT)
        diffTLT = targetTLT - (self.TAA.TLT*self.TAA.TLTp)
        print("TLT diff is ", diffTLT)
        if(abs(diffTLT) >= self.TAA.TLTp and self.TAA.TLTp != 0 and abs(diffTLT) > tradeThreshold):
            print("TLT diff is ", diffTLT, "going to do trade with ",
                  (round(diffTLT/self.TAA.TLTp)*self.TAA.TLTp))
            if(diffTLT > 0):
                self.adaptive_order_buy(TYCoContracts.USTLTAtSmart(),  round(
                    diffTLT/self.TAA.TLTp), (self.TAA.TLTp*1.005))
            else:
                self.adaptive_order_sell(TYCoContracts.USTLTAtSmart(),  round(
                    diffTLT/self.TAA.TLTp), (self.TAA.TLTp*0.995))

        targetVNQ = (AAAAllocation*AAAVNQ)
        diffVNQ = targetVNQ - (self.TAA.VNQ*self.TAA.VNQp)
        print("VNQ diff is ", diffVNQ)
        if(abs(diffVNQ) >= self.TAA.VNQp and self.TAA.VNQp != 0 and abs(diffVNQ) > tradeThreshold):
            print("VNQ diff is ", diffVNQ, "going to do trade with ",
                  (round(diffVNQ/self.TAA.VNQp)*self.TAA.VNQp))
            if(diffVNQ > 0):
                self.adaptive_order_buy(TYCoContracts.USVNQAtSmart(),  round(
                    diffVNQ/self.TAA.VNQp), (self.TAA.VNQp*1.005))
            else:
                self.adaptive_order_sell(TYCoContracts.USVNQAtSmart(),  round(
                    diffVNQ/self.TAA.VNQp), (self.TAA.VNQp*0.995))

        targetVEU = (GEMAllocation*GEMVEU)
        diffVEU = targetVEU - (self.TAA.VEU*self.TAA.VEUp)
        print("VEU diff is ", diffVEU)
        if(abs(diffVEU) >= self.TAA.VEUp and self.TAA.VEUp != 0 and abs(diffVEU) > tradeThreshold):
            print("VEU diff is ", diffVEU, "going to do trade with ",
                  (round(diffVEU/self.TAA.VEUp)*self.TAA.VEUp))
            if(diffVEU > 0):
                self.adaptive_order_buy(TYCoContracts.USVEUAtSmart(),  round(
                    diffVEU/self.TAA.VEUp), (self.TAA.VEUp*1.005))
            else:
                self.adaptive_order_sell(TYCoContracts.USVEUAtSmart(),  round(
                    diffVEU/self.TAA.VEUp), (self.TAA.VEUp*0.995))

        targetVEA = (VAAAllocation*VAAVEA)
        diffVEA = targetVEA - (self.TAA.VEA*self.TAA.VEAp)
        print("VEA diff is ", diffVEA)
        if(abs(diffVEA) >= self.TAA.VEAp and self.TAA.VEAp != 0 and abs(diffVEA) > tradeThreshold):
            print("VEA diff is ", diffVEA, "going to do trade with ",
                  (round(diffVEA/self.TAA.VEAp)*self.TAA.VEAp))
            if(diffVEA > 0):
                self.adaptive_order_buy(TYCoContracts.USVEAAtSmart(),  round(
                    diffVEA/self.TAA.VEAp), (self.TAA.VEAp*1.005))
            else:
                self.adaptive_order_sell(TYCoContracts.USVEAAtSmart(),  round(
                    diffVEA/self.TAA.VEAp), (self.TAA.VEAp*0.995))

        targetVWO = (VAAAllocation*VAAVWO)
        diffVWO = targetVWO - (self.TAA.VWO*self.TAA.VWOp)
        print("VWO diff is ", diffVWO)
        if(abs(diffVWO) >= self.TAA.VWOp and self.TAA.VWOp != 0 and abs(diffVWO) > tradeThreshold):
            print("VWO diff is ", diffVWO, "going to do trade with ",
                  (round(diffVWO/self.TAA.VWOp)*self.TAA.VWOp))
            if(diffVWO > 0):
                self.adaptive_order_buy(TYCoContracts.USVWOAtSmart(),  round(
                    diffVWO/self.TAA.VWOp), (self.TAA.VWOp*1.005))
            else:
                self.adaptive_order_sell(TYCoContracts.USVWOAtSmart(),  round(
                    diffVWO/self.TAA.VWOp), (self.TAA.VWOp*0.995))

        targetSHY = (VAAAllocation*VAASHY)
        diffSHY = targetSHY - (self.TAA.SHY*self.TAA.SHYp)
        print("SHY diff is ", diffSHY)
        if(abs(diffSHY) >= self.TAA.SHYp and self.TAA.SHYp != 0 and abs(diffSHY) > tradeThreshold):
            print("SHY diff is ", diffSHY, "going to do trade with ",
                  (round(diffSHY/self.TAA.SHYp)*self.TAA.SHYp))
            if(diffSHY > 0):
                self.adaptive_order_buy(TYCoContracts.USSHYAtSmart(),  round(
                    diffSHY/self.TAA.SHYp), (self.TAA.SHYp*1.005))
            else:
                self.adaptive_order_sell(TYCoContracts.USSHYAtSmart(),  round(
                    diffSHY/self.TAA.SHYp), (self.TAA.SHYp*0.995))

        targetLQD = (VAAAllocation*VAALQD)
        diffLQD = targetLQD - (self.TAA.LQD*self.TAA.LQDp)
        print("LQD diff is ", diffLQD)
        if(abs(diffLQD) >= self.TAA.LQDp and self.TAA.LQDp != 0 and abs(diffLQD) > tradeThreshold):
            print("LQD diff is ", diffLQD, "going to do trade with ",
                  (round(diffLQD/self.TAA.LQDp)*self.TAA.LQDp))
            if(diffLQD > 0):
                self.adaptive_order_buy(TYCoContracts.USLQDAtSmart(),  round(
                    diffLQD/self.TAA.LQDp), (self.TAA.LQDp*1.005))
            else:
                self.adaptive_order_sell(TYCoContracts.USLQDAtSmart(),  round(
                    diffLQD/self.TAA.LQDp), (self.TAA.LQDp*0.995))

        targetBND = (GEMAllocation*GEMBND) + (VAAAllocation*VAABND)
        diffBND = targetBND - (self.TAA.BND*self.TAA.BNDp)
        print("BND diff is ", diffBND)
        if(abs(diffBND) >= self.TAA.BNDp and self.TAA.BNDp != 0 and abs(diffBND) > tradeThreshold):
            print("BND diff is ", diffBND, "going to do trade with ",
                  (round(diffBND/self.TAA.BNDp)*self.TAA.BNDp))
            if(diffBND > 0):
                self.adaptive_order_buy(TYCoContracts.USBNDAtSmart(),  round(
                    diffBND/self.TAA.BNDp), (self.TAA.BNDp*1.005))
            else:
                self.adaptive_order_sell(TYCoContracts.USBNDAtSmart(),  round(
                    diffBND/self.TAA.BNDp), (self.TAA.BNDp*0.995))

        targetSCZ = (ADMAllocation*ADMSCZ)
        diffSCZ = targetSCZ - (self.TAA.SCZ*self.TAA.SCZp)
        print("SCZ diff is ", diffSCZ)
        if(abs(diffSCZ) >= self.TAA.SCZp and self.TAA.SCZp != 0 and abs(diffSCZ) > tradeThreshold):
            print("SCZ diff is ", diffSCZ, "going to do trade with ",
                  (round(diffSCZ/self.TAA.SCZp)*self.TAA.SCZp))
            if(diffSCZ > 0):
                self.adaptive_order_buy(TYCoContracts.USSCZAtSmart(),  round(
                    diffSCZ/self.TAA.SCZp), (self.TAA.SCZp*1.005))
            else:
                self.adaptive_order_sell(TYCoContracts.USSCZAtSmart(),  round(
                    diffSCZ/self.TAA.SCZp), (self.TAA.SCZp*0.995))

        targetDBC = (RDAWAllocation*RDAWDBC)+(AAAAllocation*AAADBC)
        diffDBC = targetDBC - (self.TAA.DBC*self.TAA.DBCp)
        print("DBC diff is ", diffDBC)
        if(abs(diffDBC) >= self.TAA.DBCp and self.TAA.DBCp != 0 and abs(diffDBC) > tradeThreshold):
            print("DBC diff is ", diffDBC, "going to do trade with ",
                  (round(diffDBC/self.TAA.DBCp)*self.TAA.DBCp))
            if(diffDBC > 0):
                self.adaptive_order_buy(TYCoContracts.USDBCAtSmart(),  round(
                    diffDBC/self.TAA.DBCp), (self.TAA.DBCp*1.005))
            else:
                self.adaptive_order_sell(TYCoContracts.USDBCAtSmart(),  round(
                    diffDBC/self.TAA.DBCp), (self.TAA.DBCp*0.995))

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
    cmdLineParser.add_argument(
        "-manual", nargs='?', default='0', help='whether to update price manually')
    cmdLineParser.add_argument("-price", nargs='?', default='0',
                               help='0 to choose end of month price; 1 to choose average price of a month')
    cmdLineParser.add_argument("-real", nargs='?', default='0',
                               help='1 to conduct real trade; 0 to see calculation result ')
    cmdLineParser.add_argument("-cash", nargs='?', default='0',
                               help='1 to use cash for crash protection; 0 to use default asset ')
    cmdLineParser.add_argument("-T", "--top", action="store", type=int,
                               dest="top", default=1, help="Choose the number of top assets to trade")

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
        app.manual_update = args.manual
        app.price_method = args.price
        app.real_trade = args.real
        app.cash_overwrite = args.cash
        app.top_assets = args.top

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
