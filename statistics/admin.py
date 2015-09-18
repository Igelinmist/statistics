from django.contrib import admin

from .models.journal import Journal
from .models.report import Report, Column


class ColumnInline(admin.TabularInline):
    model = Column
    extra = 1


class ReportAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'equipment']}),
    ]
    inlines = [ColumnInline]


admin.site.register(Journal)
admin.site.register(Report, ReportAdmin)
