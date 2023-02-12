import requests
from time import sleep, time
from datetime import datetime

course_list = []
url = "https://fapi.binance.com/fapi/v1/ticker/price"
time_life = 3600  # время жизни (в секундах) собираемых значений
now_price: float = 0
quote_time = None


def info_course_now(coin1='XRP', coin2='USDT'):
    global now_price, quote_time
    params = {'symbol': f'{coin1}{coin2}'}
    response = requests.get(url, params=params)
    course_now = response.json()
    now_price = float(course_now['price'])
    quote_time = datetime.utcfromtimestamp((course_now['time']) / 1000).strftime('%d-%m-%Y %H:%M:%S')
    if len(course_list) == 0:
        course_list.append(course_now)
    elif course_now['time'] != course_list[-1]['time']:
        course_list.append(course_now)
    sleep(1)


def course_for_hour():
    if len(course_list) > 0:
        max_old_time = round(time() - time_life)
        while True:
            if len(course_list) > 0:
                time_first_el = round(course_list[0]['time'] / 1000)
                if max_old_time > time_first_el:
                    del course_list[0]
                else:
                    break
            else:
                break


def informer():
    if len(course_list) > 0:
        total_max_price = float(course_list[0]['price'])
        for item in course_list:
            price = float(item['price'])
            if price > total_max_price:
                total_max_price = price

        delta_price = round((total_max_price - now_price), 4)
        delta_price_percent = round((delta_price / total_max_price * 100), 4)

        if delta_price_percent >= 1:
            warning_text = f"-->> Падение цены на {delta_price_percent} процентов!!!\n" \
                           f"{total_max_price} - максимальная цена за последние {time_life / 60} минут." \
                           f"{now_price} - текущая цена {time()}, время котировки {quote_time}\n\n"
            with open('attention.txt', 'a', encoding='utf-8') as file:
                file.write(warning_text)
            print('\n', warning_text)


if __name__ == '__main__':
    while True:
        info_course_now()
        course_for_hour()
        informer()
