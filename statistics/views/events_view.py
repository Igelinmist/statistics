from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import permission_required

from statistics.models.journal import Journal, EventItem
from statistics.forms import EventForm


@permission_required('statistics.create_journal_event',
                     login_url='iplant_login')
def event_create(request, journal_id):
    journal = get_object_or_404(Journal, pk=journal_id)
    form = EventForm(request.POST)
    if request.POST and form.is_valid():
        journal.set_event_data(form.cleaned_data)
    return redirect('statistics:show', journal_id=journal_id)


@permission_required('statistics.delete_journal_event',
                     login_url='iplant_login')
def event_delete(request, journal_id, event_id):
    template_name = 'statistics/confirm_record_delete.html'
    event = get_object_or_404(EventItem, pk=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('statistics:show', journal_id=journal_id)
    return render(request, template_name)
