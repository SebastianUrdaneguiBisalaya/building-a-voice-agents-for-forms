# **Building a voice agent for forms using FastAPI and Groq**

> Made with 💚 by <a href="https://sebastianurdanegui.com/" target="_blank">Sebastian Marat Urdanegui Bisalaya</a>

> [!TIP]
> I recommend checking out [this guide](https://sebastianurdanegui.com/blog/article-1) to learn more about my development process, and then, you can follow the guide to implementing the voice agent for forms.

## **Preview**

![Desktop image](https://res.cloudinary.com/drzumfcdp/image/upload/v1758677345/Landing%20Page%20Sebastian/web_z7zrio.png)

## **Installation**

> [!WARNING]
> The client is not connected to the server yet, so you need to run the server first.

### **Server**

- Clone the repository

```
git clone https://github.com/SebastianUrdaneguiBisalaya/building-a-voice-agents-for-forms
```

- Move to the server folder

```bash
cd building-a-voice-agents-for-forms
```

- Create a virtual environment

```bash
python -m venv venv
```

- Activate the virtual environment

```bash
source venv/bin/activate # (masOS)
venv\Scripts\activate # (Windows)
```

- Install dependencies

```bash
pip install -r requirements.txt
```

- Create a `.env` file in the root folder with the following environment variables:

```bash
ENVIRONMENT=development # (development or production)
API_GROQ=****************
```

- Run the server

```bash
fastapi dev src/app/main.py
```

### **Client**

- Move to the client folder

```bash
cd building-a-voice-agents-for-forms/client
```

- Install dependencies

```bash
pnpm install
```

- Run the project

```bash
pnpm dev
```