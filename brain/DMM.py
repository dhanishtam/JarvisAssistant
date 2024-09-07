import groq
import os
from dotenv import load_dotenv

load_dotenv()

GroqAPI = os.environ.get("GROQ_API_KEY2")

client = groq.Client(api_key=GroqAPI)

def DecisionMakingModel(Query):
    """ This function is responsible for the decision making of the program, it decides what to do with the query. """

    response = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {
                "role": "system",
                "content": "Respond 'True' if the question pertains to time-sensitive information or specific individuals like 'What is today's headline?', 'Who is akshay kumar?', 'Who is India's current prime minister?', 'What's the day today?', 'Tell me something new about YouTube', or queries about individuals like 'Who is Elon' But if the question is asking something that happened before 2021, respond with 'False'. If the question says to open any app like 'can you open (appname) for me', respond with 'open (appname)'. If the question says play music, respond with 'play (musicname)'. If the questions asks about what's the time, date, day, month, year etc. respond with 'False'. If the questions is asking for more information but not mentioning the noun like 'tell me more about him' or 'who is he', respond with 'True'. If the question ask to search a specific topic on google, Respond with 'google search (topic). If the question asks to search a specific topic on youtube, respond with 'youtube search (topic)'. If the question asks to write any type of content like application, codes, emails or anything else, respond with 'Content (topic)'. If the question asks what is the weather, respond with 'weather' else if it also provide you with a location respond with 'weather location_name'. If the question involves multiple actions or searches, respond with both actions separately. Otherwise, respond with 'False' if the question or query can be answered by a Chatbot."
            }
        ]
    }

    def add_message(response, role, content):
        response["messages"].append({"role": role, "content": content})

    add_message(response, "user", "Who is elon musk?")
    add_message(response, "assistant", "True")

    add_message(response, "user", "tell me more about him")
    add_message(response, "assistant", "True")

    add_message(response, "user", "Explain the concept of calculus.")
    add_message(response, "assistant", "False")

    add_message(response, "user", "Who is the CEO of Tesla?")
    add_message(response, "assistant", "True")

    add_message(response, "user", "what's his networth?")
    add_message(response, "assistant", "True")

    add_message(response, "user", "what is elon musk's current networth?")
    add_message(response, "assistant", "True")

    add_message(response, "user", "Do you know what is photosynthesis?")
    add_message(response, "assistant", "False")

    add_message(response, "user", "can you explain it?")
    add_message(response, "assistant", "True")

    add_message(response, "user", "Thanks, Bye, Hello, Exactly, Cool, Welcome, Let's see and more conversational queries.")
    add_message(response, "assistant", "False")

    add_message(response, "user", "who was maharana pratap?")
    add_message(response, "assistant", "False")

    add_message(response, "user", "search python programming on google")
    add_message(response, "assistant", "google search python programming")

    add_message(response, "user", "search kaushik shresth on youtube")
    add_message(response, "assistant", "youtube search kaushik shresth")

    add_message(response, "user", "Who was the first president of usa?")
    add_message(response, "assistant", "False")

    add_message(response, "user", "can you play a tutorial for how to wear a tie on youtube?")
    add_message(response, "assistant", "play how to wear a tie")

    add_message(response, "user", "can you open facebook, whatsapp, instagram and telegram for me?")
    add_message(response, "assistant", "open facebook whatsapp instagram telegram")

    add_message(response, "user", "can you tell me what's the time?")
    add_message(response, "assistant", "False")

    add_message(response, "user", "what's the date today?")
    add_message(response, "assistant", "False")

    add_message(response, "user", "what's the day?")
    add_message(response, "assistant", "False")

    add_message(response, "user", "thanks")
    add_message(response, "assistant", "False")

    add_message(response, "user", "write a python code for creating a snake game")
    add_message(response, "assistant", "Content python code for creating a snake game")

    add_message(response, "user", "can you tell me about the recent news related to the sun?")
    add_message(response, "assistant", "True")

    add_message(response, "user", "Can you open YouTube and search for funny cat videos?")
    add_message(response, "assistant", "open YouTube")
    add_message(response, "assistant", "youtube search funny cat videos")

    add_message(response, "user", "Tell me about the latest tech.")
    add_message(response, "assistant", "True")

    add_message(response, "user", "What is the latest research in quantum computing?")
    add_message(response, "assistant", "True")

    add_message(response, "user", "Provide a summary of the latest research in climate change in bullet points.")
    add_message(response, "assistant", "Content summary of the latest research in climate change in bullet points")

    add_message(response, "user", "Get me the latest articles on artificial intelligence from The Verge.")
    add_message(response, "assistant", "True")

    add_message(response, "user", "Write and execute a Python script to scrape news headlines.")
    add_message(response, "assistant", "Content Python script to scrape news headlines")
    add_message(response, "assistant", "execute Python script")

    # Weather
    add_message(response, "user", "What's the weather like?")
    add_message(response, "assistant", "weather")

    add_message(response, "user", "What is the current weather in New York?")
    add_message(response, "assistant", "weather New York")

    add_message(response, "user", "Can you tell me the weather in Paris?")
    add_message(response, "assistant", "weather Paris")

    add_message(response, "user", "Get me the latest weather update.")
    add_message(response, "assistant", "weather")

    add_message(response, "user", Query)

    completion = client.chat.completions.create(
        model=response["model"],
        messages=response["messages"],
        temperature=0.7,
        max_tokens=2048,
        top_p=1,
        stream=True,
        stop=None
    )

    Answer = ""

    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content

    return Answer

# if __name__ == "__main__":
#     while True:
#         print(DecisionMakingModel(input("Enter your query: ")))
