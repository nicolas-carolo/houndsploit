from django.shortcuts import render, redirect


def home_page(request):
    if request.POST:
        print(request.POST['term'])
        return redirect("/")
    else:
        return render(request, 'home.html')
