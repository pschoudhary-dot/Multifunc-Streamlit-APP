import streamlit as st
import newspaper

def article_summarizer():

    st.title('News Article Summarizer')
    st.write('Enter the URL of a news article to summarize it.')
    url = st.text_input('', placeholder="paste the URL here and press enter:")
    
    if url:
        article = newspaper.Article(url)
        article.download()
        article.parse()
        authors = article.authors
        publish_date = article.publish_date
        article_name = article.title
        article.nlp()
        links = article.meta_data.get('og', {}).get('url', '')
        embbed_urls = article.meta_data.get('og', {}).get('image', '')

        image_url = ''
        if isinstance(embbed_urls, dict):
            image_url = embbed_urls.get('identifier', '')
        else:
            image_url = embbed_urls

        st.text(f'Authors: {", ".join(authors)}')
        st.text(f'Publish Date: {publish_date}')
        keywords = article.keywords
        st.text(f'Keywords: {", ".join(keywords)}')
        st.text(f'Link: {links}')

        tab1, tab2 = st.tabs(tabs=['Full Article', 'Summary'])
        
        with tab1:
            st.subheader(article_name)
            if image_url:
                st.image(image_url)
            else:
                st.write("No image available.")
            st.write(article.text)
        
        with tab2:
            st.subheader('Summary')
            st.subheader(article_name)
            if image_url:
                st.image(image_url)
            else:
                st.write("No image available.")
            st.write(article.summary)

article_summarizer()