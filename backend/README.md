# WhatsApp Message Categorizer - Backend

## Setup Instructions

1. Create a virtual environment:
   `python -m venv venv`
   
2. Activate the virtual environment:
   `source venv/bin/activate` or `venv\Scripts\activate` on Windows
   
3. Install dependencies:
   `pip install -r requirements.txt`
   
4. Copy `.env.example` to `.env`:
   `cp .env.example .env`
   
5. Put your GEMINI_API_KEY in backend/.env — replace 'your_gemini_api_key_here' with your actual key from https://aistudio.google.com/apikey
   
6. Ensure PostgreSQL is running and update `DATABASE_URL` in `.env` if necessary.

7. Run the application:
   `uvicorn app.main:app --reload`
