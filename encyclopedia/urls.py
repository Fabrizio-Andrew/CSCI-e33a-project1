from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('wiki/<str:name>', views.title, name='title'),
    path('/results', views.search, name='search'),
    path('/create', views.create, name='create'),
    path('/new', views.save, name='save'),
    path('/edit', views.edit, name='edit'),
    path('/overwrite', views.overwrite, name='overwrite'),
    path('/random', views.random_page, name='random')
]
