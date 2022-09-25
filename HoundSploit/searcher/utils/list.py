def join_lists(input_list_1, input_list_2):
    resulting_list = list(input_list_1)
    resulting_list.extend(x for x in input_list_2 if x not in resulting_list)
    return resulting_list

