""" 和暦対応 datetime 拡張モジュール
Copyright (c) 2023 Solla Umiyama
Released under the MIT license
https://opensource.org/licenses/mit-license.php
"""

import datetime
import unicodedata


SPECIFIERS = ['%g', '%-g', '%#g', '%e', '%-e', '%#e', '%-a', '%#a']
ERAS = [
    {'name': 'M', 'era': '明治', 'begin': datetime.date(1868, 1, 25)},
    {'name': 'T', 'era': '大正', 'begin': datetime.date(1912, 7, 30)},
    {'name': 'S', 'era': '昭和', 'begin': datetime.date(1926, 12, 25)},
    {'name': 'H', 'era': '平成', 'begin': datetime.date(1989, 1, 8)},
    {'name': 'R', 'era': '令和', 'begin': datetime.date(2019, 5, 1)},
]
DAYS = ['日', '月', '火', '水', '木', '金', '土', '日']
NUMBERS = [chr(zen) for zen in range(0xff10,0xff1a)]
NUMBERS_DICT = {zen: unicodedata.normalize('NFKC', zen) for zen in NUMBERS}
NUMBERS_TABLE = str.maketrans(NUMBERS_DICT)


def _jp_replace(jp_format, g, gg, e, ee):
    esc = '%%'
    split_format = jp_format.split(esc)
    split_format = [s.replace('%g', g) for s in split_format]
    split_format = [s.replace('%-g', gg) for s in split_format]
    split_format = [s.replace('%#g', gg) for s in split_format]
    split_format = [s.replace('%e', e) for s in split_format]
    split_format = [s.replace('%-e', ee) for s in split_format]
    split_format = [s.replace('%#e', ee) for s in split_format]
    return esc.join(split_format)


def _day_replace(jp_format, d):
    if '%-a' not in jp_format and '%#a' not in jp_format:
        return jp_format
    esc = '%%'
    split_format = jp_format.split(esc)
    split_format = [s.replace('%-a', d) for s in split_format]
    split_format = [s.replace('%#a', d) for s in split_format]
    return esc.join(split_format)


def _era_info(j_datetime):
    j_date = datetime.date.fromordinal(j_datetime.toordinal())
    eras_filter = filter(lambda x: x['begin'] <= j_date, ERAS)
    era_info = max(eras_filter, key=lambda x: x['begin'], default=None)
    if era_info is None:
        ymd = j_date.strftime('%Y/%m/%d')
        raise ValueError('too old date to match japanese era: ' + ymd)
    return era_info


def strptime(date_string, format_string):
    try:
        return datetime.datetime.strptime(date_string, format_string)
    except ValueError:
        pass

    def _jp_parse(ds, jp_format, er, e):
        formats = set(_day_replace(jp_format, d) for d in DAYS)
        for f in formats:
            try:
                temp_format = _jp_replace(f, er['era'], er['name'], e, e)
                return datetime.datetime.strptime(ds, temp_format)
            except ValueError:
                pass
        return None

    def _adjust(dt, start_year, jp_year):
        year = start_year + jp_year - 1
        return dt.replace(year=year)

    date_str = date_string.translate(NUMBERS_TABLE)
    format_str = format_string.translate(NUMBERS_TABLE)
    eras = [e for e in ERAS if e['era'] in date_str or e['name'] in date_str]

    for era in eras:
        dtime = _jp_parse(date_str, format_str, era, '%y')
        if dtime is not None:
            return _adjust(dtime, era['begin'].year, int(dtime.strftime('%y')))

    if '元' in date_str:
        for era in eras:
            dtime = _jp_parse(date_str, format_str, era, '元')
            if dtime is not None:
                return _adjust(dtime, era['begin'].year, 1)

    for y in [n for n in range(1, 10) if str(n) in date_str]:
        for era in eras:
            dtime = _jp_parse(date_str, format_str, era, str(y))
            if dtime is not None:
                return _adjust(dtime, era['begin'].year, y)

    if '29' in date_str:
        new_format_str = format_str
        for d in ['%d', '%-d', '%#d']:
            if d in format_str:
                new_format_str = new_format_str.replace(d, '29')
        if new_format_str != format_str:
            date_obj = strptime(date_str, new_format_str)
            return date_obj.replace(day=29)

    time = '\'' + date_string + '\''
    format = '\'' + format_string + '\''
    msg = 'time data {time} does not match format {format}'
    raise ValueError(msg.format(time=time, format=format))


def strftime(date_obj, format_string, gannen=False):
    if not isinstance(format_string, str):
        raise TypeError("format_string must be a str")
    if not isinstance(gannen, bool):
        raise TypeError("gannen must be a bool")
    if all(s not in format_string.replace('%%', '') for s in SPECIFIERS):
        return date_obj.strftime(format_string)
    era_info = _era_info(date_obj)
    y = date_obj.year - era_info['begin'].year + 1
    g = era_info['era']
    gg = era_info['name']
    e = '{:02d}'.format(y)
    ee = str(y)
    if gannen and y == 1:
        e = '元'
        ee = '元'
    jp_format = _jp_replace(format_string, g, gg, e, ee)
    if '%-a' in jp_format or '%#a' in jp_format:
        d = DAYS[date_obj.isoweekday()]
        jp_format = _day_replace(jp_format, d)
        print('===>', d, date_obj.isoweekday(), jp_format, date_obj.strftime(jp_format))
    return date_obj.strftime(jp_format)
