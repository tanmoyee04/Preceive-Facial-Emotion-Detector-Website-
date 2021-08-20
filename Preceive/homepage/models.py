from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.
class Image(models.Model):
    #photo=models.ImageField()
    photo=models.FileField(validators=[FileExtensionValidator( ['png','jpg','jpeg','mp3','avi','mp4','webm','mkv','gif'] ) ])
    date=models.DateTimeField(auto_now_add=True)
    #solved=models.ImageField(default=None)
    solved=models.FileField(null=False,blank=False,default=None)

class Feedback(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length = 254)
    subject = models.CharField(max_length=30)
    message = models.CharField(max_length=1000)