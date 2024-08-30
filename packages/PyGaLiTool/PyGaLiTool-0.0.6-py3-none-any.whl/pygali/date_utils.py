import datetime
import time
from typing import Union
from dateutil import parser
import pytz


class DatePattern:
    NORM_DATE_FORMAT = "%Y-%m-%d"
    PURE_DATE_FORMAT = "%Y%m%d"
    CHINESE_DATE_FORMAT = "%Y年%m月%d日"

    NORM_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    PURE_DATETIME_FORMAT = "%Y%m%d%H%M%S"
    CHINESE_DATETIME_FORMAT = "%Y年%m月%d日%H时%M分%S秒"


def cur_date(fmt: Union[DatePattern, str] = DatePattern.NORM_DATE_FORMAT) -> str:
    """
    获取当前时区的Date
    :param fmt:
    :return:
    """
    return datetime.date.today().strftime(fmt)


def cur_datetime(fmt: Union[DatePattern, str] = DatePattern.NORM_DATETIME_FORMAT) -> str:
    """
    获取当前时区的DateTime
    :param fmt:
    :return:
    """
    return datetime.datetime.strftime(datetime.datetime.now(), fmt)


def cur_datetime_tz(time_zone: str = 'UTC', fmt: Union[DatePattern, str] = DatePattern.NORM_DATETIME_FORMAT) -> str:
    """
    获取指定时区的DateTime
    :param time_zone:默认0时区
    :param fmt:
    :return:
    """
    tz = parse_etc_tz(time_zone)
    return datetime.datetime.strftime(datetime.datetime.now(tz=tz), fmt)


def date_add(date_str: str, days: int, fmt=DatePattern.NORM_DATE_FORMAT) -> str:
    """
    DATE_ADD: 向日期加上指定的时间间隔
    :param date_str: 当前日期(%Y-%m-%d 格式的str)
    :param days: 相加天数
    :param fmt: 日期格式,默认为"%Y-%m-%d"
    :return: 当前日期 + 指定天数
    """
    dt: datetime.datetime = datetime.datetime.strptime(date_str, fmt) + datetime.timedelta(days=days)
    return dt.strftime(fmt)


def date_sub(date_str: str, days: int, fmt=DatePattern.NORM_DATE_FORMAT) -> str:
    """
    DATE_SUB: 向日期减去指定的时间间隔
    :param date_str: 当前日期(%Y-%m-%d 格式的str)
    :param days: 相加天数
    :param fmt: 日期格式,默认为"%Y-%m-%d"
    :return: 当前日期 + 指定天数
    """
    dt: datetime.datetime = datetime.datetime.strptime(date_str, fmt) - datetime.timedelta(days=days)
    return dt.strftime(fmt)


def date_format(date_time: Union[str, datetime.datetime], fmt=DatePattern.NORM_DATE_FORMAT) -> str:
    """
    日期时间格式化
    :param date_time:
    :param fmt:
    :return:
    """

    if isinstance(date_time, str):
        # str -> datetime.datetime
        parsed_datetime: datetime.datetime = parser.parse(date_time)
        # datetime.datetime -> format_str
        return datetime.datetime.strftime(parsed_datetime, fmt)
    elif isinstance(date_time, datetime.datetime):
        # datetime.datetime -> format_str
        return date_time.strftime(fmt)


def date_diff(date_1: str, date_2: str) -> int:
    date_1: datetime.date = parser.parse(date_1).date()
    date_2: datetime.date = parser.parse(date_2).date()
    diff: datetime.timedelta = (date_1 - date_2)
    return diff.days


def ts_to_datetime(ts: int, time_zone='GMT-8', fmt=DatePattern.NORM_DATETIME_FORMAT):
    """
    时间戳转Date日期
    :return:
    """
    if len(str(ts)) == 13:
        ts /= 1000

    tz = parse_etc_tz(time_zone)
    return datetime.datetime.fromtimestamp(ts, tz=tz).strftime(fmt)


def parse_etc_tz(time_zone: str):
    """
    统一转换成 ETC 时区表示
    如，东八区：GMT+8 等价于 Etc/GMT-8
    :return:
    """
    if time_zone.startswith("GMT"):
        # GMT的正负号 与Etc/GMT 是相反的
        if "+" in time_zone:
            time_zone = time_zone.replace("+", "-")
        elif "-" in time_zone:
            time_zone = time_zone.replace("-", "+")
        time_zone = 'Etc/' + time_zone
    return pytz.timezone(time_zone)


def parse_datetime(date_time: str) -> datetime.datetime:
    return parser.parse(date_time)


def parse_date(date_time: str) -> datetime.date:
    """
    时间戳转DateTime
    :return:
    """

    parsed_datetime: datetime.datetime = parser.parse(date_time)
    return parsed_datetime.date()


def to_date(date_time: str, fmt=DatePattern.NORM_DATE_FORMAT) -> str:
    """截取字符串中的 Date"""
    return parse_date(date_time).strftime(fmt)


def year(date_time: str) -> int:
    """截取字符串中的 Year"""
    return parse_datetime(date_time).year


def month(date_time: str) -> int:
    """截取字符串中的 Month"""
    return parse_datetime(date_time).month


def day_of_month(date_time: str) -> int:
    """截取字符串中的 Day"""
    return parse_datetime(date_time).day


def hour(date_time: str) -> int:
    """截取字符串中的 Hour"""
    return parse_datetime(date_time).hour


