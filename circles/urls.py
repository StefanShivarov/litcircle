from django.urls import path
from . import views


app_name = 'circles'

urlpatterns = [
    path('', views.my_circles, name='my_circles'),
    path('create/', views.create_circle, name='create_circle'),
    path('<int:circle_id>/', views.circle_details, name='circle_details'),
    path('<int:circle_id>/join/', views.request_to_join_circle, name='request_to_join_circle'),
    path('<int:circle_id>/cancel/', views.cancel_request_to_join_circle, name='cancel_request'),
    path('<int:circle_id>/leave/', views.leave_circle, name='leave_circle'),
    path('<int:circle_id>/delete/', views.delete_circle, name='delete_circle'),
    path('discover', views.search_circles, name='discover_circles'),
    path('<int:circle_id>/manage/', views.manage_circle_members, name='manage_circle_members'),
]
