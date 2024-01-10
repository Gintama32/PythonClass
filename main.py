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
        #Database connection, db information access point
        self.username = username
        self.conn = sqlite3.connect('userdata.db')
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * FROM userdata WHERE username = ?",(self.username,))
        userdata = self.cur.fetchone()
        if userdata:
            self.rank = userdata[3]
            self.mode = userdata[4]
            self.highest_record = userdata[5]
        self.point =0
        self.chat_log = [{'role': 'assistant', 'content': 'You are a python programming professor. Give response if the user answer is correct or not.'}]
        self.root = root
        self.root.title("Python Class")
        self.root.geometry("800x500")
        
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

        
    def question_bank(self):
        # Define different sets of questions based on difficulty levels
        novice_questions = [
            'What is Python?',
            'What are data types in Python?',
            'What is a variable in Python?',
            'How do I print something in Python?',
            'What are comments in Python?',
            'How do I get input from a user in Python?',
            'What is a loop in Python?',
            'How do I define a function in Python?',
            'What is a list in Python?',
            'How do I add items to a list in Python?',
            'What is a tuple in Python?',
            'How do I access elements in a tuple?',
           ' What is a dictionary in Python?',
           ' How do I access elements in a dictionary?',
            'What is a set in Python?',
            'How do I add elements to a set in Python?',
            'How do I remove elements from a set in Python?',
            'What are control structures in Python?',
            'How do I use if...else conditional statements in Python?',
            'How do I use for loops in Python?',
            'How do I use while loops in Python?',
            'What is a function in Python?',
            'How do I return a value from a function in Python?',
            'How do I use built-in functions in Python?',
            'What is a module in Python?',
            'How do I import a module in Python?',
            'What is an exception in Python?',
            'How do I handle exceptions in Python?',
            'What are file handling operations in Python?',
            'How do I open and read a file in Python?',
            'How do I write to a file in Python?',
            'What are classes and objects in Python?',
            'How do I define a class in Python?',
            'How do I create an object in Python?',
            'What are instance variables in Python?',
            'What are class variables in Python?',
            'How do I access class variables in Python?',
            'What is inheritance in Python?',
            'How do I implement inheritance in Python?',
            'What are access specifiers in Python?',
            'How do I use public, protected, and private access specifiers in Python?',
            'What is polymorphism in Python?',
            'How do I achieve polymorphism in Python?',
            'What are regular expressions in Python?',
            'How do I use regular expressions in Python?',
            'What are lambda functions in Python?',
            'How do I use lambda functions in Python?',
            'What is list comprehension in Python?',
            'How do I use list comprehension in Python?',
            'What are generator functions in Python?',
            'How do I create generator functions in Python?',
            'What are decorators in Python?',
            'How do I define and use decorators in Python?',
            'What are iterators in Python?',
            'How do I create custom iterators in Python?',
            'What are generators in Python?',
            'How do I use generators to iterate through large datasets in Python?',
            'What is the Python standard library?',
            'How do I use standard library modules in Python?',
            'What are third-party libraries in Python?',
            'How do I install and use third-party libraries in Python?',
            'What is pip in Python?',
            'How do I use pip to manage Python packages?',
            'What are virtual environments in Python?',
            'How do I create and use virtual environments in Python?',
            'What are the differences between Python 2 and Python 3?',
            'How do I migrate code from Python 2 to Python 3?',
            'What are some best practices for writing clean and efficient Python code?',
            'How do I write unit tests in Python?',
            'How do I use assert statements for testing in Python?',
            'What is PEP 8 and why is it important for Python developers?',
            'How do I format my code according to PEP 8 guidelines?',
            'What are the differences between local and global variables in Python?',
            'How do I handle scope and namespaces in Python?',
            'What are the built-in data structures in Python?',
            'How do I use dictionaries, lists, and tuples effectively in Python?',
            'What are the different ways to format strings in Python?',
            'How do I format dates and times in Python?',
            'What are the different methods for reading input from the command line in Python?',
            'How do I handle user input validation in Python?',
            'What are the different ways to handle and format errors and warnings in Python?',
            'How do I use logging for debugging and error handling in Python?',
            'What is the purpose of the init.py file in Python packages?',
            'How do I structure and organize my Python projects effectively?',
            'What are the best practices for documenting Python code using docstrings?',
            'How do I generate and view documentation for my Python code?',
            'What are context managers in Python and how do I use them?',
            'How do I work with JSON data in Python?',
            'What are the different ways to interact with databases in Python?',
            'How do I handle concurrency and parallelism in Python?',
            'What are the different options for asynchronous programming in Python?',
            'How do I create and use web APIs in Python?',
            'What are the popular web frameworks for building web applications in Python?',
            'How do I handle authentication and authorization in Python web applications?',
            'What are the different options for deploying Python web applications?',
            'How do I work with web sockets in Python?',
            'What are the best practices for securing Python web applications?',
            'How do I handle internationalization and localization in Python applications?',
           ' What are the best practices for performance optimization in Python?',
            'How do I stay updated with the latest developments and best practices in the Python community?'
        ]
        warrior_questions = [
            'Explain the concept of a generator in Python.',
            'Differentiate between a list and a tuple in Python.',
            'How do you handle exceptions in Python?',
            'Explain the purpose of the `__init__` method in Python classes.',
            'Describe the use of decorators in Python.',
            'What is the purpose of the `lambda` function in Python?',
            'How does Python manage memory?',
            'Explain the difference between shallow copy and deep copy in Python.',
            'Discuss the importance of PEP 8 in Python coding.',
            'What are the different types of namespaces in Python?',
            'Describe the use of the `yield` keyword in Python.',
            'Explain the concept of function annotations in Python.',
            'Discuss the role of `self` in Python classes.',
            'How does Python handle multi-threading?',
            'Explain the purpose of the `__str__` and `__repr__` methods in Python.',
            'Describe the purpose of `*args` and `**kwargs` in Python function parameters.',
            'Explain the use of context managers in Python.',
            'How do you handle file I/O operations in Python?',
            'Discuss the purpose of the `global` keyword in Python.',
            'Describe the purpose of the `super()` function in Python.',
            'Explain the concept of monkey patching in Python.',
            'How does Python handle circular imports?',
            'Discuss the difference between instance methods, class methods, and static methods in Python.',
            'Explain the purpose of the `functools` module in Python.',
            'Describe the purpose of the `collections` module in Python.',
            'How does Python implement inheritance?',
            'Discuss the purpose of the `__slots__` attribute in Python.',
            'Explain the concept of decorators with arguments in Python.',
            'Discuss the role of the `@property` decorator in Python.',
            'How does Python handle garbage collection?',
            'Explain the purpose of the `__call__` method in Python.',
            'Describe the use of the `itertools` module in Python.',
            'Discuss the purpose of the `__doc__` attribute in Python.',
            'How do you handle JSON data in Python?',
            'Explain the purpose of the `pickle` module in Python.',
            'Discuss the purpose of the `asyncio` module in Python.',
            'How does Python manage memory leaks?',
            'Explain the use of the `__new__` method in Python.',
            'Describe the purpose of metaclasses in Python.',
            'Discuss the difference between `__getattr__` and `__getattribute__` methods in Python.',
            'Explain the purpose of the `weakref` module in Python.',
            'How do you create a context manager in Python?',
            'Discuss the purpose of the `functools.partial` function in Python.',
            'Explain the concept of closures in Python.',
            'How does Python handle circular references in memory management?',
            'Describe the purpose of the `subprocess` module in Python.',
            'Discuss the use of the `multiprocessing` module in Python.',
            'Explain the purpose of the `__index__` method in Python.',
            'How do you handle command-line arguments in Python scripts?',
            'Discuss the purpose of the `os` module in Python.',
            'Explain the purpose of the `re` module in Python (regular expressions).',
            'How does Python handle GIL (Global Interpreter Lock)?',
            'Describe the purpose of the `warnings` module in Python.',
            'Discuss the use of `__slots__` in Python classes.',
            'Explain the purpose of the `traceback` module in Python.',
            'How do you handle timestamps in Python?',
            'Discuss the purpose of the `atexit` module in Python.',
            'Explain the concept of memoization in Python.',
            'Describe the purpose of the `unittest` module in Python.',
            'Discuss the use of `__getstate__` and `__setstate__` methods in Python.',
            'How does Python handle multi-processing?',
            'Explain the purpose of the `logging` module in Python.',
            'Describe the use of the `timeit` module in Python.',
            'Discuss the purpose of the `ctypes` module in Python.',
            'Explain the concept of operator overloading in Python.',
            'How do you handle encoding and decoding in Python?',
            'Discuss the purpose of the `sys` module in Python.',
            'Describe the use of the `platform` module in Python.',
            'Explain the purpose of the `array` module in Python.',
            'How does Python handle memory optimization?',
            'Discuss the purpose of the `concurrent.futures` module in Python.',
            'Explain the concept of method resolution order (MRO) in Python.',
            'Describe the purpose of the `resource` module in Python.',
            'Discuss the use of the `fileinput` module in Python.',
            'Explain the purpose of the `functools.lru_cache` function in Python.',
            'How does Python handle socket programming?',
            'Discuss the purpose of the `fnmatch` module in Python.',
            'Describe the use of the `zlib` module in Python.',
            'Explain the concept of named tuples in Python.',
            'Discuss the purpose of the `doctest` module in Python.',
            'How do you handle regular expressions in Python?',
            'Describe the purpose of the `random` module in Python.',
            'Explain the concept of the `argparse` module in Python.',
            'Discuss the use of the `platform` module in Python.',
            'How does Python handle type annotations?',
            'Discuss the purpose of the `shutil` module in Python.',
            'Explain the concept of the `concurrent` module in Python.',
            'Describe the purpose of the `sqlite3` module in Python.',
            'Discuss the use of the `async` and `await` keywords in Python.',
            'How does Python handle property setters and deleters?',
            'Explain the purpose of the `os.path` module in Python.',
            'Describe the concept of `__future__` in Python.',
            'Discuss the purpose of the `difflib` module in Python.',
            'Explain the use of the `unittest.mock` module in Python.',
            'How does Python handle multi-threading vs. multi-processing?',
            'Describe the purpose of the `cProfile` module in Python.',
            'Discuss the use of the `io` module in Python.',
            'Explain the concept of `os.environ` in Python.',
            'How does Python handle file permissions?',
            'Discuss the purpose of the `warnings` module in Python.'

        ]
        champion_questions = [
            'Explain the GIL (Global Interpreter Lock) in Python and its impact on multi-threading.',
            'Discuss the difference between parallelism and concurrency in Python.',
            'Describe the use of metaclasses and provide a practical example.',
            'Explain the purpose of the `__slots__` attribute and its advantages in Python classes.',
            'Discuss the concept of memory optimization and techniques used in Python.',
            'Explain the working principles behind Python decorators and provide complex use cases.',
            'Discuss the differences between coroutines and generators in Python.',
            'Describe the purpose and use cases for weak references in Python.',
            'Explain the concept of the Python data model and its significance.',
            "Discuss the complexities of Python's memory management and garbage collection.",
            'Describe the internals of Python dictionaries and their underlying data structures.',
            "Discuss the challenges and solutions related to Python's handling of circular references.",
            'Explain the role and benefits of C extensions in Python.',
            "Discuss how Python handles method resolution order (MRO) in multiple inheritance scenarios.",
            "Describe the inner workings and optimizations of Python's string handling.",
            "Explain the intricacies of Python's handling of closures and nested functions.",
            'Discuss the complexities of implementing custom iterators and iterables in Python.',
            'Describe the use of asyncio in Python and its advantages in asynchronous programming.',
            'Explain the concept of function currying and its applications in Python.',
            'Discuss the differences between eager evaluation and lazy evaluation in Python.',
            'Describe the challenges and benefits of using multi-core processors in Python.',
            'Explain the complexities and solutions for managing state in concurrent Python applications.',
            "Discuss the intricacies of Python's handling of context managers and their implementation.",
            'Describe the mechanisms and benefits of memoization in Python and its limitations.',
            'Explain the challenges and strategies for dealing with large datasets in Python.',
            'Discuss the complexities of handling race conditions in multi-threaded Python programs.',
            'Describe the challenges and techniques for debugging memory leaks in Python.',
            "Explain the intricacies of Python's handling of large-scale parallel processing.",
            'Discuss the complexities of managing thread synchronization in Python.',
            'Describe the use of custom exceptions and their implementation in Python.',
            "Explain the challenges and solutions related to Python's handling of I/O-bound tasks.",
            'Discuss the intricacies of implementing complex algorithms in Python efficiently.',
            "Describe the differences between compiled and interpreted languages and Python's nature.",
            'Explain the complexities of implementing data structures like trees and graphs in Python.',
            'Discuss the challenges and solutions for optimizing Python code for performance.',
            "Describe the intricacies of Python's memory view and buffer protocol.",
            "Explain the working principles behind Python's garbage collection strategies.",
            'Discuss the complexities of managing and optimizing database operations in Python.',
            "Describe the inner workings of Python's metaprogramming features.",
            'Explain the use of function annotations and their limitations in Python.',
            'Discuss the complexities of handling floating-point arithmetic in Python.',
            'Describe the challenges and techniques for handling large-scale data processing in Python.',
            'Explain the intricacies of implementing and optimizing search algorithms in Python.',
            "Discuss the complexities of Python's handling of complex regular expressions.",
            "Describe the inner workings and optimizations of Python's sorting algorithms.",
            "Explain the challenges and strategies for managing resources efficiently in Python.",
            "Discuss the complexities of implementing concurrency patterns in Python.",
            "Describe the challenges and solutions for achieving high-performance computing in Python.",
            "Explain the intricacies of Python's handling of closures in different scopes.",
            "Discuss the complexities and benefits of using JIT (Just-In-Time) compilation in Python.",
            "Explain the concept of metaprogramming in Python and provide examples of its usage.",
            "Discuss the complexities and strategies for handling memory fragmentation in Python.",
            "Describe the process of optimizing Python code for high-performance computing.",
            "Explain the challenges and techniques for optimizing Python code for low-level operations.",
            "Discuss the complexities and benefits of using Python's `ctypes` for interfacing with C libraries.",
            "Describe the inner workings and optimization strategies for Python's garbage collector.",
            "Explain the complexities and solutions for achieving thread safety in Python applications.",
            "Discuss the challenges and benefits of implementing custom Python interpreters.",
            "Describe the intricacies of implementing complex data structures like heaps or tries in Python.",
            "Explain the role and implementation of JIT (Just-In-Time) compilation in Python."
        ]
        if self.mode == 'Novice':
            return random.choice(novice_questions)
        elif self.mode == 'Warrior':
            return random.choice(warrior_questions)
        else:
            return random.choice(champion_questions)
    #  menu
    def toggle_menu(self):
        menu = tk.Frame(self.root, width= 200, height = 500, bg = '#3E8EDE')
        name = tk.Label(menu, text= f"Learner: {self.username}", font = ('Times New Roman', 15), bg = '#3E8EDE')
        record = tk.Label(menu, text = f"Highest Point: {self.highest_record}", font = ('Times New Roman', 15), bg = '#3E8EDE')
        mode = tk.Label(menu, text= f"Mode: {self.mode}",font= ('Times New Roman', 15), bg = '#3E8EDE')
        rank = tk.Label(menu,text = f"Rank: {self.rank}", font= ('Times New Roman', 15), bg = '#3E8EDE')
        def rank_match():
            self.mode = 'Ranked Match'
            menu.destroy()
        def difficulty():
            def easy_mode():
                self.mode = 'Novice'
                self.cur.execute("UPDATE userdata SET mode = ? WHERE username = ?", (self.mode,self.username))
                self.conn.commit()
                self.generate_question()
                menu.destroy()
            def normal_mode():
                self.mode = 'Warrior'
                self.cur.execute("UPDATE userdata SET mode = ? WHERE username = ?", (self.mode,self.username))
                self.conn.commit()
                self.generate_question()
                menu.destroy()
            def hard_mode():
                self.mode = 'Champion'
                self.cur.execute("UPDATE userdata SET mode = ? WHERE username = ?", (self.mode,self.username))
                self.conn.commit()
                self.generate_question()
                menu.destroy()

            easy_btn = tk.Button(menu, text = 'Novice', bg = 'lightgreen', font = ('Times New Roman', 10),command= easy_mode)
            middle_btn = tk.Button(menu, text = 'Warrior', bg = 'orange', font = ('Times New Roman', 10),command= normal_mode)
            hard_btn = tk.Button(menu, text = 'Champion', bg = 'red', font = ('Times New Roman', 10),command= hard_mode)
            easy_btn.place(x=10, y = 300)
            middle_btn.place(x=80, y = 300)
            hard_btn.place(x=10, y = 350)
        change_mode_btn = tk.Button(menu, text = 'Change Difficulty', font=('Times New Roman', 13), bg = 'green', command= difficulty)
        match_rank_btn = tk.Button(menu, text = 'Rank Match', font= ('Times New Roman', 13), bg = 'Red', command= rank_match)
   
        name.place(x= 5, y = 50,)
        record.place(x= 5, y = 100)
        mode.place(x = 5, y = 150)
        rank.place(x= 5, y = 200)
        change_mode_btn.place(x = 10, y = 250)
        match_rank_btn.place(x = 10, y = 400)
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
