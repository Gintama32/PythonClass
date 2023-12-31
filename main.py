import tkinter as tk
from dotenv import load_dotenv
import openai
import os
import random
from tkinter import scrolledtext
import sqlite3


# Load environment variables from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class App:
    def __init__(self, root, username):
        self.point = 0
        self.chat_log = [{'role': 'assistant', 'content': 'You are a python programming professor. Give response if the user answer is correct or not.'}]
        self.root = root
        self.root.title("Python Class")
        self.root.geometry("800x500")
        self.username = username
        self.title = tk.Label(root, text="Learn Python", font=("Arial", 14))
        self.title.pack()
        open_btn = tk.Button(self.root, text = 'Menu', command = self.toggle_menu, bg = 'lightblue', font=('Times New Roman', 15))
        open_btn.pack(side = 'left', anchor = 'n')
        self.point_display = tk.Label(root, text=f"Points: {self.point}", font=("Roboto", 12), bd = 3, background='lightgrey')
        self.point_display.pack(padx=10, pady=10)

        self.question_display = tk.Label(root, text="", font=("Ubuntu", 13))
        self.question_display.pack(padx=13, pady=13)
        self.generate_question()

        self.text_input = tk.Text(root, height=3, font=("Roboto", 14))
        self.text_input.pack(padx=10, pady=10)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack()

        self.enter_button = tk.Button(self.button_frame, text="ENTER", command=self.get_input_text, font=("Roboto", 12), background='green')
        self.enter_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.next_button = tk.Button(self.button_frame, text="NEXT", command=self.generate_question, font=("Roboto", 12), background='orange')
        self.next_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.clear_button = tk.Button(root, text="Clear All", command=self.clear_responses, font=("Roboto", 12), background='lightblue')
        self.clear_button.pack(padx=10, pady=10)

        self.assistant_response_text = scrolledtext.ScrolledText(root, height=15, wrap=tk.WORD, font=("Ubuntu", 12))
        self.assistant_response_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
#Database connection, db information access point
        self.conn = sqlite3.connect('userdata.db')
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * FROM userdata WHERE username = ?",(self.username,))
        userdata = self.cur.fetchone()
        if userdata:
            self.rank = userdata[3]
            self.mode = userdata[4]
            self.highest_record = userdata[5]
    def question_bank(self):
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
    #  menu
    def toggle_menu(self):
        menu = tk.Frame(self.root, width= 200, height = 500, bg = '#3E8EDE')
        name = tk.Label(menu, text= f"Learner: {self.username}", font = ('Times New Roman', 15), bg = '#3E8EDE')
        record = tk.Label(menu, text = f"Highest Point: {self.highest_record}", font = ('Times New Roman', 15), bg = '#3E8EDE')
        mode = tk.Label(menu, text= f"Mode: {self.mode}",font= ('Times New Roman', 15), bg = '#3E8EDE')
        rank = tk.Label(menu,text = f"Rank: {self.rank}", font= ('Times New Roman', 15), bg = '#3E8EDE')
        change_mode_btn = tk.Button(menu, text = 'Change Difficulty', font=('Times New Roman', 13), bg = 'green')
        match_rank_btn = tk.Button(menu, text = 'Rank Match', font= ('Times New Roman', 13), bg = 'Red')
        name.place(x= 5, y = 50,)
        record.place(x= 5, y = 100)
        mode.place(x = 5, y = 150)
        rank.place(x= 5, y = 200)
        change_mode_btn.place(x = 10, y = 250)
        match_rank_btn.place(x = 10, y = 290)
        menu.place(x=0,y=0)
        def dele():
            menu.destroy()
        close_btn = tk.Button(menu, text = 'close', command = dele)
        close_btn.place(x=5,y=10)

    def generate_question(self):
        new_question = self.question_bank()
        self.question_display.config(text=new_question)
        self.chat_log.append({'role': 'assistant', 'content': new_question})

    def add_points(self, point):
        self.highest_record += point
        self.point += point
        self.cur.execute("UPDATE userdata SET highest_record = ? WHERE username = ?", (self.highest_record,self.username))
        self.conn.commit()
        self.point_display.config(text=f"Points: {self.point}")
    def get_input_text(self):
        current_question = self.question_display.cget("text")
        self.chat_log.append({'role': 'assistant', 'content': current_question})
        user_msg = self.text_input.get("1.0", tk.END).strip()
        self.chat_log.append({'role': 'user', 'content': user_msg})

        assistant_response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=self.chat_log
        )
        assistant_reply = assistant_response.choices[0].message.content
        positive_words = ['correct', 'great', 'perfect', 'good', 'accurate', 'right']
        if any(word in assistant_reply.lower() for word in positive_words):
            self.add_points(5)

        self.chat_log.append({'role': 'assistant', 'content': assistant_reply.strip("\n").strip()})
        self.assistant_response_text.insert(tk.END, assistant_reply.strip() + '\n\n')
        self.text_input.delete("1.0", tk.END)

    def clear_responses(self):
        self.assistant_response_text.delete("1.0", tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
