from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .models import Journal
from .forms import RecordForm


def new_record(request, journal_id):
    journal = get_object_or_404(Journal, pk=journal_id)
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            journal.get_record(form.cleaned_data)
            return HttpResponse(form.cleaned_data)
    else:
        form = RecordForm()

    return render(request,
                  'statistics/record_form.html',
                  {'form': form, 'journal': journal})


def index(request):
    journals = Journal.objects.all()
    context = {'journals': journals}
    return render(request, 'statistics/index.html', context)


def show(request, journal_id):
    journal = get_object_or_404(Journal, pk=journal_id)
    record_list = journal.record_set.all()
    return render(
        request,
        'statistics/show.html',
        {'journal': journal, 'record_list': record_list})
