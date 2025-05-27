from django.urls import path
from .views import (
    ShareEventView,
    ListEventPermissionsView,
    UpdateEventPermissionView,
    DeleteEventPermissionView
)

urlpatterns = [
    path('events/<uuid:event_id>/share/', ShareEventView.as_view(), name='event-share'),
    path('events/<uuid:event_id>/permissions/', ListEventPermissionsView.as_view(), name='event-permissions-list'),
    path('events/<uuid:event_id>/permissions/<uuid:user_id>/', UpdateEventPermissionView.as_view(), name='event-permission-update'),
    path('events/<uuid:event_id>/permissions/<uuid:user_id>/', DeleteEventPermissionView.as_view(), name='event-permission-delete'),
]