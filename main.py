from pathlib import Path
from tkinter import END, Canvas, PhotoImage, Tk, messagebox, ttk
import pyperclip
import json
import password


BACKGROUND = "white"
FONT = ("FantasqueSansMono Nerd Font", 15, "normal")
FILE_NAME = "data.json"
IMAGE_HEIGHT = 200
IMAGE_NAME = "logo.png"
IMAGE_WIDTH = 200


script_folder = Path(__file__).absolute().parent
image_location = script_folder/IMAGE_NAME
file_location = script_folder/FILE_NAME


def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    empty = False
    is_okay = False
    if len(website) == 0 or len(password) == 0 or len(email) == 0:
        empty = True
        messagebox.showinfo(title="Empty field(s)",
                            message="Please don't leave field(s) empty")
    if not empty:
        is_okay = messagebox.askokcancel(
            title="Confirm", message=f"These are the details entered:\nWebsite: {website}\nEmail: {email}\nPassword: {password}\nIs it ok to save?")
    if is_okay and not empty:

        file = None
        user_input = {website: {
            "email": email,
            "password": password
        }}
        data = {}
        try:
            with open(file_location, "r") as file:
                data = json.load(file)
                data.update(user_input)
        except FileNotFoundError:
            print(f"File: {FILE_NAME} not found. Created it.")
        except json.decoder.JSONDecodeError:
            print(f"File: {FILE_NAME} is empty")
        with open(file_location, "w") as file:
            json.dump(data, file, indent=4)

        website_entry.delete(0, END)
        password_entry.delete(0, END)


def generate_password():
    required_password = password.random_password()
    password_entry.delete(0, END)
    password_entry.insert(0, required_password)
    pyperclip.copy(required_password)


def search():
    website = website_entry.get()
    if len(website) > 0:
        try:
            file = open(file_location)
        except FileNotFoundError:
            messagebox.showinfo(
                title="Error", message=f"File: {FILE_NAME} not found.")
        else:
            data = json.load(file)
            try:
                email = data.get(website).get("email")
                required_password = data.get(website).get("password")
            except AttributeError:
                messagebox.showinfo(
                    title="Oops!", message=f"No entry for website: {website}")
            else:
                messagebox.showinfo(
                    title="Record Found", message=f"Email: {email}\nPassword: {required_password}")
        finally:
            file.close()


window = Tk()
window.title("Password Manager")
my_canvas = Canvas(window)
lock_image = PhotoImage(file=image_location)
website_label = ttk.Label(window)
website_entry = ttk.Entry(window)
search_button = ttk.Button(window)
email_label = ttk.Label(window)
email_entry = ttk.Entry(window)
password_label = ttk.Label(window)
password_entry = ttk.Entry(window)
generate_password_button = ttk.Button(window)
add_button = ttk.Button(window)


style = ttk.Style(window)
style.configure('my.TButton', font=FONT, background=BACKGROUND)


window.config(padx=20, pady=20, background=BACKGROUND)
my_canvas.config(height=IMAGE_HEIGHT, width=IMAGE_WIDTH,
                 background=BACKGROUND, highlightthickness=0)
my_canvas.create_image(IMAGE_WIDTH/2, IMAGE_HEIGHT/2, image=lock_image)
website_label.config(text="Website:", background=BACKGROUND,
                     font=FONT, justify="center")
search_button.config(text="Search", style='my.TButton', command=search)
website_entry.config(font=FONT)
email_label.config(text="Email/Username:",
                   background=BACKGROUND, font=FONT, justify="center")
email_entry.config(width=40, font=FONT)
email_entry.insert(0, "sourish@gmail.com")
password_label.config(
    text="Password:", background=BACKGROUND, font=FONT, justify="center")
password_entry.config(width=21, font=FONT)
generate_password_button.config(
    text="Generate Password", style='my.TButton', command=generate_password)
add_button.config(text="Add", width=40, style='my.TButton', command=save)


my_canvas.grid(row=1, column=2)
website_label.grid(row=2, column=1)
website_entry.grid(row=2, column=2)
search_button.grid(row=2, column=3, sticky="WE")
email_label.grid(row=3, column=1)
email_entry.grid(row=3, column=2, columnspan=2)
password_label.grid(row=4, column=1)
password_entry.grid(row=4, column=2)
generate_password_button.grid(row=4, column=3)
add_button.grid(row=5, column=2, columnspan=2)


for widget in window.winfo_children():
    widget.grid_configure(padx=5, pady=5)

website_entry.focus()

window.mainloop()
