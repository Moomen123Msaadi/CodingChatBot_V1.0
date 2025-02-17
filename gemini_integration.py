"""
The file handles integration with Google's Gemini AI for generating responses to user input.
"""

import google.generativeai as genai

# Configure the API key
genai.configure(api_key="AIzaSyDekpdYnC9wlHURth7ducxhWqE8xcHY8ZQ")

# Initialize the model
model = genai.GenerativeModel('gemini-pro')

def generate_response(prompt):
    response = model.generate_content(prompt)
    return response.text
