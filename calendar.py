"""This module provides classes that represent dates in the Julian and Gregorian calendars."""

# pylint: disable=line-too-long


def is_divisible_by(num: int, divider: int) -> bool:
    """Return True if the first argument is divisible by the second argument, and False if not."""
    return num % divider == 0


def normalize_year(year: int) -> int:
    """Normalize year for the lack of a year zero.

    In Julian and Gregorian calendar dates, year zero is never used; the year 1 BCE (-1) is
    followed directly by the year 1 CE (+1). This discontinuity makes the calculations more
    cumbersome than they should be.

    For that reason, we increment BCE years by 1, making the year sequence continuous.
    We call the resulting year number a 'normalized year'.
    """
    if year == 0:
        raise ValueError("Year zero does not exist, so cannot be normalized.")

    return year if year > 0 else year + 1


class AbstractCalendarDate:
    """This is the base class of the JulianCalendarDate and GregorianCalendarDate classes.

    It implements the common functionality shared by these two calendar classes.

    The AbstractCalendarDate should not be instantiated directly.
    """

    # pylint: disable=no-member

    # Days before a month, for a 12-month year starting in March.
    # This table is used to convert between dates and Julian day numbers.
    _days_before_month = (0, 31, 61, 92, 122, 153, 184, 214, 245, 275, 306, 337)

    def __init__(self, year: int, month: int, day: int):
        """Generic initialization of a calendar date (Gregorian or Julian)."""
        valid_date = (year != 0) and (1 <= month <= 12) and (1 <= day <= self.length_of_month(year, month))
        if not valid_date:
            raise ValueError("Attempt to initialize an invalid date.")

        self.year  = year
        self.month = month
        self.day   = day

    def __iter__(self):
        """When using a CalendarDate as an iterator, it will yield the year, month, and day, in that order.

        This makes it possible to convert a date to a tuple, for example.
        """
        yield from (self.year, self.month, self.day)

    def __repr__(self) -> str:
        """String representation of a calendar date."""
        return "{}(year = {}, month = {}, day = {})".format(self.__class__.__name__, *self)

    # Below, we provide implementations for the six comparison operators in Python.
    #
    # We do comparison based on the underlying days denoted by the calendar dates, and we
    # ignore the difference between the types (JulianCalendarDate, GregorianCalendarDate).
    #
    # Thus, a JulianCalendarDate may compare equal to a GregorianCalendarDate, e.g.,
    # the comparison
    #
    #   JulianCalendarDate(1752, 9, 2) == GregorianCalendarDate(1752, 9, 13)
    #
    # will evaluate as True.
    #
    # This interpretation of equality is consistent with what is done in Python for
    # numeric types; there, too, the values are compared and not their representations;
    # e.g. the integer 3 (int) == 3.0 (float).

    def __lt__(self, rhs: 'AbstractCalendarDate') -> bool:
        """Return True if the lhs date is strictly before the rhs date, False otherwise."""
        return self.to_julian_day_number() < rhs.to_julian_day_number()

    def __le__(self, rhs: 'AbstractCalendarDate') -> bool:
        """Return True if the lhs date is before or on the rhs date, False otherwise."""
        return self.to_julian_day_number() <= rhs.to_julian_day_number()

    def __eq__(self, rhs: 'AbstractCalendarDate') -> bool:
        """Return True if the lhs date is on the same day as the right hand side day, False otherwise."""
        return self.to_julian_day_number() == rhs.to_julian_day_number()

    def __ne__(self, rhs: 'AbstractCalendarDate') -> bool:
        """Return True if the lhs date is not on the same day as the right hand side day, False otherwise."""
        return self.to_julian_day_number() != rhs.to_julian_day_number()

    def __gt__(self, rhs: 'AbstractCalendarDate') -> bool:
        """Return True if the lhs date strictly after the right hand side day, False otherwise."""
        return self.to_julian_day_number() > rhs.to_julian_day_number()

    def __ge__(self, rhs: 'AbstractCalendarDate') -> bool:
        """Return True if the lhs date is on or after the right hand side day, False otherwise."""
        return self.to_julian_day_number() >= rhs.to_julian_day_number()

    def __next__(self) -> 'AbstractCalendarDate':
        """Calculate the next calendar day.

        Note that this method skips over the year zero.
        """
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
        """Return if the year is a leapyear according to the calendar's leapyear rule."""
        normalized_year = normalize_year(year)
        return cls._leapyear_rule(normalized_year)

    @classmethod
    def length_of_month(cls, year: int, month: int) -> int:
        """Return the length of the specified month in the specified year."""

        valid_month = (year != 0) and (1 <= month <= 12)
        if not valid_month:
            raise ValueError("Invalid month specified.")

        # The months January, March, May, July, August, October, and December have 31 days.
        # The months April, June, September, and November have 30 days.
        # The month February has 28 days in a regular year and 29 days in a leapyear.
        return (29 if cls.is_leapyear(year) else 28) if month == 2 else (30 if month in (4, 6, 9, 11) else 31)

    def to_julian_day_number(self) -> int:
        """Convert a calendar date to a Julian day number."""

        (year, month, day) = self

        normalized_year = normalize_year(year)

        # Start the year in March, moving January and February (and its leap day, if present)
        # to the end of the previous year.
        month -= 3
        if month < 0:
            month += 12
            normalized_year -= 1

        day -= 1

        # Calculate and return the Julian day number.
        return self._year_julian_day_number(normalized_year) + AbstractCalendarDate._days_before_month[month] + day

    @classmethod
    def from_julian_day_number(cls, julian_day_number: int) -> 'AbstractCalendarDate':
        """Convert a Julian day number to a calendar date."""

        # We perform our calculations with years that start in March. The advantage of this is that
        # February will be the last month in the year, and its leapday (if present) will be the last
        # day of the year. This simplifies the calculations.

        # "Day zero" for our calculations will be March 1st in the year 1 BCE, which is our 'year zero'.

        year = 0
        julian_day_number -= cls._year_julian_day_number(0)

        # Perform the reductions for the leap-year periods.

        for (period_days, period_years, max_periods) in cls._leapyear_periods:
            periods = julian_day_number // period_days
            if max_periods is not None and periods > max_periods:
                periods = max_periods
            year += periods * period_years
            julian_day_number -= periods * period_days

        # Handle months.

        for month in range(12):
            if month == 11 or julian_day_number < AbstractCalendarDate._days_before_month[month + 1]:
                julian_day_number -= AbstractCalendarDate._days_before_month[month]
                break

        day = julian_day_number + 1

        # Move start-of-year from March to January.

        month += 3
        if month > 12:
            month -= 12
            year += 1

        # Skip over year 0 ("un-normalize" the year).

        if year <= 0:
            year -= 1

        return cls(year, month, day)


