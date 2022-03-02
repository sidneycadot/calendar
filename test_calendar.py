#! /usr/bin/env -S python3 -B

"""Unit test for the calendar functions."""

#pylint: disable=invalid-name

import unittest

from calendar import Calendar, calendar_date_to_julian_day_number, next_calendar_day, is_divisible_by, julian_day_number_to_julian_date


class TestCalendarFunctionality(unittest.TestCase):
    """Test the calendar functionality."""

    def test_all(self):
        """Test calendar functions."""

        julian_date    = (-4713,  1,  1)
        gregorian_date = (-4714, 11, 24)
        jd = 0

        while gregorian_date[0] <= 9999:

            jd_from_julian_date = calendar_date_to_julian_day_number(*julian_date, Calendar.JULIAN)
            jd_from_gregorian_date = calendar_date_to_julian_day_number(*gregorian_date, Calendar.GREGORIAN)

            self.assertEqual(jd_from_julian_date, jd)
            self.assertEqual(jd_from_gregorian_date, jd)

            julian_date_from_jd = julian_day_number_to_julian_date(jd)
            assert julian_date == julian_date_from_jd

            #show = False

            #if gregorian_date == (1, 1):
            #    if GY in (-4713, -1, +1) or is_divisible_by(GY, 1000):
            #        show = True

            #if (jd_from_julian_date == 0) or (jd_from_gregorian_date == 0):
            #    show = True

            #if show:
            #    print("gregorian {:5d}-{:02d}-{:02d} julian {:5d}-{:02d}-{:02d} julian_day {:7d}".format(*gregorian_date, *julian_date, jd))

            julian_date = next_calendar_day(*julian_date, Calendar.JULIAN)
            gregorian_date = next_calendar_day(*gregorian_date, Calendar.GREGORIAN)
            jd += 1


if __name__ == "__main__":
    unittest.main()
