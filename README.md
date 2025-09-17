> [!NOTE]
> English version

# **Building a voice agent for forms using FastAPI and Groq**

> Made with 💚 by [Sebastian Marat Urdanegui Bisalaya](https://sebastianurdanegui.vercel.app/)

## **Description**

## **Installation**

```bash
ENVIRONMENT=development
API_GROQ=****************
```

## **Business logic**


> [!NOTE]
> Spanish version

# **Construyendo un agente de voz para formularios usando FastAPI y Groq**

> Hecho con 💚 por [Sebastian Marat Urdanegui Bisalaya](https://sebastianurdanegui.vercel.app/)

## **Descripción**

Actualmente, las aplicaciones de la inteligencia artificial (AI) se han vuelto cada vez más populares en diferentes sectores económicos, pero quiero hacer hincapié en el área de atención al cliente, el cual paso del uso de chatbots con procedimientos rígidos al uso de herramientas de procesamiento de lenguaje natural (NLP) mediante los Large Language Models (LLMs).

Hace poco tuve la idea de crear un **agente de voz para formularios desde cero** con el objetivo que el cliente (a partir de ahora denotaré al usuario como cliente) pueda completar los formularios que se presenten en su actividad laboral, sin tener que escribir directamente los datos, sino utilizando su voz para agilizar el proceso reduciendo el tiempo de ingesta de datos. Sin embargo, antes de lanzarse a _codear_ es importante entender cuál es el proceso detrás del telón y, a partir de ello, construir la herramienta. La idea me parece genial y más aún que consideré documentar el proceso de desarrollo, para que los demás puedan replicar y mejorar la aplicación.

Por ahora, me enfocaré en el desarrollo del back-end ya que considero que es la parte fundamental para que el cliente (web/mobile app) pueda interactuar con nuestro agente. Utilizaré [Apidog](https://apidog.com/?utm_source=google_search&utm_medium=g&utm_campaign=21950794503&utm_content=174276878794&utm_term=postman&gad_source=1&gad_campaignid=21950794503&gbraid=0AAAAA-gKXrAXuQ5SDywhkC-p3I7Q1GrPk&gclid=Cj0KCQjwuKnGBhD5ARIsAD19RsZMH8AR5znhCr0T3MPvjfuflAkfQJa3YVRNtnNnpNug5e4DvTL_mgoaAl6CEALw_wcB) como plataforma de desarrollo de APIs para probar los endpoints.

A continuación, detallaré los pasos para clonar el presente [repositorio](https://github.com/SebastianUrdaneguiBisalaya/building-a-voice-agents-for-forms) en tu máquina y puedas seguir la explicación de cada uno de los pasos, y si deseas, realizar los cambios que consideres necesarios para adaptarlo a tus necesidades.

En esta ocasión, utilizaré [FastAPI](https://fastapi.tiangolo.com/) como framework para crear el back-end y [Groq](https://groq.com/) para conectarme a los modelos de AI y obtener los resultados.

> [!TIP]
> Puedes desarrollar esta aplicación en el framework de tu preferencia como [Express.js](https://expressjs.com/), [NestJS](https://nestjs.com/), [Route Handlers de Next.js](p), etc. Eligo [FastAPI](https://fastapi.tiangolo.com/) por el alto rendimiento, la facilidad de uso y utiliza el lenguaje de programación [Python](https://www.python.org/), logrando que el desarrollo se más fácil y robusto.

## **Instalación**

Dirígete a la terminal y ejecuta los siguientes comandos:

- Clonar el repositorio

```bash
git clone
```

- Crea un entorno virtual

```bash
python -m venv venv
```

- Activar el entorno virtual

```
source venv/bin/activate # (masOS)
venv\Scripts\activate # (Windows)
```

- Instalar las dependencias

```bash
pip install -r requirements.txt
```

- Crear un archivo `.env` en la raíz del proyecto con las siguientes variables de entorno:

```bash
ENVIRONMENT=development # (development o production)
API_GROQ=****************
```

- Ejecutar el servidor

```bash
fastapi dev src/app/main.py
```

## **Lógica de negocio**

