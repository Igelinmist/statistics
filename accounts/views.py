from django.shortcuts import render


def profile_show(request):
    return render(request, 'accounts/home.html')


def profile_edit(request):
    return render(request, 'accounts/home.html')
