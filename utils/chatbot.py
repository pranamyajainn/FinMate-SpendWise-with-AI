from transformers import pipeline

# Function to initialize chatbot model
def initialize_chatbot():
    chatbot = pipeline("text-generation", model="gpt2")
    return chatbot

# Function to get chatbot response
def get_chatbot_response(query, chatbot):
    response = chatbot(query, max_length=100, do_sample=True)[0]['generated_text']
    return response