
# -*- coding: utf-8 -*-
'''
Experiment: RealtimeAPI delay socket.io vs websocket.
- Socket.IO 2.0 (WebSocket)
- JSON-RPC 2.0 over WebSocket
'''
from time import sleep
from datetime import datetime
import concurrent.futures

from satrade.bitflyer.realtme import Subscriptions
from satrade.bitflyer.realtme import RealtimeAPI_SIO
from satrade.bitflyer.realtme import RealtimeAPI_WS

# callback pylint: disable-msg=unused-argument


def sio_on_message_executions(sio, pair, datas):
    '''callback for socket.io'''
    # print('sio', len(rdatas))
    update_data(0, datas)


def task_sio():
    '''task for socket.io'''
    sio_rtapi.start()


def web_on_message_executions(ws, pair, datas):
    '''callback for websocket'''
    # print('web', len(rdatas))
    update_data(1, datas)


def task_web():
    '''task for websocket'''
    ws_rtapi.start()


def update_data(idx, datas):
    'update data'
    now = datetime.now().timestamp()
    for ex in datas:
        if ex.order_id in rdatas:
            rdatas[ex.order_id][idx] = now
            rdatas[ex.order_id][2] = rdatas[ex.order_id][0] - rdatas[ex.order_id][1]
        else:
            rdatas[ex.order_id] = [None, None, None]
            rdatas[ex.order_id][idx] = now


subs = [Subscriptions.EXECUTIONS_FX_BTC_JPY]
sio_rtapi = RealtimeAPI_SIO(subs, on_message_executions=sio_on_message_executions)
ws_rtapi = RealtimeAPI_WS(subs, on_message_executions=web_on_message_executions)

rdatas = {}

if __name__ == '__main__':

    print('Start program.')
    executor = concurrent.futures.ThreadPoolExecutor()
    f_sio = executor.submit(task_sio)
    f_web = executor.submit(task_web)
    while True:
        try:
            sleep(1)
            print(len(rdatas))
        except KeyboardInterrupt:
            sio_rtapi.stop()
            ws_rtapi.stop()
            break

    f_sio.result(10)
    f_web.result(10)
    print('Generate csv.')
    fname = datetime.now().strftime('%Y%m%d%H%M%S') + '.csv'
    with open(fname, 'w') as fcsv:
        fcsv.write('order_id,socket.io,websocket,delta\n')
        for key, val in rdatas.items():
            if None not in val:
                wtxt = '{},{},{},{}\n'.format(key, str(val[0]), str(val[1]), str(val[2]))
            fcsv.write(wtxt)
    print('Finish program.')
