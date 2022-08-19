def remove_list_duplicates(input_list):
    """
    Remove the duplicates from the input list
    :param input_list: the input list
    :return: the input list without duplicates
    """
    return list(dict.fromkeys(input_list))


def join_lists(input_list_1, input_list_2):
    resulting_list = list(input_list_1)
    resulting_list.extend(x for x in input_list_2 if x not in resulting_list)
    return resulting_list
