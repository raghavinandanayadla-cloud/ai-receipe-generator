import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# Load secret from Streamlit Cloud
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

st.set_page_config(
    page_title="AI Recipe Generator",
    page_icon="🍽️"
)

st.title("🍽️ AI Recipe Generator")
st.write("Enter ingredients and generate a recipe instantly!")

ingredients = st.text_area(
    "🥕 Enter Ingredients",
    placeholder="banana, bread, honey"
)

if st.button("Generate Recipe"):

    if not ingredients:
        st.warning("Please enter some ingredients.")
        st.stop()

    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.7
        )

        prompt = PromptTemplate(
            input_variables=["ingredients"],
            template="""
Generate a recipe using:

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

Keep the recipe short and easy to read.
"""
        )

        chain = prompt | llm

        with st.spinner("👨‍🍳 Generating Recipe..."):
            result = chain.invoke(
                {"ingredients": ingredients}
            )

        st.markdown(result.content)

    except Exception as e:
        st.error(f"Error: {e}")
