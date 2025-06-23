import streamlit as st
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from rag_operations import rag_with_memory

load_dotenv()

GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GEMINI_API_KEY:
    st.error("API KEY not found")
    st.stop()

st.set_page_config(page_title="Streamlit AI Guide: Ask ... Learn ... Code.", page_icon="🤖", layout="centered")

st.markdown("""
<style>
    .reportview-container .main .block-container{
        max_width: 800px;
        padding-top: 2rem;
        padding-right: 1rem;
        padding-left: 1rem;
        padding-bottom: 2rem;
    }
    .stSpinner > div > div {
        border-top-color: #6a0dad;
    }
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .stButton>button, .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 0.5rem;
    }
    .stCodeBlock {
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 Streamlit AI Guide")
st.markdown("""
**Welcome to Streamlit AI Guide** 

Hey there! 

I'm here to help with your Streamlit questions. You can ask me about features, how to use the API, how to deploy your app, or anything else related to Streamlit.  
I’ll give you clear answers and short code examples when needed.

Let’s get started and build something great together.

**Try asking:**  
- “Teach me the basics of Streamlit”  
- “How do I use `st.slider`?”  
- “What’s the best way to deploy a Streamlit app?”
""")
st.markdown("---")



if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append(
        AIMessage(content="Hello! How can I help you learn Streamlit today?"))

for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

with st.spinner("loading..."):
    rag_chain = rag_with_memory(GEMINI_API_KEY)

if query := st.chat_input("Ask me anything about Streamlit..."):
    st.session_state.messages.append(HumanMessage(content=query))
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                chat_history_for_llm = st.session_state.messages[-6:-1]

                response = rag_chain.invoke({
                    "input": query,
                    "chat_history": chat_history_for_llm
                })
                if "context" in response:
                    retrive_content = response.get("context", [])

                response_content = response["answer"]

                st.markdown(response_content)
                st.session_state.messages.append(AIMessage(content=response_content))

                greet_response = "Hello there! How can I help you with your Streamlit project today?"

                outside_scope = [
                    "i don't have enough information",
                    "not in my knowledge base",
                    "cannot provide information on that topic",
                    "streamlit-focused ai tutor",
                    "i am sorry",
                    "i apologize",
                    "not related to streamlit"
                ]
                outside_scope_response = any(
                    phrase in response_content.lower() for phrase in outside_scope
                )
                is_greet_response = (response_content.strip() == greet_response)

                if not outside_scope_response and not is_greet_response:
                    with st.expander("Show Retrieved Sources"):
                        if response.get("context"):
                            for i, doc in enumerate(response["context"]):
                                source_url = doc.metadata.get('source', 'Unknown Source')
                                st.markdown(f"**Document {i + 1} from:** {source_url}")
                                st.code(doc.page_content[:300] + "...", language="markdown")
                                st.markdown("---")
                        else:
                            st.info("Sorry, I couldn’t find anything on that. Could you try asking a more specific question about Streamlit?")

            except Exception as e:
                st.error(f"Oops, something didn’t work. Please try again: {e}")
                st.session_state.messages.append(AIMessage(
                    content="Sorry, I encountered an issue. Please try again or check the console for errors."))
