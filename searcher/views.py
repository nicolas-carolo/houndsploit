from django.shortcuts import render, redirect
from searcher.models import Exploit


def home_page(request):
    if request.POST:
        search_string = 'select * from exploits where ' + request.POST['search_item']
        print(search_string)
        for exploit in Exploit.objects.raw(search_string):
            print(exploit.id, exploit.file, exploit.description)
        return redirect("/")
    else:
        return render(request, 'home.html')
