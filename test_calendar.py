#! /usr/bin/env -S python3 -B

"""Unit test for the calendar functions."""

#pylint: disable=invalid-name

import unittest

from calendar import Calendar, calendar_date_to_julian_day_number, next_calendar_day, is_divisible_by


class TestCalendarFunctionality(unittest.TestCase):
    """Test the calendar functionality."""

    def test_all(self):
        """Test calendar functions."""

        (GY, GM, GD) = (-4714, 11, 24)
        (JY, JM, JD) = (-4713,  1,  1)
        jd = 0

        while GY <= 9999:

            jd_from_julian_date = calendar_date_to_julian_day_number(JY, JM, JD, Calendar.JULIAN)
            jd_from_gregorian_date = calendar_date_to_julian_day_number(GY, GM, GD, Calendar.GREGORIAN)

            self.assertEqual(jd_from_julian_date, jd)
            self.assertEqual(jd_from_gregorian_date, jd)

            show = False

            if (GM, GD) == (1, 1):
                if GY in (-4713, -1, +1) or is_divisible_by(GY, 1000):
                    show = True

            if (jd_from_julian_date == 0) or (jd_from_gregorian_date == 0):
                show = True

            if show:
                print("gregorian {:5d}-{:02d}-{:02d} julian {:5d}-{:02d}-{:02d} julian_day {:7d}".format(GY, GM, GD, JY, JM, JD, jd))

            (GY, GM, GD) = next_calendar_day(GY, GM, GD, Calendar.GREGORIAN)
            (JY, JM, JD) = next_calendar_day(JY, JM, JD, Calendar.JULIAN)

            jd += 1


if __name__ == "__main__":
    unittest.main()
