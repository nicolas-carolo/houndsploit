import datetime


def is_date_range_valid(start_date, end_date):
    """
    Check if the lower range value is smaller than the highest and if the two date are both in the past or in the
    present or if the two date fields are both void.
    :param start_date: the lower range value.
    :param end_date: the highest range value.
    :return: True only if the range is valid or the two fields are both void.
    """
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
