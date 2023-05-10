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


def read_btc(new_price_btc):
    global last_price_btc, correction_btc
    if last_price_btc is None:
        last_price_btc = new_price_btc
    else:
        correction_btc = round((new_price_btc - last_price_btc) / last_price_btc * 100, 4)
        last_price_btc = new_price_btc


def read_eth(time, new_price_eth):
    global last_price_eth, correction_eth, prices_eth
    if last_price_eth is None:
        last_price_eth = new_price_eth
    else:
        correction_eth = round((new_price_eth - last_price_eth) / last_price_eth * 100, 5)
        personal_correction = round(correction_eth - correction_btc, 3)
        sign_correction = '+' if personal_correction > 0 else ''
        print(f'Собственное движение цены ETH: {sign_correction}{personal_correction}%')
        prices_eth.append([time, new_price_eth])
        while check_time(prices_eth[0][0]):
            prices_eth.pop(0)
        # print(prices_eth[0])
        price_change = round((new_price_eth - prices_eth[0]) / prices_eth[0] * 100, 3)
        if price_change > 1:
            print(f'За последние 60 минут цена изменилась на: {price_change}% ({prices_eth[0]} >>> {new_price_eth})')
        last_price_eth = new_price_eth


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

    d_dict = json.loads(data)
    if d_dict['s'] == s_btc:
        new_price_btc = float(d_dict['c'])

        read_btc(new_price_btc)

    if d_dict['s'] == s_eth:
        time = d_dict['E']
        new_price_eth = float(d_dict['c'])

        read_eth(time, new_price_eth)

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

