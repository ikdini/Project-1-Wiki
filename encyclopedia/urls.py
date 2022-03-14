from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/search", views.search, name="search"),
    path("wiki/new-entry", views.new_entry, name="new_entry"),
    path("wiki/random", views.rand, name="random"),
    path("wiki/edit/<str:entry>", views.edit, name="edit"),
    path("wiki/<str:entry>", views.content, name="content"),
]
