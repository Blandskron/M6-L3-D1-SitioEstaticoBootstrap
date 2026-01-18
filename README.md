# Aplicación 1: Despliegue de contenido estático y estructura visual base

**Proyecto:** `sitio_estatico_bootstrap`  
**App:** `web`

Este tutorial muestra paso a paso cómo crear un proyecto Django que sirva **contenido estático moderno** usando **templates, herencia, archivos estáticos, Bootstrap y formularios con validación en backend**, respetando el patrón **MTV** y el principio **DRY**.

---

## 1) Crear carpeta del proyecto y entrar

```bash
mkdir sitio_estatico_bootstrap
cd sitio_estatico_bootstrap
````

---

## 2) Crear y activar entorno virtual

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3) Instalar Django

```bash
python -m pip install --upgrade pip
pip install django
```

---

## 4) Crear el proyecto Django (doble carpeta)

```bash
django-admin startproject sitio_estatico_bootstrap
```

Entrar donde está `manage.py`:

```bash
cd sitio_estatico_bootstrap
```

---

## 5) Crear la aplicación

```bash
python manage.py startapp web
```

---

## 6) Migraciones base y primer arranque

```bash
python manage.py migrate
python manage.py runserver
```

Servidor disponible en:

```
http://127.0.0.1:8000/
```

Detener servidor:

```bash
# CTRL + C
```

---

## 7) Configurar el proyecto

### 7.1 Editar `settings.py`

Agregar la app:

```python
INSTALLED_APPS += [
    "web",
]
```

Configurar templates globales:

```python
TEMPLATES[0]["DIRS"] = [BASE_DIR / "templates"]
```

Configurar archivos estáticos:

```python
STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]
```

---

### 7.2 Editar `urls.py` del proyecto

```python
from django.urls import include, path

urlpatterns += [
    path("", include(("web.urls", "web"), namespace="web")),
]
```

---

## 8) Configurar URLs de la app

Crear `web/urls.py`:

```python
from django.urls import path
from . import views

app_name = "web"

urlpatterns = [
    path("", views.home, name="home"),
    path("acerca/", views.acerca, name="acerca"),
    path("contacto/", views.contacto, name="contacto"),
]
```

---

## 9) Crear formulario con validación backend

Crear `web/forms.py`:

```python
from django import forms


class ContactoForm(forms.Form):
    nombre = forms.CharField(max_length=60, required=True)
    email = forms.EmailField(required=True)
    asunto = forms.CharField(max_length=80, required=True)
    mensaje = forms.CharField(min_length=10, required=True, widget=forms.Textarea)
```

---

## 10) Crear vistas

Editar `web/views.py`:

```python
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .forms import ContactoForm


def home(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "web/home.html",
        {
            "titulo": "Inicio",
            "beneficios": [
                "Bootstrap",
                "Templates con herencia",
                "Archivos estáticos",
                "Navegación interna",
            ],
        },
    )


def acerca(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "web/acerca.html",
        {
            "titulo": "Acerca",
            "equipo": ["Backend", "Frontend", "UX"],
        },
    )


def contacto(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ContactoForm(request.POST)
        if form.is_valid():
            return render(
                request,
                "web/contacto_ok.html",
                {
                    "titulo": "Contacto",
                    "data": form.cleaned_data,
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
```

---

## 11) Crear estructura de templates y static

```bash
mkdir templates
mkdir templates\web
mkdir templates\partials
mkdir static
mkdir static\css
```

---

## 12) Crear template base (herencia)

`templates/base.html`

* Contiene:

  * `<header>`
  * navbar
  * footer
  * bloques `{% block %}` reutilizables
  * Bootstrap vía CDN
  * carga de archivos static

---

## 13) Crear parciales reutilizables (DRY)

* `templates/partials/navbar.html`
* `templates/partials/footer.html`

Estos se incluyen con:

```django
{% include "partials/navbar.html" %}
{% include "partials/footer.html" %}
```

---

## 14) Crear templates de la app

* `templates/web/home.html`
* `templates/web/acerca.html`
* `templates/web/contacto.html`
* `templates/web/contacto_ok.html`

Todos extienden:

```django
{% extends "base.html" %}
```

Usan:

* variables (`{{ }}`)
* iteradores (`{% for %}`)
* condicionales (`{% if %}`)
* etiquetas URL (`{% url %}`)
* CSRF (`{% csrf_token %}`)

---

## 15) Crear CSS estático

`static/css/site.css`

Archivo cargado con:

```django
{% load static %}
<link rel="stylesheet" href="{% static 'css/site.css' %}">
```

---

## 16) Probar el sitio

Levantar servidor:

```bash
python manage.py runserver
```

Rutas disponibles:

* `/` → página principal
* `/acerca/` → página informativa
* `/contacto/` → formulario con validación backend

---

## 17) Principios aplicados

* **DRY**: base.html + includes
* **MTV**:

  * Model: no utilizado intencionalmente
  * Template: presentación
  * View: lógica y control
* **Static files**: CSS propio
* **Bootstrap**: estructura visual
* **Formularios Django**: validación en backend
* **Navegación**: `{% url %}`

---

## 18) Salir del entorno virtual

```bash
deactivate
```

---

## Estado final

Proyecto funcional que demuestra:

* Django sirviendo contenido estático
* Templates con herencia
* Archivos estáticos
* Navegación interna
* Formulario validado en backend
* Estructura limpia y modular
