import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# Page Config
st.set_page_config(
    page_title="AI Recipe Generator",
    page_icon="🍽️",
    layout="centered"
)

st.title("🍽️ AI Recipe Generator")
st.write("Enter the ingredients you have and let AI create a recipe for you!")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input(
        "Gemini API Key",
        type="password"
    )

# User Input
ingredients = st.text_area(
    "🥕 Enter Ingredients",
    placeholder="banana, bread, honey"
)

# Generate Button
if st.button("Generate Recipe"):

    if not api_key:
        st.error("Please enter your Gemini API Key.")
        st.stop()

    if not ingredients:
        st.error("Please enter some ingredients.")
        st.stop()

    os.environ["GOOGLE_API_KEY"] = api_key

    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.7
        )

        prompt = PromptTemplate(
            input_variables=["ingredients"],
            template="""
            Generate a simple recipe using:

            {ingredients}

            Return in markdown format:

            # Recipe Name

            ## Ingredients
            - item 1
            - item 2

            ## Procedure
            1. Step 1
            2. Step 2
            3. Step 3

            Keep the recipe concise and easy to read.
            """
        )

        chain = prompt | llm

        with st.spinner("👨‍🍳 Generating Recipe..."):
            result = chain.invoke(
                {"ingredients": ingredients}
            )

        st.success("Recipe Generated Successfully!")
        st.markdown(result.content)

    except Exception as e:
        st.error(f"Error: {e}")
