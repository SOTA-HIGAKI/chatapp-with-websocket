from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Message(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name = 'message_owner')
    content = models.TextField(max_length=1000)
    pub_date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(self.content) + '(' + str(self.owner) + ')'

class Friend(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='friend_owner')
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)

class Document(models.Model):
    photo =models.ImageField(upload_to = 'documents/',default = 'defo')
    uploaded_at =models.DateTimeField(auto_now_add=True)
