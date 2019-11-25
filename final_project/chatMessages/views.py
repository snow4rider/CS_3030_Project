from chatMessages.models import Message
from chatMessages.serializers import MessageSerializer
from chatMessages.permissions import IsRecipientOrSender

from rest_framework import generics


class MessageList(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsRecipientOrSender,)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsRecipientOrSender,)