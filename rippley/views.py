from django.shortcuts import render
from about.models import About  # Import the About model
def home(request):
    women_profiles = About.objects.all()
    return render(request, 'home.html', {'women_profiles': women_profiles})

def team_view(request):
    return render(request, 'team.html')


def about_list(request):
    about_profiles = About.objects.all()
    return render(request, 'about_list.html', {'about_profiles': about_profiles})