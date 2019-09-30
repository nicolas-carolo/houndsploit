def remove_duplicates_by_list(input_list):
    """
    Remove the duplicates from the input list
    :param input_list: the input list
    :return: the input list without duplicates
    """
    return list(dict.fromkeys(input_list))