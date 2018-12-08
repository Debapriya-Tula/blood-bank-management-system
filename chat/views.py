from django.shortcuts import render

# Create your views here.
# chat/views.py
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.safestring import mark_safe
import json

def index(request):
    return render(request, 'chat/index.html', {})
def sg(req,chatroom):
    return HttpResponse("<h1> welcome to chatroom: "+chatroom+" </h1>")

from django.shortcuts import render


def index(request):
    return render(request, 'chat/index.html', {})


def room(request, chatroom):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(chatroom))
    })
