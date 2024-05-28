import PyPDF2
from dotenv import load_dotenv, find_dotenv
import os
import streamlit as st
import google.generativeai as genai

load_dotenv(find_dotenv())
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
generation_config = {"temperature": 0.7, "top_p": 1 , "top_k" : 1,  "max_output_tokens" : 2048}

try:
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel("gemini-pro", generation_config=generation_config)
except ModuleNotFoundError:
    print("Warning: Google Generative AI library not found. Functionality may be limited.")
    genai = None
    model = None

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    try:
        reader = PyPDF2.PdfReader(pdf_file, strict=False)
        pdf_text = []
        for page in reader.pages:
            content = page.extract_text()
            if content:  # Check if there is text on the page
                pdf_text.append(content)
        return pdf_text
    except Exception as e:
        st.write(f"Error extracting text from PDF: {e}")
        return []

# Function to clean extracted text
def text_cleaning(extracted_text):
    cleaned_text = []
    for text in extracted_text:
        cleaned = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")
        cleaned_text.append(cleaned)
    return cleaned_text

st.title("Resume Roaster")
st.subheader("Think your resume is flawless? Let us roast it to a crisp!")

with st.sidebar:
    st.link_button("GitHub", "https://github.com/Shaheer04", use_container_width=True)
    st.link_button("LinkedIn", "https://www.linkedin.com/in/shaheerjamal", use_container_width=True)
    st.info("Upload your resume in PDF format to get started.")
    uploaded_file = st.file_uploader("Choose a file", type=['pdf'])
    if uploaded_file is not None:
        extracted_text = extract_text_from_pdf(uploaded_file)
        cleaned_data = text_cleaning(extracted_text)
        # Define the prompt
        prompt = ["""
           Gemini AI. I need a humorous and sarcastic critique of my resume,
        focusing on the essential aspects without offering advice. 
        Please use the following information to create a concise and witty critique:
        Previous job positions and companies.
        Educational background and certifications.
        Key skills and areas of expertise.
        Achievements and notable projects.
        Your feedback should be insightful and entertaining,
        providing a balance of humor, sarcasm and wittyness. 
        Please do not use my name in the critique. Focus on the provided resume details, and let the critique begin! 
        Use a conversational language and tone, and employ simpler words to enhance the overall readability. 
        Remember, no advice or headings in the response.
                """]
        prompt.extend(cleaned_data)

    # Function to query from the API
        def get_response():
            try:
                if genai and model:
            # Use Google Generative AI if available
                    result = model.generate_content(prompt)
                    response = result.text.replace("```", "").replace("JSON", "").replace("json", "")
                    return response
                else:
            # Provide a fallback mechanism (if applicable)
                    print("Warning: Text generation functionality not available.")
                    return {"error": "Text generation not supported"}
            except Exception as error:
                return {"error": str(error)}
        

# Get the output from the API
if st.button("Roast my resume!", type="primary"):
    if uploaded_file is None:
        st.warning("Please upload a resume first.")
    else:    
        with st.spinner("Roasting your resume..."):
            output = get_response()
            if "error" in output:
                st.write(output["error"])
            else:
                st.warning(output)
st.caption("Made with ❤️ by Shaheer Jamal")