class JulianCalendarDate(AbstractCalendarDate):
    """Represent a date in the proleptic Julian calendar."""

    _leapyear_periods = ((1461, 4, None), (365, 1, 3))

    @staticmethod
    def _leapyear_rule(normalized_year: int) -> bool:
        """Is the normalized year is a leapyear, according to the Julian calendar?"""
        return is_divisible_by(normalized_year, 4)

    @staticmethod
    def _year_julian_day_number(normalized_year: int) -> int:
        """Calculate the Julian day number of March 1st of a normalized year, according to the Julian calendar."""
        return 1721118 + (normalized_year * 365) + (normalized_year // 4)


class GregorianCalendarDate(AbstractCalendarDate):
    """Represent a date in the proleptic Gregorian calendar."""

    _leapyear_periods = ((146097, 400, None), (36524, 100, 3), (1461, 4, None), (365, 1, 3))

    @staticmethod
    def _leapyear_rule(normalized_year: int) -> bool:
        """Is the normalized year a leapyear, according to the Gregorian calendar?"""
        return is_divisible_by(normalized_year, 4) ^ is_divisible_by(normalized_year, 100) ^ is_divisible_by(normalized_year, 400)

    @staticmethod
    def _year_julian_day_number(normalized_year: int) -> int:
        """Calculate the Julian day number of March 1st of a normalized year, according to the Gregorian calendar."""
        return 1721120 + (normalized_year * 365) + (normalized_year // 4) - (normalized_year // 100) + (normalized_year // 400)
