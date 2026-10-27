# Code-Review-GPT 🚀

**Code-Review-GPT** is a full-stack AI-powered code auditing tool designed to provide instant, expert-level feedback on Python snippets. Built with a modern tech stack including **FastAPI**, **MySQL**, and **Google Gemini AI**, it allows developers to analyze code for efficiency, security, and best practices. ✨

---

## ✨ Features

* **AI-Powered Analysis**: Leverages the Gemini 3 Flash model to provide detailed code reviews.
* **Persistent History**: Automatically saves every review to a MySQL database for future reference.
* **Real-time Search**: Instant client-side filtering to find specific snippets in your history.
* **PDF Export**: Generate and download professional PDF reports of your code reviews.
* **CRUD Operations**: Full control to create, view, search, and delete reviews permanently.
* **Modern UI**: Responsive, dark-mode dashboard built with Tailwind CSS.

---

## 🛠️ Tech Stack

| Layer | Technology Used |
| :--- | :--- |
| **Backend** | Python, FastAPI, SQLAlchemy |
| **AI Engine** | Google Gemini 3 Flash Preview |
| **Database** | MySQL (via SQLAlchemy + PyMySQL) |
| **Frontend** | HTML5, JavaScript (ES6+), Tailwind CSS |
| **Reporting** | FPDF (Python PDF Library) |

---

## 🚀 Getting Started

### 1. Prerequisites
* Python 3.9+
* MySQL 8 installed and running, with a database created: `CREATE DATABASE code_review_db;`
* A Google Gemini API Key

### 2. Installation
```bash
git clone [https://github.com/your-username/code-review-gpt.git](https://github.com/your-username/code-review-gpt.git)
cd code-review-gpt
pip install -r requirements.txt
```

### 3. Environment Setup
Create a .env file in the root directory and add your credentials:
    DATABASE_URL=mysql+pymysql://root:yourpassword@localhost:3306/code_review_db
    GEMINI_API_KEY=your_gemini_api_key_here

> **Using PostgreSQL instead?** The app talks to the database through SQLAlchemy, so no code changes are needed. Run `pip install psycopg2-binary` and set
> `DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/code_review_db`.

### 4. Running the application
Run the following command to start the server:
    python -m uvicorn main:app --reload
Open your browser and navigate to http://127.0.0.1:8000 to start reviewing code.

### 📊 Database Schema
The application uses a relational schema to manage code reviews efficiently:

id: Primary Key (Auto-incrementing)

code_snippet: Text

ai_feedback: Text

created_at: Timestamp (UTC)

### Lessons Learned

During the development of this project, I strengthened my skills in:

Asynchronous Programming: Handling non-blocking API calls with async/await in Python and JavaScript to ensure a smooth user experience.

Database Management: Managing relational data persistence and real-time synchronization between the UI and MySQL via SQLAlchemy, and migrating the project from PostgreSQL to MySQL by changing only the connection URL and driver.

Security & Credential Management: Implementing safety measures using .gitignore and practicing secure API key rotation after identifying potential leaks.

Full-Stack Integration: Bridging a FastAPI backend with a dynamic Tailwind-styled frontend, including implementing custom PDF generation logic.