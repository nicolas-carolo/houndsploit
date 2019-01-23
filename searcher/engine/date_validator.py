import datetime


def is_date_range_valid(start_date, end_date):
    if start_date is not None and end_date is not None:
        if start_date <= end_date <= datetime.datetime.now().date():
            return True
        else:
            return False
    else:
        if start_date is None and end_date is None:
            return True
        else:
            return False
