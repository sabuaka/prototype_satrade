'''Test realtime API module for bitFlyer'''
import builtins as __builtin__

from satrade.bitflyer.realtme import Subscriptions
# from satrade.bitflyer.realtme import RealtimeAPI_SIO as RealtimeAPI
from satrade.bitflyer.realtme import RealtimeAPI_WS as RealtimeAPI


def print(*args, **kwargs):  # override pylint: disable-msg=W0622
    '''override print'''
    kwargs['end'] = '\r\n'
    return __builtin__.print(*args, **kwargs)


def on_message(_, pair, channel, message):
    '''test on_message callback'''
    print('pair=', pair)
    print(channel)
    print(message, type(message))


def on_message_board(_, pair, data):
    '''test on_message_board callback'''
    print('pair=', pair)
    print('mid_price=' + str(data.mid_price))
    print('asks=' + str(data.asks))
    print('bids=' + str(data.bids))


def on_message_board_snapshot(_, pair, data):
    '''test on_message callback'''
    print('pair=', pair)
    print('mid_price=' + str(data.mid_price))
    print('asks=' + str(data.asks))
    print('bids=' + str(data.bids))


def on_message_ticker(_, pair, data):
    '''test on_message_board_snapshot callback'''
    print('pair=', pair)
    print('product_code=' + str(data.product_code) + ' type=' + str(type(data.product_code)))
    print('timestamp=' + str(data.timestamp) + ' type=' + str(type(data.timestamp)))
    print('tick_id=' + str(data.tick_id) + ' type=' + str(type(data.tick_id)))
    print('best_bid=' + str(data.best_bid) + ' type=' + str(type(data.best_bid)))
    print('best_ask=' + str(data.best_ask) + ' type=' + str(type(data.best_ask)))
    print('best_bid_size=' + str(data.best_bid_size) + ' type=' + str(type(data.best_bid_size)))
    print('best_ask_size=' + str(data.best_ask_size) + ' type=' + str(type(data.best_ask_size)))
    print('total_bid_depth=' + str(data.total_bid_depth) + ' type=' + str(type(data.total_bid_depth)))
    print('total_ask_depth=' + str(data.total_ask_depth) + ' type=' + str(type(data.total_ask_depth)))
    print('ltp=' + str(data.ltp) + ' type=' + str(type(data.ltp)))
    print('volume=' + str(data.volume) + ' type=' + str(type(data.volume)))
    print('volume_by_product=' + str(data.volume_by_product) + ' type=' + str(type(data.volume_by_product)))


def on_message_executions(_, pair, datas):
    '''test on_message_executions callback'''
    print('pair=', pair)
    for data in datas:
        print('id=' + str(data.order_id) + ' type=' + str(type(data.order_id)))
        print('side=' + str(data.side) + ' type=' + str(type(data.side)))
        print('price=' + str(data.price) + ' type=' + str(type(data.price)))
        print('size=' + str(data.size) + ' type=' + str(type(data.size)))
        print('exec_date=' + str(data.exec_date) + ' type=' + str(type(data.exec_date)))
        print('buy_child_order_acceptance_id=' + str(data.buy_child_order_acceptance_id)
              + ' type=' + str(type(data.buy_child_order_acceptance_id)))
        print('sell_child_order_acceptance_id=' + str(data.sell_child_order_acceptance_id)
              + ' type=' + str(type(data.sell_child_order_acceptance_id)))


def on_error(_, e):
    '''test on_error'''
    print(e)

if __name__ == "__main__":

    subs = [
        # Subscriptions.BOARD_FX_BTC_JPY,
        # Subscriptions.BOARD_SNAPSHOT_FX_BTC_JPY,
        # Subscriptions.TICKER_FX_BTC_JPY,
        Subscriptions.EXECUTIONS_FX_BTC_JPY,
        # Subscriptions.BOARD_BTC_JPY,
        # Subscriptions.BOARD_SNAPSHOT_BTC_JPY,
        # Subscriptions.TICKER_BTC_JPY,
        # Subscriptions.EXECUTIONS_BTC_JPY,
    ]
    # rtapi = RealtimeAPI(subs, on_message=on_message)
    # rtapi = RealtimeAPI(subs, on_message_board=on_message_board)
    # rtapi = RealtimeAPI(subs, on_message_board_snapshot=on_message_board_snapshot)
    # rtapi = RealtimeAPI(subs, on_message_ticker=on_message_ticker)
    rtapi = RealtimeAPI(subs, on_message_executions=on_message_executions)

    try:
        rtapi.start()
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
        rtapi.stop()
    except:
        rtapi.stop()
        import traceback
        traceback.print_exc()
