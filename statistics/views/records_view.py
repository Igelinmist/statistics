from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import permission_required
from datetime import datetime

from django.http import JsonResponse

from statistics.models.journal import Journal
from statistics.forms import RecordForm


def records(request, journal_id):
    journal = get_object_or_404(Journal, pk=journal_id)
    record_list = journal.record_set.order_by('-date').all()
    paginator = Paginator(record_list, 25)

    page = request.GET.get('page')
    try:
        records = paginator.page(page)
    except PageNotAnInteger:
        records = paginator.page(1)
    except EmptyPage:
        records = paginator.page(paginator.num_pages)
    return render(
        request,
        'statistics/records.html',
        {'records': records, 'journal': journal})


@permission_required('statistics.create_journal_record',
                     login_url='iplant_login')
def record_create(request, journal_id):
    journal = get_object_or_404(Journal, pk=journal_id)
    form = RecordForm(request.POST or None, journal=journal)
    if request.POST and form.is_valid():
        journal.set_record_data(form.cleaned_data)
        return redirect('statistics:show', journal_id=journal_id)
    return render(request,
                  'statistics/record_form.html',
                  {'form': form, 'journal': journal, 'record_id': None})


@permission_required('statistics.create_journal_record',
                     login_url='iplant_login')
def simple_record_create(request, journal_id):
    if request.is_ajax():
        journal = get_object_or_404(Journal, pk=journal_id)
        record_fields = ('date', 'work', 'pusk_cnt', 'ostanov_cnt')
        data = {key: request.POST[key] for key in record_fields}
        data['date'] = datetime.strptime(request.POST['date'], '%d.%m.%Y')
        rec = journal.set_record_data(
            data,
            record_id=request.POST.get('record_id', None),
            process_ext_states=False)
        response = {'journal_id': journal.id,
                    'work': rec.work,
                    'rec_id': rec.id,
                    }
    else:
        response = "not AJAX!"
    return JsonResponse(response)


@permission_required('statistics.edit_journal_record',
                     login_url='iplant_login')
def record_update(request, journal_id, record_id):
    journal = get_object_or_404(Journal, pk=journal_id)
    form = RecordForm(request.POST or journal.get_record_data(record_id),
                      journal=journal)
    if request.POST and form.is_valid():
        journal.set_record_data(form.cleaned_data, record_id)
        return redirect('statistics:show', journal_id=journal_id)
    return render(request,
                  'statistics/record_form.html',
                  {'form': form, 'journal': journal, 'record_id': record_id})


@permission_required('statistics.delete_journal_record',
                     login_url='iplant_login')
def record_delete(request, journal_id, record_id):
    template_name = 'statistics/confirm_record_delete.html'
    journal = get_object_or_404(Journal, pk=journal_id)
    if request.method == 'POST':
        journal.delete_record(record_id)
        return redirect('statistics:show', journal_id=journal_id)
    return render(request, template_name)
