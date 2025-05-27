from django.contrib import admin
from .models import EventHistory

@admin.register(EventHistory)
class EventHistoryAdmin(admin.ModelAdmin):
    list_display = ('event', 'change_type', 'changed_by', 'timestamp')
    readonly_fields = ('event', 'changed_by', 'change_type', 'old_data', 'new_data', 'timestamp')

    def has_add_permission(self, request):
        return False  # Prevent manual addition of history records

    def has_change_permission(self, request, obj=None):
        return False  # Prevent editing history records