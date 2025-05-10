import json
import streamlit as st
from openai import OpenAI
import os
import re
# NEW LINES
from google import generativeai
from dotenv import load_dotenv
load_dotenv()

# client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY")) # Get your API key from https://aistudio.google.com/prompts/new_chat

def generate_prompt(company_description):
    prompt = ("Generate a SWOT analysis for a company based on the following description:\n\n" +

    f"{company_description} \n\n"

    """ Provide a Pretty JSON Format Output with No Additional Text other than JSON And output in the following format:
       
    {"Strengths": Business Strengths in Comma Seperated Python List Format
    , "Weakness": Business Weakness in Comma Seperated Python List Format
    , "Opportunity": Business Opportunities  in Comma Seperated Python List Format
    , "Threat": Business Threats in Comma Seperated Python List Format}""")
   
    return prompt

def generate_response_gemini(user_key,prompt):
    client = generativeai.Client(api_key=user_key)
    response = client.models.generate_content(
    model="gemini-1.5-flash",
    contents=prompt
    # stream=True
    )
    api_response =  response.text
    return api_response


def generate_response_chatgpt(user_key,prompt):
    client = OpenAI(api_key=user_key)

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.5,
    max_tokens=2048
    )
    api_response = completion.choices[0].message.content
    return api_response

# Define the layout of the Streamlit app
st.title("SWOT Analysis Generator")
user_key = st.text_input("Enter your OpenAI API Key:", type="password")
company_description = st.text_area("Enter your Company's Detailed Outlook here:")

if st.button("Generate"):
    prompt = generate_prompt(company_description)
    with st.spinner(text="Loading Wisdom..."):
        # api_response = json.loads(generate_response_chatgpt(user_key,prompt))        
        # api_response = json.loads(generate_response_gemini(user_key,prompt))        
        api_response = generate_response_gemini(user_key,prompt)
        try:
            # Try to find the JSON part within the response
            match = re.search(r'\{.*\}', api_response, re.DOTALL)
            if match:
                api_response = json.loads(match.group(0))
            else:
                st.error("Could not find valid JSON in the API response.")
                api_response = None
        except json.JSONDecodeError as e:
            st.error(f"Error decoding JSON response after extraction: {e}")
            st.error(f"Raw API Response: {api_response}")
            api_response = None
   
    st.divider()
   
    format_output_tab,prompt_input_tab,api_response_tab = st.tabs(["Formatted Output","Prompt Input","API Response"])
   
    with format_output_tab:
        for section, items in api_response.items():
            with st.expander(section):
                print(items)
                for points in items:    
                    st.write(points)
   
    with prompt_input_tab:
        st.write(prompt)
       
    with api_response_tab:
        st.write(api_response)