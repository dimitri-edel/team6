from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),
    path('<int:quiz_id>/submit/', views.quiz_submit, name='quiz_submit'),
    path('submit-all/', views.quiz_submit_all, name='quiz_submit_all'),
]
