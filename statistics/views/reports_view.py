from django.shortcuts import get_object_or_404, render

from statistics.models.report import Report
from statistics.forms import ChooseReportForm
from catalog.models import Unit


def reports(request):
    root = Unit.objects.filter(plant=None)[0]
    if request.user.is_authenticated():
        try:
            root = Unit.objects.get(name=request.user.profile.
                                    responsible_for_equipment.name)
        except AttributeError:
            pass
    report_choices = Report.get_reports_collection(root)
    form = ChooseReportForm(choices=report_choices)

    return render(
        request,
        'statistics/reports.html',
        {'form': form, })


def report_show(request):
    report = get_object_or_404(Report, pk=request.GET['report_id'])
    context = {
        'rdata': report.prepare_reports_content(request.GET['date']),
        'rdate': request.GET['date'],
    }
    return render(
        request,
        'statistics/report.html',
        context
    )
