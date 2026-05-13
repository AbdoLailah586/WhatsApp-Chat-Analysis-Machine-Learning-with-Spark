# 📱 WhatsApp Chat Analysis & ML with Spark

A high-performance Big Data project that parses, analyzes, and classifies WhatsApp chat logs using **Apache Spark**, featuring a premium **React Dashboard** and an interactive **Jupyter Notebook**.

## 🌟 Overview
This project transforms raw WhatsApp text exports into actionable insights. It uses Spark's distributed computing to handle large-scale chat data and Spark MLlib to categorize conversations into groups like **Work (Important)**, **Friends**, and **Studying**.

### Key Features
- **Big Data Scale**: Powered by PySpark for high-speed processing.
- **AI Classification**: Random Forest ML model for automated chat categorization.
- **Premium Dashboard**: Beautiful React UI with glassmorphism and real-time charts.
- **Interactive EDA**: Comprehensive Jupyter Notebook for step-by-step analysis.
- **Urgency Tracking**: Keyword-based urgency detection for critical messages.

## 🛠️ Tech Stack
- **Backend**: Python, PySpark, Flask (API)
- **Frontend**: React, Vite, Tailwind CSS, Recharts, Lucide Icons
- **ML/DS**: Spark MLlib, TF-IDF, Jupyter Notebooks

## 📂 Project Structure
```text
├── dataset/               # Your categorized chat files (.txt)
├── backend/               # Flask API serving Spark results
├── frontend/              # Modern React Dashboard
├── whatsapp_analysis.ipynb # Interactive Jupyter Notebook
├── spark_processor.py      # Core Spark ML engine
├── run_full_app.bat       # Master runner for the entire stack
└── .gitignore             # Configured for clean git history
```

## 🚀 Getting Started

### 1. Requirements
- Python 3.11+
- Java (JDK 17 recommended for Spark)
- Node.js (for React frontend)

### 2. Setup
1. Clone the repository.
2. Place your WhatsApp `.txt` files in `dataset/work`, `dataset/friends`, or `dataset/studying`.
3. Run `npm install` inside the `frontend` folder.

### 3. Execution
The easiest way to run the project on Windows is using the provided scripts:

- **Run Full Dashboard**: Double-click `run_full_app.bat`. This starts the Backend, Frontend, and opens your browser.
- **Run Terminal Report**: Double-click `run_all.bat`.
- **Run Notebook**: Open `whatsapp_analysis.ipynb` in VS Code or Jupyter Lab.

## 📊 Machine Learning Pipeline
The system uses a sophisticated NLP pipeline:
1. **Tokenization**: Breaking messages into words.
2. **Stopwords Removal**: Cleaning non-essential words.
3. **TF-IDF Vectorization**: Converting text to numerical data.
4. **Random Forest Classifier**: Training a model with 50 trees for robust classification.

## 📄 License
This project was developed as part of a Big Data
