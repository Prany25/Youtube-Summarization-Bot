import validators
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader

st.set_page_config(page_title="Langchain: Summarize text from youtube or website url")
st.title("Langchain: Summarize text from youtube or website url")
st.sub_header('Summarize URL')

with st.sidebar:
    groq_api_key=st.text_input("Enter your GROQ API key:",value="",type="password")
    url=st.text_input("Enter the Youtube or website URL:",label_visibility="collapsed")

if st.button("Summarize the content from the website/youtube"):
    if not groq_api_key.strip() or not url.strip():
        st.error("Please provide the information to get started")
    elif not validators.url(url):
        st.error("The given url is not valid")
    else:
        try:
            with st.spinner("Waiting..."):
                