from django.urls import path
from . import views

app_name = 'discussions'

urlpatterns = [
    path('<int:circle_id>/discussion', views.discussion_room, name='discussion_room'),
]