from django.urls import path
from . import views

urlpatterns = [    
    path('makePrediction/',views.makePrediction),
]