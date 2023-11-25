from django.urls import path
from .views import post_create, post_list, post_detail

urlpatterns = [
     path('create', post_create),
     path('list', post_list),
     path('detail/<int:post_id>', post_detail),
]
