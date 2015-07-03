from django.shortcuts import render


def account_show(request):
    return render(request, 'accounts:account_show')


def account_edit(request):
    return render(request, 'accounts:account_edit')
