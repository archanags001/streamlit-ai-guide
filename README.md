# Streamlit AI Guide: AI-Powered Streamlit Documentation Tutor

## Project Overview

Welcome to **Streamlit AI Guide** – an interactive AI tutor built to help you learn Streamlit easily and efficiently.

Streamlit is a powerful Python library for building data apps. But official docs can be long and sometimes hard to navigate. This tool makes that easier.

Instead of searching through pages of documentation, just ask a question in plain English. The AI will give you a clear answer and often include a working code example. It’s like having a helpful Streamlit expert always around when you need them.

This guide is designed to run locally on your own computer, so you can explore, learn, and build at your own pace.

---

#### Example Questions You Can Ask:
- “Teach me the basics of Streamlit”
- “How do I use `st.slider`?”
- “What’s the best way to deploy a Streamlit app?”

---

Let’s build something great with Streamlit!


## Technical Stack

**Frontend Interface**  
- **Streamlit** – Simple and interactive UI built using Streamlit.

**AI Brain (RAG System)**  
- **LangChain** – Orchestrates how the AI retrieves and responds with relevant information.

**Knowledge Bank**  
- **ChromaDB** – Stores indexed Streamlit documentation for fast, accurate lookups.

**Language Model & Embeddings**  
- **Google Gemini API**  
  - `gemini-1.5-flash` – Handles conversation and answers.  
  - `embedding-001` – Converts text into embeddings for better understanding.

**Document Loading & Processing**  
- **RecursiveUrlLoader**, **WebBaseLoader**, **BeautifulSoupTransformer**, **RecursiveCharacterTextSplitter**  
  - These tools help load and break down content from web pages into usable chunks.

**Secret Management**  
- **python-dotenv** – Keeps your API keys and environment variables safe on your local machine.

## Repository Structure

Here’s a quick overview of how this project is organized:

```markdown
- streamlit-ai-guide/        
├── code/
│   ├── app.py                # Your Streamlit app, which is the main program you run
│   ├── data_collection.py    # The script that downloads Streamlit docs and builds the knowledge base
│   └── rag_operations.py     # Contains the brain for the AI and how it finds answers
├── .env.example              # A template for your private API key file (we do NOT upload your actual key!)
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

