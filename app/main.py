import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    # Set the title and description with enhanced styling
    st.title("📧 Cold Email Generator")
    st.markdown("""
        <style>
        .title {
            font-size: 2.5rem;
            font-weight: bold;
            color: #333;
            margin-bottom: 20px;
        }
        .description {
            font-size: 1.2rem;
            color: #555;
            margin-bottom: 40px;
        }
        </style>
        """, unsafe_allow_html=True)
    
    # Layout containers for better organization
    header_container = st.container()
    input_container = st.container()
    output_container = st.container()
    
    with header_container:
        st.subheader("Generate professional cold emails with AI")
        st.markdown("""
            Enter the URL of the page you want to analyze and generate tailored emails for job opportunities.
        """, unsafe_allow_html=True)
    
    with input_container:
        url_input = st.text_input("Enter a URL:", value="", placeholder="https://example.com/job-listing")
        submit_button = st.button("🔍 Analyze & Generate Emails")

    if submit_button:
        try:
            with st.spinner("Processing... Please wait."):
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)
                portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)

                for idx, job in enumerate(jobs):
                    st.markdown(f"### Job {idx + 1}: {job.get('title', 'Untitled')}")
                    skills = job.get('skills', [])
                    links = portfolio.query_links(skills)
                    email = llm.write_mail(job, links)
                    
                    with st.expander(f"📧 Generated Email for {job.get('title', 'this job')}"):
                        st.code(email, language='markdown')
        except Exception as e:
            st.error(f"🚨 An error occurred: {e}")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)

