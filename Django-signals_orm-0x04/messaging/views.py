#Create views here.
from django.shortcuts import render
from .models import User, Message
from django.http import HttpResponse

#Allow users to delete their account
def delete_user(request, username):
    try:
        user = User.objects.get(username=username)
        user.delete()
        return HttpResponse(f"User {username} deleted successfully.")
    except User.DoesNotExist:
        return HttpResponse(f"User {username} does not exist.", status=404)
    
#Optimize querying for messages and their replies
def view_message_with_replies(request, message_id):
    try:
        message = Message.objects.prefetch_related('replies').get(id=message_id)
        replies = message.replies.all()
        response_content = f"Message from {message.sender} to {message.receiver}: {message.content}\nReplies:\n"
        for reply in replies:
            response_content += f"- {reply.sender} to {reply.receiver}: {reply.content}\n"
        return HttpResponse(response_content)
    except Message.DoesNotExist:
        return HttpResponse(f"Message with ID {message_id} does not exist.", status=404)
