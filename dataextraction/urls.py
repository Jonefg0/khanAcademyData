from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='inicio'),
    path('viewData',views.viewData,name='viewData'),
    path('updateData',views.updateData,name='updateData'),
    path('run',views.runscript,name = 'run')
]


