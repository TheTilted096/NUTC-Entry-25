from enum import Enum
from collections import deque

from sklearn import linear_model
import numpy
import math

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

        self.ethcounter = 0 # so every 20, push data point to the DQ
        self.btccounter = 0
        self.ltccounter = 0

        self.feature1eth = 0 # ratio of sell ORDERS to total ORDERS
        self.feature2eth = 0 # total QUANTITY of all
        self.feature3eth = 0 # total QUANTITY of sell

        self.previousfeature1eth = 0
        self.previousfeature2eth = 0
        self.previousfeature3eth = 0

        self.feature1btc = 0
        self.feature2btc = 0
        self.feature3btc = 0

        self.feature1ltc = 0
        self.feature2ltc = 0
        self.feature3ltc = 0

        self.ethprice = None
        self.btcprice = None
        self.ltcprice = None

        self.ethfitter = linear_model.Lasso(alpha=0.1)
        self.btcfitter = linear_model.Lasso(alpha=0.1)
        self.ltcfitter = linear_model.Lasso(alpha=0.1)

        self.ethdata = deque(maxlen = 1000)
        self.ethlabel = deque(maxlen = 1000)

        self.amounteth = 0
        self.amountbtc = 0
        self.amountltc = 0
        self.amountcapital = 100000

        self.previous_eth_buy_id = None
        self.previous_eth_sell_id = None
        self.previous_btc_buy_id = None
        self.previous_btc_sell_id = None
        self.previous_ltc_buy_id = None
        self.previous_ltc_sell_id = None

    def on_trade_update(self, ticker: Ticker, side: Side, quantity: float, price: float) -> None:
        return
    def on_orderbook_update(
        self, ticker: Ticker, side: Side, quantity: float, price: float
    ) -> None:
        #print("thingy called with")
        if ticker == Ticker.ETH:
            #print("inner thingy called")
            self.orderbooketh.append((side, price, quantity))
            #print("appended")
            self.ethcounter += 1
            if len(self.orderbooketh) == 1000: # ensure there is at least 1000 in the buffer
                #print("got inside")
                self.ethprice = 0 
                for order in self.orderbooketh: # compute averages
                    self.feature1eth += (int(side.value)/1000)
                    self.feature2eth += int(quantity)
                    self.feature3eth += (int(side.value)*quantity)
                    self.ethprice += order[1]/1000.0 

                self.ethdata.append((self.feature1eth, self.feature2eth, self.feature3eth))
                self.ethlabel.append(self.ethprice)                    
                
                if self.ethcounter % 20 == 0: # on 20th update, place order         
                    #train model
                    print("inside batch")
                    self.ethfitter.fit(np.array(self.ethdata)[:980, :], np.array(self.ethlabel)[-980:])
                    print("after fit")
                    pred_market = self.ethfitter.predict(self.ethdata[-1]).item()
                    print("after pred")

                    pct_diff = 100 * (pred_market - self.ethprice) / self.ethprice
                    buy_price = (90+20/(1+math.exp(-0.25 * pct_diff)))/100.0 * self.ethprice
                    sell_price = (88+24/(1+math.exp(-0.25 * pct_diff)))/100.0 * self.ethprice
                    buy_quantity = (200/(1+math.exp(-0.25 * pct_diff))) * self.capital * 0.30 / buy_price
                    sell_quantity = (200/(1+math.exp(-0.25 * pct_diff))) * self.ethamount / sell_price

                    print("after calcs")

                    self.cancel_order(0, self.previous_eth_buy_id)
                    self.cancel_order(0, self.previous_eth_sell_id)
                    print("after cancels")

                    self.previous_eth_buy_id = place_limit_order(Side.BUY, Ticker.ETH, int(buy_quantity), buy_price)
                    self.previous_eth_sell_id = place_limit_order(Side.SELL, Ticker.ETH, int(sell_quantity), sell_price)
                    print("end")
        return
    

    def on_account_update(
        self,
        ticker: Ticker,
        side: Side,
        price: float,
        quantity: float,
        capital_remaining: float,
    ) -> None:
        self.capital = capital_remaining
        if ticker == Ticker.ETH:
            if side == Side.BUY:
                self.amounteth += quantity
            else:
                self.amounteth -= quantity

        return



        # actually increment amount variables