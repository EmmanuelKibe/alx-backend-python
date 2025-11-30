#Create views here.
from django.shortcuts import render
from .models import User
from django.http import HttpResponse

#Allow users to delete their account
def delete_user(request, username):
    try:
        user = User.objects.get(username=username)
        user.delete()
        return HttpResponse(f"User {username} deleted successfully.")
    except User.DoesNotExist:
        return HttpResponse(f"User {username} does not exist.", status=404)
