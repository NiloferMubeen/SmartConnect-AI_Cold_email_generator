import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
import base64
from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    st.markdown("<h1 style='text-align: center; color: white;'>📧 SmartConnect AI : Cold Mail Generator</h1>", unsafe_allow_html=True)
    
    url_input = st.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-43133")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    # Setting the Background

    def get_base64_of_bin_file(bin_file):
                with open(bin_file, 'rb') as f:
                    data = f.read()
                return base64.b64encode(data).decode()
            
    def set_png_as_page_bg(png_file):
                    bin_str = get_base64_of_bin_file(png_file)
                    page_bg_img = '''
                                    <style>
                                    .stApp {
                                    background-image: url("data:image/png;base64,%s");
                                    background-size: cover;
                                    }
                                    </style>
                                    ''' % bin_str
                                                            
                    st.markdown(page_bg_img, unsafe_allow_html=True)
                    return
    set_png_as_page_bg('my_app\img1.png')  
    with st.container():
        create_streamlit_app(chain, portfolio, clean_text)