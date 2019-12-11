from chatMessages.models import Message
from chatMessages.serializers import MessageSerializer
from chatMessages.permissions import IsRecipientOrSender

from rest_framework import generics, permissions


class MessageList(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.username)


class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsRecipientOrSender,)