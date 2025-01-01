import streamlit as st

st.set_page_config(
    page_title="Week-3 NLP and Text Analysis projects - EnactOn",
    page_icon="🤖",
)

# Title and description
st.title("Week-3 NLP and Text Analysis Projects - EnactOn")

st.write(
    """
    Welcome to the Week-3 NLP and Text Analysis projects at EnactOn. 
    This application demonstrates various Natural Language Processing 
    techniques and text analysis workflows using Python libraries.
    \n
    **How to Navigate**  
    - Use the sidebar to switch between different pages, such as:
    
      1. **Auto Dashboard** (for CSV visualization and analysis) and \n
      2. **Article Summarizer** (for extracting and summarizing online news). \n
      3. **Sentiment Analyzer** ( for analyzing the sentiment of text data) \n
      4. **Multi-Model Chatbot** (for interacting with different chatbot models). \n
    \n
    
    **Additional Resources**
    - [Streamlit Documentation](https://docs.streamlit.io)  
    - [NLTK Documentation](https://www.nltk.org)  
    - [Newspaper3k Docs](https://newspaper.readthedocs.io/en/latest/)  
    - [Python Pandas Docs](https://pandas.pydata.org/docs/)  
    \n
    
    **Need Help?**  
    - Check out the official docs linked above.  
    - If you have any issues or suggestions, please contact the project maintainers.
    """
)
