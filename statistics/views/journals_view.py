from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import permission_required

from statistics.models.journal import Journal, Record
from statistics.forms import EventForm, ChooseDateForm
from catalog.models import Unit
from statistics.helpers import yesterday_local


def index(request):
    root = Unit.objects.filter(plant=None)[0]
    if request.user.is_authenticated():
        try:
            root = Unit.objects.get(name=request.user.profile.
                                    responsible_for_equipment.name)
        except AttributeError:
            pass
    unit_list = root.unit_tree()

    context = {'equipment_list': unit_list}
    return render(request, 'statistics/index.html', context)


@permission_required('statistics.create_journal_record',
                     login_url='iplant_login')
def journals_on_date(request):
    root = Unit.objects.filter(plant=None).all()[0]
    if request.user.is_authenticated():
        try:
            root = Unit.objects.get(name=request.user.profile.
                                    responsible_for_equipment.name)
        except AttributeError:
            pass
    unit_list = root.unit_tree()
    if 'date' in request.POST:
        journal_date = request.POST['date']
        request.session['input_date'] = request.POST['date']
    elif 'input_date' in request.session:
        journal_date = request.session['input_date']
    else:
        journal_date = None

    records_dict = Record.get_records_on_date(journal_date)
    form_date = ChooseDateForm()
    context = dict(equipment_list=unit_list,
                   records_dict=records_dict,
                   form_date=form_date)
    return render(request, 'statistics/journals_on_date.html', context)


@permission_required('statistics.create_journal_record',
                     login_url='iplant_login')
def journals_write(request):
    try:
        root = Unit.objects.get(name=request.user.profile.
                                responsible_for_equipment.name)
    except AttributeError:
        root = Unit.objects.filter(plant=None).all()[0]
    unit_tree = root.unit_tree()
    if 'date' in request.GET:
        write_date = request.GET['date']
        request.session['input_date'] = request.GET['date']
    elif 'input_date' in request.session:
        write_date = request.session['input_date']
    else:
        write_date = yesterday_local()
    available_recs = root.journal.get_records(write_date)
    form_date = ChooseDateForm(initials={'date': write_date})
    context = {
        'equipment_list': unit_tree,
        'available_recs': available_recs,
        'form_date': form_date
    }
    return render(request, 'statistics/journals_write.html', context)


def show(request, journal_id):
    journal = get_object_or_404(Journal, pk=journal_id)
    record_list = journal.get_last_records(depth=5)
    event_list = journal.eventitem_set.order_by('-date')[:3]
    form = EventForm(None)
    context = {
        'journal': journal,
        'record_list': record_list,
        'event_list': event_list,
        'form': form,
    }
    return render(
        request,
        'statistics/show.html',
        context)
