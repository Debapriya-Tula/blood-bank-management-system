from django.db import models


class Room(models.Model):
	
	roomname = models.CharField(max_length = 200)
	
	def __str__(self):
		return self.roomname


class Chat(models.Model):
	
	chat = models.CharField(max_length = 2000, blank = True)
	room = models.ForeignKey(Room, on_delete = models.CASCADE)
	


	
	
