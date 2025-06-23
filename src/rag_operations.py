import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import MessagesPlaceholder 
from langchain_google_genai import HarmCategory, HarmBlockThreshold

vector_db_dir = "../data/vector_db_data"
doc_collection_name = "streamlit_documents"

@st.cache_resource
def get_embeddings(api_key):
    return GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)

@st.cache_resource
def load_vectorstore(_embeddings_model: GoogleGenerativeAIEmbeddings):
    if not os.path.exists(vector_db_dir) or not os.listdir(vector_db_dir):
        st.error("Something isn’t working right now. It will be fixed shortly")
        st.stop()
    return Chroma( persist_directory=vector_db_dir,
        embedding_function=_embeddings_model,
        collection_name=doc_collection_name)

@st.cache_resource
def load_llm(api_key):
    safety_settings = {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }
    return ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2,
                                  google_api_key=api_key,
                                  safety_settings=safety_settings)


@st.cache_resource
def rag_with_memory(api_key):
    llm = load_llm(api_key)
    embeddings_model = get_embeddings(api_key)
    vectorstore = load_vectorstore(embeddings_model)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 8})
    prompt = """You are an enthusiastic and helpful AI tutor strictly specialized in Streamlit.
    Your primary function is to answer questions *only* about Streamlit, its features, API, concepts,development and deployment.
    Use the following retrieved context and the chat history to answer the current question accurately and comprehensively.
    If the user asks a question that is NOT related to Streamlit in any way (e.g., general knowledge, math problems, questions about 
    other frameworks or tools, or questions about your own internal workings like 'safety settings'), you MUST politely decline to answer by 
    stating: "I am a Streamlit-focused AI tutor and do not have information on that topic, suggesting they check the official Streamlit documentation for relevant queries.Please ask me a question related to Streamlit." 
    Do NOT provide any other information. 
    If the user says a greeting like "hi", "hello", "hey", or "thank you", respond with: "Hello there! How can I help you with your Streamlit project today?" .Do not provide any other information or retrieved context for these greetings.
    Keep your answers concise, clear, and highly relevant to Streamlit topics.
    If the user's question explicitly asks for a code example or implies the need for one (e.g., "how to use X", "show me an example of Y"),
    provide a small, runnable Python code snippet within a markdown code block (```python\n...\n```).

    Context: {context}
    """

    final_answer_prompt = ChatPromptTemplate.from_messages([
        ("system", prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ])
    document_chain = create_stuff_documents_chain(llm, final_answer_prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    return retrieval_chain

