from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_dashboard, name='task_dashboard'),
    path('tasks/board/', views.board_view, name='board_view'),
    path('tasks/timeline/', views.timeline_view, name='timeline_view'),
    path('tasks/add/', views.add_task, name='add_task'),
    path('tasks/<int:id>/', views.task_detail, name='task_detail'),
    path('tasks/update/<int:id>/', views.update_task_inline, name='update_task_inline'),
    path('meetings/add/', views.add_meeting_note, name='add_meeting_note'),
    path('meetings/', views.meeting_list, name='meeting_list'),
    path('meetings/new/', views.add_meeting_note, name='add_meeting_note'),
    path('meetings/<int:id>/', views.meeting_detail, name='meeting_detail'),
    path('timeline/', views.timeline_view, name='timeline_view'),
]
