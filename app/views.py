from django.shortcuts import render
from django.http import HttpResponse
from app.forms import FaceRecognitionform
from app.machinelearning import pipeline_model
from django.conf import settings
from app.models import FaceRecognition
import os

# Create your views here.

def index(request):
    form = FaceRecognitionform()

    if request.method == 'POST':
        form = FaceRecognitionform(request.POST or None, request.FILES or None)
        if form.is_valid():
            save = form.save(commit=True)

            # extract the image object from database
            primary_key = save.pk
            imageobj = FaceRecognition.objects.get(pk=primary_key)
            fileroot = str(imageobj.image)
            filepath = os.path.join(settings.MEDIA_ROOT,fileroot)
            results = pipeline_model(filepath)
            print(results)

            return render(request,'index.html',{'form':form,'upload':True,'results':results})


    return render(request,'index.html',{'form':form,'upload':False})
