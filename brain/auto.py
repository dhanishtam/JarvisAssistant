from pywhatkit import playonyt, search
import random
import requests
from bs4 import BeautifulSoup
import os
import subprocess
import webbrowser
import platform
import pyautogui
import threading
from time import sleep
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GroqAPI = os.environ.get('GROQ_API_KEY')

system_platform = platform.system()

def OpenNotepad(File):
    """ This function opens the file in notepad. """
    file_path = File
    if os.name == 'posix':
        default_text_editor = 'open'
    elif os.name == 'nt':
        default_text_editor = 'notepad.exe'
    subprocess.call([default_text_editor, file_path])

client = Groq(api_key=GroqAPI)
Username = "Dhanishta"
messages = []
SystemChatBot = [{"role": "system", "content": f"Hello, I am {Username}. You are a content writer. You must write only the necessary content based on the prompt. Do not include any extra lines, explanations, or additional text. Write only what is explicitly asked for."}]

def ContentWriterAI(prompt):
    """ This function writes the content based on the prompt. """
    messages.append({"role": "user", "content": f"{prompt}"})

    completion = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=SystemChatBot + messages,
        max_tokens=1024,
        temperature=0.7,
        top_p=1,
        stream=True,
        stop=None
    )

    Answer = ""

    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content

    Answer = Answer.replace("</s>", "")
    messages.append({"role": "assistant", "content": Answer})
    return Answer

def Content(Topic):
    """ This function writes the content based on the topic and saves it in a text file and opens it. """
    Topic: str = Topic.replace("Content ", "")
    ContentByAI = ContentWriterAI(Topic)

    # Ensure the 'safe' directory exists
    safe_dir = "safe"
    if not os.path.exists(safe_dir):
        os.makedirs(safe_dir)

    file_path = os.path.join(safe_dir, f"{Topic}.txt")

    with open(file_path, "w") as file:
        file.write(ContentByAI)

    threading.Thread(target=OpenNotepad, args=(file_path,)).start()

    return random.choice(professional_responses)

classes = ["zCubwf", "hgKElc", "LTKOO sY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta",
           "IZ6rdc", "O5uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table__webanswers-table",
           "dDoNo ikb4Bb gsrt", "sXLaOe", "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

def GoogleSearch(query):
    """ This function searches the query on google and returns the answer. """
    query = query.replace(" + ", " plus ")
    query = query.replace(" - ", " minus ")
    URL = "https://www.google.co.in/search?q=" + query
    headers = {'User-Agent': useragent}

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    for i in classes:
        try:
            result = soup.find(class_=i).get_text()

            if "Description" in result[:11]:
                Answer = result.replace("Description", "")
            if " Wikipedia" in Answer[-10:]:
                Answer = Answer.replace(" Wikipedia", "")
            return Answer

        except Exception:
            pass

    return None

professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need—don't hesitate to ask.",
    "Continued support is my commitment to you. Let me know if there's anything more I can do for you.",
    "I'm here to ensure your experience is seamless. If you have any further requests, please let me know.",
    "Your needs are important to me. If there's anything I can assist you with, I'm just a message away.",
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

def Play(Topic):
    """ This function plays the video on youtube about the given topic. """
    playonyt(Topic)
    return random.choice(professional_responses)

def Search(Topic):
    """ This function searches the query on Google and returns the answer. """

    query = Topic.replace(" + ", " plus ")
    query = query.replace(" - ", " minus ")
    URL = "https://www.google.co.in/search?q=" + query
    useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
    headers = {'User-Agent': useragent}

    classes = [
        "zCubwf", "hgKElc", "LTKOO sY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee",
        "tw-Data-text tw-text-small tw-ta", "IZ6rdc", "O5uR6d LTKOO", "vlzY6d",
        "webanswers-webanswers_table__webanswers-table", "dDoNo ikb4Bb gsrt", "sXLaOe",
        "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"
    ]

    try:
        page = requests.get(URL, headers=headers)
        page.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(page.content, 'html.parser')

        for cls in classes:
            try:
                result = soup.find(class_=cls).get_text()

                if "Description" in result[:11]:
                    Answer = result.replace("Description", "")
                if " Wikipedia" in Answer[-10:]:
                    Answer = Answer.replace(" Wikipedia", "")
                return Answer

            except Exception as e:
                # print(f"Error processing class {cls}: {e}")
                pass

        return None

    except requests.exceptions.RequestException as e:
        # print(f"Error fetching the page: {e}")
        return None
    
def YouTubeSearch(Topic):
    """ This function searches the topic on youtube. """
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Search)
    return random.choice(professional_responses)

def OpenApplications(Topic):
    """ This function opens the application according to the query. """
    Appname = Topic.lower().replace("open ", "").replace(".", "").replace(" ", "")

    if "youtube" in Appname or "instagram" in Appname or "google" in Appname or "amazon" in Appname or "facebook" in Appname:
        link = f"https://www.{Appname}.com"
        webbrowser.open(link)
        return random.choice(professional_responses)
    else:
        def open_spotlight_and_search(query):
            sleep(.5)
            pyautogui.hotkey('win')
            sleep(1.2)
            pyautogui.write(query)
            sleep(.2)
            pyautogui.press('enter')

        if system_platform == 'Windows':
            finalnamememe = Topic.replace("open ", "").lower()
            open_spotlight_and_search(finalnamememe)
            return random.choice(professional_responses)
        else:
            return random.choice(professional_responses)
