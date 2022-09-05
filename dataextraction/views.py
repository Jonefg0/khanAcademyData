from django.shortcuts import render
from django.http import HttpResponse# Create your views here.


def home(request):
    return render(request, 'pages/home.html')

def updateData(request):
    return render(request, 'pages/updateData.html')

def viewData(request):
    return render(request, 'pages/viewData.html')
