import datetime as dt


def compute_days_elapsed(date_entered, current_date):
    """Computes the number of weekdays (Mondays, Tuesdays, Wednesdays,
    Thursdays, and Fridays) that have elapsed between two dates. This is used by
    Odin to compute how long a position has been held in the portfolio.

    Parameters
    ----------
    date_entered: Datetime object.
        The date of origination, which is used as a starting point for computing
        the number of business days elapsed.
    current_date: Datetime object.
        The end date of the time series, which marks the date at which the
        number of days elapsed ends.
    """
    # Compute the weekday for the two provided dates. Zero is Monday and six is
    # Sunday.
    from_weekday = date_entered.weekday()
    to_weekday = current_date.weekday()
    # If start date is after Friday, modify it to Monday
    if from_weekday > 4:
        from_weekday = 0
        corr = 7 - date_entered.weekday()
        date_entered = date_entered + dt.timedelta(days=corr)

    # Compute the number of weekdays between the specified weekdays
    day_diff = to_weekday - from_weekday
    # Compute the number of whole weeks that have elapsed between the two dates.
    # We assume that there are five work days in each whole week.
    whole_weeks = (
        ((current_date.date() - date_entered.date()).days - day_diff) / 7
    )
    workdays_in_whole_weeks = whole_weeks * 5
    # Return the number of weekdays elapsed between the two dates.
    beginning_end_correction = (
        min(day_diff, 5) - (max(current_date.weekday() - 4, 0) % 5)
    )
    return max(workdays_in_whole_weeks + beginning_end_correction, 0)
