from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import permission_required
from datetime import datetime, timedelta

from django.http import JsonResponse

from statistics.models.journal import Journal
# from statistics.helpers import date2req

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
    # Подготовить форму либо на основе данных POST, либо
    # если этот словарь пустой, инициализировать новую форму
    form = RecordForm(request.POST or None, extended_stat=journal.extended_stat)
    # Рендерим форму если словарь POST пустой (пришли по GET),
    # проверяем и записываем данные, если пришли по POST
    if request.POST and form.is_valid():
        journal.set_record_data(form.cleaned_data)
        # если нажали кнопку Применить и выйти, то переходим к журналу
        if request.POST['submit'] == 'af':
            return redirect('statistics:show', journal_id=journal_id)
        # если Применить и меняется день:
        else:
            days_cnt = int(request.POST['submit'])
            new_date = datetime.strptime(request.POST['date'], '%d.%m.%Y') + timedelta(days_cnt)
            rec = journal.rec_on_date(new_date)
            if rec:
                return redirect(
                    'statistics:record_edit',
                    journal_id=journal.id,
                    record_id=rec.id,
                )
            else:
                form = RecordForm(
                    None,
                    extended_stat=journal.extended_stat,
                    initial={'date': new_date.strftime('%d.%m.%Y')}
                )
                return render(
                    request,
                    'statistics/record_form.html',
                    {'form': form, 'journal': journal, 'record_id': None})

    return render(request,
                  'statistics/record_form.html',
                  {'form': form, 'journal': journal, 'record_id': None})


@permission_required('statistics.edit_journal_record',
                     login_url='iplant_login')
def record_update(request, journal_id, record_id):
    journal = get_object_or_404(Journal, pk=journal_id)
    form = RecordForm(request.POST or journal.get_record_data(record_id),
                      extended_stat=journal.extended_stat)
    if request.POST and form.is_valid():
        journal.set_record_data(form.cleaned_data, record_id)
        # если нажали кнопку Применить и выйти, то переходим к журналу
        if request.POST['submit'] == 'af':
            return redirect('statistics:show', journal_id=journal_id)
        # если Применить и меняется день:
        else:
            days_cnt = int(request.POST['submit'])
            new_date = datetime.strptime(
                request.POST['date'], '%d.%m.%Y') + timedelta(days_cnt)
            rec = journal.rec_on_date(new_date)
            if rec:
                return redirect(
                    'statistics:record_edit',
                    journal_id=journal.id,
                    record_id=rec.id,
                )
            else:
                form = RecordForm(
                    None,
                    extended_stat=journal.extended_stat,
                    initial={'date': new_date.strftime('%d.%m.%Y')}
                )
                return render(request,
                              'statistics/record_form.html',
                              {'form': form, 'journal': journal, 'record_id': None})
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


@permission_required('statistics.create_journal_record',
                     login_url='iplant_login')
def simple_record_create(request, journal_id):
    journal = get_object_or_404(Journal, pk=journal_id)
    if request.is_ajax():
        form = RecordForm(request.POST, extended_stat=journal.extended_stat)
        if form.is_valid():
            rec = journal.set_record_data(form.cleaned_data)
            response = {'journal_id': journal.id,
                        'work': rec.work,
                        'rec_id': rec.id,
                        }
        else:
            response = "bad Record data"
    else:
        response = "not AJAX!"
    return JsonResponse(response)