def minute(date_time: str) -> int:
    """截取字符串中的 Minute"""
    return parse_datetime(date_time).minute


def second(date_time: str) -> int:
    """截取字符串中的 Second"""
    return parse_datetime(date_time).second


def next_month(date_time: str) -> int:
    """截取字符串中的 Month对应的下个月"""
    date_time = parser.parse(date_time)
    return 1 if date_time.month + 1 == 13 else date_time.month + 1


def last_month(date_time: str) -> int:
    """截取字符串中的 Month对应的上个月"""
    date_time = parser.parse(date_time)
    return 12 if date_time.month - 1 == 0 else date_time.month - 1


def begin_date_of_month(date_time: str, fmt=DatePattern.NORM_DATE_FORMAT) -> str:
    """
    指定日期对应的 当月第1天
    :param date_time:
    :param fmt:
    :return:
    """

    # str -> datetime.datetime
    date_time = parser.parse(date_time)
    _year = date_time.year
    _month = date_time.month
    return datetime.datetime(year=_year, month=_month, day=1).date().strftime(fmt)


def end_date_of_month(date_time: str, fmt=DatePattern.NORM_DATE_FORMAT) -> str:
    """
    指定日期对应的 当月最后1天
    :param date_time:
    :param fmt:
    :return:
    """
    # str -> datetime.datetime
    date_time = parser.parse(date_time)
    _year = date_time.year
    _month = date_time.month
    return (datetime.datetime(year=_year, month=_month + 1, day=1) - datetime.timedelta(days=1)).date().strftime(fmt)


def begin_date_of_month_offset(date_time: str, offset=1, fmt=DatePattern.NORM_DATE_FORMAT) -> str:
    """
    指定日期对应的 偏移指定月份后的当月第一天,如:
        offset=-1 -> 上个月的第1天
        offset=1  -> 下个月的第1天
    :param date_time:
    :param offset: 偏移的月份数
    :param fmt:
    :return:
    """
    # str -> datetime.datetime
    date_time = parser.parse(date_time)
    _year = date_time.year
    _month = date_time.month
    return datetime.datetime(year=_year, month=_month + offset, day=1).date().strftime(fmt)


def end_date_of_month_offset(date_time: str, offset=1, fmt=DatePattern.NORM_DATE_FORMAT) -> str:
    """
    指定日期对应的 偏移指定月份后的当月第一天,如:
        offset=-1 -> 上个月的最后1天
        offset=1  -> 下个月的最后1天
    :param date_time:
    :param offset: 偏移的月份数
    :param fmt:
    :return:
    """
    # str -> datetime.datetime
    date_time = parser.parse(date_time)
    _year = date_time.year
    _month = date_time.month
    return (datetime.datetime(year=_year, month=_month + offset + 1, day=1) - datetime.timedelta(days=1)).date().strftime(fmt)


if __name__ == '__main__':
    # cur_date
    print(cur_date())
    print(cur_date("%Y%m%d"))
    print(cur_date(DatePattern.CHINESE_DATE_FORMAT))
    # cur_datetime
    print(cur_datetime())
    print(cur_datetime("%Y%m%d%H%M%S"))
    print(cur_datetime(DatePattern.CHINESE_DATETIME_FORMAT))
    # date_add/date_sub
    print(date_sub(cur_date(), 1))
    print(date_add(cur_date(), -1))
    print(date_add(cur_date(), 1))
    # cur_datetime_tz
    print(cur_datetime_tz())
    print(cur_datetime_tz("GMT-2"))
    print(cur_datetime_tz("GMT-8"))
    # date_format
    print(date_format(cur_datetime(), "%Y-%m-%d"))
    print(date_format(cur_datetime(), "%Y-%m-%d %H"))
    # date_diff
    print(date_diff('2024-10-10', '2024-10-01'))
    # ts_to_datetime
    print(ts_to_datetime(int(time.time()), 'GMT-8'))
    print(ts_to_datetime(int(time.time()), 'Etc/GMT-8'))
    print(ts_to_datetime(int(time.time()), 'GMT+8'))
    print(ts_to_datetime(int(time.time()), 'GMT+2'))
    # parse_date, parse_datetime
    print(parse_date('2024-08-29 12:34:56'))
    print(parse_datetime('2024-08-29 12:34:56'))
    # to_date, year, month, day_of_month
    print(to_date('2024-08-29 12:34:56'))
    print(year('2024-08-29 12:34:56'), month('2024-08-29 12:34:56'), day_of_month('2024-08-29 12:34:56'))
    print(hour('2024-08-29 12:34:56'), minute('2024-08-29 12:34:56'), second('2024-08-29 12:34:56'))
    # last_month, next_month, last_year, next_year
    print(last_month('2024-01-01 12:34:56'))
    print(next_month('2024-12-01 12:34:56'))
    # begin_date_of_month, end_date_of_month
    print(begin_date_of_month('2024-08-10 12:34:56'))
    print(end_date_of_month('2024-08-10 12:34:56'))
    # begin_date_of_month_offset, end_date_of_month_offset
    print(begin_date_of_month_offset('2024-08-31 12:34:56', -1))
    print(end_date_of_month_offset('2024-08-31 12:34:56', -1))
    print(begin_date_of_month_offset('2024-08-31 12:34:56', 1))
    print(end_date_of_month_offset('2024-08-31 12:34:56', 1))
