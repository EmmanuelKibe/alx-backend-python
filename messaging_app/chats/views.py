from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer


# Create your views here.

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get("participants", [])

        if not participant_ids:
            return Response(
                {"error": "Please provide participant IDs."},
                status=status.HTTP_400_BAD_REQUEST
            )

        users = User.objects.filter(user_id__in=participant_ids)

        if len(users) != len(participant_ids):
            return Response(
                {"error": "One or more participants not found."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create conversation
        conversation = Conversation.objects.create()
        conversation.participants.set(users)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get("conversation")
        sender_id = request.data.get("sender")
        message_body = request.data.get("message_body", "").strip()

        # Validate input
        if not conversation_id or not sender_id or not message_body:
            return Response(
                {"error": "conversation, sender, and message_body are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate conversation and sender
        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
            sender = User.objects.get(user_id=sender_id)
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except User.DoesNotExist:
            return Response(
                {"error": "Sender not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            message_body=message_body
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



