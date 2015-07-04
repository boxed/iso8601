[![Build Status](https://travis-ci.org/boxed/iso8601.svg?branch=master)](https://travis-ci.org/boxed/iso8601)

ISO8601
=======

Implementation of (most of) the ISO 8601 specification. Just call `iso8601.parse()` with your string in any format and it will be auto detected.

Supports
-----------------
- Naive times
- Timezone information (specified as offsets or as Z for 0 offset)
- Year
- Year-month
- Year-month-date
- Year-week
- Year-week-weekday
- Year-ordinal day
- Hour
- Hour-minute
- Hour-minute
- Hour-minute-second
- Hour-minute-second-microsecond
- All combinations of the three "families" above!

Not supported formats
---------------------
- Time durations
- Time intervals
- Repeating intervals
