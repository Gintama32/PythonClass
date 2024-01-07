import tkinter as tk
import socket
from sign_in import run_signup_page

root = tk.Tk()
root.geometry('380x440')
root.title("Login")

def login():
    # Get username and password when the Login button is clicked
    username = username_entry.get()
    password = password_entry.get()

    # Connect to the server and send credentials
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("localhost", 9999))

        message = client.recv(1024).decode()
        client.send(username.encode())

        message = client.recv(1024).decode()
        client.send(password.encode())

        check = (client.recv(1024).decode())
        if check == "Login successful!":
            from main import App
            root.destroy()  # Close the login window
            main_root = tk.Tk()  # Create a new window for the main app
            app = App(main_root,username)
            main_root.mainloop()
    except ConnectionRefusedError:
        print("Connection was refused. Please ensure the server is running.")
    except Exception as e:
        print("An error occurred:", e)

    finally:
        client.close()
    
# Creating widget
frame = tk.Frame(root)
header = tk.Label(frame, text="Login Page", font=("Arial", 30))
username = tk.Label(frame, text="Username", font=("Arial", 16))
username_entry = tk.Entry(frame, font=('Arial', 16))
password_entry = tk.Entry(frame, show="*", font=('Arial', 16))
password = tk.Label(frame, text="Password", font=("Arial", 16))
login_btn = tk.Button(frame, text='Login', font=("Arial", 16),cursor = 'hand2', command=login)
question = tk.Label(frame, text="Don't have an account?", font=('Arial', 13))
sign_in = tk.Button(frame, text="Sign Up", width = 6, border = 0,cursor = 'hand2',font=('Arial',13), command= run_signup_page)

header.grid(row=0, column=0, columnspan=2, pady=40)
username.grid(row=1, column=0, pady=20)
password.grid(row=2, column=0, pady=20)
username_entry.grid(row=1, column=1)
password_entry.grid(row=2, column=1)
login_btn.grid(row=3, column=0, columnspan=2)
question.grid(row=5, column=0, columnspan=2, padx=20, pady=20, sticky='e')
sign_in.grid(row=5, column=2, columnspan=2, padx=(0, 20), pady=20, sticky='w')
frame.pack()

root.mainloop()
