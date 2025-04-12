import google.generativeai as genai

genai.configure(api_key="AIzaSyDjdY7reXA74pkRUrjxq8IRrTOEaJ2HDqg")

model = genai.GenerativeModel("gemini-pro")
response = model.generate_content("Hello! Can you tell me how to save money?")
print(response.text)
try:
    response = model.generate_content(user_query)
    bot_reply = response.text
except Exception as e:
    bot_reply = f"❌ Gemini Error: {e}"