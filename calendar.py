"""This module provides classes that represent dates in the Julian and Gregorian calendars."""

#pylint: disable=line-too-long

def is_divisible_by(k: int, divider: int) -> bool:
    """Return True if the first argument is divisible by the second argument, and False if not."""
    return k % divider == 0


def fix_year(year: int) -> int:
    """Correct year for the lack of a year zero.

    In dates, year zero is never used. The year -1 is followed by the year +1.
    This discontinuity makes the calculation more cumbersome than it should be.
    For that reason, we increase BCE years by 1, making the year sequence continuous.
    """
    if year == 0:
        raise ValueError()
    return year if year > 0 else year + 1


class AbstractCalendarDate:
    """This is the base class of the JulianCalendarDate and GregorianCalendarDate classes.

    It abstracts calendar systems with a 12-month year, with February being either 28 or 29 days long,
    that are distinguished in the way they classify years as leapyears.

    The AbstractCalendarDate is not intended to be instantiated; only its derived classes are.
    """

    # pylint: disable=no-member

    # Days before a month month, for a year starting in March.
    # This table is used to convert between dates and Julian day numbers.
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
        """When using an AbstractCalendarDate as an iterator, it will yield the year, month, and day, in that order.

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

    @classmethod
    def is_leapyear(cls, year: int) -> bool:
        """Return True iff the year is a leapyear according to the rules of the Julian calendar."""
        fixed_year = fix_year(year)
        return cls.leapyear_rule(fixed_year)

    @classmethod
    def length_of_month(cls, year: int, month: int) -> int:
        """Return the length of the specified month in the specified year, in the Julian calendar."""

        valid_month = (year != 0) and (1 <= month <= 12)
        if not valid_month:
            raise ValueError()

        # The months January, March, May, July, August, October, and December have 31 days.
        # The months April, June, September, and November have 30 days.
        # The month February has 28 days in a regular year and 29 days in a leapyear.
        return (29 if cls.is_leapyear(year) else 28) if month == 2 else 30 if month in (4, 6, 9, 11) else 31

    def __int__(self) -> int:
        """Convert a calendar date to a Julian day number."""

        (year, month, day) = self

        fixed_year = fix_year(year)

        # Start the year in March, moving February (and its leap day, if present)
        # to the end of the year.
        month -= 3
        if month < 0:
            month += 12
            fixed_year -= 1

        day -= 1

        # Calculate and return the Julian day number.
        return self.__class__.to_julian_day_number(fixed_year) + AbstractCalendarDate.days_before_month[month] + day

    @classmethod
    def from_julian_day_number(cls, julian_day_number: int) -> 'AbstractCalendarDate':
        """Convert a Julian day number to a calendar date."""

        year = 0
        julian_day_number -= cls.to_julian_day_number(0)

        for (period_days, period_years, limit) in cls._reductions:
            periods = julian_day_number // period_days
            if limit is not None:
                periods = min(periods, limit)
            year += periods * period_years
            julian_day_number -= periods * period_days

        # Handle months.

        for month in range(12):
            if month == 11 or julian_day_number < AbstractCalendarDate.days_before_month[month + 1]:
                julian_day_number -= AbstractCalendarDate.days_before_month[month]
                break

        day = julian_day_number + 1

        # Move start-of-year from March to January.

        month += 3
        if month > 12:
            month -= 12
            year += 1

        # Skip over year 0.

        if year <= 0:
            year -= 1

        return cls(year, month, day)


class JulianCalendarDate(AbstractCalendarDate):
    """Represent a date in the proleptic Julian calendar."""

    _reductions = ((1461, 4, None), (365, 1, 3))

    @staticmethod
    def leapyear_rule(fixed_year: int) -> bool:
        """Return True if the regularized year is a leapyear according to the Julian calendar, False if not."""
        return is_divisible_by(fixed_year, 4)

    @staticmethod
    def to_julian_day_number(fixed_year: int) -> int:
        """Return the Julian day number of March 1st according to the Julian calendar with regularized years."""
        return 1721118 + (fixed_year * 365) + (fixed_year // 4)


class GregorianCalendarDate(AbstractCalendarDate):
    """Represent a date in the proleptic Gregorian calendar."""

    _reductions = ((146097, 400, None), (36524, 100, 3), (1461, 4, None), (365, 1, 3))

    @staticmethod
    def leapyear_rule(fixed_year: int) -> bool:
        """Return True if the regularized year is a leapyear according to the Gregorian calendar, False if not."""
        return is_divisible_by(fixed_year, 4) ^ is_divisible_by(fixed_year, 100) ^ is_divisible_by(fixed_year, 400)

    @staticmethod
    def to_julian_day_number(fixed_year: int) -> int:
        """Return the Julian day number of March 1st according to the Gregorian calendar with regularized years."""
        return 1721120 + (fixed_year * 365) + (fixed_year // 4) - (fixed_year // 100) + (fixed_year // 400)
