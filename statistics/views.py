
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Journal, EventItem
from .forms import RecordForm, EventForm
from catalog.models import Unit


def index(request):
    root = None
    if request.user.is_authenticated():
        try:
            root = Unit.objects.get(name=request.user.profile.responsible_for_equipment.name)
        except AttributeError:
            pass

    unit_list = Unit.tree_list(root)
    context = {'equipment_list': unit_list}
    return render(request, 'statistics/index.html', context)


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
