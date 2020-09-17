from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:name>", views.title, name="title"), # This path supports the first spec
    path("/results", views.search, name="search")
]
