from django.urls import path
from . import views

urlpatterns = [
    path("toy_create/", views.ToyCreateAPI.as_view()),
    path("toy_update/", views.ToyUpdateAPI.as_view()),
    path("toy_delete/", views.ToyDeleteAPI.as_view()),
    path("toy_details/", views.AllToyDetailsAPI.as_view()),
    path("toy_details/<str:model>/", views.ToyDetailsAPI.as_view()),  
]
