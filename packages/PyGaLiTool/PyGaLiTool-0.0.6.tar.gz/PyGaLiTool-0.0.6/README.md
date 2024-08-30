
```
# 前置安装twine
python -m pip install --upgrade twine
```

```
# 检查
python setup.py check

# 打包
python setup.py sdist bdist_wheel

# 上传
twine upload dist/*
```

```shell
# 安装使用
pip install PyGaLiTool
pip install PyGaLiTool==0.0.3
```

```python
# 使用方式
from pygali.date_utils import cur_date
print(cur_date())
```

```python
# 一些常见用法:
# cur_date
cur_date()
cur_date("%Y%m%d")
cur_date(DatePattern.CHINESE_DATE_FORMAT)

# cur_datetime
cur_datetime()
cur_datetime("%Y%m%d%H%M%S")
cur_datetime(DatePattern.CHINESE_DATETIME_FORMAT)

# date_add/date_sub
date_sub(cur_date(), 1)
date_add(cur_date(), -1)
date_add(cur_date(), 1)

# cur_datetime_tz
cur_datetime_tz()
cur_datetime_tz("GMT-2")
cur_datetime_tz("GMT-8")

# date_format
date_format(cur_datetime(), "%Y-%m-%d")
date_format(cur_datetime(), "%Y-%m-%d %H")

# date_diff
date_diff('2024-10-10', '2024-10-01')

# ts_to_datetime
ts_to_datetime(int(time.time()), 'GMT-8')
ts_to_datetime(int(time.time()), 'Etc/GMT-8')
ts_to_datetime(int(time.time()), 'GMT+8')
ts_to_datetime(int(time.time()), 'GMT+2')

# parse_date, parse_datetime
parse_date('2024-08-29 12:34:56')
parse_datetime('2024-08-29 12:34:56')

# to_date, year, month, day_of_month
to_date('2024-08-29 12:34:56')
year('2024-08-29 12:34:56'), month('2024-08-29 12:34:56'), day_of_month('2024-08-29 12:34:56')
hour('2024-08-29 12:34:56'), minute('2024-08-29 12:34:56'), second('2024-08-29 12:34:56')

# last_month, next_month, last_year, next_year
last_month('2024-01-01 12:34:56')
next_month('2024-12-01 12:34:56')

# begin_date_of_month, end_date_of_month
begin_date_of_month('2024-08-10 12:34:56')
end_date_of_month('2024-08-10 12:34:56')

# begin_date_of_month_offset, end_date_of_month_offset
begin_date_of_month_offset('2024-08-31 12:34:56', -1)
end_date_of_month_offset('2024-08-31 12:34:56', -1)
begin_date_of_month_offset('2024-08-31 12:34:56', 1)
end_date_of_month_offset('2024-08-31 12:34:56', 1)
```