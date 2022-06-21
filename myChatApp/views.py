import json
import profile
from django.http import JsonResponse
from django.shortcuts import redirect, render

from .models import ChatMessage, Friend, Profile
from .forms import ChatMessageForm

# Create your views here.

def index(request):
    user =request.user.profile
    friends = user.friends.all()
    context = {"user": user, "friends": friends}
    return render(request, "myChatApp/index.html", context)

def detail(request, pk ):
    friend = Friend.objects.get(profile_id=pk)
    user = request.user.profile                         # sender
    profile = Profile.objects.get(pk=friend.profile.id) # receiver
    chats = ChatMessage.objects.all()
    form = ChatMessageForm()

    if request.method == "POST":
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.msg_sender = user
            chat_message.msg_receiver = profile
            chat_message.save()
            return redirect("detail", pk=friend.profile.id)
    
    context={"friend": friend, "form": form, "user":user, "profile":profile, "chats": chats}
    return render(request, "myChatApp/detail.html", context)

def sentMessage(request, pk):
    user = request.user.profile                             # sender
    friend = Friend.objects.get(profile_id=pk)
    profile = Profile.objects.get(id=friend.profile.id)     # receiver

    data = json.loads(request.body)
    new_chat = data["msg"]
    new_chat_msg = ChatMessage.objects.create(body=new_chat, msg_sender=user, msg_receiver=profile)
    return JsonResponse(new_chat_msg.body, safe=False)