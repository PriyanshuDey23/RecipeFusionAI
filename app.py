import streamlit as st
from RecipeFusionAI.helper import *
from RecipeFusionAI.utils import *
from RecipeFusionAI.prompt import *

# Page config
st.set_page_config(layout="wide")

# Title
st.title("Recipe Generator")

# Choice menu
choice = st.selectbox("Select your choice", ["Select your choice", "Self Generation", "Audio", "Video", "URL", "PDF OR TEXT File"])



# For Audio
if choice == "Audio":
    st.subheader(f"Recipe Generator From {choice}")
    audio_file = st.file_uploader("Upload Audio File", type=["wav", "mp3"])

    if audio_file:
        if st.button("Generate Recipe from Audio"):
            with st.spinner("Analyzing your Audio..."):
                try:
                    # Save the uploaded audio file
                    audio_path = save_uploaded_file(audio_file)
                    
                    # Play the audio file
                    st.audio(audio_path)

                    # Extract text from the audio file
                    extracted_text = audio_to_text(audio_path)
                    st.text_area("Extracted Text", extracted_text, height=200)

                    # Generate the recipe from extracted text
                    with st.spinner("Generating Recipe..."):
                        st.subheader("Generated Recipe")
                        recipe = generate_recipe(extracted_text,PROMPT_ALL)
                        st.write(recipe)

                    # Download options for the generated recipe
                    if recipe:
                        result = f"Generated Recipe:\n\n{recipe}"
                        st.download_button(
                            label="Download Results as TXT",
                            data=convert_to_txt(result),
                            file_name="recipe.txt",
                            mime="text/plain",
                        )
                        st.download_button(
                            label="Download Results as DOCX",
                            data=convert_to_docx(result),
                            file_name="recipe.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        )
                except Exception as e:
                    st.error(f"An error occurred: {e}")

# For Self Generation
if choice =="Self Generation":
    st.title("Professional Recipe Generator")

    # Input fields
    ingredients = st.text_area("Enter Ingredients (separate with commas)")

    dietary_restrictions = st.selectbox(
        "Select Dietary Restrictions", ["Vegetarian", "Gluten-Free", "Dairy-Free", "None"]
    )

    cuisine = st.selectbox(
        "Select Cuisine",
        ["Italian", "Chinese", "Indian", "Mexican", "American", "Other (please specify)"]
    )
    if cuisine == "Other (please specify)":
        cuisine = st.text_input("Specify the Cuisine", placeholder="Enter custom cuisine")
    else:
        cuisine = cuisine  # Keep the selected value

    course_type = st.selectbox(
        "Select Course Type", ["Appetizer", "Main Course", "Dessert", "Other (please specify)"]
    )
    if course_type == "Other (please specify)":
        course_type = st.text_input("Specify the Course Type", placeholder="Enter custom course type")
    else:
        course_type = course_type

    meal_duration = st.number_input("Enter Meal Duration (in minutes)", min_value=1)

    calorie_intake = st.number_input("Enter Desired Calorie Intake(kcal)", min_value=0)

    allergies = st.text_input(
        "Enter Allergies (comma-separated, e.g., nuts, dairy)"
    )

    cooking_method = st.selectbox(
        "Select Cooking Method", ["Grilling", "Baking", "Frying", "Boiling", "Steaming", "Other (please specify)"]
    )
    if cooking_method == "Other (please specify)":
        cooking_method = st.text_input(
            "Specify the Cooking Method", placeholder="Enter custom cooking method"
        )
    else:
        cooking_method = cooking_method

    cooking_equipment = st.text_input(
        "Enter Cooking Equipment (e.g., Instant Pot, Oven, Grill)"
    )

    recipe_name = st.text_input("Enter Recipe Name")

    flavor_profile = st.selectbox(
        "Select Flavor Profile", ["Spicy", "Sweet", "Tangy", "Savory", "Other (please specify)"]
    )
    if flavor_profile == "Other (please specify)":
        flavor_profile = st.text_input(
            "Specify the Flavor Profile", placeholder="Enter custom flavor profile"
        )
    else:
        flavor_profile = flavor_profile

    # Generate recipe on button click
    if st.button("Generate Recipe"):
        with st.spinner("Generating Recipe.."):
            recipe = user_generate_recipe(ingredients, dietary_restrictions, cuisine, course_type, meal_duration, calorie_intake, allergies, cooking_method, cooking_equipment, recipe_name, flavor_profile)
            st.subheader("Generated Recipe:")
            st.write(recipe)

            # Download options for Video
            if recipe:
                        result = f"Generated Recipe:\n\n{recipe}"
                        st.download_button(
                            label="Download Results as TXT",
                            data=convert_to_txt(result),
                            file_name="recipe.txt",
                            mime="text/plain",
                        )
                        st.download_button(
                            label="Download Results as DOCX",
                            data=convert_to_docx(result),
                            file_name="recipe.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        )



# For Video (YouTube) 
if choice == "Video":
    st.subheader(f"Recipe Generator From {choice}")
    text_input = st.text_input("Insert your video URL")

    if st.button("Generate Recipe"):
        if text_input:
            try:
                with st.spinner("Analyzing your Video..."):
                    extracted_text = extract_transcript(text_input)
                    st.text_area(f"Extracted Text from {choice}", extracted_text, height=200)

                    with st.spinner("Generating Recipe..."):
                        st.subheader("Generated Recipe")
                        recipe = generate_recipe(extracted_text,prompt=PROMPT_ALL)
                        st.write(recipe)

                    # Download options for Video
                    if recipe:
                        result = f"Generated Recipe:\n\n{recipe}"
                        st.download_button(
                            label="Download Results as TXT",
                            data=convert_to_txt(result),
                            file_name="recipe.txt",
                            mime="text/plain",
                        )
                        st.download_button(
                            label="Download Results as DOCX",
                            data=convert_to_docx(result),
                            file_name="recipe.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        )
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("Please provide a valid YouTube video URL.")





# For URL
if choice == "URL":
    st.subheader(f"Recipe Generator From {choice}")
    text_input = st.text_input("Insert your URL")

    if st.button("Analyze your URL"):
        if text_input:
            try:
                with st.spinner("Analyzing your URL..."):
                    extracted_text = extract_text_from_url(text_input)
                    st.text_area(f"Extracted Text from {choice}", extracted_text, height=200)

                    with st.spinner("Generating Recipe..."):
                        st.subheader("Generated Recipe")
                        recipe = generate_recipe(extracted_text,PROMPT_ALL)
                        st.write(recipe)

                    # Download options for URL
                    if recipe:
                        result = f"Generated Recipe:\n\n{recipe}"
                        st.download_button(
                            label="Download Results as TXT",
                            data=convert_to_txt(result),
                            file_name="recipe.txt",
                            mime="text/plain",
                        )
                        st.download_button(
                            label="Download Results as DOCX",
                            data=convert_to_docx(result),
                            file_name="recipe.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        )
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("Please provide a valid URL.")





# For PDF OR TEXT File
if choice == "PDF OR TEXT File":
    st.subheader(f"Recipe Generator From {choice}")
    uploaded_file = st.file_uploader("Upload a PDF or Text file", type=("pdf", "txt"))

    if uploaded_file:
        if st.button("Analyze your PDF or Text File"):
            with st.spinner("Analyzing your file..."):
                # Extracting text from the file
                extracted_text = extract_text_from_file(uploaded_file)
                st.text_area(f"Extracted Text from {choice}", extracted_text, height=200)

                # Recipe Generation
                with st.spinner("Generating Recipe..."):
                    st.subheader("Generated Recipe")
                    recipe = generate_recipe(extracted_text,PROMPT_ALL)
                    st.write(recipe)

                # Download options for PDF or Text
                if recipe:
                    result = f"Generated Recipe:\n\n{recipe}"
                    st.download_button(
                        label="Download Results as TXT",
                        data=convert_to_txt(result),
                        file_name="recipe.txt",
                        mime="text/plain",
                    )
                    st.download_button(
                        label="Download Results as DOCX",
                        data=convert_to_docx(result),
                        file_name="recipe.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    )

# Placeholder for the "Select your choice"
if choice == "Select your choice":
    st.write("Please select a choice from the dropdown above to get started.")
