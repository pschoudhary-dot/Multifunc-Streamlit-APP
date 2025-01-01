import streamlit as st
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os
from PIL import Image
import io
import random
import time
import PyPDF2
import tempfile

# Load environment variables
load_dotenv()
HF_API = os.environ.get("HF_API_KEY")
client = InferenceClient(api_key=HF_API)

# Set up Streamlit page
st.set_page_config(page_title="AI Chat Assistant", page_icon="🤖")
st.title("AI Chat Assistant")

# Define available models and categorize them
available_models = {
    "Text Models": [
        "Qwen/QwQ-32B-Preview",
    ],
    "Image Models": [
        "black-forest-labs/FLUX.1-dev",
    ],
    "Vision & Text Models": [
        "Qwen/QVQ-72B-Preview",
    ]
}

# Predefined system instruction templates
system_templates = {
    "Default": "Your Name is EnactCoder",
    "Friendly Assistant": "You are a friendly and helpful AI assistant.",
    "Professional Assistant": "You are a professional AI assistant specialized in software development.",
    "Coder Assistant": """You are an expert AI coding assistant designed to help users with all aspects of software development, from initial project setup to debugging and optimization. Your primary focus is on generating high-quality, functional code, understanding user needs, and providing comprehensive coding assistance.
    
    Key Capabilities and Behaviors:
    *   Project Focus: You can manage and work on entire projects, not just individual code snippets. This includes creating project structures, managing dependencies, and generating necessary files (e.g., configuration files, build scripts).
    *   Code Generation: You can generate code in various programming languages based on user requirements. Prioritize clean, efficient, well-documented, and idiomatic code that adheres to best practices.
    *   Debugging and Error Resolution: You can help users identify and fix bugs in their code. You can analyze error messages, suggest potential solutions, and even generate corrected code. Explain the reasoning behind your suggestions.
    *   Understanding User Needs: You are adept at understanding natural language descriptions of coding tasks and translating them into concrete code implementations. Ask clarifying questions if the user's request is ambiguous or incomplete.
    *   Context Awareness: You maintain context throughout the conversation, remembering previous interactions and code generated. This allows you to build upon previous work and provide more relevant assistance.
    *   Language Proficiency: You are proficient in a wide range of programming languages (e.g., Python, JavaScript, Java, C++, C#, Go, Rust, Swift, Kotlin, PHP, Ruby, TypeScript, HTML, CSS, SQL).
    *   Framework and Library Support: You are familiar with popular frameworks and libraries (e.g., React, Angular, Vue.js, Node.js, Spring, Django, Flask, TensorFlow, PyTorch).
    *   Code Explanation: You can explain the functionality of existing code, making it easier for users to understand complex logic.
    *   Code Refactoring: You can suggest and perform code refactoring to improve code quality, readability, and maintainability.
    *   Testing and Test Generation: You can help users write unit tests and integration tests for their code. You can also generate basic test cases based on the code's functionality.
    *   Documentation Generation: You can generate code documentation (e.g., docstrings, comments) to improve code clarity and maintainability.
    *   Security Best Practices: You are aware of common security vulnerabilities and avoid generating code that is susceptible to them.
    *   Step-by-Step Guidance: When providing complex solutions, break them down into smaller, manageable steps, explaining each step along the way.
    *   Avoid Over-Explaining Simple Concepts: While you can explain concepts, avoid overly verbose explanations for very basic coding principles unless explicitly asked.
    
    Interaction Guidelines:
    *   When a user provides a task, first try to understand the overall goal and then break it down into smaller, manageable sub-tasks.
    *   If you are unsure about something, ask clarifying questions instead of making assumptions.
    *   Provide multiple solutions or approaches when appropriate, explaining the pros and cons of each.
    *   Prioritize providing functional code over theoretical explanations.
    *   Use code blocks with proper syntax highlighting to present code.
    *   Be concise and to the point.
    
    Example Interaction:
    User: "Create a simple web app using React that displays a list of users fetched from a JSON API."
    Your Response: (You would then proceed to generate the necessary React components, API call logic, and other required code, including instructions on setting up the project.)
    
    By adhering to these guidelines, you will be an invaluable coding assistant for users of all skill levels.
    Your Name is EnactCoder"""
}

# Sidebar for file upload, model selection, system instructions, and save button
with st.sidebar:
    st.write("### Upload a File to Chat with the Model")
    upload_file = st.file_uploader("Upload a file", type=["txt", "pdf", "docx", "doc", "png", "jpg", "jpeg"])

    st.write("### Choose the Model for the Chat Assistant")
    model_category = st.selectbox("Select Model Category", list(available_models.keys()))
    selected_model = st.selectbox("Select Model", available_models[model_category])

    st.write("### System Instructions")
    instruction_option = st.selectbox("Choose Instruction Method", ["Select Template", "Custom Instruction"])
    
    if instruction_option == "Select Template":
        selected_template = st.selectbox("Select a Template", list(system_templates.keys()))
        system_instruction = system_templates[selected_template]
    else:
        system_instruction = st.text_area("Enter Custom System Instruction", value="Your Name is EnactCoder")
    
    save_button = st.button("Save Settings")

