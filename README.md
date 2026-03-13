# 🏛️ Heritage Guide AI

An AI-powered heritage site guide that helps users explore, learn about, and interact with historical and cultural heritage sites through intelligent conversation and knowledge retrieval.

---

## 📋 Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

---

## 🌟 About the Project

**Heritage Guide AI** is a Python-based intelligent assistant designed to serve as a virtual guide for heritage and cultural sites. It leverages AI models and a curated knowledge base to answer questions, provide historical context, and assist users in understanding the significance of heritage locations.

Whether you're a traveler, researcher, or student, Heritage Guide AI makes exploring cultural history more accessible and engaging.

---

## ✨ Features

- 🤖 **AI-Powered Conversations** — Natural language Q&A about heritage sites and history
- 📚 **Knowledge Base Integration** — Queries are grounded in a structured, curated knowledge base
- 🖼️ **File Upload Support** — Upload documents or images related to heritage sites for context-aware responses
- ⚙️ **Configurable Models** — Easily swap or configure AI models via the `models/` and `config/` directories
- 🛠️ **Utility Modules** — Modular utility functions for clean, maintainable code

---

## 📁 Project Structure

```
heritage-guide-ai/
├── app.py               # Main application entry point
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
├── .gitignore
│
├── config/              # Configuration files (model settings, app config)
├── knowledge_base/      # Curated heritage site data and documents
├── models/              # AI model definitions and integrations
├── uploads/             # Directory for user-uploaded files
└── utils/               # Helper utilities and shared functions
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- `pip` package manager
- An API key for your configured AI model (e.g., OpenAI, Anthropic, etc.)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Aishwary0402/heritage-guide-ai.git
   cd heritage-guide-ai
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Open `.env` and fill in your credentials and configuration:
   ```env
   API_KEY=your_api_key_here
   MODEL_NAME=your_model_name
   # Add any other required variables
   ```

---

## 🖥️ Usage

Run the application with:

```bash
python app.py
```

Once running, interact with the AI guide through the provided interface. You can ask questions about heritage sites, upload relevant documents, and get detailed, contextual responses powered by the knowledge base.

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

Please ensure your code follows the existing structure and is well-documented.

---

