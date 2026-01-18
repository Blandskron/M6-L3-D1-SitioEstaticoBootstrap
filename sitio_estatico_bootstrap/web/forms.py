from __future__ import annotations

from django import forms


class ContactoForm(forms.Form):
    # Validación backend: required, max_length, email, etc.
    nombre = forms.CharField(
        label="Nombre",
        max_length=60,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Tu nombre"}),
    )
    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "tu@email.com"}),
    )
    asunto = forms.CharField(
        label="Asunto",
        max_length=80,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Motivo del contacto"}),
    )
    mensaje = forms.CharField(
        label="Mensaje",
        required=True,
        min_length=10,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "Escribe tu mensaje..."}),
    )

    def clean_nombre(self) -> str:
        # Ejemplo de validación específica adicional (backend)
        nombre = self.cleaned_data["nombre"].strip()
        if len(nombre) < 2:
            raise forms.ValidationError("El nombre debe tener al menos 2 caracteres.")
        return nombre