if save_button:
    st.session_state['saved_model_category'] = model_category
    st.session_state['saved_model'] = selected_model
    st.session_state['saved_system_instruction'] = system_instruction
    st.success("Settings saved successfully!")

# Retrieve saved settings or use current selections
model_category = st.session_state.get('saved_model_category', model_category)
selected_model = st.session_state.get('saved_model', selected_model)
system_instruction = st.session_state.get('saved_system_instruction', system_instruction)

# Initialize the conversation in session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": system_instruction
        }
    ]

# Update system instruction if saved
st.session_state.messages[0]["content"] = system_instruction

# Function to display random funny loading texts
def get_random_loading_text():
    funny_texts = [
        "Processing your request... Almost there!",
        "Crunching the numbers... 🍪",
        "Whipping up some magic! ✨",
        "Loading... Patience is a virtue! 🕰️",
        "Calculating... Did you know honey never spoils?",
        "Generating content... Why did the programmer quit his job? 😄",
        "Hold tight! We're on it!",
        "Fetching data... Did you hear about the mathematician who's afraid of negative numbers?",
    ]
    return random.choice(funny_texts)

# Function to extract text from PDF
def extract_text_from_pdf(file):
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(file.read())
        tmp_file_path = tmp_file.name
    reader = PyPDF2.PdfReader(tmp_file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    os.unlink(tmp_file_path)
    return text

# Handle Text Models
def handle_text_model(user_input):
    if upload_file:
        if upload_file.type.startswith("image"):
            image = Image.open(upload_file)
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_str = buffered.getvalue()
            user_input += f" [Image Uploaded: {upload_file.name}]"
        elif upload_file.type == "application/pdf":
            text = extract_text_from_pdf(upload_file)
            user_input += f" [PDF Content: {text[:500]}...]"  # Limiting text length
        else:
            content = upload_file.read().decode()
            user_input += f" [File Content: {content[:500]}...]"  # Limiting text length

    st.session_state.messages.append({"role": "user", "content": user_input})

    completion = client.chat.completions.create(
        model=selected_model,
        messages=st.session_state.messages,
        max_tokens=2800,
        temperature=0.7,
    )

    assistant_response = completion.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})

# Handle Image Models
def handle_image_model(user_input):
    loading_text = get_random_loading_text()
    with st.spinner(loading_text):
        time.sleep(1)
        try:
            image = client.text_to_image(user_input)
            if isinstance(image, Image.Image):
                img_buffer = io.BytesIO()
                image.save(img_buffer, format="PNG")
                img_buffer.seek(0)
                st.image(img_buffer, caption="Generated Image", use_column_width=True)
            else:
                st.error("The model did not return an image.")
        except Exception as e:
            st.error(f"Error generating image: {e}")

# Handle Vision & Text Models
def handle_vision_text_model(user_input):
    loading_text = get_random_loading_text()
    with st.spinner(loading_text):
        time.sleep(1)
        try:
            if upload_file:
                if upload_file.type.startswith("image"):
                    image = Image.open(upload_file)
                    buffered = io.BytesIO()
                    image.save(buffered, format="PNG")
                    img_str = buffered.getvalue()
                    user_input += f" [Image Uploaded: {upload_file.name}]"
                elif upload_file.type == "application/pdf":
                    text = extract_text_from_pdf(upload_file)
                    user_input += f" [PDF Content: {text[:500]}...]"  # Limiting text length
                else:
                    content = upload_file.read().decode()
                    user_input += f" [File Content: {content[:500]}...]"  # Limiting text length

            messages = [
                {
                    "role": "user",
                    "content": user_input
                }
            ]
            completion = client.chat.completions.create(
                model=selected_model,
                messages=messages,
                max_tokens=500,
                temperature=0.7,
            )
            assistant_response = completion.choices[0].message.content
            st.write(f"**Assistant:** {assistant_response}")
        except Exception as e:
            st.error(f"Error processing vision & text model: {e}")

# Capture user input
user_input = st.chat_input("What's your question?")
if user_input:
    if selected_model in available_models["Text Models"]:
        handle_text_model(user_input)
    elif selected_model in available_models["Image Models"]:
        handle_image_model(user_input)
    elif selected_model in available_models["Vision & Text Models"]:
        handle_vision_text_model(user_input)

# Display the conversation for text models, skipping system messages
if selected_model in available_models["Text Models"]:
    for message in st.session_state.messages:
        if message["role"] == "system":
            continue

        with st.chat_message(message["role"]):
            st.write(message["content"])

elif selected_model in available_models["Vision & Text Models"]:
    for message in st.session_state.messages:
        if message["role"] == "system":
            continue
        if message["role"] == "assistant":
            st.write(f"**Assistant:** {message['content']}")
