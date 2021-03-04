from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Message(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name = 'message_owner')
    # getter = models.
    contents = models.CharField(max_length=1000)
    pub_date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return '(' + str(self.owner) + ')'+str(self.contents) + str(self.pub_date)

class Document(models.Model):
    photo =models.ImageField(upload_to = 'documents/',default = 'defo')
    uploaded_at =models.DateTimeField(auto_now_add=True)
