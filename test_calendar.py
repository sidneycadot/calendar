#! /usr/bin/env -S python3 -B

"""Unit test for the calendar functions."""

#pylint: disable=invalid-name

import unittest

from calendar import JulianCalendarDate, GregorianCalendarDate


class TestCalendarFunctionality(unittest.TestCase):
    """Test the calendar functionality."""

    def test_julian_calendar_functionality(self):
        """Test Julian calendar functionality."""

        julian_date = JulianCalendarDate(-4713,  1,  1)
        jd = 0

        while julian_date.year <= 9999:

            jd_from_julian_date = int(julian_date)

            self.assertEqual(jd_from_julian_date, jd)

            julian_date_from_jd = JulianCalendarDate.from_julian_day_number(jd)

            self.assertEqual(julian_date, julian_date_from_jd)

            julian_date = next(julian_date)
            jd += 1

    def test_gregorian_calendar_functionality(self):
        """Test Gregorian calendar functionality."""

        gregorian_date = GregorianCalendarDate(-4714,  11,  24)
        jd = 0

        while gregorian_date.year <= 9999:

            jd_from_gregorian_date = int(gregorian_date)

            self.assertEqual(jd_from_gregorian_date, jd)

            gregorian_date_from_jd = GregorianCalendarDate.from_julian_day_number(jd)

            self.assertEqual(gregorian_date, gregorian_date_from_jd)

            gregorian_date = next(gregorian_date)
            jd += 1


if __name__ == "__main__":
    unittest.main()
