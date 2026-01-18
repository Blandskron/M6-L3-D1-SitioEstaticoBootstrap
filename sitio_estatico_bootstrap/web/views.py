from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .forms import ContactoForm


def home(request: HttpRequest) -> HttpResponse:
    # Vista mínima (MTV): prepara contexto y renderiza template
    return render(
        request,
        "web/home.html",
        {
            "titulo": "Inicio",
            "beneficios": [
                "Estructura clara (proyecto vs app)",
                "Templates con herencia (DRY)",
                "Archivos estáticos (CSS/JS)",
                "Navegación con {% url %}",
            ],
        },
    )


def acerca(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "web/acerca.html",
        {
            "titulo": "Acerca",
            "equipo": ["Backend", "Frontend", "UX", "DevOps"],
        },
    )


def contacto(request: HttpRequest) -> HttpResponse:
    # Formulario con validación backend (Django Forms)
    if request.method == "POST":
        form = ContactoForm(request.POST)
        if form.is_valid():
            # En este proyecto no se persiste ni envía email; solo confirma validación exitosa.
            data = form.cleaned_data
            return render(
                request,
                "web/contacto_ok.html",
                {
                    "titulo": "Contacto",
                    "data": data,
                },
            )
    else:
        form = ContactoForm()

    return render(
        request,
        "web/contacto.html",
        {
            "titulo": "Contacto",
            "form": form,
        },
    )
