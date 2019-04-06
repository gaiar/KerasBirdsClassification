# Инструкция:

# URL: http://hidemy.name/ru/api/proxylist.php
# Возможные параметры:

import requests

BASE_URL = "http://hidemy.name/ru/api/proxylist.php"


def download_proxies(out="plain", country="FIFRDEPL", maxtime="500", ports=None, type="hs", anon="12", uptime=95, code=None):
    arg = {}
    arg['out'] = out
    arg['country'] = country
    arg['maxtime'] = maxtime
    arg['type'] = type
    arg['anon'] = anon
    arg['uptime'] = uptime

    if ports is not None:
        arg['ports'] = ports

    if code is not None:
        arg['code'] = code

    r = requests.get(BASE_URL, params=arg)
    return r.content.splitlines()


print(download_proxies(code="286280102143064"))


# out - формат экспорта [обязательный параметр]
# Доступны следующие форматы:
# plain - текстовый список в формате ip:port
# csv - csv таблица
# php - сериализованный php массив
# js - json формат
# xml - xml формат
# Пример:
# http://hidemy.name/ru/api/proxylist.php?out=csv

# country - двухбуквенный код страны, один или несколько.
# Пример:
# http://hidemy.name/ru/api/proxylist.php?out=csv&country=RU
# http://hidemy.name/ru/api/proxylist.php?out=csv&country=UAUS

# maxtime - максимально допустимая задержка.
# Прокси, задержка у которых превышает данный параметр (время в мс), не будут показаны.
# Пример:
# http://hidemy.name/ru/api/proxylist.php?out=csv&maxtime=500

# ports - показать только прокси с заданными портами.
# Пример:
# http://hidemy.name/ru/api/proxylist.php?out=csv&ports=25,80-500,8080

# type - тип прокси.
# Используются следующие коды:
# HTTP - h
# HTTPS - s
# SOCKS4 - 4
# SOCKS5 - 5
# Например, если надо только HTTPS и SOCKS5, то:
# http://hidemy.name/ru/api/proxylist.php/api/proxylist.php?out=csv&type=s5

# anon - анонимность.
# Используются следующие коды:
# Нет - 1
# Низкая - 2
# Средняя - 3
# Высокая - 4
# Например, если надо только среднюю и высокую, то:
# http://hidemy.name/ru/api/proxylist.php/api/proxylist.php?out=csv&anon=34

# uptime - минимально желаемый аптайм прокси (1-100)
# Пример:
# http://hidemy.name/ru/api/proxylist.php?out=csv&uptime=95

# code - для работы без авторизации на сайте, добавьте к ссылке свой код.
# Пример:
# http://hidemy.name/ru/api/proxylist.php?out=csv&code=12345

# Быстрое получение URL через сайт:
# 1. Войдите на сайт с рабочим кодом.
# 2. Откройте http://hidemy.name/ru/proxy-list/
# 3. Если требуется - настройте фильтры и нажмите Применить
# Скопируйте ссылку для экспорта, например:
# http://hidemy.name/ru/api/proxylist.php?country=US&maxtime=1000&ports=3124&type=h&anon=4&out=csv

# Для экспорта всех листов в csv формате без фильтров адрес будет такой:
# http://hidemy.name/ru/api/proxylist.php?out=csv

# Для работы без авторизации на сайте, добавьте к ссылке свой код, например &code=12345

# Чтобы изменить формат экспорта, отредактируйте параметр out.
