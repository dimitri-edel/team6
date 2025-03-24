from django.shortcuts import render, get_object_or_404
from .models import About

def home(request):
    about_profiles = About.objects.all()
    return render(request, 'home.html' , {'about_profiles': about_profiles})

def about_list(request):
    about_profiles = About.objects.all()
    return render(request, 'about_list.html', {'about_profiles': about_profiles})

def about_detail(request, pk):
    about_profile = get_object_or_404(About, pk=pk)
    return render(request, 'about_detail.html', {'about_profile': about_profile})