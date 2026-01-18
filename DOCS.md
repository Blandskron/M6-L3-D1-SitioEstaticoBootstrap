# Aplicación 1: Despliegue de contenido estático y estructura visual base

Proyecto: **sitio_estatico_bootstrap**  
App: **web**

Este documento explica en detalle qué hace cada parte del ejercicio y cómo se conecta el código (MTV + DRY + templates + static + formulario con validación backend).

---

## 1) Estructura final (carpetas relevantes)

Ubicación típica (dentro de la carpeta donde está `manage.py`):

```

sitio_estatico_bootstrap/
├─ manage.py
├─ sitio_estatico_bootstrap/
│  ├─ settings.py
│  ├─ urls.py
│  └─ ...
├─ web/
│  ├─ views.py
│  ├─ urls.py
│  ├─ forms.py
│  └─ ...
├─ templates/
│  ├─ base.html
│  ├─ partials/
│  │  ├─ navbar.html
│  │  └─ footer.html
│  └─ web/
│     ├─ home.html
│     ├─ acerca.html
│     ├─ contacto.html
│     └─ contacto_ok.html
└─ static/
└─ css/
└─ site.css

````

Piezas del patrón MTV:
- **Views**: `web/views.py` (controla el flujo de respuesta).
- **Templates**: `templates/...` (presentación).
- **Models**: no se usan (intencionalmente, para mantener el enfoque del ejercicio).

---

## 2) Configuración del proyecto (`settings.py`) y por qué es crítica

### 2.1 Registrar la app en `INSTALLED_APPS`

Código:

```python
INSTALLED_APPS += [
    "web",
]
````

Qué logra:

* Django “carga” la app `web` al iniciar.
* Permite que Django use los módulos de la app si se agregan después (admin, modelos, señales, etc.).
* Mantiene el proyecto modular: la app existe como unidad independiente.

---

### 2.2 Configurar templates globales con `TEMPLATES[0]["DIRS"]`

Código:

```python
TEMPLATES[0]["DIRS"] = [BASE_DIR / "templates"]
```

Qué significa:

* Django tiene un “motor de templates”.
* Para renderizar `render(request, "web/home.html", ctx)` necesita saber **dónde buscar** templates.
* `DIRS` define carpetas explícitas de búsqueda (en este proyecto: `templates/`).

Por qué se usa `BASE_DIR / "templates"`:

* `BASE_DIR` es la ruta base del proyecto (normalmente donde está `manage.py`).
* `BASE_DIR / "templates"` construye una ruta segura (pathlib) sin concatenar strings.

---

### 2.3 Configuración de archivos estáticos: `STATIC_URL` y `STATICFILES_DIRS`

Código:

```python
STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]
```

Qué significa:

* `STATIC_URL` es el prefijo que Django usa para servir static en desarrollo:

  * Ej: `/static/css/site.css`
* `STATICFILES_DIRS` le dice a Django:

  * “además de buscar static dentro de apps, busca también en esta carpeta global `static/`”

En la práctica:

* `static/css/site.css` se puede referenciar desde templates usando `{% static %}`.

---

## 3) Enrutamiento (URLs) y flujo de ejecución

### 3.1 URLs del proyecto (`sitio_estatico_bootstrap/urls.py`)

Código:

```python
urlpatterns += [
    path("", include(("web.urls", "web"), namespace="web")),
]
```

Qué hace:

* Al visitar cualquier URL, Django empieza en el `urls.py` del proyecto.
* Con `include(...)` delega la resolución de rutas a la app.

Qué aportan `namespace="web"` y `app_name="web"`:

* Permiten generar URLs por nombre en templates sin colisiones.
* Ejemplo:

  * `{% url 'web:contacto' %}` apunta a la ruta cuyo `name="contacto"` dentro de `web`.

---

### 3.2 URLs de la app (`web/urls.py`)

Código:

```python
urlpatterns = [
    path("", views.home, name="home"),
    path("acerca/", views.acerca, name="acerca"),
    path("contacto/", views.contacto, name="contacto"),
]
```

