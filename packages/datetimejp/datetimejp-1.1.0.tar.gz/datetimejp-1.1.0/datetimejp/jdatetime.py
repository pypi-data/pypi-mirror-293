""" 和暦対応 datetime.datetime 拡張クラス
Copyright (c) 2023 Solla Umiyama
Released under the MIT license
https://opensource.org/licenses/mit-license.php
"""


import datetime
from datetimejp import common
from datetimejp import jdate


def to_jdatetime(datetime_obj):
    """datetime.datetimeオブジェクトをdatetimejp.JDatetimeオブジェクトに変換する。"""
    if not isinstance(datetime_obj, datetime.date):
        raise TypeError("datetime_obj must be a datetime object")
    # Python 3.7 前後のバージョンで分岐
    if hasattr(datetime.datetime, 'fromisoformat'):
        serial = datetime_obj.isoformat(timespec='microseconds')
        dt = JDatetime.fromisoformat(serial)
    else:
        keys = ['year',
                'month',
                'day',
                'hour',
                'minute',
                'second',
                'microsecond']
        datetime_dict = {key: getattr(datetime_obj, key) for key in keys}
        dt = JDatetime(**datetime_dict)
    # タイムゾーン情報を取得
    if datetime_obj.tzinfo is not None:
        dt = dt.replace(tzinfo=datetime_obj.tzinfo)
    return dt


class JDatetime(datetime.datetime):
    """和暦対応日付時刻クラス"""
    def _override(self, method, other):
        dt = method(other)
        if isinstance(dt, datetime.datetime):
            if not isinstance(dt, self.__class__):
                dt = to_jdatetime(dt)
        return dt

    def __add__(self, other):
        return self._override(super().__add__, other)

    def __radd__(self, other):
        return self._override(super().__radd__, other)

    def __sub__(self, other):
        return self._override(super().__sub__, other)

    def __rsub__(self, other):
        return self._override(super().__rsub__, other)

    def strftime(self, format, gannen=False):
        """
        与えられた書式に従ってJDatetimeインスタンスを文字列に変換する。


        Args:
            format: 出力する日付文字列のフォーマット
                通常のdatetime.strftimeの引数formatと同様の書式化指定子に加え、次を指定できる。
                    %g: 元号を日本語表記で指定
                    %-g: 元号をローマ字表記で指定
                    %e: 年を0埋めを行うものとして指定
                    %-e: 年を0埋めを行わないものとして指定
            gannen: 改元後の初年を元年として出力するか、数字で出力するかを指定する倫理値

        Returns:
            str: 日本語表記の日付文字列
        """
        return common.strftime(super(), format, gannen)

    @classmethod
    def strptime(cls, date_string, format):
        """
        指定された対応する書式で文字列を構文解析して JDatetime オブジェクトにする。


        Args:
            date_string: 構文解析を行う対象となる日付文字列
            format: 構文解析のフォーマット文字列
                通常のdatetime.strptimeの引数formatと同様の書式化指定子に加え、次を指定できる。
                    %g: 元号を日本語表記で指定
                    %-g: 元号をローマ字表記で指定
                    %e: 年を0埋めを行うものとして指定
                    %-e: 年を0埋めを行わないものとして指定

        Returns:
            JDatetime: 構文解析によって得られたJDatetimeオブジェクト
        """
        datetime_obj = common.strptime(date_string, format)
        return to_jdatetime(datetime_obj)

    @property
    def j_era(self):
        return self.strftime('%g')

    @property
    def j_year(self):
        return int(self.strftime('%e'))

    def date(self):
        return jdate.to_jdate(self)
