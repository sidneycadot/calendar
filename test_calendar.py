#! /usr/bin/env -S python3 -B

"""Unit test for the calendar functions."""

#pylint: disable=line-too-long, invalid-name

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

    def test_julian_start_of_year(self):
        """Test routine to obtain the 1st of March date of a regularized year in the Julian calendar."""

        for year in range(-50000, +50000):
            if year == 0:
                continue

            regularized_year = year if year > 0 else year + 1

            j1 = JulianCalendarDate.to_julian_day_number(regularized_year)
            j2 = int(JulianCalendarDate(year, 3, 1))

            self.assertEqual(j1, j2)

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

    def test_gregorian_start_of_year(self):
        """Test routine to obtain the 1st of March date of a regularized year in the Gregorian calendar."""

        for year in range(-50000, +50000):
            if year == 0:
                continue

            regularized_year = year if year > 0 else year + 1

            g1 = GregorianCalendarDate.to_julian_day_number(regularized_year)
            g2 = int(GregorianCalendarDate(year, 3, 1))

            self.assertEqual(g1, g2)


if __name__ == "__main__":
    unittest.main()
