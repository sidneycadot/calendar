#! /usr/bin/env -S python3 -B

"""Unit test for the calendar functions."""

#pylint: disable=line-too-long, invalid-name

import unittest

from calendar import JulianCalendarDate, GregorianCalendarDate


class TestJulianCalendarDate(unittest.TestCase):
    """Test the Julian calendar date functionality."""

    def test_conversion_to_and_from_julian_day_number(self):
        """Test conversion of a Julian calendar date to a Julian day number and vice versa."""

        # Julian day 0 is January 1st, 4713 BCE in the proleptic Julian calendar.
        julian_date = JulianCalendarDate(-4713,  1,  1)
        julian_day_number = 0

        # Iterate over days up to the year 5000.
        while julian_date.year < 5000:

            julian_day_number_from_julian_date = int(julian_date)

            self.assertEqual(julian_day_number_from_julian_date, julian_day_number)

            julian_date_from_julian_day_number = JulianCalendarDate.from_julian_day_number(julian_day_number)

            self.assertEqual(julian_date, julian_date_from_julian_day_number)

            julian_date = next(julian_date)
            julian_day_number += 1

    def test_year_julian_day_number(self):
        """Verify that the '_year_julian_day_number' method yields the Julian day number of March 1st.

        Note: this test presumes that the calendar methods are correct.
        """

        for year in range(-5000, +5001):
            if year == 0:
                continue  # Skip non-existing year 0.

            normalized_year = year if year > 0 else year + 1

            julian_day_number_1 = JulianCalendarDate._year_julian_day_number(normalized_year)
            julian_day_number_2 = int(JulianCalendarDate(year, 3, 1))

            self.assertEqual(julian_day_number_1, julian_day_number_2)


class TestGregorianCalendarDate(unittest.TestCase):
    """Test the Gregorian calendar date functionality."""

    def test_conversion_to_and_from_julian_day_number(self):
        """Test conversion of a Gregorian calendar date to a Julian day number and vice versa."""

        # Julian day 0 is November 24th, 4714 BCE in the proleptic Gregorian calendar.
        gregorian_date = GregorianCalendarDate(-4714,  11,  24)
        julian_day_number = 0

        # Iterate over days up to the year 5000.
        while gregorian_date.year <= 9999:

            julian_day_numberfrom_gregorian_date = int(gregorian_date)

            self.assertEqual(julian_day_numberfrom_gregorian_date, julian_day_number)

            gregorian_date_from_julian_day_number = GregorianCalendarDate.from_julian_day_number(julian_day_number)

            self.assertEqual(gregorian_date, gregorian_date_from_julian_day_number)

            gregorian_date = next(gregorian_date)
            julian_day_number += 1

    def test_year_julian_day_number(self):
        """Verify that the '_year_julian_day_number' method yields the Julian day number of March 1st.

        Note: this test presumes that the calendar methods are correct.
        """

        for year in range(-5000, +5001):
            if year == 0:
                continue  # Skip non-existing year 0.

            normalized_year = year if year > 0 else year + 1

            julian_day_number_1 = GregorianCalendarDate._year_julian_day_number(normalized_year)
            julian_day_number_2 = int(GregorianCalendarDate(year, 3, 1))

            self.assertEqual(julian_day_number_1, julian_day_number_2)


if __name__ == "__main__":
    unittest.main()
