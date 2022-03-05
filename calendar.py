"""This module provides functions to work with dates in the Julian and Gregorian calendars."""

#pylint: disable=line-too-long

def is_divisible_by(k: int, divider: int) -> bool:
    """Return True if the first argument is divisible by the second argument, and False if not."""
    return k % divider == 0


class AbstractCalendarDate:
    """This is the base class of both the JulianCalendarDate and GregorianCalendarDate classes."""

    # Days before month M, for a year starting in March.
    # This table is used to convert between dates and julian day numbers.
    days_before_month = (0, 31, 61, 92, 122, 153, 184, 214, 245, 275, 306, 337)

    def __init__(self, year: int, month: int, day: int):
        """Generic initialization of a calendar date (Gregorian or Julian)."""
        valid_date = (year != 0) and (1 <= month <= 12) and (1 <= day <= self.length_of_month(year, month))
        if not valid_date:
            raise ValueError()

        self.year  = year
        self.month = month
        self.day   = day

    def __iter__(self):
        """When using a CalendarDate as an iterator, it will yield the year, month, and day, in that order.

        This makes it possible to convert a date to a tuple, for example.
        """
        yield self.year
        yield self.month
        yield self.day

    def __repr__(self) -> str:
        """String representation of a calendar date (Gregorian or Julian)."""
        return "{}(year = {}, month = {}, day = {})".format(self.__class__.__name__, *self)

    def __eq__(self, rhs: 'AbstractCalendarDate') -> bool:
        """Return True if the date types and dates match, False if otherwise."""
        return (self.__class__ is rhs.__class__) and (tuple(self) == tuple(rhs))

    def __next__(self) -> 'AbstractCalendarDate':
        """Calculate the next calendar day."""
        (year, month, day) = self

        if day == self.length_of_month(year, month):
            day = 0
            if month == 12:
                month = 0
                if year == -1:
                    year = 0
                year += 1
            month += 1
        day += 1

        return self.__class__(year, month, day)


    @staticmethod
    def is_leapyear(year: int) -> bool:
        """This abstract method is implemented in the derived classes."""
        raise NotImplementedError()

    @classmethod
    def length_of_month(cls, year: int, month: int) -> int:
        """Return the length of the specified month in the specified year, in the Julian calendar."""

        valid_month = (year != 0) and (1 <= month <= 12)
        if not valid_month:
            raise ValueError()

        # The months January, March, May, July, August, October, and December have 31 days.
        if month in (1, 3, 5, 7, 8, 10, 12):
            return 31

        # The months April, June, September, and November have 30 days.
        if month in (4, 6, 9, 11):
            return 30

        # The month February has 29 days in leap years, 28 days in normal years.
        return 29 if cls.is_leapyear(year) else 28


class JulianCalendarDate(AbstractCalendarDate):
    """Represent a Julian calendar date."""

    @staticmethod
    def is_leapyear(year: int) -> bool:
        """Return True iff the year is a leapyear according to the rules of the Julian calendar."""

        # The year -1 (1 BCE) is followed directly by +1 (1 CE); year 0 is invalid.
        if year == 0:
            raise ValueError()

        # Handle the absence of year 0 by incrementing BCE years by one,
        # so the years increment smoothly.
        if year < 0:
            year += 1

        return is_divisible_by(year, 4)

    def __int__(self) -> int:
        """Convert a Julian calendar date to a Julian day number."""

        (year, month, day) = self

        # Handle the absence of year 0 by incrementing BCE years by one,
        # so the years increment smoothly.
        if year < 0:
            year += 1

        # Start the year in March, moving February (and its leap day, if present)
        # to the end of the year.
        month -= 3
        if month < 0:
            month += 12
            year -= 1

        # Calculate and return the Julian day number.
        return 1721117 + (year * 365) + (year // 4) + AbstractCalendarDate.days_before_month[month] + day


    @staticmethod
    def from_julian_day_number(jday: int) -> 'JulianCalendarDate':
        """Convert a Julian day number to a Julian calendar date."""

        year  = 0
        jday -= 1721118

        # Handle (subtract) 4-year periods.

        periods = jday // 1461  # May be negative.

        year +=    4 * periods
        jday -= 1461 * periods

        # Handle (subtract) up to three 1-year periods.

        periods = min(jday // 365, 3)

        year +=       periods
        jday -= 365 * periods

        # Handle months.

        for month in range(12):
            if month == 11 or jday < AbstractCalendarDate.days_before_month[month + 1]:
                jday -= AbstractCalendarDate.days_before_month[month]
                break

        day = jday + 1

        # Move start-of-year from March to January.

        month += 3
        if month > 12:
            month -= 12
            year  += 1

        # Skip over year 0.

        if year <= 0:
            year -= 1

        return JulianCalendarDate(year, month, day)


class GregorianCalendarDate(AbstractCalendarDate):
    """Represent a Gregorian calendar date."""

    @staticmethod
    def is_leapyear(year: int) -> bool:
        """Return True iff the year is a leapyear according to the rules of the Gregorian calendar."""

        # The year -1 (1 BCE) is followed directly by +1 (1 CE); year 0 is invalid.
        if year == 0:
            raise ValueError()

        # Handle the absence of year 0 by incrementing BCE years by one,
        # so the years increment smoothly.
        if year < 0:
            year += 1

        return is_divisible_by(year, 4) ^ is_divisible_by(year, 100) ^ is_divisible_by(year, 400)

    def __int__(self) -> int:
        """Convert a Gregorian calendar date to a Julian day number."""

        (year, month, day) = self

        # Handle the absence of year 0 by incrementing BCE years by one,
        # so the years increment smoothly.
        if year < 0:
            year += 1

        # Start the year in March, moving February (and its leap day, if present)
        # to the end of the year.
        month -= 3
        if month < 0:
            month += 12
            year  -= 1

        # Calculate and return the Julian day number.
        return 1721119 + (year * 365) + (year // 4) - (year // 100) + (year // 400) + AbstractCalendarDate.days_before_month[month] + day

    @staticmethod
    def from_julian_day_number(jday: int) -> 'GregorianCalendarDate':
        """Convert a Julian day number to a Gregorian calendar date."""

        year  = 0
        jday -= 1721120

        # Handle (subtract) 400-year periods.

        periods = jday // 146097  # May be negative.

        year +=    400 * periods
        jday -= 146097 * periods

        # Handle (subtract) up to three 100-year periods.

        periods = min(jday // 36524, 3)

        year +=   100 * periods
        jday -= 36524 * periods

        # Handle (subtract) 4-year periods.

        periods = jday // 1461

        year +=    4 * periods
        jday -= 1461 * periods

        # Handle (subtract) up to three 1-year periods.

        periods = min(jday // 365, 3)

        year +=       periods
        jday -= 365 * periods

        # Handle months.

        for month in range(12):
            if month == 11 or jday < AbstractCalendarDate.days_before_month[month + 1]:
                jday -= AbstractCalendarDate.days_before_month[month]
                break

        day = jday + 1

        # Move start-of-year from March to January.

        month += 3
        if month > 12:
            month -= 12
            year  += 1

        # Skip over year 0.

        if year <= 0:
            year -= 1

        return GregorianCalendarDate(year, month, day)
