from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Message(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name = 'message_owner')
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name = 'message_receiver')
    contents = models.CharField(max_length=1000)
    pub_date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return '(by:' + str(self.owner) + ')'+str(self.contents) + str(self.pub_date)

class Image(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'myapp/css/img/',default = 'myapp/css/img/default.png')


    def __str__(self):
        return str(self.user)