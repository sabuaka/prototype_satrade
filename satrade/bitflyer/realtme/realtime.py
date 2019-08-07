# -*- coding: utf-8 -*-
'''(Abstract)Realtime API for bitFlyer'''

from enum import Enum
from types import DynamicClassAttribute

# pylint: disable=too-few-public-methods
# pylint: disable=too-many-instance-attributes


class Pairs(Enum):
    '''trade pair enumeration'''
    BTC_JPY = 'BTC_JPY'
    FX_BTC_JPY = 'FX_BTC_JPY'


class Channels(Enum):
    '''channel enumeration'''
    BOARD_SNAPSHOT = 'lightning_board_snapshot'
    BOARD = 'lightning_board'
    TICKER = 'lightning_ticker'
    EXECUTIONS = 'lightning_executions'


class Subscriptions(Enum):
    '''Subscription channels'''
    # for BTC_JPY
    BOARD_SNAPSHOT_BTC_JPY = (Channels.BOARD_SNAPSHOT, Pairs.BTC_JPY)
    BOARD_BTC_JPY = (Channels.BOARD, Pairs.BTC_JPY)
    TICKER_BTC_JPY = (Channels.TICKER, Pairs.BTC_JPY)
    EXECUTIONS_BTC_JPY = (Channels.EXECUTIONS, Pairs.BTC_JPY)
    # for FX_BTC_JPY
    BOARD_SNAPSHOT_FX_BTC_JPY = (Channels.BOARD_SNAPSHOT, Pairs.FX_BTC_JPY)
    BOARD_FX_BTC_JPY = (Channels.BOARD, Pairs.FX_BTC_JPY)
    TICKER_FX_BTC_JPY = (Channels.TICKER, Pairs.FX_BTC_JPY)
    EXECUTIONS_FX_BTC_JPY = (Channels.EXECUTIONS, Pairs.FX_BTC_JPY)

    @DynamicClassAttribute
    def subscription(self):
        '''return string for subscribe'''
        vals = list(self.value)
        return vals[0].value + '_' + vals[1].value

    @DynamicClassAttribute
    def channel(self):
        '''return member in Channels'''
        vals = list(self.value)
        return vals[0]

    @DynamicClassAttribute
    def pair(self):
        '''return member in Channels'''
        vals = list(self.value)
        return vals[1]


class BoardData():
    '''board data class for callback'''
    def __init__(self, msg):
        self.mid_price = msg['mid_price']
        self.bids = msg['bids']
        self.asks = msg['asks']


class TickerData():
    '''ticker data class for callback'''
    def __init__(self, msg):
        self.product_code = msg['product_code']
        self.timestamp = msg['timestamp']
        self.tick_id = msg['tick_id']
        self.best_bid = msg['best_bid']
        self.best_ask = msg['best_ask']
        self.best_bid_size = msg['best_bid_size']
        self.best_ask_size = msg['best_ask_size']
        self.total_bid_depth = msg['total_bid_depth']
        self.total_ask_depth = msg['total_ask_depth']
        self.ltp = msg['ltp']
        self.volume = msg['volume']
        self.volume_by_product = msg['volume_by_product']


class ExecutionData():
    '''executions data class for callback'''
    def __init__(self, msg):
        self.order_id = msg['id']
        self.side = msg['side']
        self.price = msg['price']
        self.size = msg['size']
        self.exec_date = msg['exec_date']
        self.buy_child_order_acceptance_id = \
            msg['buy_child_order_acceptance_id']
        self.sell_child_order_acceptance_id = \
            msg['sell_child_order_acceptance_id']


class RealtimeAPI():
    '''
    (Abstract)root class for RealtimeAPI
    '''

    def __init__(self,
                 subscriptions,
                 *,
                 on_message=None,
                 on_message_board=None,
                 on_message_board_snapshot=None,
                 on_message_ticker=None,
                 on_message_executions=None):

        # callback
        self.__cb_on_message = on_message
        self.__cb_on_message_board = on_message_board
        self.__cb_on_message_board_snapshot = on_message_board_snapshot
        self.__cb_on_message_ticker = on_message_ticker
        self.__cb_on_message_executions = on_message_executions

        # subscription channels
        self._subscriptions = []
        for sub in subscriptions:
            self._subscriptions.append(sub)

    def _on_message(self, pair, channel, message):
        self._callback(self.__cb_on_message, pair, channel, message)

    def _on_message_board_snapshot(self, pair, message):
        self._on_message(pair, Channels.BOARD_SNAPSHOT, message)

        data = BoardData(message)
        self._callback(self.__cb_on_message_board_snapshot, pair, data)

    def _on_message_board(self, pair, message):
        self._on_message(pair, Channels.BOARD, message)

        data = BoardData(message)
        self._callback(self.__cb_on_message_board, pair, data)

    def _on_message_ticker(self, pair, message):
        self._on_message(pair, Channels.TICKER, message)

        data = TickerData(message)
        self._callback(self.__cb_on_message_ticker, pair, data)

    def _on_message_executions(self, pair, message):
        self._on_message(pair, Channels.EXECUTIONS, message)

        data_list = []
        for execution in message:
            data = ExecutionData(execution)
            data_list.append(data)
        self._callback(self.__cb_on_message_executions, pair, data_list)

    def _callback(self, callback, *args):
        if callback:
            try:
                callback(self, *args)
            except:
                import traceback
                traceback.print_exc()
