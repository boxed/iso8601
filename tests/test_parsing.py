import pytest
from iso8601 import parse, parse_time, TimeZone
from datetime import date, datetime, time, timedelta


@pytest.mark.parametrize(
    'function, data, expected', [
    (parse, '2012', date(2012, 1, 1)),
    (parse, '2012-05-03', date(2012, 5, 3)),
    (parse, '20120503', date(2012, 5, 3)),
    (parse, '2012-05', date(2012, 5, 1)),

    # week numbers
    (parse, '2012-W05', date(2012, 1, 30)),
    (parse, '2012W05', date(2012, 1, 30)),
    (parse, '2012-W05-5', date(2012, 2, 3)),
    (parse, '2012W055', date(2012, 2, 3)),

    # ordinal days
    (parse, '2012-007', date(2012, 1, 7)),
    (parse, '2012007', date(2012, 1, 7)),

    # times
    (parse, '00:00', time(0, 0)),
    (parse, '12:04:23', time(12, 4, 23)),
    (parse, '120423', time(12, 4, 23)),
    (parse, '12:04', time(12, 4, 0)),
    (parse, '1204', date(1204, 1, 1)),
    (parse_time, '1204', time(12, 4, 0)),
    (parse, '12', time(12, 0, 0)),
    (parse, '02', time(2, 0, 0)),
    (parse, '12:04:23.450686', time(12, 4, 23, 450686)),
    (parse, '12:04:23.45', time(12, 4, 23, 450000)),

    # combined
    (parse, '2008-09-03T20:56:35.450686', datetime(2008, 9, 3, 20, 56, 35, 450686)),
    (parse, '2008-09-03T20:56:35.450686Z', datetime(2008, 9, 3, 20, 56, 35, 450686, TimeZone(timedelta()))),
    (parse, '2008-09-03T20:56:35.45Z', datetime(2008, 9, 3, 20, 56, 35, 450000, TimeZone(timedelta()))),
    (parse, '2008-09-03T20:56:35.450686+01', datetime(2008, 9, 3, 20, 56, 35, 450686, TimeZone(timedelta(minutes=60)))),
    (parse, '2008-09-03T20:56:35.45+01', datetime(2008, 9, 3, 20, 56, 35, 450000, TimeZone(timedelta(minutes=60)))),
    (parse, '2008-09-03T20:56:35.450686+0100', datetime(2008, 9, 3, 20, 56, 35, 450686, TimeZone(timedelta(minutes=60)))),
    (parse, '2008-09-03T20:56:35.450686+01:30', datetime(2008, 9, 3, 20, 56, 35, 450686, TimeZone(timedelta(minutes=60 + 30)))),
    (parse, '2008-09-03T20:56:35.450686-01:30', datetime(2008, 9, 3, 20, 56, 35, 450686, TimeZone(timedelta(minutes=-(60 + 30))))),
    (parse, '2013-03-28T02:30:24+00:00', datetime(2013, 3, 28, 2, 30, 24, tzinfo=TimeZone(timedelta(minutes=0)))),
])
def test(function, data, expected):
    actual = function(data)
    assert type(actual) == type(expected)
    assert actual == expected

