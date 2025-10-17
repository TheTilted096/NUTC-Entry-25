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
        self.orderbook1 = deque(maxlen = 10000)
        self.orderbook2 = deque(maxlen = 10000)
        self.orderbook3 = deque(maxlen = 10000)
    def on_trade_update(self, ticker: Ticker, side: Side, quantity: float, price: float) -> None:
        pass
    def on_orderbook_update(
        self, ticker: Ticker, side: Side, quantity: float, price: float
    ) -> None:
        if ticker == 1:
            self.orderbook1.append((side, price, quantity))
        if ticker == 2:
            self.orderbook2.append((side, price, quantity))
        if ticker == 3:
            self.orderbook3.append((side, price, quantity))
    def on_account_update(
        self,
        ticker: Ticker,
        side: Side,
        price: float,
        quantity: float,
        capital_remaining: float,
    ) -> None:
      pass