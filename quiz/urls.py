from django.urls import path
from . import views


urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),
    path('<int:quiz_id>/', views.quiz_question, name='quiz_question'),
    path('<int:quiz_id>/answer/', views.quiz_answer, name='quiz_answer'),
    path('results/', views.quiz_results, name='quiz_results'),
]