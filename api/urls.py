from django.urls import path
from . import views

urlpatterns = [
    path('todos/', views.TaskListApi.as_view(), name= 'taskapi' ),
    path('todo/<int:id>/update', views.TaskUpdate.as_view(), name= 'updatetaskapi' ),
    path('todo/<int:id>/complete', views.TaskCompleted.as_view(), name= 'completetaskapi' ),

    #auth
    path('signup', views.signup),
    path('login', views.login),
]