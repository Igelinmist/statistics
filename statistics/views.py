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


def record_create_or_edit(request, journal_id, record_id=None):
    form = RecordForm(request.POST or Journal.get_data(record_id))
    journal = get_object_or_404(Journal, pk=journal_id)
    if request.POST and form.is_valid():
        Journal.set_data(journal, form.cleaned_data, record_id)
        return redirect('statistics:show', journal_id=journal_id)
    return render(request,
                  'statistics/record_form.html',
                  {'form': form, 'journal': journal, 'record_id': record_id})


def record_delete(request, journal_id, record_id):
    template_name = 'statistics/confirm_record_delete.html'
    record = get_object_or_404(Record, pk=record_id)
    if request.method == 'POST':
        record.delete()
        return redirect('statistics:show', journal_id=journal_id)
    return render(request, template_name)
