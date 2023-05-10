import keyboard
import websocket
import json
import datetime


s_btc = 'BTCUSDT'
last_price_btc = None
correction_btc = None

s_eth = 'ETHUSDT'
last_price_eth = None
correction_eth = None
prices_eth = []


def check_time(time):
    time_now = datetime.datetime.now()
    time_event = datetime.datetime.fromtimestamp(time / 1000.0)
    check_one_hour = time_event + datetime.timedelta(hours=1)
    return check_one_hour < time_now


def lets_close_ws():
    with open('closing.txt') as f:
        return int(f.readline()) > 0


def on_open(_wsa):
    data = dict(
        method='SUBSCRIBE',
        params=['btcusdt@ticker', 'ethusdt@ticker'],
        id=1)
    _wsa.send(json.dumps(data))


def on_message(_wsa, data):
    global s_btc, s_eth, last_price_btc, last_price_eth, prices_eth, correction_btc, correction_eth

    d_dict = json.loads(data)
    print(d_dict)
    if d_dict['s'] == s_btc:
        new_price_btc = float(d_dict['c'])
        if last_price_btc is None:
            last_price_btc = new_price_btc
        else:
            correction_btc = float((last_price_btc - new_price_btc) / last_price_btc * 100)

    if d_dict['s'] == s_eth:
        time = d_dict['E']
        new_price_eth = float(d_dict['c'])

        if last_price_eth is None:
            last_price_eth = new_price_eth
        else:
            correction_eth = float((last_price_eth - new_price_eth) / last_price_eth * 100)
            personal_correction = round(correction_eth - correction_btc, 3)
            print(personal_correction)




            prices_eth.append([d_dict['E'], personal_price])

    print(last_price_btc, correction_btc)
    print(last_price_eth, correction_eth)



    if lets_close_ws():
        _wsa.close()


def run():
    print('***xxx***')
    stream = 'binance_stream'
    wss = 'wss://stream.binance.com:9443/ws/%s' % stream
    wsa = websocket.WebSocketApp(wss, on_message=on_message, on_open=on_open)
    wsa.run_forever()


if __name__ == '__main__':
    run()

