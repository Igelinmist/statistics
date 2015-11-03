from datetime import datetime, timedelta, date
import re


rus_date_re = re.compile(r"\d{2}\.\d{2}\.\d{4}")
req_date_re = re.compile(r"\d{4}-\d{2} -\d{2}")


def default_stat():
    return "wd=00:00,psk=0,ost=0"


def change_date(inp_date, days_cnt):
    return (datetime.strptime(
        inp_date, '%d.%m.%Y') + timedelta(days_cnt)
    ).strftime('%d.%m.%Y')


def stat_timedelta(time_delta):
    if time_delta or time_delta == timedelta(0):
        sec = time_delta.total_seconds()
        hours, remainder = divmod(sec, 3600)
        minutes, sec = divmod(remainder, 60)
        return '%d:%02d' % (int(hours), int(minutes))
    else:
        return '-'


def stat_timedelta_for_report(time_delta):
    if time_delta:
        sec = time_delta.total_seconds()
        hours, remainder = divmod(sec, 3600)
        if remainder >= 1800:
            hours += 1
        return str(int(hours))
    else:
        return '-'


def reqdate(inp_date):
    if isinstance(inp_date, str):
        if rus_date_re.search(inp_date):
            date_comp = inp_date.split('.')
            return '{2}-{1}-{0}'.format(*date_comp)
        elif req_date_re.search(inp_date):
            return inp_date
        else:
            return None
    elif isinstance(inp_date, date):
        return inp_date.strftime('%Y-%m-%d')
    return None


def yesterday_local():
    return (date.today() - timedelta(days=1)).strftime('%d.%m.%Y')
