from django.shortcuts import render, redirect
from .models import Utilisateur

def home(request):
    utilisateurs = Utilisateur.objects.all()
    return render(request, 'index.html', {'utilisateurs': utilisateurs})


def form_view(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')

        if nom:
            Utilisateur.objects.create(nom=nom)

        return redirect('home')

    return render(request, 'form.html')
