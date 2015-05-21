from django.http import HttpResponse
from django.views import generic

from .models import Journal

# from django.shortcuts import render


class IndexView(generic.ListView):
    template_name = 'statistics/index.html'
    context_object_name = 'journal_list'

    def get_queryset(self):
        return Journal.objects.all()


def detail(request, journal_id):
    return HttpResponse("Hello! Let's view Journal Lines")


def write(request, journal_id):
    return HttpResponse("Let's write some stats")
