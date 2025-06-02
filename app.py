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

llm=ChatGroq(model="TinyLlama-1.1B-Chat-v1.0",groq_api_key=groq_api_key)

prompt_template="""
Provide a summary of the following content in 300 words:
Context:{text}
"""

prompt=PromptTemplate(template=prompt_template,input_variables=["text"])

if st.button("Summarize the content from the website/youtube"):
    if not groq_api_key.strip() or not url.strip():
        st.error("Please provide the information to get started")
    elif not validators.url(url):
        st.error("The given url is not valid")
    else:
        try:
            with st.spinner("Waiting..."):
                if "youtube.com" in url:
                    loader=YoutubeLoader.from_youtube_url(url,add_video_info=True)
                else:
                    loader=UnstructuredURLLoader(urls=[url],ssl_verify=False,headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHMIL, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
                
                docs=loader.load()

                chain=load_summarize_chain(llm,chain_type="stuff",prompt=prompt)
                output_summary=chain.run(docs)

                st.success(output_summary)
        
        except Exception as e:
            st.Exception(f"Exception:{e}")
