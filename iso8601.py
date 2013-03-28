#!/usr/local/bin/python
# coding: utf8

# Based on http://en.wikipedia.org/wiki/ISO_8601
# NOTE: this library only supports date in the range 1 AD - 9999 AD due to limitations in pythons datetime module

# NOTE: autodetect between YYYY and hhmm is impossible, YYYY is preferred
# TODO: durations
# TODO: time intervals
# TODO: repeating intervals

from datetime import date, datetime, time, timedelta, tzinfo
import re
import unittest

class TimeZone(tzinfo):
    def __init__(self, delta):
        super(TimeZone, self).__init__()
        self.offset = delta

    def utcoffset(self, dt):
        return self.offset

    def tzname(self, dt):
        return str(self.offset)

    def dst(self, dt):
        return self.offset

    def __cmp__(self, other):
        return cmp(self.offset, other.offset)

    def __repr__(self):
        return '%s' % self.offset

def parse(s):
    timezone = None
    if s.endswith('Z'):
        timezone = TimeZone(timedelta())
        s = s[:-1]
    length = len(s)
    if 'T' in s:
        date_part, time_part = s.split('T')
        return datetime.combine(parse_date(date_part), parse_time(time_part, timezone))
    if ':' in s or length in {6, 2}:
        return parse_time(s, timezone)
    return parse_date(s)

def parse_timezone(s):
    assert s[0] in {'+', '-'}
    sign, timezone = s[0], s[1:]
    timezone = parse_time(timezone)
    minutes = timezone.hour*60 + timezone.minute
    if sign == '-':
        minutes = -minutes
    return TimeZone(timedelta(minutes=minutes))


def parse_date(s):
    # calendar dates
    # YYYY-MM-DD
    # YYYYMMDD
    result = None
    m = re.match(r'^(?P<year>\d{4})-?(?P<month>\d{2})-?(?P<day>\d{2})', s)
    if m:
        s = s[m.end():]
        result = date(int(m.groupdict()['year']), int(m.groupdict()['month']), int(m.groupdict()['day']))

    # week dates
    if result is None:
        if 'W' in s:
            formats = [
                # suffix for parsing, format, description
                ( '', '%Y-W%W-%w', 'YYYY-Www-D'),
                ( '', '%YW%W%w',   'YYYYWwwD'),
                ('1', '%Y-W%W%w',  'YYYY-Www'), # week only
                ('1', '%YW%W%w',   'YYYYWww'), # week only
            ]
            for suffix, week_format, description in formats:
                if len(description) == len(s):
                    try:
                        result = datetime.strptime(s[:len(description)]+suffix, week_format).date()
                        s = s[:len(description)]
                        break
                    except ValueError:
                        pass

    # ordinal dates
    description = 'YYYY-DDD'
    if result is None and len(s) >= len(description):
        try:
            result = datetime.strptime(s[:len(description)], '%Y-%j').date()
            s = s[:len(description)]
        except ValueError:
            pass

    description = 'YYYYDDD'
    if result is None and len(s) >= len(description):
        try:
            result = datetime.strptime(s[:len(description)], '%Y%j').date()
            s = s[:len(description)]
        except ValueError:
            pass

    # YYYY-MM # month only
    if result is None:
        m = re.match(r'^(?P<year>\d{4})-?(?P<month>\d{2})', s)
        if m:
            s = s[m.end():]
            result = date(int(m.groupdict()['year']), int(m.groupdict()['month']), 1)

    if result is None:
        description = 'YYYY'
        result = datetime.strptime(s[:len(description)], '%Y').date()
        s = s[:len(description)]

    return result

