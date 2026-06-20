# MedLens+ Cloud Backend

AI-powered medical Q&A system with cloud-edge collaboration. This repository contains the Django REST backend and the llama.cpp inference server that powers the **Deep Mode** (cloud) tier of MedLens+. It handles user authentication, session persistence, and runs the MedGemma 27B model for complex clinical queries.

## 🧠 Tech Stack

- **Django REST Framework** – API backend
- **PostgreSQL** (SQLite for development) – session storage
- **llama.cpp** – LLM inference server (C++/CUDA)
- **MedGemma 27B** – medical LLM (GGUF quantized)
- **JWT** – stateless authentication
- **Nginx + Gunicorn** – production deployment (optional)

---

## 📁 Repository Structure

```
.
├── chat/                     # Django chat app (models, views, API)
├── medlens_backend/          # Django project settings
├── Model/                    # Place the GGUF model file here
├── media/                    # Uploaded images (temporarily stored)
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── .gitignore                # Excludes model files, venv, DB, etc.
└── README.md                 # This file
```

---

## 🚀 Quick Start

### 1. Clone & Setup Virtual Environment

```bash
git clone https://github.com/Umarii101/MedLensPlus.git
cd MedLensPlus
python3 -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Download the MedGemma 27B GGUF Model

The model is **not included** in this repository due to size. You must download a quantized GGUF version from Hugging Face.

**Recommended quantization**: `UD-IQ2_XXS` (7.85 GB) – good balance of quality and VRAM usage.

```bash
# Create the Model directory if it doesn't exist
mkdir -p Model

# Download using wget (or use huggingface-hub)
wget https://huggingface.co/unsloth/medgemma-27b-it-GGUF/resolve/main/UD-IQ2_XXS/medgemma-27b-it-UD-IQ2_XXS.gguf -O Model/medgemma-27b-it-UD-IQ2_XXS.gguf
```

Alternatively, use the `huggingface-hub` Python library:

```bash
pip install huggingface-hub
huggingface-cli download unsloth/medgemma-27b-it-GGUF UD-IQ2_XXS/medgemma-27b-it-UD-IQ2_XXS.gguf --local-dir ./Model --local-dir-use-symlinks False
```

> **Note**: If you prefer a different quantization (e.g., `Q4_K_M` for better quality at 16.5 GB), replace the file name accordingly. Check the [Hugging Face model page](https://huggingface.co/unsloth/medgemma-27b-it-GGUF) for all available versions.

### 5. Set Environment Variables (Optional)

Create a `.env` file in the root directory (or set them in your shell):

```
DEBUG=True
SECRET_KEY=your-secret-key-here
```

If you want to use PostgreSQL instead of SQLite, update `DATABASES` in `medlens_backend/settings.py`.

### 6. Start the Django Server

```bash
python manage.py runserver 0.0.0.0:8000
```

The API will be available at `http://localhost:8000`.

### 7. Start the llama.cpp Server (Inference)

You need the `llama-server` binary. Download a pre-built binary from the [llama.cpp releases](https://github.com/ggerganov/llama.cpp/releases) or build from source.

**Example command** (adjust paths as needed):

```bash
# Assuming llama-server is in your PATH
llama-server -m Model/medgemma-27b-it-UD-IQ2_XXS.gguf \
             --host 0.0.0.0 --port 8080 \
             --parallel 2 --cont-batching
```

> **Important**: The Django backend expects the llama.cpp server to be running on `http://localhost:8080`. If you change the port, update the `LLAMA_SERVER_URL` in your Django settings.

---

## 🔌 API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `POST` | `/api/register/` | Create a new user account | ❌ |
| `POST` | `/api/login/` | Obtain JWT access & refresh tokens | ❌ |
| `POST` | `/api/chat/` | Send a message (text + optional image) | ✅ Bearer |
| `GET` | `/api/chat/<id>/` | Fetch full conversation history | ✅ Bearer |
| `GET` | `/api/chats/` | List all sessions for the authenticated user | ✅ Bearer |

All authenticated endpoints require a `Bearer <access_token>` header.

---

## 🧪 Testing the System

### 1. Create a user

```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass"}'
```

### 2. Login to get JWT

```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass"}'
```

Save the `access` token from the response.

### 3. Send a chat message (text only)

```bash
curl -X POST http://localhost:8000/api/chat/ \
  -H "Authorization: Bearer <your_access_token>" \
  -H "Content-Type: application/json" \
  -d '{"message":"Describe the differential diagnosis of a lung nodule."}'
```

### 4. Send a chat message with an image

```bash
curl -X POST http://localhost:8000/api/chat/ \
  -H "Authorization: Bearer <your_access_token>" \
  -F "message=What does this X-ray show?" \
  -F "image=@/path/to/chest_xray.jpg"
```

---

## 📦 Deployment Notes

- **Production**: Use `Gunicorn` and `Nginx` instead of `runserver`. Example:
  ```bash
  gunicorn medlens_backend.wsgi:application --bind 0.0.0.0:8000 --workers 4
  ```
- **Database**: Switch to PostgreSQL in production. Update `DATABASES` in `settings.py`.
- **Model Storage**: Keep the GGUF file on a fast disk (preferably NVMe SSD) for optimal inference speed.
- **GPU**: The llama.cpp server uses GPU if compiled with CUDA support. Ensure you have a compatible NVIDIA GPU with at least 10 GB VRAM for the 27B model.

---

## 🧾 License

This project is for academic and research purposes only. The MedGemma model is governed by the [Health AI Developer Foundations terms](https://developers.google.com/health-ai-developer-foundations/terms). Please ensure compliance when using this system in any production environment.

---

## 🤝 Contributing

This is a course project – contributions are not expected, but feel free to report issues or suggest improvements.

---

## 📄 References

- [MedGemma on Hugging Face](https://huggingface.co/unsloth/medgemma-27b-it-GGUF)
- [llama.cpp](https://github.com/ggerganov/llama.cpp)
- [Django REST Framework](https://www.django-rest-framework.org/)
```

---

### What I Included:

- ✅ **Clear setup instructions** – virtual env, dependencies, migrations.
- ✅ **Model download** – exact `wget` command and alternative `huggingface-hub` approach.
- ✅ **llama.cpp server command** – with the specific GGUF file.
- ✅ **API endpoints** – complete table with auth info.
- ✅ **Testing with curl** – text and image upload examples.
- ✅ **Deployment hints** – for production readiness.

