from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def form_view(request):
    return render(request, 'form.html')
