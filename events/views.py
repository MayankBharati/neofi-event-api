from rest_framework import viewsets
from .models import Event
from .serializers import EventSerializer
from .permissions import IsOwner
from history.models import EventHistory
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
import json,uuid

def convert_uuid_to_str(data):
    """Recursively convert UUID objects to strings in a dict."""
    if isinstance(data, dict):
        return {key: convert_uuid_to_str(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_uuid_to_str(value) for value in data]
    elif isinstance(data, uuid.UUID):
        return str(data)
    else:
        return data


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsOwner]

    def perform_create(self, serializer):
        user = self.request.user
        event = serializer.save(owner=user)

        # Convert UUID to str before dumping
        serialized_data = convert_uuid_to_str(serializer.data)

        EventHistory.objects.create(
            event=event,
            changed_by=user,
            change_type='create',
            new_data=json.dumps(serialized_data)
        )

    def perform_update(self, serializer):
        old_event = self.get_object()
        old_data = EventSerializer(old_event).data

        # Convert UUIDs before saving
        old_serialized = convert_uuid_to_str(old_data)
        updated_event = serializer.save()
        new_serialized = convert_uuid_to_str(EventSerializer(updated_event).data)

        EventHistory.objects.create(
            event=updated_event,
            changed_by=self.request.user,
            change_type='update',
            old_data=json.dumps(old_serialized),
            new_data=json.dumps(new_serialized)
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'])
    def batch_create(self, request):
        events = request.data
        if not isinstance(events, list):
            return Response(
                {"detail": "Expected a list of events"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=events, many=True)
        if serializer.is_valid():
            owner = request.user
            for event_data in serializer.validated_data:
                event_data['owner'] = owner
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)