# Multifunc Streamlit APP

This is a multifunctional Streamlit application that includes various tools such as an article summarizer, auto dashboard, sentiment analyzer, and a multimodel chatbot.

## Project Structure

In this Streamlit app, there are several pages:
1. **Article Scraper**: Scrape articles and view their summaries and other details.
2. **Auto Dashboard**: Preprocess and clean any type of CSV file and get basic visualizations.
3. **Sentiment Analysis**: Perform sentiment analysis on text and CSV files.
4. **Multimodel Chatbot and Image Generator**: Chat with different models and generate images.
5. **In Progress**: Document and article chatbot (under development).

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/pschoudhary-dot/Multifunc-Streamlit-APP.git
    cd Multifunc-Streamlit-APP
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a [.env](http://_vscodecontentref_/1) file and add your API keys:
    ```properties
    GEMINI_API_KEY='your key'
    HF_API_KEY='your key'
    ```

## Running the Application

To run the Streamlit application, use the following command:
```sh
streamlit run Home.py
```