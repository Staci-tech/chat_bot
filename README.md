# ChatBot Code Explanation Guide
## A Complete Line-by-Line Breakdown for Beginners

---

## Table of Contents
1. [Introduction](#introduction)
2. [Importing Libraries](#importing-libraries)
3. [Setting Up Files and Variables](#setting-up-files-and-variables)
4. [Helper Functions](#helper-functions)
5. [Main ChatBot Function](#main-chatbot-function)
6. [Understanding the Features](#understanding-the-features)
7. [Setup Instructions](#setup-instructions)

---

## Introduction

This is a smart chatbot program written in Python. Think of it like creating your own personal assistant on your computer that can:
- Have conversations with you
- Remember your name
- Tell jokes
- Check the weather
- Search for information using AI
- Do math calculations
- Keep a to-do list
- Set reminders
- And much more!

Let's break down every single line to understand how it works.

---

## Importing Libraries

```python
import datetime
import requests
import json
import os
import random
import time
import re
from textblob import TextBlob
from openai import OpenAI
```

**What this does:** These are like tools we're borrowing to help build our chatbot.

- `datetime` - Helps us work with dates and times (like telling you what time it is)
- `requests` - Lets our program talk to websites on the internet (like getting weather data)
- `json` - Helps us save and read data in a organized way (like saving your name)
- `os` - Lets us work with files and folders on your computer
- `random` - Helps us pick random things (like random jokes)
- `time` - Lets us pause the program or work with time
- `re` - Helps us find patterns in text (like finding coordinates in a message)
- `TextBlob` - Analyzes the mood/emotion of text you write
- `OpenAI` - Connects to OpenAI's smart AI to answer questions

---

## Setting Up Files and Variables

```python
USER_FILE = "user_data.json"
CUSTOM_FILE = "custom_responses.json"
```

**What this does:** We're creating names for two files:
- `USER_FILE` will store your name so the bot remembers you
- `CUSTOM_FILE` will store custom responses you teach the bot

```python
# Initialize OpenAI client
# Make sure to set your OpenAI API key as an environment variable
# export OPENAI_API_KEY="your-api-key-here"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

**What this does:** This connects our chatbot to OpenAI's AI brain. Think of it like giving our bot access to a super smart library that knows about everything.

```python
custom_responses = {}
if os.path.exists(CUSTOM_FILE):
    with open(CUSTOM_FILE, "r") as file:
        custom_responses = json.load(file)
```

**What this does:** 
- We create an empty box called `custom_responses` to store things you teach the bot
- If the custom responses file already exists (meaning you taught the bot before), we load all those teachings back into memory

```python
user_name = ""
if os.path.exists(USER_FILE):
    with open(USER_FILE, "r") as file:
        data = json.load(file)
        user_name = data.get("name", "")
```

**What this does:**
- We start with no name stored
- If there's already a file with your name saved, we load it so the bot remembers you

```python
greeting_keywords = ["hello", "hi", "hey", "greetings", "good morning", "good evening"]
```

**What this does:** This is a list of words that mean "hello" - so the bot knows when you're greeting it.

```python
jokes = [
    "Why don't programmers like nature? Too many bugs!",
    "Why did the function break up with the loop? It was stuck in a cycle.",
    "Why do Python programmers wear glasses? Because they can't C."
]
```

**What this does:** A collection of programming jokes the bot can tell you when you ask for a joke.

```python
todo_list = []
conversation_memory = []
```

**What this does:**
- `todo_list` is an empty list to store your tasks
- `conversation_memory` remembers the last 5 things you said

---

## Helper Functions

### Function 1: Saving Custom Responses

```python
def save_custom_responses():
    with open(CUSTOM_FILE, "w") as file:
        json.dump(custom_responses, file)
```

**What this does:** When you teach the bot something new, this function saves it to a file so the bot remembers even after you close the program.

### Function 2: Saving Your Name

```python
def save_user_name(name):
    with open(USER_FILE, "w") as file:
        json.dump({"name": name}, file)
```

**What this does:** When you tell the bot your name, this saves it to a file so it can greet you by name next time.

### Function 3: Resetting Your Name

```python
def reset_user_name():
    global user_name
    user_name = ""
    if os.path.exists(USER_FILE):
        os.remove(USER_FILE)
```

**What this does:** If you want the bot to forget your name, this function erases it from memory and deletes the file.

### Function 4: Getting Weather Information

```python
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
```

**What this does:** 
- Takes a city name as input
- Contacts a weather website using a special key
- Gets the current temperature and weather description
- If something goes wrong (no internet, wrong city name), it tells you what happened

### Function 5: OpenAI Search

```python
def openai_search(query):
    """Search using OpenAI's ChatGPT model"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides concise, accurate information. Keep responses brief and informative, typically 2-3 sentences."},
                {"role": "user", "content": f"Please provide information about: {query}"}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Sorry, I couldn't search for that information. Error: {str(e)}"
```

**What this does:**
- Takes your search question
- Asks OpenAI's smart AI about it
- Gets back a helpful answer (2-3 sentences)
- If something goes wrong, it tells you there was an error

---

## Main ChatBot Function

```python
def chatbot():
    global user_name
    print("Hello! I am ChatBot. Type 'bye' to exit.")
    print("Teach me using: add: question = answer")

    if user_name:
        print(f"ChatBot: Welcome back, {user_name}!")
```

**What this does:**
- Starts the main conversation
- Greets you and explains how to teach it
- If it knows your name, it welcomes you back personally

```python
    while True:
        user_input = input("You: ").lower().strip()
```

**What this does:**
- Starts an endless loop (until you say "bye")
- Waits for you to type something
- Converts what you type to lowercase and removes extra spaces

```python
        # Save to memory
        conversation_memory.append(user_input)
        if len(conversation_memory) > 5:
            conversation_memory.pop(0)
```

**What this does:**
- Adds what you just said to the memory
- If memory has more than 5 things, it forgets the oldest one (keeps only last 5)

---

## Understanding the Features

### 1. Saying Goodbye

```python
        if user_input == 'bye':
            print("ChatBot: Goodbye!")
            break
```

**What this does:** When you type "bye", the bot says goodbye and stops the conversation.

### 2. Teaching the Bot

```python
        elif user_input.startswith("add:"):
            try:
                _, pair = user_input.split(":", 1)
                question, answer = pair.split("=", 1)
                custom_responses[question.strip()] = answer.strip()
                save_custom_responses()
                print("ChatBot: Got it! I'll remember that.")
            except ValueError:
                print("ChatBot: Use format: add: question = answer")
```

**What this does:**
- If you type something starting with "add:", it tries to learn
- It splits your text to find the question and answer
- Saves this new knowledge
- If you don't format it correctly, it reminds you how

**Example:** Type "add: favorite color = blue" and the bot learns that your favorite color is blue.

### 3. Using Custom Responses

```python
        elif user_input in custom_responses:
            print(f"ChatBot: {custom_responses[user_input]}")
```

**What this does:** If you ask something you previously taught the bot, it gives you the answer you taught it.

### 4. Showing What You Taught

```python
        elif user_input == "show commands":
            if custom_responses:
                print("ChatBot: Here are your custom questions and answers:")
                for q, a in custom_responses.items():
                    print(f"- {q.strip()} = {a.strip()}")
            else:
                print("ChatBot: You haven't taught me anything yet!")
```

**What this does:** Shows you all the things you've taught the bot.

### 5. Deleting Custom Responses

```python
        elif user_input.startswith("delete:"):
            question_to_delete = user_input.replace("delete:", "").strip()
            if question_to_delete in custom_responses:
                del custom_responses[question_to_delete]
                save_custom_responses()
                print(f"ChatBot: Deleted the command '{question_to_delete}'.")
            else:
                print("ChatBot: I couldn't find that question to delete.")
```

**What this does:** If you type "delete: something", it forgets that teaching.

### 6. Showing Memory

```python
        elif user_input == "show memory":
            if conversation_memory:
                print("ChatBot: Here's our recent chat:")
                for msg in conversation_memory:
                    print("-", msg)
            else:
                print("ChatBot: Memory is empty.")
```

**What this does:** Shows you the last 5 things you said in the conversation.

### 7. Greetings

```python
        elif any(greet in user_input for greet in greeting_keywords):
            print("ChatBot: Hello there! How can I help you?")
```

**What this does:** If your message contains any greeting word (hello, hi, etc.), the bot greets you back.

### 8. Bot Identity

```python
        elif "your name" in user_input:
            print("ChatBot: I'm a simple chatbot")

        elif "how are you" in user_input:
            print("ChatBot: I'm just a bunch of code, but I'm doing great! And you?")
```

**What this does:** Responds to questions about the bot itself.

### 9. Time and Date

```python
        elif "time" in user_input:
            print("ChatBot: The current time is", datetime.datetime.now().strftime("%H:%M:%S"))

        elif "date" in user_input:
            print("ChatBot: Today's date is", datetime.datetime.now().strftime("%Y-%m-%d"))
```

**What this does:** 
- If you ask about time, it tells you the current time
- If you ask about date, it tells you today's date

### 10. Weather Feature

```python
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
                        print(f"ChatBot: It's {temp}°C with {desc} near {city}")
                    else:
                        print("ChatBot: Couldn't get weather info.")
                except:
                    print("ChatBot: Error getting weather data.")
            else:
                city = input("ChatBot: Please enter your city: ")
                print("ChatBot:", get_weather(city))
```

**What this does:**
- If you mention "weather", it helps you get weather info
- It can work with coordinates (like 40.7128, -74.0060 for New York)
- Or it asks you for your city name and gets the weather

### 11. Math Calculator

```python
        elif re.match(r'^what is \d+\s*[\+\-\*/]\s*\d+$', user_input):
            try:
                result = eval(user_input.replace("what is", "").strip())
                print(f"ChatBot: The answer is {result}")
            except:
                print("ChatBot: I couldn't calculate that.")
```

**What this does:** If you ask "what is 5 + 3", it calculates and gives you the answer.

### 12. AI Search

```python
        elif user_input.startswith("search "):
            term = user_input.replace("search", "").strip()
            print("ChatBot: Searching...")
            result = openai_search(term)
            print("ChatBot:", result)
```

**What this does:** If you type "search something", it uses AI to find information about that topic.

### 13. Currency Conversion

```python
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
                print("ChatBot: Couldn't convert currency.")
```

**What this does:** Converts money between different currencies. Example: "convert currency 100 USD to EUR"

### 14. Unit Conversion

```python
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
```

**What this does:** Converts between different units like kilometers to miles, kg to pounds, etc.

### 15. Emotion Analysis

```python
        elif user_input.startswith("feel "):
            text = user_input.replace("feel", "").strip()
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            if polarity > 0.2:
                print("ChatBot: You sound positive!")
            elif polarity < -0.2:
                print("ChatBot: I sense you're feeling down. Want to talk?")
            else:
                print("ChatBot: You seem neutral.")
```

**What this does:** If you type "feel I'm so happy today", it analyzes if your message is positive, negative, or neutral.

### 16. Jokes

```python
        elif "joke" in user_input:
            print("ChatBot:", random.choice(jokes))
```

**What this does:** When you ask for a joke, it picks a random one from the joke list.

### 17. Name Management

```python
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
```

**What this does:**
- Learns and remembers your name when you introduce yourself
- Tells you your name when you ask "who am i"
- Forgets your name if you ask it to reset

### 18. To-Do List

```python
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
```

**What this does:**
- Adds tasks to your to-do list when you type "add task: buy groceries"
- Shows all your tasks when you type "show tasks"

### 19. Reminders

```python
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
```

**What this does:** Sets a timer and reminds you about something. Example: "remind me in 10 seconds to check email"

### 20. Default Response

```python
        else:
            print("ChatBot: I'm not sure how to respond. You can teach me using 'add: question = answer'.")
```

**What this does:** If the bot doesn't understand what you said, it suggests you can teach it.

### 21. Program Execution

```python
if __name__ == "__main__":
    chatbot()
```

**What this does:** This line starts the chatbot when you run the program.

---

## Setup Instructions

### Step 1: Install Required Software
You need Python installed on your computer. Download it from python.org

### Step 2: Install Required Libraries
Open your command line/terminal and type:
```bash
pip install openai textblob requests
```

### Step 3: Get OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Create an account and get your API key
3. Set it as an environment variable:
   - On Mac/Linux: `export OPENAI_API_KEY="your-key-here"`
   - On Windows: `set OPENAI_API_KEY=your-key-here`

### Step 4: Create Virtual Environment (Optional but Recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 5: Run the Program
Save the code as `chatbot.py` and run:
```bash
python chatbot.py
```

---

## How It All Works Together

Think of this chatbot as a smart friend that lives in your computer:

1. **Memory**: It remembers your name and things you teach it
2. **Learning**: You can teach it new responses
3. **Internet Access**: It can get weather, search information, and convert currencies
4. **Utilities**: It helps with math, time, reminders, and to-do lists
5. **Personality**: It tells jokes and analyzes emotions

The bot keeps running until you say "bye", constantly listening for your input and trying to help with whatever you need.

Each feature is like a different skill the bot has learned, and when you type something, it goes through all its skills to see which one matches what you're asking for.

---

## Conclusion

This chatbot is a great example of how programming can create useful, interactive applications. It combines many different technologies and concepts to create something that feels almost human-like in its interactions.

The beauty of this code is that it's modular - each feature is separate, so you can easily add new features or modify existing ones without breaking the whole program.

Remember: programming is like teaching a computer to think step by step, and this chatbot is a perfect example of breaking down complex interactions into simple, logical steps!
