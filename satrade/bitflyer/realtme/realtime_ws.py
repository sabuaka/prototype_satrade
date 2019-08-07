# -*- coding: utf-8 -*-
'''Realtime API for bitFlyer by JSON-RPC 2.0 over WebSocket'''

import json
import websocket

from .realtime import RealtimeAPI, Subscriptions, Channels


class RealtimeAPI_WS(RealtimeAPI):
    '''
    Realtime API for bitFlyer by JSON-RPC 2.0 over WebSocket

    *** The description of callback ***
    on_message and on_close are normal callbacks from websocket.
    on_message_board, on_message_board_snapshot, on_message_ticker
    and on_message_executions are special callbacks created
    by parsing message.
    '''

    CONNECTION_URL = 'wss://ws.lightstream.bitflyer.com/json-rpc'

    def __init__(self,
                 subscriptions,
                 *,
                 on_message=None,
                 on_message_board=None,
                 on_message_board_snapshot=None,
                 on_message_ticker=None,
                 on_message_executions=None,
                 on_close=None,
                 on_error=None,
                 ping_interval=30,  # sec
                 ping_timeout=10):  # sec

        super().__init__(subscriptions,
                         on_message=on_message,
                         on_message_board=on_message_board,
                         on_message_board_snapshot=on_message_board_snapshot,
                         on_message_ticker=on_message_ticker,
                         on_message_executions=on_message_executions)

        # additional callbacks
        self.__cb_on_close = on_close
        self.__cb_on_error = on_error

        # websocket
        self.__ws = None
        self.__ws_ping_interval = ping_interval
        self.__ws_ping_timeout = ping_timeout

    def __ws_on_open(self, ws):
        for sub in self._subscriptions:
            ws.send(json.dumps({'method': 'subscribe', 'params': {'channel': sub.subscription}}))

    def __ws_on_message(self, _, message):

        json_message = json.loads(message)
        if json_message['method'] != 'channelMessage':
            return

        # parse message
        parsed_params = json_message['params']
        parsed_channel = parsed_params['channel']
        parsed_message = parsed_params['message']

        def _parse_str_ch(str_ch):
            for sub in Subscriptions:
                if str_ch == sub.subscription:
                    return sub.channel, sub.pair
            return None, None

        ch, pair = _parse_str_ch(parsed_channel)
        if None in (ch, pair):
            return

        # callback
        if ch == Channels.BOARD_SNAPSHOT:
            self._on_message_board_snapshot(pair, parsed_message)
        elif ch == Channels.BOARD:
            self._on_message_board(pair, parsed_message)
        elif ch == Channels.TICKER:
            self._on_message_ticker(pair, parsed_message)
        elif ch == Channels.EXECUTIONS:
            self._on_message_executions(pair, parsed_message)

    def __ws_on_close(self, _, *close_args):
        self._callback(self.__cb_on_close, *close_args)

    def __ws_on_error(self, _, e):
        self._callback(self.__cb_on_error, e)

    def start(self):
        '''start listening'''
        if self.__ws is not None:
            self.stop()

        self.__ws = websocket.WebSocketApp(self.CONNECTION_URL,
                                           on_message=self.__ws_on_message,
                                           on_open=self.__ws_on_open,
                                           on_close=self.__ws_on_close,
                                           on_error=self.__ws_on_error)
        self.__ws.run_forever(ping_interval=self.__ws_ping_interval,
                              ping_timeout=self.__ws_ping_timeout)

    def stop(self):
        '''stop listening'''
        if self.__ws is not None:
            self.__ws.close()
        self.__ws = None
