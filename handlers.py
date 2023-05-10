def check_time(time):
    time_now = datetime.datetime.now()
    time_event = datetime.datetime.fromtimestamp(time / 1000.0)
    check_one_hour = time_event + datetime.timedelta(seconds=5)
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
        print(prices_eth[0])
        price_change = round((new_price_eth - prices_eth[0]) / prices_eth[0] * 100, 3)
        if price_change > 1:
            print(f'За последние 60 минут цена изменилась на: {price_change}%')
        last_price_eth = new_price_eth