from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files import File
from .forms import ImageForm
from .models import Image, Feedback
from .facial_emotion import main
from django.contrib import messages
import os
from django.core.files.storage import default_storage

def get_filetype(filename):
    ext=os.path.splitext(filename)[1][1:]
    if ext in ['jpg', 'jpeg', 'png']:
        return True
    else:
        return False

# Create your views here.

def index(request):
    form=ImageForm()
    img=None
    idx=None
    if request.method=="POST":
        form=ImageForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            img=Image.objects.last()    # if valid then show
            idx=get_filetype(img.photo.name)
    context={'form':form, 'img':img, 'idx':idx}
    return render(request,'index.html',context)

def emotion(request):
    if request.method=="POST":
        img=Image.objects.last()
        filename=img.photo.name
        idx=get_filetype(filename)
        if not idx:
            filename=os.path.splitext(filename)[0]+'.mp4'
        outpath=settings.MEDIA_ROOT+"/solved_"+filename
        main(img.photo.path,outpath,idx)                    ###### Error: django is unable to save the opencv processed file, video save extension problem
        #img.solved.save("solved_"+filename,File(open(outpath,'rb')),save=True)
        if not idx:
            img.solved=File(open(outpath,'rb'))
        img.solved.name='solved_'+filename
        img.save()
    context={'img':img,'idx':idx}
    return render(request,'index.html',context)

def takeFeedback(request):
    if request.method=="POST":
        temp=[]
        temp.append(request.POST.get('nameval'))
        temp.append(request.POST.get('emailval'))
        temp.append(request.POST.get('subjectval'))
        temp.append(request.POST.get('messageval'))
        if(all(temp)):
            form1=Feedback(name=temp[0],email=temp[1], subject=temp[2],message=temp[3])
            form1.save()
            messages.success(request, 'Thank you for your feedback')
            return redirect ("/")
        else:
            messages.error(request, 'Empty fileds!')
    context={'temp':''}
    return render(request,'index.html',context)