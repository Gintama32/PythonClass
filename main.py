import tkinter as tk
from dotenv import load_dotenv
import openai
import os
import random
from tkinter import ttk
from tkinter import scrolledtext 
# Load environment variables from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
chat_log=[]
root = tk.Tk()

def question_bank():
    # Your list of questions remains the same
    questions = [
        'What is OOP, and why is it important in Python?',
        'What is a class in Python?',
        'What is an object in Python?',
        'How do you create an instance of a class?',
        'What are the four pillars of OOP?',
        'What is encapsulation?',
        'What is abstraction?',
        'What is method overloading?',
        'What is method overriding?',
        'What are the different types of inheritance in Python?',
        'What is polymorphism?',
        'What is the difference between a class method and a static method?',
        'What is the difference between an abstract class and a concrete class?',
        'What is a constructor?',
        'What is a destructor?',
        'What is garbage collection?',
        'What is the difference between a list and a tuple?',
        'What is a dictionary?',
        'What is a set?',
        'What is a generator?'
    ]
    return random.choice(questions)
def generate_question():
    new_question = question_bank()
    question_display.config(text=new_question)
    chat_log.append({'role': 'assistant', 'content': new_question})  # Append the new question to the chat log
    return new_question

def get_input_text():
    global chat_log
    current_question = question_display.cget("text")
    chat_log.append({'role': 'assistant', 'content': current_question})
    user_msg = text_input.get("1.0", tk.END).strip()
    chat_log.append({'role': 'user', 'content': user_msg})
    
    assistant_response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=chat_log
    )
    assistant_reply = assistant_response.choices[0].message.content
    chat_log.append({'role': 'assistant', 'content': assistant_reply.strip("\n").strip()})
    
    # Update or create a label for assistant's response
    assistant_response_text.insert(tk.END, assistant_reply.strip() + '\n\n')
    text_input.delete("1.0", tk.END)  # Clear the input field

def clear_responses():
    assistant_response_text.delete("1.0", tk.END)  # Clear all displayed responses

root.geometry("800x500")
root.title("Python Class")
title = tk.Label(root, text="Learn Python", font=("Arial", 14))
title.pack()

question_display = tk.Label(root, text="", font=("Ubuntu", 13))
question = generate_question()
question_display.config(text=question)
question_display.pack(padx = 13,pady=13)

text_input = tk.Text(root, height=3, font=("Roboto", 14))
text_input.pack(padx=10, pady=10)

# Create a frame to contain the buttons and pack them horizontally
button_frame = tk.Frame(root)
button_frame.pack()

enter_button = tk.Button(button_frame, text="ENTER", command=get_input_text, font=("Roboto",12), background='green' )
enter_button.pack(side=tk.LEFT, padx=10, pady=10)

next_button = tk.Button(button_frame, text="NEXT", command=generate_question, font=("Roboto",12),background='orange')
next_button.pack(side=tk.LEFT, padx=10, pady=10)

clear_button = tk.Button(root, text="Clear All", command=clear_responses, font=("Roboto",12), background='lightblue')
clear_button.pack(padx=10, pady=10)

# Create scrolled text for displaying assistant's responses
assistant_response_text = scrolledtext.ScrolledText(root, height=15, wrap=tk.WORD, font=("Ubuntu", 12))
assistant_response_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

root.mainloop()




    