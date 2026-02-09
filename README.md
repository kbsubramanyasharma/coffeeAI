# Coffee AI

Coffee AI is a comprehensive project that combines a chatbot for answering coffee-related queries and a web application for managing coffee products, orders, and user interactions. The project is structured into multiple components, including a chatbot backend, a database service, and a frontend web application.

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## Features
- **Chatbot**: A Retrieval-Augmented Generation (RAG) chatbot for answering coffee-related queries.
- **Product Management**: Manage coffee products and their details.
- **Order Processing**: Handle customer orders and process them efficiently.
- **User Authentication**: Secure login and registration system.
- **Responsive Design**: A modern and responsive web interface.

## Project Structure
```
Coffee_AI-main/
├── chatbot_rag-main/       # Backend for the chatbot
│   ├── core/               # Core chatbot logic
│   ├── data/               # Data files for embeddings and vector stores
│   ├── database/           # Database service and schema
│   ├── requirements.txt    # Python dependencies
│   └── main.py             # Entry point for the chatbot server
├── src/                    # Frontend web application
│   ├── components/         # Reusable UI components
│   ├── pages/              # Application pages
│   ├── services/           # API services
│   └── App.tsx             # Main React application file
├── public/                 # Static assets
├── package.json            # Node.js dependencies
└── README.md               # Project documentation
```

## Setup Instructions

### Prerequisites
- Node.js (v16 or higher)
- Python (v3.8 or higher)
- Git

### Backend Setup
1. Navigate to the `chatbot_rag-main` directory:
   ```bash
   cd chatbot_rag-main
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the database:
   ```bash
   python setup_database.py
   ```
4. Run the chatbot server:
   ```bash
   python main.py
   ```

### Frontend Setup
1. Navigate to the root directory:
   ```bash
   cd Coffee_AI-main
   ```
2. Install Node.js dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

## Usage
- Access the web application at `http://localhost:3000`.
- Interact with the chatbot via the provided interface.

## Technologies Used
- **Frontend**: React, TypeScript, Tailwind CSS
- **Backend**: Python, FastAPI
- **Database**: SQLite
- **Other Tools**: Vite, PostCSS

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

