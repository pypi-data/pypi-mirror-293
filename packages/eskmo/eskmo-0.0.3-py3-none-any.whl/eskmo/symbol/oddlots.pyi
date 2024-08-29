from eskmo.base.mvtype import *
from eskmo.const.skcom import *
from eskmo.const.event import *
from eskmo.skcom.function import *
from _typeshed import Incomplete
from eskmo.base.extension import Extension as Extension
from eskmo.base.handler import APIHandler as APIHandler
from eskmo.base.subscribable import SubscribableInfo as SubscribableInfo, SymbolSubscribable as SymbolSubscribable
from eskmo.skcom.handler import SkcomHandler as SkcomHandler
from eskmo.symbol.position import StockPosition as StockPosition
from eskmo.symbol.stock import StockInfo as StockInfo, StockInfoHandler as StockInfoHandler
from eskmo.utils.logger import Logger as Logger
from eskmo.utils.misc import threadStart as threadStart, toDollar as toDollar
from eskmo.utils.thread import ThreadHandler as ThreadHandler

HANDLER_ODD_LOTS_INFO: str
RUNNER_TAG_ODD_LOTS: int

class OddLotsInfoHandler(StockInfoHandler):
    def __init__(self, trigger, defaultApi: Incomplete | None = None, page=...) -> None: ...

class OddLotsInfo(StockInfo):
    def __init__(self, handler: Incomplete | None = None, api: Incomplete | None = None, symbol: str = '', page=..., tag: str = '', name: str = '') -> None: ...
    def getOddLotsRunnerName(self): ...
    def callSkcomSubscribeBest5(self, pid, newPage): ...
    def callSkcomUnsubscribeBest5(self, pid): ...
    def callSkcomSubscribeQuote(self, pid, codes): ...
    def callSkcomUnsubscribeQuote(self, pid): ...
