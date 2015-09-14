
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime


from django.http import JsonResponse


from .models import Journal, EventItem, Record, Report
from .forms import RecordForm, EventForm, ChooseDateForm
from catalog.models import Unit


def index(request):
    root = None
    if request.user.is_authenticated():
        try:
            root = Unit.objects.get(name=request.user.profile.
                                    responsible_for_equipment.name)
        except AttributeError:
            pass
    unit_list = Unit.tree_list(root)
    context = {'equipment_list': unit_list}
    return render(request, 'statistics/index.html', context)


def journals_on_date(request):
    root = None
    if request.user.is_authenticated():
        try:
            root = Unit.objects.get(name=request.user.profile.
                                    responsible_for_equipment.name)
        except AttributeError:
            pass
    unit_list = Unit.tree_list(root)
    if 'date' in request.POST:
        jourlnal_date = request.POST['date']
        request.session['input_date'] = request.POST['date']
    elif 'input_date' in request.session:
        jourlnal_date = request.session['input_date']
    else:
        jourlnal_date = None

    records_dict = Record.get_records_on_date(jourlnal_date)
    form_date = ChooseDateForm()
    context = {
        'equipment_list': unit_list,
        'records_dict': records_dict,
        'form_date': form_date}
    return render(request, 'statistics/journals_on_date.html', context)


def show(request, journal_id):
    journal = get_object_or_404(Journal, pk=journal_id)
    record_list = journal.get_last_records()
    event_list = journal.eventitem_set.order_by('-date')[:3]
    form = EventForm(None)
    context = {
        'journal': journal,
        'record_list': record_list,
        'event_list': event_list,
        'form': form, }
    return render(
        request,
        'statistics/show.html',
        context)


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


def record_create(request, journal_id):
    journal = get_object_or_404(Journal, pk=journal_id)
    form = RecordForm(request.POST or None, journal=journal)
    if request.POST and form.is_valid():
        journal.set_record_data(form.cleaned_data)
        return redirect('statistics:show', journal_id=journal_id)
    return render(request,
                  'statistics/record_form.html',
                  {'form': form, 'journal': journal, 'record_id': None})


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
                    }
    else:
        response = "not AJAX!"
    return JsonResponse(response)


def record_update(request, journal_id, record_id):
    journal = get_object_or_404(Journal, pk=journal_id)
    form = RecordForm(request.POST or Journal.get_record_data(record_id),
                      journal=journal)
    if request.POST and form.is_valid():
        journal.set_record_data(form.cleaned_data, record_id)
        return redirect('statistics:show', journal_id=journal_id)
    return render(request,
                  'statistics/record_form.html',
                  {'form': form, 'journal': journal, 'record_id': record_id})


def record_delete(request, journal_id, record_id):
    template_name = 'statistics/confirm_record_delete.html'
    journal = get_object_or_404(Journal, pk=journal_id)
    if request.method == 'POST':
        journal.delete_record(record_id)
        return redirect('statistics:show', journal_id=journal_id)
    return render(request, template_name)


def event_create(request, journal_id):
    journal = get_object_or_404(Journal, pk=journal_id)
    form = EventForm(request.POST)
    if request.POST and form.is_valid():
        journal.set_event_data(form.cleaned_data)
    return redirect('statistics:show', journal_id=journal_id)


def event_delete(request, journal_id, event_id):
    template_name = 'statistics/confirm_record_delete.html'
    event = get_object_or_404(EventItem, pk=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('statistics:show', journal_id=journal_id)
    return render(request, template_name)


def reports(request):
    report_list = Report.objects.all()
    return render(
        request,
        'statistics/reports.html',
        {'reports': report_list, })
