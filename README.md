# 🧠 AI-Powered Note Summarizer + PDF Extractor API

**NoteWise** is an AI-powered backend API built with **Flask**, designed to allow users to upload PDF or text files, extract text using OCR (if needed), and generate concise summaries using AI models. Built with background task processing (via **Celery + Redis**), it ensures responsive performance and is secured with **JWT-based authentication**. This project is perfect for integrating into web or mobile platforms where automatic note generation is needed.

---

## 🚀 Features

- 📄 **Upload PDF/Text Files** – Accepts both plain text and PDF files.
- 👁 **OCR Support** – Automatically extracts text from scanned PDFs using Tesseract OCR.
- ✨ **AI Summarization** – Summarizes extracted or provided text using a free AI model.
- 🧾 **User Auth & JWT** – Secure login and protected endpoints using JSON Web Tokens.
- ⏳ **Asynchronous Tasks** – Background summarization using **Celery** and **Redis**.
- 📂 **CRUD for Summaries** – Users can create, retrieve, update, and delete their summaries.
- 📦 **REST API** – Swagger/OpenAPI docs included using **Flasgger**.
- 🗃 **PostgreSQL** – Stores users and summaries efficiently using SQLAlchemy ORM.

---

## 🧱 Tech Stack

| Tech            | Purpose                              |
|------------------|--------------------------------------|
| Flask           | Python Web Framework                  |
| Celery + Redis  | Background task queue                 |
| PostgreSQL      | Database                              |
| SQLAlchemy      | ORM for database management           |
| PyJWT / Flask-JWT-Extended | Token-based authentication |
| Flasgger        | Swagger-based API documentation       |
| Tesseract OCR   | PDF text extraction from images       |
| SpaCy / Transformers | AI/NLP-based summarization       |

---

## 📁 Project Structure

```

ai-note-summarizer/
├── app/
│   ├── auth/                  # Authentication logic
│   ├── models/                # SQLAlchemy models
│   ├── routes/                # Main routes (upload, summarize)
│   ├── tasks/                 # Celery background tasks
│   ├── utils/                 # Helpers (OCR, summarizer)
│   ├── **init**.py            # Flask app factory
├── instance/
│   └── config.py              # Configuration file
├── migrations/                # Alembic DB migrations
├── run.py                     # App entry point
├── celery\_worker.py           # Celery task runner
├── requirements.txt           # Python dependencies
└── README.md

````

---

## ✅ Getting Started

### 📌 Prerequisites

- Python 3.10+
- PostgreSQL
- Redis
- Tesseract OCR engine installed
- `virtualenv` or `pipenv` recommended

---

### ⚙️ Installation

```bash
git clone https://github.com/your-username/ai-note-summarizer.git
cd ai-note-summarizer
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
````

---

### 🔧 Configure Your Environment

Update `instance/config.py` or use `.env` with the following:

```env
SECRET_KEY=your-secret
JWT_SECRET_KEY=your-jwt-secret
SQLALCHEMY_DATABASE_URI=postgresql://username:password@localhost/note_summarizer
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

---

### 🗃 Initialize the Database

```bash
flask db init       # Only once
flask db migrate -m "initial"
flask db upgrade
```

---

### 🧠 Start Redis & Celery Worker

```bash
# In a new terminal
redis-server

# In another terminal
celery -A app.tasks.celery worker --loglevel=info
```

---

### ▶️ Start the Flask API

```bash
flask run
```

Visit Swagger UI docs at:
🔗 [http://localhost:5000/apidocs](http://localhost:5000/apidocs)

---

## 🔐 API Endpoints

| Method | Endpoint         | Description                     |
| ------ | ---------------- | ------------------------------- |
| POST   | `/auth/register` | Register new user               |
| POST   | `/auth/login`    | Log in and receive JWT          |
| POST   | `/summarize`     | Upload file and trigger summary |
| GET    | `/summaries`     | Retrieve all user summaries     |
| GET    | `/summary/<id>`  | Retrieve single summary         |
| DELETE | `/summary/<id>`  | Delete a summary                |

> 🛡 All endpoints except `/auth/*` require `Authorization: Bearer <JWT>` in headers.

---

## 🧠 How It Works

1. User uploads PDF or text via `/summarize`.
2. Text is extracted (with OCR if needed).
3. A Celery background task performs AI summarization.
4. The summary is saved and can be accessed via `/summaries`.

---

## 🧪 Sample AI Models Used

* Free-tier **HuggingFace Transformers** (e.g., `t5-small`, `bart`, or `spacy`)
* Easy to plug in OpenAI/GPT-based summarizers (if needed)

---

## 🧭 Roadmap

* [x] Token-based authentication
* [x] Text/PDF Upload + OCR support
* [x] Background summarization task
* [x] CRUD API for summaries
* [x] Swagger UI documentation
* [ ] Email-based user verification
* [ ] Multi-language summarization support
* [ ] Web frontend for users

---

## 🙋‍♂️ Author

**Chinedu Aguwa**
AI Engineer | Software Developer | Civil Engineer
📧 [neduaguwa443@gmail.com](mailto:neduaguwa443@gmail.com)
🔗 [LinkedIn](https://www.linkedin.com/in/chinedu-aguwa)
💻 [GitHub](https://github.com/chi2785443)

---

## 🤝 Contributing

Pull requests, ideas, and feedback are welcome!
Fork the repo and submit a PR or open an issue.

---

## 📄 License

Licensed under the **MIT License**.
See the [LICENSE](LICENSE) file for details.

```

