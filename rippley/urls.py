from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('team/', views.team_view, name='team'),
    path('admin/', admin.site.urls),
    path('categories/', include('category.urls')),
    path('about/', include('about.urls')),
    path('quizzes/', include('quiz.urls')),
    path('summernote/', include('django_summernote.urls')),

]
