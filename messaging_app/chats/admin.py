from django.contrib import admin

# Register your models here.
from .models import User, Conversation, Message
admin.site.register(User)
admin.site.register(Conversation)
admin.site.register(Message)
