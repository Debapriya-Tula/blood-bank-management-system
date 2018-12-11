from django.shortcuts import render

# Create your views here.
# chat/views.py
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.safestring import mark_safe
import json
from .models import Room,Chat


""" def index(request):
    return render(request, 'chat/index.html', {})
def sg(req,chatroom):
    return HttpResponse("<h1> welcome to chatroom: "+chatroom+" </h1>") """

from django.shortcuts import render


def index(request):
    return render(request, 'chat/index.html', {})


""" def room(request, chatroom):
    newroomtemp = Room.objects.all()
    flag =0
    for i in newroomtemp:
    	if i.roomname == chatroom:
    		flag=1
    if not flag:
    	roomname = Room.objects.create(roomname = chatroom)
    	roomname.save()
    	
    newroom = Room.objects.all()
    for room1 in newroom:
    	print(room1.roomname)
    
    chat1 = Chat.objects.all()
    
    for room1 in chat1:
    	print(room1.chat) """

	
    #new = Room.objects.filter(roomname="sidh").delete()



def room(request, chatroom):
	return render(request, 'chat/room.html', {
		'room_name_json': mark_safe(json.dumps(chatroom))
    })
    
   
""" def msg(request,chatroom,msgs):
    room1 = Room.objects.get(roomname = chatroom)
    chat1 = Chat.objects.create(room = room1, chat=msgs)
    chat1.save()
    
    massg = Chat.objects.filter(room = room1)
    
    return render(request, 'chat/room.html', {'msg':massg}) """
   	
   
   
   
   
   
   
   
   
   
   
   
