from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai
import streamlit as st
import os

load_dotenv()

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

def generate_story(input,image):
    # model=genai.GenerativeModel('gemini-pro-vision')
    model=genai.GenerativeModel('gemini-1.5-pro-latest')
    response=model.generate_content([input,image[0]])
    return response.text

##initialize our streamlit app

st.set_page_config(page_title="Story Generator")

st.header("Image to Story Generator")
st.write("Upload an Image to create a story")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

image=""  

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit=st.button("Generate a Story")

input_prompt="""
    You are an expert Story teller where you see an image
    and generate a short story about it. Be creative and innovative
"""

if submit:
    image_data=input_image_setup(uploaded_file)
    story=generate_story(input_prompt,image_data)
    st.subheader("Here is a short story")
    st.write(story)