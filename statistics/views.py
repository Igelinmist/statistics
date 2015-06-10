from django.shortcuts import get_object_or_404, render, redirect

from .models import Journal, Record
from .forms import RecordForm


def index(request):
    journals = Journal.objects.all()
    context = {'journals': journals}
    return render(request, 'statistics/index.html', context)


def show(request, journal_id):
    journal = get_object_or_404(Journal, pk=journal_id)
    record_list = journal.record_set.order_by('-date')[:10]
    return render(
        request,
        'statistics/show.html',
        {'journal': journal, 'record_list': record_list})


def record_create(request, journal_id):
    journal = get_object_or_404(Journal, pk=journal_id)
    form = RecordForm(request.POST or None, journal=journal)
    if request.POST and form.is_valid():
        journal.set_data(form.cleaned_data)
        return redirect('statistics:show', journal_id=journal_id)
    return render(request,
                  'statistics/record_form.html',
                  {'form': form, 'journal': journal, 'record_id': None})


def record_update(request, journal_id, record_id):
    journal = get_object_or_404(Journal, pk=journal_id)
    form = RecordForm(request.POST or Journal.get_data(record_id),
                      journal=journal)
    if request.POST and form.is_valid():
        journal.set_data(form.cleaned_data, record_id)
        return redirect('statistics:show', journal_id=journal_id)
    return render(request,
                  'statistics/record_form.html',
                  {'form': form, 'journal': journal, 'record_id': record_id})


def record_delete(request, journal_id, record_id):
    template_name = 'statistics/confirm_record_delete.html'
    record = get_object_or_404(Record, pk=record_id)
    journal = record.journal
    if request.method == 'POST':
        record.delete()
        # journal.update_state_cash()
        return redirect('statistics:show', journal_id=journal_id)
    return render(request, template_name)
