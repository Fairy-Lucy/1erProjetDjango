from django.shortcuts import render, redirect
from .models import Utilisateur
import google.generativeai as genai
from PIL import Image
import os
from django.conf import settings

# Configuration Gemini
genai.configure(api_key="TA_CLE_API")


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


def upload_image(request):
    result = ""

    if request.method == "POST" and request.FILES.get("image"):
        file = request.FILES["image"]

        media_path = os.path.join(settings.MEDIA_ROOT, file.name)

        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

        with open(media_path, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        image = Image.open(media_path)

        model = genai.GenerativeModel('gemini-1.5-flash')

        response = model.generate_content([
            "Je souhaite évaluer le plan suivant, représentant un outillage pour fonderie. Ce qui m'intéresse, c'est les dimensions totales de l'outillage. Saurais tu procéder à un OCR, et de reconstituer les côtes principales sur ce plan, et d'estimer le poids ?",
            image
        ])

        result = response.text

    return render(request, "upload.html", {"result": result})
