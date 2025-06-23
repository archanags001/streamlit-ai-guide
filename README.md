# Streamlit AI Guide: AI-Powered Streamlit Documentation Tutor

<img src="https://raw.githubusercontent.com/archanags001/streamlit-ai-guide/main/streamlit_ai_home.png" alt="Streamlit AI Guide Home Screen" width="700" height="600">


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

## Key Features
* **Interactive Chat Interface**: Enjoy a smooth, user-friendly chat experience right in your web browser.
* **Conversational Memory**: Streamlit AI Guide remembers what we've talked about. If you ask a follow-up question, like "What about its arguments?" after discussing a function, it knows what "its" refers to. This makes our chats feel natural and easy.
* **Context-Aware Responses**: All answers come from Streamlit’s official documentation, so it reducing AI "hallucinations" and ensuring you get accurate, reliable information
* **On-Demand Code Examples**: Ask how to use something like st.slider, and the guide will give you a short, working code example you can try right away.
* **Focused on Streamlit Only**: This guide is built for Streamlit. If you ask about math or another tool, it’ll tell you it doesn’t cover that. It sticks to what it knows best.
* **See the Source:** For answers that come from the documents, you can click "Show Retrieved Sources." This lets you see the exact parts the AI used. It helps you trust the answers. This source section hides itself if the AI cannot find info or cannot answer your question.
---

## Technologies Used 

**Frontend Interface**  
- [Streamlit](https://streamlit.io/) – Simple and interactive UI built using Streamlit.

**AI Brain (RAG System)**  
- [LangChain](https://www.langchain.com/) – Orchestrates how the AI retrieves and responds with relevant information.

**Vector Database**  
- [ChromaDB](https://www.trychroma.com/) – Stores indexed Streamlit documentation for fast, accurate lookups.

**Large Language Model (LLM) & Embeddings**  
- [Google Gemini API](https://ai.google.dev/)
  - `gemini-1.5-flash` – Handles conversation and answers.  
  - `embedding-001` – Converts text into embeddings for better understanding.

**Document Loading & Processing**  
- **RecursiveUrlLoader**, **WebBaseLoader**, **BeautifulSoupTransformer**, **RecursiveCharacterTextSplitter**  
  - These tools help load and break down content from web pages into usable chunks.

**Secret Management**  
- **python-dotenv** – Keeps your API keys and environment variables safe on your local machine.
---

## Repository Structure
```
streamlit-ai-guide/        
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
---

## Installation & Setup
1. Clone the Repository
```
git clone https://github.com/archanags001/streamlit-ai-guide.git
cd streamlit-ai-guide
```
2. Install Dependencies
Install all required Python packages from requirements.txt:
```
pip install -r requirements.txt
```
3.  Set Up Your Google Gemini API Key
Create a .env file in the root directory and add your API key:
```
GOOGLE_API_KEY="YOUR_GEMINI_API_KEY_HERE"
```
4. Build the Streamlit Knowledge Base

This step downloads the Streamlit documentation. It then turns it into a searchable brain for your AI. You only need to do this **one time**. You might want to do it again if Streamlit's documentation changes a lot, or if you simply want to rebuild this brain.

First, open your terminal. Make sure you are in your project folder, with your virtual environment ready. Then,
  ``` python code/data_collection.py ```
  
This step may take a few minutes. Once it finishes, you’ll find a new `data/vector_db_data` folder in your project. This folder holds all the knowledge your AI will use.

5. Run the Streamlit AI Guide

1. Open your terminal
2. Run this command:
 `streamlit run code/app.py`
This command will open the **Streamlit AI Guide** in your web browser.
Now, you can start asking questions about Streamlit

---

Here's a quick example of how the **Streamlit AI Guide** can help you:

<img src="https://raw.githubusercontent.com/archanags001/streamlit-ai-guide/main/images/imag_streamlitAI_result.png" alt="Streamlit AI Guide Interaction" width="700">


## License

This project is licensed under the MIT License – see the [LICENSE](https://github.com/archanags001/streamlit-ai-guide/blob/main/LICENSE) file for details.

## Contact
archanags001@gmail.com

