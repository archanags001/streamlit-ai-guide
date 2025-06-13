import os
import shutil
import time
from langchain_community.document_loaders import RecursiveUrlLoader, WebBaseLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from dotenv import load_dotenv
load_dotenv()


GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found")

vector_db_dir = "../data/vector_db_data"
doc_collection_name = "streamlit_documents"

#Loads and transforms documentation
def load_streamlit_docs():
    raw_doc = []
    all_documents = []

    try:
        loader = RecursiveUrlLoader(
            url="https://docs.streamlit.io/",
            max_depth=6,
        )
        for i, doc_item in enumerate(loader.load()):
            if isinstance(doc_item, Document):
                all_documents.append(doc_item)

        bst = BeautifulSoupTransformer()
        transformed_documents = bst.transform_documents(all_documents)

        filter_by_url = [
            doc for doc in transformed_documents
            if doc.metadata.get('source', '').startswith("https://docs.streamlit.io/")
        ]
        raw_doc.extend(filter_by_url)
        important_url = [
            "https://docs.streamlit.io/develop/concepts/multipage-apps/overview",
            "https://docs.streamlit.io/get-started/fundamentals/main-concepts",
            "https://docs.streamlit.io/library/api-reference",
            "https://docs.streamlit.io/deploy",
        ]
        for url in important_url:
            try:
                webloader = WebBaseLoader(url)
                page_doc= webloader.load()
                raw_doc.extend(bst.transform_documents(page_doc))
                # print(f"  Added: {url}")
                time.sleep(0.5)
            except Exception as e:
                print(f"Failed to load {url}: {e}")

        docs_splitting = [doc for doc in raw_doc if doc.page_content.strip() and len(doc.page_content) > 50]
    except Exception as e:
        return
#
    text_split = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200,
        length_function=len,
        add_start_index=True,
    )
    splits = text_split.split_documents(docs_splitting)
    embeddings_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GEMINI_API_KEY)

    if os.path.exists(vector_db_dir):
        try:
            shutil.rmtree(vector_db_dir)
        except Exception as e:
            print(e)

    try:
        vectorstore = Chroma.from_documents( documents=splits, embedding=embeddings_model,
            persist_directory=vector_db_dir,
            collection_name=doc_collection_name,
        )
    except Exception as e:
        print('Error in creating or updating vector DB')


def main():
    if os.path.exists(vector_db_dir) and os.listdir(vector_db_dir):
        print("ChromaDB data found at")
    else:
        load_streamlit_docs()
if __name__ == "__main__":
    main()


