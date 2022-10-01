from datetime import datetime

def sort_results(results_list, sorting_type):
    if sorting_type == "Oldest":
        return sort_results_by_date(results_list, False)
    elif sorting_type == "Description A-Z":
        return sort_results_alphabetically_on_description(results_list, False)
    elif sorting_type == "Description Z-A":
        return sort_results_alphabetically_on_description(results_list, True)
    else:
        return sort_results_by_date(results_list, True)


def sort_results_by_date(results_list, reverse_flag):
    return sorted(results_list, key=lambda result: datetime.strptime(result.date, "%Y-%m-%d"), reverse=reverse_flag)


def sort_results_alphabetically_on_description(results_list, reverse_flag):
    return sorted(results_list, key=lambda result: str(result.description).lower(), reverse=reverse_flag)