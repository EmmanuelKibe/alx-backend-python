from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsConversationParticipant(BasePermission):
    """
    Allows access only to participants of the conversation.
    """

    def has_object_permission(self, request, view, obj):
        # obj is a Conversation instance
        return request.user in obj.participants.all()


class IsMessageSenderOrConversationParticipant(BasePermission):
    """
    Allows:
    - Any participant in the conversation to read messages
    - Only the sender to modify/delete their own messages
    """

    def has_object_permission(self, request, view, obj):
        # obj is a Message instance
        user = request.user

        # Read permissions: any participant can read
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return user in obj.conversation.participants.all()

        # Write permissions: only sender can update/delete
        return obj.sender == user
