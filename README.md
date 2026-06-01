# ☕ Coffee AI — E-commerce + AI Chatbot

An AI-powered full-stack coffee shop application featuring a FastAPI backend, RAG-based intelligent chatbot, and a modern React.js frontend.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=flat&logo=tailwindcss&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)

---

## 🚀 Features

- 🛒 **Product Catalog** — Browse and search coffee products with filters
- 🛍️ **Cart & Order Management** — Add to cart, place and track orders
- 🔐 **JWT Authentication** — Secure user registration, login, and protected routes
- 🤖 **AI Chatbot** — RAG-based chatbot with vector embeddings for semantic product search and personalized recommendations
- 📱 **Responsive UI** — Built with React.js and Tailwind CSS

---

## 🏗️ Project Structure

```
coffeeAI/
├── chatbot_rag-main/        # Python FastAPI backend + RAG chatbot
│   ├── core/                # RAG logic, embeddings, vector search
│   ├── data/                # Vector store and data files
│   ├── database/            # Database schema and service
│   ├── main.py              # FastAPI entry point
│   └── requirements.txt     # Python dependencies
├── src/                     # React.js frontend
│   ├── components/          # Reusable UI components
│   ├── pages/               # Application pages
│   ├── services/            # API service calls (Axios)
│   └── App.tsx              # Main React app
├── public/                  # Static assets
├── .gitignore
├── package.json
└── README.md
```

---

## ⚙️ Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js v16+
- Git

### 1. Clone the repository
```bash
git clone https://github.com/kbsubramanyasharma/coffeeAI.git
cd coffeeAI
```

### 2. Backend Setup
```bash
cd chatbot_rag-main
pip install -r requirements.txt
python setup_database.py
python main.py
```
Backend runs at: `http://localhost:8000`
API docs available at: `http://localhost:8000/docs`

### 3. Frontend Setup
```bash
cd ..
npm install
npm run dev
```
Frontend runs at: `http://localhost:5173`

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login and get JWT token |
| GET | `/products` | Get all products |
| GET | `/products/{id}` | Get product by ID |
| POST | `/cart` | Add item to cart |
| GET | `/orders` | Get user orders |
| POST | `/orders` | Place new order |
| POST | `/chat` | Chat with AI chatbot |

---

## 🧠 How the RAG Chatbot Works

1. Product data is converted into **vector embeddings** at setup
2. User query is embedded and compared using **cosine similarity**
3. Most relevant products are retrieved from the vector store
4. Retrieved context is passed to the **AI model** to generate a response
5. User gets a personalized, context-aware recommendation

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python, FastAPI |
| AI / Chatbot | RAG, Vector Embeddings, Generative AI |
| Database | SQLite (migrating to MySQL) |
| Frontend | React.js, TypeScript, Tailwind CSS, Vite |
| Auth | JWT (JSON Web Tokens) |
| Tools | Git, Postman, VS Code |

---

## 📸 Screenshots

> *Coming soon — will add after deployment*

---

## 🔮 Future Improvements

- [ ] Migrate database from SQLite to MySQL
- [ ] Deploy backend on AWS EC2 with RDS
- [ ] Store product images in AWS S3
- [ ] Add payment gateway integration
- [ ] Write unit tests with pytest

---

## 👤 Author

**Subrahmanya Sharma K B**
- GitHub: [@kbsubramanyasharma](https://github.com/kbsubramanyasharma)
- LinkedIn: [subrahmanyasharma-kb](https://www.linkedin.com/in/subrahmanyasharma-kb)
- Email: subrahmanyasharmakb@gmail.com

---

## 📄 License

This project is licensed under the MIT License.
