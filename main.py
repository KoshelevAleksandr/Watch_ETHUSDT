import keyboard
import websocket
import json


def lets_close_ws():
    with open('closing.txt') as f:
        return int(f.readline()) > 0


def on_open(_wsa):
    data = dict(
        method='SUBSCRIBE',
        params=['btcusdt@kline_1h', 'btcusdt@depth@1000ms'],
        id=1)
    _wsa.send(json.dumps(data))



def on_message(_wsa, data):
    prices = []
    d_dict = json.loads(data)
    if d_dict['e'] == 'kline':
        print(d_dict['s'], d_dict['k']['h'], d_dict['k']['l'])
    elif d_dict['e'] == 'depthUpdate':
        print(d_dict['s'], d_dict['b'][0], d_dict['a'][0])
    print(d_dict, '\n')

    if lets_close_ws(): _wsa.close()


def run():
    print('***xxx***')
#     data_send = {
#         'method': 'SUBSCRIBE',
#         'params': ['btcusdt@depth@1000ms'],
#         'id': 1}
#     stream = 'binance_stream'
#     wss = 'wss://stream.binance.com:9443/ws/%s' % stream
#     ws = websocket.WebSocket()
#     ws.connect(wss)
#     ws.send('{"method": "SUBSCRIBE","params": ["btcusdt@depth@1000ms"], "id": 1}')
#     while True:
#         data = ws.recv()
#         print(json.dumps(data[1:-1]), '\n')

    btc = 'BTCUSDT'.lower()
    eth = 'ETHUSDT'.lower()
    interval = '1m'
    stream_name_btc = '%s@kline_%s' % (btc, interval)
    stream_name_eth = '%s@kline_%s' % (eth, interval)
    stream = 'binance_stream'

    # wss = 'wss://stream.binance.com:9443/stream?streams=btcusdt@kline_1m/ethusdt@kline_1m/'

    wss = 'wss://stream.binance.com:9443/ws/%s' % stream
    wsa = websocket.WebSocketApp(wss, on_message=on_message, on_open=on_open)
    wsa.run_forever()


if __name__ == '__main__':
    run()

