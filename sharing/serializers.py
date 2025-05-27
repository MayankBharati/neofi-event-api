from rest_framework import serializers
from .models import EventPermission
from users.models import User

class EventPermissionSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user')

    class Meta:
        model = EventPermission
        fields = ['id', 'event', 'user_id', 'role', 'user_email']
        read_only_fields = ['event', 'user_email']