def parse_time(in_s, timezone=None):
    result = None
    micros = 0
    s = in_s
    if '.' in s:
        s, micros = s.split('.')
        s, micros = s+micros[6:], int(micros[:6])

    # hh:mm:ss
    # hhmmss
    if result is None:
        m = re.match(r'^(?P<hour>\d{2}):?(?P<minute>\d{2}):?(?P<second>\d{2})', s)
        if m:
            s = s[m.end():]
            result = time(int(m.groupdict()['hour']), int(m.groupdict()['minute']), int(m.groupdict()['second']), micros, timezone)
    # hh:mm
    # hhmm
    if result is None:
        m = re.match(r'^(?P<hour>\d{2}):?(?P<minute>\d{2})', s)
        if m:
            s = s[m.end():]
            result = time(int(m.groupdict()['hour']), int(m.groupdict()['minute']), 0, micros, timezone)
    # hh
    if result is None:
        m = re.match(r'^(?P<hour>\d{2})', s)
        if m:
            s = s[m.end():]
            result = time(int(m.groupdict()['hour']), 0, 0, micros, timezone)

    if result is not None:
        if s:
            result = result.replace(tzinfo=parse_timezone(s))
        return result

    raise Exception('Could not parse "%s" as a time' % in_s)


class Test(unittest.TestCase):
    def test(self):
        self.assertEquals(parse('2012'), date(2012, 1, 1))
        self.assertEquals(parse('2012-05-03'), date(2012, 5, 3))
        self.assertEquals(parse('20120503'), date(2012, 5, 3))
        self.assertEquals(parse('2012-05'), date(2012, 5, 1))

        # week numbers
        self.assertEquals(parse('2012-W05'), date(2012, 1, 30))
        self.assertEquals(parse('2012W05'), date(2012, 1, 30))
        self.assertEquals(parse('2012-W05-5'), date(2012, 2, 3))
        self.assertEquals(parse('2012W055'), date(2012, 2, 3))

        # ordinal days
        self.assertEquals(parse('2012-007'), date(2012, 1, 7))
        self.assertEquals(parse('2012007'), date(2012, 1, 7))

        # times
        self.assertEquals(parse('00:00'), time(0, 0))
        self.assertEquals(parse('12:04:23'), time(12, 4, 23))
        self.assertEquals(parse('120423'), time(12, 4, 23))
        self.assertEquals(parse('12:04'), time(12, 4, 0))
        self.assertEquals(parse('1204'), date(1204, 1, 1))
        self.assertEquals(parse_time('1204'), time(12, 4, 0))
        self.assertEquals(parse('12'), time(12, 0, 0))
        self.assertEquals(parse('02'), time(2, 0, 0))
        self.assertEquals(parse('12:04:23.450686'), time(12, 4, 23, 450686))

        # combined
        self.assertEquals(parse('2008-09-03T20:56:35.450686'), datetime(2008, 9, 3, 20, 56, 35, 450686))
        self.assertEquals(parse('2008-09-03T20:56:35.450686Z'), datetime(2008, 9, 3, 20, 56, 35, 450686, TimeZone(timedelta())))
        self.assertEquals(parse('2008-09-03T20:56:35.450686+01'), datetime(2008, 9, 3, 20, 56, 35, 450686, TimeZone(timedelta(minutes=60))))
        self.assertEquals(parse('2008-09-03T20:56:35.450686+0100'), datetime(2008, 9, 3, 20, 56, 35, 450686, TimeZone(timedelta(minutes=60))))
        self.assertEquals(parse('2008-09-03T20:56:35.450686+01:30'), datetime(2008, 9, 3, 20, 56, 35, 450686, TimeZone(timedelta(minutes=60+30))))
        self.assertEquals(parse('2008-09-03T20:56:35.450686-01:30'), datetime(2008, 9, 3, 20, 56, 35, 450686, TimeZone(timedelta(minutes=-(60+30)))))
        self.assertEqual(parse('2013-03-28T02:30:24+00:00'), datetime(2013, 3, 28, 2, 30, 24, tzinfo=TimeZone(timedelta(minutes=0))))

if __name__ == '__main__':
    unittest.main()