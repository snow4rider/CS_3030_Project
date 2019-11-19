from rest_framework import serializers
from chatMessages.models import Message


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.username')

    class Meta:
        model = Message
        fields = ('id', 'text', 'created', 'sender', 'recipient')