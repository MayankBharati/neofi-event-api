from django.urls import path
from .views import EventVersionDiffView,EventVersionRollbackView,EventChangelogView,EventVersionDetailView

urlpatterns = [
    path('events/<uuid:version_id1>/diff/<uuid:version_id2>/', EventVersionDiffView.as_view(), name='event-version-diff'),
    path('events/<uuid:event_id>/rollback/<uuid:version_id>/', EventVersionRollbackView.as_view(), name='event-rollback'),
    path('events/<uuid:event_id>/changelog/', EventChangelogView.as_view(), name='event-changelog'),
    path('events/<uuid:event_id>/version/<uuid:version_id>/', EventVersionDetailView.as_view(), name='event-version-detail')

]