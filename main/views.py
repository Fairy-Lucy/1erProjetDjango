from django.shortcuts import render
from google import genai
import os


client = genai.Client(api_key="")

def ask_gemini(request):
    response_text = ""
    question = ""

    if request.method == "POST":
        question = request.POST.get("question", "").strip()

        if question:
            prompt = f"""
Tu es un assistant spécialisé en mécanique industrielle.
Réponds de manière claire, pédagogique et précise, comme à un technicien expérimenté.

Question de l'utilisateur :
{question}
"""

            # ✅ APPEL CORRIGÉ ici
            response = client.models.generate_content(
                model="gemini-2.5-flash",      # le plus rapide et performant de ta liste
                contents=prompt
            )

            response_text = response.text

    return render(request, "ask_gemini.html", {
        "question": question,
        "response_text": response_text,
    })