Qué significa:

* La ruta `""` (vacía) corresponde a `/`.
* `acerca/` corresponde a `/acerca/`.
* `contacto/` corresponde a `/contacto/`.

Cada ruta apunta a una función de vista (`views.*`).

---

## 4) Vistas (`web/views.py`) — lógica del lado servidor (MTV)

Las vistas se encargan de:

* recibir la request
* decidir qué template renderizar
* construir el contexto (datos para el template)
* devolver `HttpResponse`

### 4.1 `home()`

Código clave:

```python
return render(request, "web/home.html", {"titulo": "Inicio", "beneficios": [...]})
```

Qué hace:

* Renderiza `templates/web/home.html`.
* Entrega un contexto:

  * `titulo`: string (para título en el layout)
  * `beneficios`: lista (se itera con `{% for %}` en template)

Qué demuestra:

* Renderización de contenido dinámico simple (lista → HTML).
* Separación de responsabilidades:

  * la vista prepara datos
  * el template decide cómo mostrarlos

---

### 4.2 `acerca()`

Código clave:

```python
return render(request, "web/acerca.html", {"titulo": "Acerca", "equipo": [...]})
```

Qué hace:

* Renderiza una página informativa.
* Pasa una lista `equipo` para iterar en template.

Qué demuestra:

* Página “estática” con estructura moderna pero datos simples.

---

### 4.3 `contacto()` — formulario y validación backend

Esta vista usa el patrón clásico:

* Si es GET: mostrar formulario vacío
* Si es POST: validar, y si es válido, mostrar confirmación

Código conceptual:

```python
if request.method == "POST":
    form = ContactoForm(request.POST)
    if form.is_valid():
        return render(... ok ...)
else:
    form = ContactoForm()

return render(... form ...)
```

Puntos clave:

#### a) `request.method`

* `GET`: el navegador pide la página
* `POST`: el navegador envía datos del formulario

#### b) `ContactoForm(request.POST)`

* `request.POST` contiene datos enviados (campos del form).
* El form los “absorbe” y prepara validación.

#### c) `form.is_valid()`

* Ejecuta validaciones del backend:

  * campos requeridos
  * tamaños máximos
  * validación de email
  * `min_length` para mensaje
  * cualquier validación extra definida en el form

Si falla:

* el form queda con errores en `form.<campo>.errors`
* el template los muestra en rojo

Si pasa:

* `form.cleaned_data` contiene datos limpios y tipados.

#### d) Confirmación sin persistencia

La confirmación `contacto_ok.html` se usa para mostrar:

* que la validación se ejecutó correctamente
* los datos recibidos

No se guarda en DB porque el foco del ejercicio es templates/static/form validation.

---

## 5) Formularios (`web/forms.py`) — validación backend

Se usa `forms.Form`.

Ejemplo (campo):

```python
email = forms.EmailField(required=True)
```

Qué valida automáticamente:

* que exista (`required=True`)
* que tenga formato de email válido

Campo `mensaje`:

```python
mensaje = forms.CharField(min_length=10, widget=forms.Textarea)
```

Qué valida:

* no vacío
* al menos 10 caracteres

Qué hace `widget=forms.Textarea`:

* cambia la representación HTML del input:

  * en vez de `<input>`, se renderiza un `<textarea>`

---

## 6) Templates — presentación con herencia e includes (DRY)

### 6.1 `base.html` — layout principal

Este template contiene:

* carga de Bootstrap CDN
* carga de CSS propio desde `/static/`
* navbar y footer por `include`
* secciones `block` para que los hijos reemplacen contenido

Bloques usados:

```django
{% block title %}...{% endblock %}
{% block h1 %}...{% endblock %}
{% block subtitle %}...{% endblock %}
{% block content %}...{% endblock %}
```

Qué permite:

* Cada página define su contenido específico.
* El header/navbar/footer no se repite.

---

