import streamlit as st
import os

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

DB_FAISS_PATH = "vectorstore/db_faiss"

@st.cache_resource
def get_vectorstore():
    embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    db = FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)
    return db

def main():
    st.set_page_config(page_title="Animal Rescue App", layout="wide")

    st.markdown(
    """
    <style>
        body { background-color: #f8e8d2 !important; }
        .navbar { position: fixed; top: 0; left: 0; width: 100%; height: 20%;
                  background-color: #ffcc99; padding: 10px; display: flex; 
                  justify-content: center; z-index: 1000; align-items:center;}
        .navbar a { margin: 0 15px; padding: 50px 20px; font-size: 16px; 
                         border: none; border-radius: 20px; background-color: #ff9966; text-align:center;font-weight:bold; 
                         color: white !important; cursor: pointer; transition: background 0.3s ease;display:inline-block;text-decoration:none;
                          align-items:center; }
        .navbar a:hover { background-color: #ff7744; }
        .main-content { margin-top: 70px; padding:20px; }
        
    </style>
    """,
    unsafe_allow_html=True
    )

    # Navbar with buttons
    st.markdown(
    """
    <div class="navbar">
        <a href="http://127.0.0.1:5000/About_us " target="_blank">About Us</a>
        <a href="http://127.0.0.1:5000/real-timechat" target="_blank">Real-time Chat</a>
        <a href="http://127.0.0.1:5000/report" target="_blank">Report</a>
    </div>
    <div class="main-content">
    """,
    unsafe_allow_html=True
    )

    st.title("PawCare-Connect")

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        st.chat_message(message['role']).markdown(message['content'])

    warning_placeholder=st.empty()
    warning_placeholder.warning("## Welcome to The one-stop solution for all the animal rescues")

    prompt = st.chat_input("Ask your questions here")

    if prompt:
        st.chat_message('user').markdown(prompt)
        st.session_state.messages.append({'role': 'user', 'content': prompt})

        CUSTOM_PROMPT_TEMPLATE = """
                Use the pieces of information provided in the context to answer user's question.
                If you don't know the answer, just say that you don't know. 
                Don't make up an answer. Use the given context only.

                Context: {context}
                Question: {question}

                Start the answer directly. No small talk.
                """

        HUGGINGFACE_REPO_ID = "mistralai/Mistral-7B-Instruct-v0.3"
        HF_TOKEN = os.environ.get("HF_TOKEN")

        try:
            vectorstore = get_vectorstore()
            if vectorstore is None:
                st.error("Failed to load the vector store")

            qa_chain = RetrievalQA.from_chain_type(
                llm=HuggingFaceEndpoint(repo_id=HUGGINGFACE_REPO_ID, temperature=0.5,
                                        model_kwargs={"token": HF_TOKEN, "max_length": "512"}),
                chain_type="stuff",
                retriever=vectorstore.as_retriever(search_kwargs={'k': 3}),
                return_source_documents=True,
                chain_type_kwargs={'prompt': PromptTemplate(template=CUSTOM_PROMPT_TEMPLATE,
                                                            input_variables=["context", "question"])}
            )

            response = qa_chain.invoke({'query': prompt})
            result = response["result"]
            st.chat_message('assistant').markdown(result)
            st.session_state.messages.append({'role': 'assistant', 'content': result})

        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()