

from datetime import datetime


import decimal


units = (
    u'ноль',

    (u'один', u'одна'),
    (u'два', u'две'),

    u'три', u'четыре', u'пять',
    u'шесть', u'семь', u'восемь', u'девять'
)

teens = (
    u'десять', u'одиннадцать',
    u'двенадцать', u'тринадцать',
    u'четырнадцать', u'пятнадцать',
    u'шестнадцать', u'семнадцать',
    u'восемнадцать', u'девятнадцать'
)

tens = (
    teens,
    u'двадцать', u'тридцать',
    u'сорок', u'пятьдесят',
    u'шестьдесят', u'семьдесят',
    u'восемьдесят', u'девяносто'
)

hundreds = (
    u'сто', u'двести',
    u'триста', u'четыреста',
    u'пятьсот', u'шестьсот',
    u'семьсот', u'восемьсот',
    u'девятьсот'
)

orders = (# plural forms and gender
    #((u'', u'', u''), 'm'), # ((u'рубль', u'рубля', u'рублей'), 'm'), # ((u'копейка', u'копейки', u'копеек'), 'f')
    ((u'тысяча', u'тысячи', u'тысяч'), 'f'),
    ((u'миллион', u'миллиона', u'миллионов'), 'm'),
    ((u'миллиард', u'миллиарда', u'миллиардов'), 'm'),
)

minus = u'минус'


async def thousand(rest, sex):
    """Converts numbers from 19 to 999"""
    prev = 0
    plural = 2
    name = []
    use_teens = rest % 100 >= 10 and rest % 100 <= 19
    if not use_teens:
        data = ((units, 10), (tens, 100), (hundreds, 1000))
    else:
        data = ((teens, 10), (hundreds, 1000))
    for names, x in data:
        cur = int(((rest - prev) % x) * 10 / x)
        prev = rest % x
        if x == 10 and use_teens:
            plural = 2
            name.append(teens[cur])
        elif cur == 0:
            continue
        elif x == 10:
            name_ = names[cur]
            if isinstance(name_, tuple):
                name_ = name_[0 if sex == 'm' else 1]
            name.append(name_)
            if cur >= 2 and cur <= 4:
                plural = 1
            elif cur == 1:
                plural = 0
            else:
                plural = 2
        else:
            name.append(names[cur-1])
    return plural, name


async def num2text(num, main_units=((u'', u'', u''), 'm'), flag=False):
    """
    http://ru.wikipedia.org/wiki/Gettext#.D0.9C.D0.BD.D0.BE.D0.B6.D0.B5.D1.81.\
    D1.82.D0.B2.D0.B5.D0.BD.D0.BD.D1.8B.D0.B5_.D1.87.D0.B8.D1.81.D0.BB.D0.B0_2
    """
    _orders = (main_units,) + orders
    if num == 0:
        return ' '.join((units[0], _orders[0][0][2])).strip() # ноль

    rest = abs(num)
    ord = 0
    name = []
    while rest > 0:
        plural, nme = await thousand(rest % 1000, _orders[ord][1])
        if nme or ord == 0:
            name.append(_orders[ord][0][plural])
        name += nme
        rest = int(rest / 1000)
        ord += 1
    if num < 0:
        name.append(minus)
    name.reverse()
    if flag:
        return name[len(name) - 1].strip()
    return ' '.join(name).strip()


async def decimal2text(value, places=2,
                 int_units=(('', '', ''), 'm'),
                 exp_units=(('', '', ''), 'm')):
    value = decimal.Decimal(value)
    q = decimal.Decimal(10) ** -places

    integral, exp = str(value.quantize(q)).split('.')
    return u'{} {}'.format(
        await num2text(int(integral), int_units),
        await num2text(int(exp), exp_units))


async def convert_seconds_to_human_time(seconds):
    minute_in_seconds = 60
    hour_in_seconds = minute_in_seconds * 60
    day_in_seconds = hour_in_seconds * 24
    week_in_seconds = day_in_seconds * 7
    month_in_seconds = day_in_seconds * 30
    year_in_seconds = day_in_seconds * 365

    time_dict = {
        'год': year_in_seconds,
        'месяц': month_in_seconds,
        'неделя': week_in_seconds,
        'день': day_in_seconds,
        'час': hour_in_seconds,
        'минута': minute_in_seconds,
        'секунда': 1
    }

    time_parts = []
    for time_name, time_value in time_dict.items():
        if seconds >= time_value:
            time_amount = seconds // time_value
            if time_name == 'секунда':
                female_units = ((u'секунда', u'секунды', u'секунд'), 'f')
                time_name = await num2text(time_amount, female_units, True)

            if time_name == 'минута':
                female_units = ((u'минута', u'минуты', u'минут'), 'f')
                time_name = await num2text(time_amount, female_units, True)

            if time_name == 'час':
                male_units = ((u'час', u'часа', u'часов'), 'm')
                time_name = await num2text(time_amount, male_units, True)

            if time_name == 'день':
                male_units = ((u'день', u'дня', u'дней'), 'm')
                time_name = await num2text(time_amount, male_units, True)

            if time_name == 'неделя':
                female_units = ((u'неделя', u'недели', u'недель'), 'f')
                time_name = await num2text(time_amount, female_units, True)

            if time_name == 'месяц':
                male_units = ((u'месяц', u'месяца', u'месяцев'), 'm')
                time_name = await num2text(time_amount, male_units, True)

            if time_name == 'гол':
                male_units = ((u'год', u'года', u'лет'), 'm')
                time_name = await num2text(time_amount, male_units)

            time_parts.append(f'{time_amount} {time_name}')
            seconds %= time_value

    return ', '.join(time_parts)


async def unix_to_time(time_seconds):
    value = datetime.fromtimestamp(time_seconds)
    time_msg = value.strftime('%d.%m.%Y %H:%M')
    return time_msg
