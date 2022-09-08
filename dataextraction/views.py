from django.shortcuts import render
from django.http import HttpResponse
from dataextraction.dataextraction import *
from .models import Logros


def home(request):
    return render(request, 'pages/home.html')

def updateData(request):
    return render(request, 'pages/updateData.html')

def viewData(request):
    logros = Logros.objects.all()
    return render(request, 'pages/viewData.html',{'logros':logros})

def runscript(request):
    try:
        run_script()
        ress = "data updated"
        return render(request, 'pages/updateData.html',{'ress': ress})
    except:
        ress = "error running"
        return render(request, 'pages/updateData.html',{'ress': ress})
    