from django.shortcuts import render
from google import genai
from google.genai import types   # ← NOUVEAU pour les PDF
from PIL import Image
import io
import base64

client = genai.Client(api_key="macle")

SYSTEM_PROMPT = """Tu es un assistant technique spécialisé en lecture de plans industriels, outillages de fonderie, moules, usinage et conception mécanique.

Tu analyses des plans techniques fournis sous forme d’images ou de PDF.

Tu dois toujours :

- extraire uniquement les informations visibles ou logiquement déductibles,
- signaler toute incertitude,
- ne jamais inventer de dimensions,
- utiliser un vocabulaire industriel simple et professionnel,
- produire des réponses structurées, claires et exploitables en atelier, bureau d’études.

Quand le document est incomplet, flou ou ambigu :
- tu le dis explicitement,
- tu fournis une analyse partielle plutôt qu’une réponse approximative.

Tu dois être particulièrement attentif à :
- les cotes,
- cartouche en bas à droite,
- les annotations manuscrites,
- la masse

Tu dois toujours fournir :

1. un résumé simple,
2. les dimensions principales,
3. un tableau des cotes importantes,
4. une estimation de la masse,
5. le contenu du cartouche du plan,
6. les limites de fiabilité de l’analyse."""

def ask_gemini(request):
    response_text = ""
    question = ""
    uploaded_image = None
    uploaded_file_name = None

    if request.method == "POST":
        question = request.POST.get("question", "").strip()
        file = request.FILES.get("plan_file")

        if file or question:
            if file:
                file_bytes = file.read()
                mime_type = file.content_type or "application/octet-stream"
                file_name = file.name

                if mime_type.startswith("image/"):
                    pil_image = Image.open(io.BytesIO(file_bytes))
                    uploaded_image = f"data:{mime_type};base64,{base64.b64encode(file_bytes).decode('utf-8')}"
                    file_part = pil_image
                elif mime_type == "application/pdf" or file_name.lower().endswith(".pdf"):
                    uploaded_file_name = file_name
                    file_part = types.Part.from_bytes(
                        data=file_bytes,
                        mime_type="application/pdf"
                    )
                else:
                    response_text = "Format de fichier non supporté. Seules les images et les PDF sont acceptés."
                    file_part = None

                user_text = SYSTEM_PROMPT + "\n\n"
                if question:
                    user_text += f"Question supplémentaire de l'utilisateur :\n{question}\n\n"
                user_text += "Analyse ce document (image ou PDF) en suivant STRICTEMENT les instructions ci-dessus."

                contents = [user_text, file_part] if file_part else None

            else:
                contents = f"{SYSTEM_PROMPT}\n\nQuestion de l'utilisateur :\n{question}"

            if contents:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=contents
                )
                response_text = response.text

    return render(request, "ask_gemini.html", {
        "question": question,
        "response_text": response_text,
        "uploaded_image": uploaded_image,
        "uploaded_file_name": uploaded_file_name,
    })