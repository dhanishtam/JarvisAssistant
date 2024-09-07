import os
from dotenv import load_dotenv
import sys
import random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from brain.DMM import DecisionMakingModel
from brain.auto import Play, Search, YouTubeSearch, Content, OpenApplications
from brain.groqApi import Chatbot 
from Features.weather import current_weather_details

load_dotenv()

success = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can assist you with.",
    "I'm at your service for any additional questions or support you may need—don't hesitate to ask.",
    "Continued support is my commitment to you. Let me know if there's anything more I can help with.",
    "I'm here to ensure your experience is seamless. If you have any further requests, please let me know.",
    "Your needs are important to me. If there's anything else I can assist you with, I'm just a message away.",
    "I'm dedicated to providing excellent service. Should you require further assistance, I'm here for you.",
    "Exceeding your expectations is my goal. Don't hesitate to reach out for any additional help you may need.",
    "Your satisfaction matters. If you have more questions or need assistance, feel free to ask.",
    "I'm committed to making your experience positive. Let me know if there's anything else I can do for you.",
    "Your feedback is valued. If there's anything I can do to enhance your experience, please let me know.",
    "If there's anything specific you'd like assistance with, please share, and I'll be happy to help.",
    "Your concerns are important to me. Feel free to ask for further guidance or information.",
    "I'm here to address any additional queries or provide clarification as needed.",
    "For a seamless experience, let me know if there's anything else you require assistance with.",
    "Your satisfaction is key; if there's a specific area you'd like more support in, I'm here for you.",
    "Don't hesitate to let me know if there's a particular aspect you'd like further clarification on.",
    "I aim to make your interaction effortless. If there's more you need, feel free to inform me.",
    "Your input is valuable. Please share any additional requirements, and I'll respond promptly.",
    "Should you require more details or have additional questions, I'm ready to provide assistance.",
    "Your success is important to me. If there's anything else you need support with, feel free to ask."
]


def process_query(query):

    response = DecisionMakingModel(query)
    
    if response == "True":
        return Search(query)
    elif response == "False":
        return Chatbot().send_message(user_input=query)
    elif response.startswith("google search "):
        topic = response[len("google search "):]
        return Search(topic)
    elif response.startswith("youtube search "):
        topic = response[len("youtube search "):]
        return YouTubeSearch(topic)
    elif response.startswith("weather"):
        location = response[len("weather"):].strip()
        if location:
            return current_weather_details(location)
        else:
            return current_weather_details() 
    elif response.startswith("Content "):
        topic = response[len("Content"):].strip()
        Content(topic)
        return random.choice(success)
    elif response.startswith("play "):
        topic = response[len("play "):]
        Play(topic)
        return random.choice(success)
    elif response.startswith("open "):
        apps = response[len("open "):].strip()
        OpenApplications(apps)
        return random.choice(success)
    else:
        return response

if __name__ == "__main__":
    while True:
        user_query = input("Enter your query: ")
        process_query(user_query)
