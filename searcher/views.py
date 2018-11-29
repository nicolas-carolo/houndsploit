from django.shortcuts import render, redirect
from searcher.search_engine import search_exploits_in_db


def get_results_table(request):
    if request.POST and request.POST['search_item'] != "":
        search_text = request.POST['search_item']
        return render(request, "results_table.html", {'searched_item': str(search_text),
                                                      'results': search_exploits_in_db(search_text),
                                                      'n_results': len(search_exploits_in_db(search_text))})
    else:
        return render(request, 'results_table.html')


def home_page(request):
    if request.POST and request.POST['search_item'] != "":
        search_text = request.POST['search_item']
        return render(request, "results_table.html", {'searched_item': str(search_text),
                                                      'results': search_exploits_in_db(search_text),
                                                      'n_results': len(search_exploits_in_db(search_text))})
    else:
        return render(request, 'home.html')

