from django.contrib import admin
from .models import Image, Feedback

# Register your models here.
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display=['id','photo','date','solved']

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display=['id','name','email','subject','message']