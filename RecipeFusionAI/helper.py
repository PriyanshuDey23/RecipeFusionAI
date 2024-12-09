import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
from RecipeFusionAI.prompt import *
import streamlit as st
import tempfile
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain



# Load environment variables
load_dotenv()

# Access API key from environment
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure the Generative AI client
genai.configure(api_key=GOOGLE_API_KEY)

# Generate Recipe
def generate_recipe(transcript_text, prompt):
    try:
        # Initialize the generative model
        model = genai.GenerativeModel(model_name="gemini-1.5-flash-8b")
        
        # Generate content by combining the prompt and the transcript
        response = model.generate_content(prompt + transcript_text)
        
        return response.text
    except Exception as e:
        st.error(f"Error generating recipe: {e}")
        return None

# Function to extract transcript from YouTube video
def extract_transcript(youtube_video_url):
    # Check if URL is in 'youtu.be' format and extract video ID
    if "youtu.be" in youtube_video_url:
        video_id = youtube_video_url.split("/")[-1]
    # Check if URL is in 'youtube.com' format and extract video ID
    elif "youtube.com" in youtube_video_url:
        video_id = youtube_video_url.split("v=")[1].split("&")[0]  # Ensure video ID is properly split
    else:
        raise ValueError("Invalid YouTube URL format.")
    
    # Fetch the transcript of the video
    transcript_data = YouTubeTranscriptApi.get_transcript(video_id=video_id)
    
    # Combine all the transcript texts into a single string
    transcript = " ".join([item["text"] for item in transcript_data])
    
    return transcript


    

# User generated recipe
def user_generate_recipe(ingredients, dietary_restrictions, cuisine, course_type, meal_duration, calorie_intake, allergies, cooking_method, cooking_equipment, recipe_name, flavor_profile):
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro-002",
            temperature=1,
            api_key=GOOGLE_API_KEY
        )
        prompt = PromptTemplate(
            input_variables=["ingredients", "dietary_restrictions", "cuisine", "course_type", "meal_duration", "calorie_intake", "allergies", "cooking_method", "cooking_equipment", "recipe_name", "flavor_profile"],
            template=PROMPT_RECIPE_GENERATION
        )
        llm_chain = LLMChain(llm=llm, prompt=prompt)
        return llm_chain.run({
            "ingredients": ingredients,
            "dietary_restrictions": dietary_restrictions,
            "cuisine": cuisine,
            "course_type": course_type,
            "meal_duration": meal_duration,
            "calorie_intake": calorie_intake,
            "allergies": allergies,
            "cooking_method": cooking_method,
            "cooking_equipment": cooking_equipment,
            "recipe_name": recipe_name,
            "flavor_profile": flavor_profile
        })
    except Exception as e:
        print(f"Error generating recipe: {e}")
        return "Error generating recipe."





# For Audio

# Function to initialize the generative model
def get_model():
    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-flash-8b")
        return model
    except Exception as e:
        raise ValueError(f"Error initializing the model: {e}")



# Function to save uploaded audio file
def save_uploaded_file(uploaded_file):
    """Save uploaded audio file to a temporary file."""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.' + uploaded_file.name.split('.')[-1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            return tmp_file.name
    except Exception as e:
        raise ValueError(f"Error saving uploaded file: {e}")

# Function to extract text from audio using Google's Generative API
def audio_to_text(audio_file_path):
    """Convert audio to text using Google's Generative API."""
    try:
        model = get_model()
        # Upload audio file to Google API
        audio_file = genai.upload_file(path=audio_file_path)
        # Request the model to transcribe audio to text
        response = model.generate_content(
            [
                "Please transcribe the following audio.",
                audio_file
            ]
        )
        return response.text
    except Exception as e:
        raise ValueError(f"Error converting audio to text: {e}")