### 6.2 Parciales: `partials/navbar.html` y `partials/footer.html`

Se incluyen en `base.html`:

```django
{% include "partials/navbar.html" %}
{% include "partials/footer.html" %}
```

Qué logra:

* DRY: no repetir navbar/footer en cada página.
* Un cambio en navbar afecta todo el sitio inmediatamente.

---

### 6.3 Templates de páginas (herencia)

Ejemplo:

```django
{% extends "base.html" %}
```

Significa:

* el template hijo “hereda” base.html
* solo define bloques que necesita modificar

---

### 6.4 Variables, for, if

#### Variables

`{{ titulo }}` imprime el valor del contexto.

#### For

En `home.html`, se itera:

```django
{% for b in beneficios %}
  <li>{{ b }}</li>
{% endfor %}
```

Se transforma una lista Python en HTML.

#### If

En `contacto.html` se usan condicionales para mostrar errores si existen:

```django
{% if form.nombre.errors %}
  ...
{% endif %}
```

---

### 6.5 `{% url %}` y namespacing

Ejemplo:

```django
<a href="{% url 'web:contacto' %}">Contacto</a>
```

Qué hace:

* Genera la URL real buscando por nombre.
* Evita hardcodear rutas (`/contacto/`) en el HTML.
* Si cambias la ruta en `urls.py`, los links siguen funcionando (si el name se mantiene).

---

## 7) Archivos estáticos — `{% load static %}` y `{% static %}`

En `base.html`:

```django
{% load static %}
<link rel="stylesheet" href="{% static 'css/site.css' %}">
```

Qué hace:

* `load static` habilita el tag `{% static %}`.
* `{% static 'css/site.css' %}` produce una URL como:

  * `/static/css/site.css`

`STATICFILES_DIRS` define de dónde se obtiene ese archivo.

---

## 8) Bootstrap — estructura visual base

Bootstrap se cargó por CDN para no instalar nada adicional.

Se usan componentes/estilos típicos:

* `navbar` con `navbar-expand-lg` para responsividad
* grilla `row` / `col-*` para responsive layout
* tarjetas `card`
* botones `btn`

Esto permite:

* diseño “moderno” y usable con poco CSS propio.

---

## 9) Formulario en template y seguridad: CSRF

En `contacto.html`:

```django
{% csrf_token %}
```

Qué es:

* Token anti-CSRF que Django exige en formularios POST.
* Protege contra envíos maliciosos desde otros sitios.

Si no se pone:

* Django rechaza el POST con error 403.

---

## 10) Flujo completo de cada ruta

### `/`

```
urls.py (proyecto)
 → include web.urls
 → web.urls: "" → views.home
 → render("web/home.html", contexto)
 → base.html + home.html
 → respuesta HTML
```

### `/acerca/`

```
urls.py (proyecto)
 → include web.urls
 → web.urls: "acerca/" → views.acerca
 → render("web/acerca.html", contexto)
 → base.html + acerca.html
 → respuesta HTML
```

### `/contacto/` GET

```
views.contacto (GET)
 → form = ContactoForm()
 → render("web/contacto.html", {"form": form})
```

### `/contacto/` POST

```
views.contacto (POST)
 → form = ContactoForm(request.POST)
 → form.is_valid()
   - si falla: render contacto.html con errores
   - si pasa: render contacto_ok.html con cleaned_data
```

---

## 11) Qué cumple este ejercicio (en términos de código)

* **Entorno virtual**: `venv`
* **Templates**: renderización con contexto
* **Herencia de plantillas**: `base.html` + `{% extends %}`
* **DRY**: includes de navbar/footer y layout único
* **Control en plantillas**: `{% for %}`, `{% if %}`
* **Static**: configuración `STATIC_URL`, `STATICFILES_DIRS`, `{% static %}`
* **Navegación**: `{% url %}` con namespace
* **MTV**: vistas (lógica) + templates (presentación) + (sin modelos)
* **Formulario**: validación backend con `forms.Form` y `is_valid()`
