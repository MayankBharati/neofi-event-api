from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import EventPermission
from .serializers import EventPermissionSerializer
from events.models import Event
from history.models import EventHistory
import json

class ShareEventView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({"detail": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        users_data = request.data.get('users', [])
        if not isinstance(users_data, list):
            return Response({"detail": "Expected a list of users."}, status=status.HTTP_400_BAD_REQUEST)

        results = []
        errors = []

        for item in users_data:
            user_id = item.get('user_id')
            role = item.get('role')

            if role not in dict(EventPermission.ROLE_CHOICES).keys():
                errors.append({"user_id": user_id, "error": "Invalid role"})
                continue

            try:
                user = request.user
                permission, created = EventPermission.objects.update_or_create(
                    event=event,
                    user_id=user_id,
                    defaults={'role': role}
                )
                results.append(EventPermissionSerializer(permission).data)

                # Log permission change
                EventHistory.objects.create(
                    event=event,
                    changed_by=request.user,
                    change_type='update',
                    old_data=None,
                    new_data=json.dumps({
                        "permission_change": {
                            "user": str(user_id),
                            "role": role
                        }
                    })
                )

            except Exception as e:
                errors.append({"user_id": user_id, "error": str(e)})

        return Response({"permissions": results, "errors": errors}, status=status.HTTP_200_OK)


class ListEventPermissionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id):
        try:
            permissions = EventPermission.objects.filter(event_id=event_id)
            serializer = EventPermissionSerializer(permissions, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateEventPermissionView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, event_id, user_id):
        try:
            permission = EventPermission.objects.get(event_id=event_id, user_id=user_id)
        except EventPermission.DoesNotExist:
            return Response({"detail": "Permission not found"}, status=status.HTTP_404_NOT_FOUND)

        role = request.data.get("role")
        if role not in dict(EventPermission.ROLE_CHOICES).keys():
            return Response({"detail": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)

        permission.role = role
        permission.save()

        # Log change
        EventHistory.objects.create(
            event_id=event_id,
            changed_by=request.user,
            change_type='update',
            old_data=json.dumps(EventPermissionSerializer(permission).data),
            new_data=json.dumps({
                "user": user_id,
                "role": role
            })
        )

        return Response(EventPermissionSerializer(permission).data)


class DeleteEventPermissionView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, event_id, user_id):
        try:
            permission = EventPermission.objects.get(event_id=event_id, user_id=user_id)
            permission.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except EventPermission.DoesNotExist:
            return Response({"detail": "Permission not found"}, status=status.HTTP_404_NOT_FOUND)