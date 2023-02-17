import requests

city = "MOSCOW,RU"
key = "2a3842a855e0a311a8c38f797c10aceb"
resultWeek = requests.get("http://api.openweathermap.org/data/2.5/forecast", params={'q': city, 'units': 'metric',
                                                                              'lang': 'ru', 'APPID': key})
resultDay = requests.get("http://api.openweathermap.org/data/2.5/weather", params={'q': city, 'units': 'metric',
                                                                             'lang': 'ru', 'APPID': key})

data1 = resultWeek.json()
data2 = resultDay.json()


def weak_report():
    print("Скорость ветра и видимость на несколько дней")
    for i in data1['list']:
        print(str(i['wind']['speed']) + "m/s " + str(i['visibility']) + "m " + str(i['dt_txt']) + "\n")


def day_report():
    print("Скорость ветра и видимость на текущий день")
    print(data2['wind']['speed'])


weak_report()
day_report()

