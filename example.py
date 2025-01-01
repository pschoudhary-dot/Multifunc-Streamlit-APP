import streamlit as st
import pandas as pd
import huggingface_hub as hf_hub
import transformers as tf
import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def multimodel_chatbot():
    Description, chat, Settings = st.tabs(["Description", "Chat", "Settings"])
    with Description:
        st.title("Multi-Model Chatbot")
        st.markdown(
                """
                ## Here is the information for your chatbot model.
                - First enter your API keys for:
                    - the `Hugging face key` Link: [Hugging Face API](https://huggingface.co/)
                    - the `Google generative AI key` Link: [Google AI Studio](https://aistudio.google.com)
                - Then you can chat with the model using the chat tab.
                - Select the Task you want to perform.
                - Select the model you want to use.
                - uplaod the file if you want to use.
                - just start chatting and get things done!!
                """)
        
        
    # with Settings:
    #     st.title("Settings")
    #     st.write("Enter your API keys for the Hugging face and Google generative AI")
    #     HUGGING_FACE_API = st.text_input("Hugging face key")
    #     GEMINI_API_KEY = st.text_input("Google generative AI key")
    
    
    with chat:
        # Create the model
        generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
        }

        gemini_model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
        )
        chat_session = gemini_model.start_chat(history=[] )
        
        prompt = st.chat_input("Enter your message", key="chat_input")
        
        response = chat_session.send_message(prompt)
        print(response.text)
        #give the option to chat with files using different models and show the output
        #give option to choose different models
        #give option to choose different files
        #give option to generatae images
        #give option to generate summaries from the links

if __name__ == "__main__":
    multimodel_chatbot()
    
    
    
    """
    The current interface is straightforward. Adding features like message editing, reply quoting, or attachment support could enhance user experience.
    """