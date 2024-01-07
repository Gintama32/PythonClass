import tkinter as tk
import sqlite3 as sq
import hashlib

def create_connection(db_file):
    conn = None
    try:
        conn = sq.connect(db_file)
        return conn
    except sq.Error as e:
        print(e)
    return conn

def create_user(conn, username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cur = conn.cursor()
    cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    return cur.lastrowid

def sign_up_user():
    new_user = new_username_entry.get()
    new_pswd = new_password_entry.get()

    conn = create_connection("userdata.db")
    if conn is not None:
        create_user(conn, new_user, new_pswd)
        conn.close()
        signup_status_label.config(text="User created successfully!", fg="green")
    else:
        signup_status_label.config(text="Error creating user. Please try again.", fg="red")

def run_signup_page():
    root = tk.Tk()
    root.geometry('380x440')
    root.title("SignUp page")

    global new_username_entry, new_password_entry, signup_status_label
    frame = tk.Frame(root)
    header = tk.Label(frame, text="Sign-up New User", font=("Arial", 30))
    username = tk.Label(frame, text="Username", font=("Arial", 16))
    new_username_entry = tk.Entry(frame, font=('Arial', 16))
    new_password_entry = tk.Entry(frame, show="*", font=('Arial', 16))
    password = tk.Label(frame, text="Password", font=("Arial", 16))
    sign_btn = tk.Button(frame, text='Sign-up', font=("Arial", 16), cursor='hand2', command=sign_up_user)
    signup_status_label = tk.Label(frame, text="", fg="black")

    header.grid(row=0, column=0, columnspan=2, pady=40)
    username.grid(row=1, column=0, pady=20)
    password.grid(row=2, column=0, pady=20)
    new_username_entry.grid(row=1, column=1)
    new_password_entry.grid(row=2, column=1)
    sign_btn.grid(row=3, column=0, columnspan=2)
    signup_status_label.grid(row=4, column=0, columnspan=2)

    frame.pack()
    root.mainloop()

if __name__ == "__main__":
    run_signup_page()
