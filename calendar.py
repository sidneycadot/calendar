"""This module provides functions to calculate with dates in the Julian and Gregorian calendars."""

#pylint: disable=invalid-name

import enum
from typing import Tuple


class Calendar(enum.Enum):
    """Define calendar systems that the functions below are designed to handle.

    We handle the *proleptic* Julian and Gregorian calendars, meaning that we extend
    them to the time before their introduction.
    """
    JULIAN = 1
    GREGORIAN = 2


def is_divisible_by(a: int, b: int) -> bool:
    """Return True if the first argument is divisible by the second argument, and False if not."""
    return a % b == 0


def is_leapyear(Y: int, calendar: Calendar) -> bool:
    """Return True iff Y is a leapyear according to the rules of the Julian calendar."""

    # The year -1 (1 BCE) is followed directly by +1 (1 CE); year 0 is invalid.
    if Y == 0:
        raise ValueError("Invalid year 0 specified.")

    # Handle the absence of year 0 by incrementing BCE years by one,
    # so the years increment smoothly.
    if Y < 0:
        Y += 1

    if calendar == Calendar.GREGORIAN:
        return is_divisible_by(Y, 4) ^ is_divisible_by(Y, 100) ^ is_divisible_by(Y, 400)

    if calendar == Calendar.JULIAN:
        return is_divisible_by(Y, 4)

    raise ValueError("Unhandled calendar: {}".format(calendar))


def length_of_month(Y: int, M: int, calendar: Calendar) -> int:
    """Return the length of month M in year Y.

    This function uses 'is_leapyear_func' to determine if the year is a leapyear, if needed."""

    # The months January, March, May, July, August, October, and December have 31 days.
    if M in (1, 3, 5, 7, 8, 10, 12):
        return 31

    # The months April, June, September, and November have 30 days.
    if M in (4, 6, 9, 11):
        return 30

    # The month February has 29 days in leap years, 28 days in normal years.
    return 29 if is_leapyear(Y, calendar) else 28


def next_calendar_day(Y: int, M: int, D, calendar: Calendar) -> Tuple[int, int, int]:
    """Calculate the next calendar day of a given calendar day."""
    if D == length_of_month(Y, M, calendar):
        D = 0
        if M == 12:
            M = 0
            if Y == -1:
                Y = 0
            Y += 1
        M += 1
    D += 1
    return (Y, M, D)


def calendar_date_to_julian_day_number(Y, M, D, calendar: Calendar=Calendar.GREGORIAN) -> int:
    """Calculate the Julian day number of a date expressed in the proleptic Julian calendar."""

    # The year -1 (1 BCE) is followed directly by +1 (1 CE); year 0 is invalid.
    if Y == 0:
        raise ValueError("Invalid year 0 specified.")

    # Handle the absence of year 0 by incrementing BCE years by one,
    # so the years increment smoothly.
    if Y < 0:
        Y += 1

    # Start the year in March, moving February (and its leap day, if present)
    # to the end of the year.
    M -= 3
    if M < 0:
        M += 12
        Y -= 1

    # Days before month M, for a year starting in March.
    days_before_month = (0, 31, 61, 92, 122, 153, 184, 214, 245, 275, 306, 337)

    # Calculate the offset of the Gregorian calendar relkative to the Julian calendar.
    gregorian_offset = 2 - (Y // 100) + (Y // 400) if calendar == Calendar.GREGORIAN else 0

    # Calculate and return the Julian day number.
    return 1721117 + (Y * 365) + (Y // 4) + gregorian_offset + days_before_month[M] + D


def julian_day_number_to_sidney_date(jd):
    """test function."""
    years = jd // 365
    jd -= years * 365

    assert 0 <= jd <= 365

    if jd < 0:
        pass
