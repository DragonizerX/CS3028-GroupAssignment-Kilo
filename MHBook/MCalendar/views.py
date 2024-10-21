from django.shortcuts import render
from django.views import generic

# Create your views here.

def examplePage(request):
    return render(request, 'example.html')














def sidebarPage(request):
    return render(request, 'sidebar.html')