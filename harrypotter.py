from enum import Enum
from collections import deque

class Side(Enum):
    BUY = 0
    SELL = 1

class Ticker(Enum):
    ETH = 0
    BTC = 1
    LTC = 2

def place_market_order(side: Side, ticker: Ticker, quantity: float) -> bool:
    return True

def place_limit_order(side: Side, ticker: Ticker, quantity: float, price: float, ioc: bool = False) -> int:
    return 0

def cancel_order(ticker: Ticker, order_id: int) -> bool:
    return True

# You can use print() and view the logs after sandbox run has completed
class Strategy:
    def __init__(self) -> None:
        self.orderbookbtc = deque(maxlen = 1000)
        self.orderbooketh = deque(maxlen = 1000)
        self.orderbookltc = deque(maxlen = 1000)
        self.ethcounter = 0
        self.btccounter = 0
        self.ltccounter = 0
        self.feature1eth = 0
        self.feature2eth = 0
        self.feature3eth = 0
        self.feature1btc = 0
        self.feature2btc = 0
        self.feature3btc = 0
        self.feature1ltc = 0
        self.feature2ltc = 0
        self.feature3ltc = 0
    def on_trade_update(self, ticker: Ticker, side: Side, quantity: float, price: float) -> None:
        pass
    def on_orderbook_update(
        self, ticker: Ticker, side: Side, quantity: float, price: float
    ) -> None:
        self.ethcounter += 1
        self.btccounter += 1
        self.ltccounter += 1
        if ticker == 0:
            self.orderbooketh.append((side, price, quantity))
            if len(self.orderbooketh) == 100:
                for order in self.orderbooketh:
                    self.feature1eth += (int(side)/10000)
        if ticker == 1:
            self.orderbookbtc.append((side, price, quantity))
            if len(self.orderbookbtc) == 100:
                for order in self.orderbookbtc:
                    self.feature1btc += (int(side)/10000)
        if ticker == 2:
            self.orderbookltc.append((side, price, quantity))
            if len(self.orderbookltc) == 100:
                for oder in self.orderbookltc:
                    self.feature1ltc += (int(side)/10000)
        if self.ethcounter % 20 == 0:
            pass
        if self.btccounter % 20 == 0:
            pass
        if self.ltccounter % 20 == 0:
            pass
    def on_account_update(
        self,
        ticker: Ticker,
        side: Side,
        price: float,
        quantity: float,
        capital_remaining: float,
    ) -> None:
      pass