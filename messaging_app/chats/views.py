from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer


# Create your views here.

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def get_queryset(self):
        # Only show conversations where the authenticated user is a participant
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get("participants", [])

        if not participant_ids:
            return Response({"error": "Please provide participant IDs."}, status=400)

        # Ensure the authenticated user is included
        if str(request.user.user_id) not in participant_ids:
            return Response({"error": "You must be a participant in the conversation."}, status=403)

        users = User.objects.filter(user_id__in=participant_ids)

        if len(users) != len(participant_ids):
            return Response({"error": "One or more participants not found."}, status=400)

        conversation = Conversation.objects.create()
        conversation.participants.set(users)

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=201)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get("conversation")
        message_body = request.data.get("message_body", "").strip()

        if not conversation_id or not message_body:
            return Response(
                {"error": "conversation and message_body are required."},
                status=400
            )

        # Validate conversation exists
        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found."}, status=404)

        # Ensure user is part of the conversation
        if request.user not in conversation.participants.all():
            return Response({"error": "You are not a participant of this conversation."}, status=403)

        # Sender is ALWAYS the authenticated user, not from request body
        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            message_body=message_body
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=201)

    
    def get_queryset(self):
        # Only messages where the user is a participant
        return Message.objects.filter(conversation__participants=self.request.user)




