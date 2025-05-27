from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from history.models import EventHistory
from events.models import Event
from events.serializers import EventSerializer
import json

class EventVersionDiffView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, version_id1, version_id2, *args, **kwargs):
        try:
            version1 = EventHistory.objects.get(id=version_id1)
            version2 = EventHistory.objects.get(id=version_id2)
        except EventHistory.DoesNotExist:
            return Response({"error": "One or both versions not found"}, status=404)

        # Ensure both versions belong to the same event
        if version1.event_id != version2.event_id:
            return Response({"error": "Versions belong to different events"}, status=400)

        data1 = json.loads(version1.new_data)
        data2 = json.loads(version2.new_data)

        diff = self.compare_dicts(data1, data2)
        return Response(diff)

    def compare_dicts(self, d1, d2):
        result = {}
        all_keys = set(d1.keys()).union(d2.keys())
        for key in all_keys:
            v1 = d1.get(key)
            v2 = d2.get(key)
            if v1 != v2:
                result[key] = {
                    "from": v1,
                    "to": v2
                }
        return result

class EventVersionRollbackView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id, version_id):
        try:
            history = EventHistory.objects.get(id=version_id, event_id=event_id)
        except EventHistory.DoesNotExist:
            return Response({"error": "Version not found"}, status=404)

        # Restore from new_data
        old_data = json.loads(history.new_data)
        event = Event.objects.get(id=event_id)

        # Update event fields
        for key, value in old_data.items():
            setattr(event, key, value)
        event.save()

        # Log rollback
        EventHistory.objects.create(
            event=event,
            changed_by=request.user,
            change_type='rollback',
            old_data=json.dumps(EventSerializer(event).data),
            new_data=json.dumps(old_data)
        )

        return Response({"detail": "Rolled back to selected version"})

class EventChangelogView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id):
        histories = EventHistory.objects.filter(event_id=event_id).order_by('timestamp')
        data = [
            {
                "id": str(h.id),
                "change_type": h.change_type,
                "changed_by": h.changed_by.email,
                "timestamp": h.timestamp.isoformat(),
                "summary": f"{h.change_type} at {h.timestamp}"
            } for h in histories
        ]
        return Response(data)

class EventVersionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id, version_id):
        try:
            history = EventHistory.objects.get(id=version_id, event_id=event_id)
        except EventHistory.DoesNotExist:
            return Response({"error": "Version not found"}, status=404)

        return Response(json.loads(history.new_data))