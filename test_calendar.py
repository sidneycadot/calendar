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
        julian_day_number = 0

        while julian_date.year <= 9999:

            jd_from_julian_date = int(julian_date)

            self.assertEqual(jd_from_julian_date, julian_day_number)

            julian_date_from_julian_day_number = JulianCalendarDate.from_julian_day_number(julian_day_number)

            self.assertEqual(julian_date, julian_date_from_julian_day_number)

            julian_date = next(julian_date)
            julian_day_number += 1

    def test_julian_start_of_year(self):
        """Test routine to obtain the 1st of March date of a fixed year in the Julian calendar."""

        for year in range(-50000, +50001):
            if year == 0:
                continue  # Skip non-existing year 0.

            fixed_year = year if year > 0 else year + 1

            julian_day_number_1 = JulianCalendarDate.to_julian_day_number(fixed_year)
            julian_day_number_2 = int(JulianCalendarDate(year, 3, 1))

            self.assertEqual(julian_day_number_1, julian_day_number_2)

    def test_gregorian_calendar_functionality(self):
        """Test Gregorian calendar functionality."""

        gregorian_date = GregorianCalendarDate(-4714,  11,  24)
        julian_day_number = 0

        while gregorian_date.year <= 9999:

            jd_from_gregorian_date = int(gregorian_date)

            self.assertEqual(jd_from_gregorian_date, julian_day_number)

            gregorian_date_from_julian_day_number = GregorianCalendarDate.from_julian_day_number(julian_day_number)

            self.assertEqual(gregorian_date, gregorian_date_from_julian_day_number)

            gregorian_date = next(gregorian_date)
            julian_day_number += 1

    def test_gregorian_start_of_year(self):
        """Test routine to obtain the 1st of March date of a fixed year in the Gregorian calendar."""

        for year in range(-50000, +50001):
            if year == 0:
                continue  # Skip non-existing year 0.

            fixed_year = year if year > 0 else year + 1

            julian_day_number_1 = GregorianCalendarDate.to_julian_day_number(fixed_year)
            julian_day_number_2 = int(GregorianCalendarDate(year, 3, 1))

            self.assertEqual(julian_day_number_1, julian_day_number_2)


if __name__ == "__main__":
    unittest.main()
