from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views import generic

from .models import Journal, STATE_CHOICES, PERIOD_IN_CHOICES
from .forms import RecordForm


def get_record(request, journal_id):
    journal = get_object_or_404(Journal, pk=journal_id)
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            return HttpResponse("Good record!")
    else:
        form = RecordForm()

    return render(request,
                  'statistics/record.html',
                  {'form': form, 'journal': journal})


class IndexView(generic.ListView):
    template_name = 'statistics/index.html'
    context_object_name = 'journal_list'

    def get_queryset(self):
        return Journal.objects.all()


def show(request, journal_id):
    return HttpResponse("Hello! Let's view Journal Lines")


def edit(request, journal_id):
    return HttpResponse("Let's write some stats")


def create(request, journal_id):
    return HttpResponse("Action create")


def record_create(request, journal_id):
    journal = get_object_or_404(Journal, pk=journal_id)
    return render(request, 'statistics/record_form.html', {
                  'journal': journal,
                  'choices': STATE_CHOICES,
                  'periods': PERIOD_IN_CHOICES,
                  })
