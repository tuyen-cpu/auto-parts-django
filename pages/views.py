from django.shortcuts import render

from .models import AboutPage


def about(request):
    page = AboutPage.objects.first()
    return render(request, 'about.html', {'page': page})

# Create your views here.
