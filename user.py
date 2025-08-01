import datetime
import requests
import json
import os
import random
import time
import re
import wikipedia
from textblob import TextBlob
import webbrowser

USER_FILE = "user_data.json"
CUSTOM_FILE = "custom_responses.json"

custom_responses = {}
if os.path.exists(CUSTOM_FILE):
    with open(CUSTOM_FILE, "r") as file:
        custom_responses = json.load(file)

user_name = ""
if os.path.exists(USER_FILE):
    with open(USER_FILE, "r") as file:
        data = json.load(file)
        user_name = data.get("name", "")

greeting_keywords = ["hello", "hi", "hey", "greetings", "good morning", "good evening"]
jokes = [
    "Why don't programmers like nature? Too many bugs!",
    "Why did the function break up with the loop? It was stuck in a cycle.",
    "Why do Python programmers wear glasses? Because they can't C."
]

todo_list = []
conversation_memory = []

def save_custom_responses():
    with open(CUSTOM_FILE, "w") as file:
        json.dump(custom_responses, file)

def save_user_name(name):
    with open(USER_FILE, "w") as file:
        json.dump({"name": name}, file)

def reset_user_name():
    global user_name
    user_name = ""
    if os.path.exists(USER_FILE):
        os.remove(USER_FILE)

def get_weather(city):
    api_key = "1e7c4fa56ca5278859fec5f89e0be068"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data["cod"] == 200:
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            return f"It is currently {temp}°C with {description} in {city}."
        else:
            return "ChatBot: Couldn't retrieve weather info. Try a valid city name."
    except:
        return "ChatBot: Error retrieving weather data. Connect to the Internet or there may be other problems."

