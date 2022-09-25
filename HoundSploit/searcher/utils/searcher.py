from HoundSploit.searcher.utils.constants import N_RESULTS_FOR_PAGE

def get_n_needed_pages_for_showing_results(n_results):
    if n_results % N_RESULTS_FOR_PAGE == 0:
        return int(n_results / N_RESULTS_FOR_PAGE)
    else:
        return int(n_results / N_RESULTS_FOR_PAGE) + 1