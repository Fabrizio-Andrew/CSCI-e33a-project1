from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:name>", views.title, name="title"), # This path supports the first spec
    path("/results", views.search, name="search"),
    path("/create", views.create, name="create"),
    path("/new", views.new, name="new"),
    path("/edit", views.edit, name="edit"),
    path("/overwrite", views.overwrite, name='overwrite')
]