def chatbot():
    global user_name
    print("Hello! I am ChatBot. Type 'bye' to exit.")
    print("Teach me using: add: question = answer")

    if user_name:
        print(f"ChatBot: Welcome back, {user_name}!")

    while True:
        user_input = input("You: ").lower().strip()

        # Save to memory
        conversation_memory.append(user_input)
        if len(conversation_memory) > 15:
            conversation_memory.pop(0)

        if user_input == 'bye':
            print("ChatBot: Goodbye!")
            break

        elif user_input.startswith("add:"):
            try:
                _, pair = user_input.split(":", 1)
                question, answer = pair.split("=", 1)
                custom_responses[question.strip()] = answer.strip()
                save_custom_responses()
                print("ChatBot: Got it! I'll remember that.")
            except ValueError:
                print("ChatBot: Use format: add: question = answer")

        elif user_input in custom_responses:
            print(f"ChatBot: {custom_responses[user_input]}")

        elif user_input == "show commands":
            if custom_responses:
                print("ChatBot: Here are your custom questions and answers:")
                for q, a in custom_responses.items():
                    print(f"- {q.strip()} = {a.strip()}")
            else:
                print("ChatBot: You haven't taught me anything yet!")

        elif user_input.startswith("delete:"):
            question_to_delete = user_input.replace("delete:", "").strip()
            if question_to_delete in custom_responses:
                del custom_responses[question_to_delete]
                save_custom_responses()
                print(f"ChatBot: Deleted the command '{question_to_delete}'.")
            else:
                print("ChatBot: I couldn't find that question to delete.")

        elif user_input == "show memory":
            if conversation_memory:
                print("ChatBot: Here’s our recent chat:")
                for msg in conversation_memory:
                    print("-", msg)
            else:
                print("ChatBot: Memory is empty.")

        elif any(greet in user_input for greet in greeting_keywords):
            print("ChatBot: Hello there! How can I help you?")

        elif "your name" in user_input:
            print("ChatBot: I'm a simple chatbot")

        elif "how are you" in user_input:
            print("ChatBot: I'm just a bunch of code, but I'm doing great! And you?")

        elif "time" in user_input:
            print("ChatBot: The current time is", datetime.datetime.now().strftime("%H:%M:%S"))

        elif "date" in user_input:
            print("ChatBot: Today's date is", datetime.datetime.now().strftime("%Y-%m-%d"))

        elif "weather" in user_input:
            # Check for coordinates
            coord_match = re.search(r"([-+]?\d*\.?\d+),\s*([-+]?\d*\.?\d+)", user_input)
            if coord_match:
                lat, lon = coord_match.groups()
                api_key = "1e7c4fa56ca5278859fec5f89e0be068"
                url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
                try:
                    response = requests.get(url)
                    data = response.json()
                    if data["cod"] == 200:
                        temp = data["main"]["temp"]
                        desc = data["weather"][0]["description"]
                        city = data.get("name", "")
                        print(f"ChatBot: It’s {temp}°C with {desc} near {city}")
                    else:
                        print("ChatBot: Couldn’t get weather info.")
                except:
                    print("ChatBot: Error getting weather data.")
            else:
                city = input("ChatBot: Please enter your city: ")
                print("ChatBot:", get_weather(city))

        elif re.match(r'^what is \d+\s*[\+\-\*/]\s*\d+$', user_input):
            try:
                result = eval(user_input.replace("what is", "").strip())
                print(f"ChatBot: The answer is {result}")
            except:
                print("ChatBot: I couldn't calculate that.")

        elif user_input.startswith("search "):
            term = user_input.replace("search", "").strip()
            try:
                summary = wikipedia.summary(term, sentences=10)
                print("ChatBot:", summary)
            except:
                print("ChatBot: Couldn’t find that topic.")

        elif user_input.startswith("convert currency"):
            try:
                parts = user_input.split()
                amount = float(parts[2])
                from_curr = parts[3].upper()
                to_curr = parts[5].upper()
                url = f"https://open.er-api.com/v6/latest/{from_curr}"
                response = requests.get(url)
                rates = response.json()["rates"]
                rate = rates[to_curr]
                converted = amount * rate
                print(f"ChatBot: {amount} {from_curr} = {converted:.2f} {to_curr}")
            except:
                print("ChatBot: Couldn’t convert currency.")

        elif user_input.startswith("convert"):
            try:
                parts = user_input.split()
                value = float(parts[1])
                from_unit = parts[2]
                to_unit = parts[4]
                conversions = {
                    ("km", "miles"): 0.621371,
                    ("miles", "km"): 1.60934,
                    ("kg", "pounds"): 2.20462,
                    ("pounds", "kg"): 0.453592
                }
                factor = conversions.get((from_unit, to_unit))
                if factor:
                    result = value * factor
                    print(f"ChatBot: {value} {from_unit} = {result:.3f} {to_unit}")
                else:
                    print("ChatBot: Conversion not supported.")
            except:
                print("ChatBot: Please use: convert 5 km to miles")

        elif user_input.startswith("feel "):
            text = user_input.replace("feel", "").strip()
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            if polarity > 0.2:
                print("ChatBot: You sound positive!")
            elif polarity < -0.2:
                print("ChatBot: I sense you’re feeling down. Want to talk?")
            else:
                print("ChatBot: You seem neutral.")
            
        elif "joke" in user_input:
            print("ChatBot:", random.choice(jokes))

        elif "my name is" in user_input:
            user_name = user_input.split("is")[-1].strip().capitalize()
            save_user_name(user_name)
            print(f"ChatBot: Nice to meet you, {user_name}!")

        elif "who am i" in user_input:
            if user_name:
                print(f"ChatBot: You are {user_name}!")
            else:
                print("ChatBot: I don't know your name yet.")

        elif "reset name" in user_input:
            reset_user_name()
            print("ChatBot: Name has been reset.")

        elif user_input.startswith("add task:"):
            task = user_input.replace("add task:", "").strip()
            todo_list.append(task)
            print("ChatBot: Task added!")

        elif user_input == "show tasks":
            if todo_list:
                print("ChatBot: Here are your tasks:")
                for i, task in enumerate(todo_list, 1):
                    print(f"{i}. {task}")
            else:
                print("ChatBot: You have no tasks.")

        elif "remind me in" in user_input:
            try:
                parts = user_input.split("remind me in")[1].strip().split(" to ")
                time_part = parts[0].strip()
                reminder_msg = parts[1].strip()
                seconds = int(time_part.split()[0])
                print(f"ChatBot: Okay, I will remind you in {seconds} seconds.")
                time.sleep(seconds)
                print(f"ChatBot: Reminder! {reminder_msg}")
            except:
                print("ChatBot: Use this format: remind me in 5 seconds to drink water")

        else:
            print("ChatBot: I'm not sure how to respond. You can teach me using 'add: question = answer'.")

chatbot()

#//virtual envirnment = python3 -m venv venv then source venv/bin/activate
