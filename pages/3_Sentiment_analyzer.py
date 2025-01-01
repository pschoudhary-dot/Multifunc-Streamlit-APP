import streamlit as st
import pandas as pd
import textblob
import cleantext
from transformers import pipeline

def sentiment_analyzer():
    """
    Streamlit app that provides two tabs:
    1. Simple Sentiment Analysis (using TextBlob)
    2. Advanced Sentiment Analysis (using Zero-Shot Classification from Hugging Face)
    """

    # Create two tabs
    Simple_sentiment_analysis, Advanced_sentiment_analysis = st.tabs(
        ["Simple Sentiment Analysis", "Advanced Sentiment Analysis"]
    )
    
    # --------------------------------------------------------------------------------------
    # 1) SIMPLE SENTIMENT ANALYSIS TAB
    # --------------------------------------------------------------------------------------
    with Simple_sentiment_analysis:
        st.header("Sentiment Analyzer")
        st.subheader("Simple Sentiment Analysis with TextBlob")
        
        # ----------------------------------------------------------------------------------
        # (A) Single Text Analysis
        # ----------------------------------------------------------------------------------
        with st.expander("Analyze your text ⬇"):
            st.write(
                "Enter the text you want to analyze and click on the button "
                "to get the sentiment (polarity & subjectivity)."
            )
            text = st.text_input(" ", placeholder="Enter the text here:")
            
            if text:
                blob = textblob.TextBlob(text)
                st.write("Polarity:", round(blob.sentiment.polarity, 2))
                st.write("Subjectivity:", round(blob.sentiment.subjectivity, 2))
            
            # ----------------------------------------------------------------------------------
            # (B) Clean Text
            # ----------------------------------------------------------------------------------
            pre = st.text_input("Clean text", placeholder="Enter text here:")
            if (pre or text) and st.button("Clean"):
                cleaned = cleantext.clean_words(
                    pre, 
                    clean_all=False, 
                    lowercase=True, 
                    stopwords=True, 
                    extra_spaces=True,
                    numbers=True,
                    punct=True,
                    stp_lang="english"
                )
                st.text(f"Cleaned text: {cleaned}")
            else:
                pass
        
        # ----------------------------------------------------------------------------------
        # (C) CSV File Analysis
        # ----------------------------------------------------------------------------------
        with st.expander("Analyze your CSV"):
            upload = st.file_uploader("Upload your CSV file here", type="csv", key="simple-file-uploader")
            
            @st.cache_data
            def score(x):
                blob1 = textblob.TextBlob(x)
                return round(blob1.sentiment.polarity, 2)
            
            def analyze(x):
                if x >= 0.5:
                    return "Positive"
                elif x <= -0.5:
                    return "Negative"
                else:
                    return "Neutral"
                
            if upload:
                df = pd.read_csv(upload, encoding="latin1")
                st.write("**Original Data Sample**:", df.head())
                
                # Let user drop columns
                data_to_delete = st.multiselect("Select columns to delete:", df.columns)
                df.drop(columns=data_to_delete, inplace=True)
                
                # Choose which column to analyze for sentiment
                tex_to_analyze = st.text_input("Enter the column name to analyze:", value="text")
                
                # Apply TextBlob sentiment
                if tex_to_analyze in df.columns:
                    df["Sentiment Score"] = df[tex_to_analyze].apply(score)
                    df["Analysis"] = df["Sentiment Score"].apply(analyze)
                    
                    value_to_display = st.slider(
                        "Select the number of rows to display:", 
                        min_value=1, max_value=100, value=5
                    )
                    st.write(df.head(value_to_display))
                    
                    @st.cache_data
                    def convert_df_for_download(dataframe):
                        return dataframe.to_csv(index=False).encode("utf-8")
                    
                    csv_data = convert_df_for_download(df)
                    st.download_button(
                        label="Download CSV", 
                        data=csv_data, 
                        file_name="textblob_sentiment_analysis.csv", 
                        mime="text/csv"
                    )
                else:
                    st.warning(
                        f"The column '{tex_to_analyze}' does not exist in your CSV. "
                        "Please check the column name."
                    )

    # --------------------------------------------------------------------------------------
    # 2) ADVANCED SENTIMENT ANALYSIS TAB
    # --------------------------------------------------------------------------------------
    with Advanced_sentiment_analysis:
        st.header("Advanced Sentiment Analysis")
        st.subheader("Zero-Shot Classification (Hugging Face)")

        # -------------------------------------------------------------------------
        # (A) Single Text Classification
        # -------------------------------------------------------------------------
        st.write(
            "This approach uses a large pre-trained model (e.g. `bart-large-mnli`) "
            "to classify text into a set of candidate labels without any prior training."
        )
        user_input = st.text_input("Enter a tweet or short text:", "I love Streamlit!")
        
        # Candidate classes — customize as needed
        candidate_labels = ["positive", "negative", "neutral"]
        
        # Initialize the zero-shot classifier
        # (We do this outside any function so we only load once)
        zero_shot_classifier = pipeline(
            "zero-shot-classification", 
            model="facebook/bart-large-mnli"
        )
        
        # Function to classify text using Zero-Shot Classification
        def classify_text(text):
            result = zero_shot_classifier(text, candidate_labels, multi_label=False)
            # result example:
            # {
            #   'sequence': "the original text",
            #   'labels': ['positive', 'neutral', 'negative'],  # sorted by score
            #   'scores': [0.8, 0.15, 0.05]
            # }
            return result["labels"][0]

        if st.button("Classify"):
            prediction = classify_text(user_input)
            st.write(f"Predicted label: **{prediction}**")

        # -------------------------------------------------------------------------
        # (B) CSV File Classification
        # -------------------------------------------------------------------------
        st.write("---")
        st.subheader("Analyze Your CSV with Zero-Shot Classification")
        
        csv_upload = st.file_uploader("Upload your CSV file here", type="csv", key="advanced-file-uploader")
        
        if csv_upload is not None:
            df_zs = pd.read_csv(csv_upload, encoding="latin1")
            st.write("**Original Data Sample**:", df_zs.head())

            # Let user remove unnecessary columns
            cols_to_drop_zs = st.multiselect("Select columns to delete:", df_zs.columns)
            df_zs.drop(columns=cols_to_drop_zs, inplace=True)
            
            # Choose which column to analyze
            text_column_zs = st.text_input(
                "Enter the column name that contains text to classify:", 
                value="text"
            )
            
            if text_column_zs in df_zs.columns:
                # Apply zero-shot classification on the entire column
                with st.spinner("Classifying all rows..."):
                    df_zs["Predicted_Sentiment"] = df_zs[text_column_zs].apply(classify_text)
                
                st.write("**Classification Results**:")
                row_count_zs = st.slider(
                    "Select the number of rows to display:", 
                    min_value=1, max_value=100, value=5
                )
                st.write(df_zs.head(row_count_zs))
                
                # Option to download the results
                @st.cache_data
                def convert_zs_df_for_download(dataframe):
                    return dataframe.to_csv(index=False).encode("utf-8")
                
                zs_csv = convert_zs_df_for_download(df_zs)
                st.download_button(
                    label="Download CSV (Zero-Shot Results)", 
                    data=zs_csv, 
                    file_name="zero_shot_sentiment_analysis.csv", 
                    mime="text/csv"
                )
            else:
                st.warning(
                    f"The column '{text_column_zs}' does not exist in your CSV. "
                    "Please check the column name."
                )
if __name__ == '__main__':
    sentiment_analyzer()