from tkinter import *
from tkinter import messagebox
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
FONT_NAME = "Courier"
import random
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

nr_letters = random.randint(8, 10)
nr_symbols = random.randint(2, 4)
nr_numbers = random.randint(2, 4)
def generate() :
    password_list = []

    for char in range(nr_letters):
      password_list.append(random.choice(letters))

    for char in range(nr_symbols):
      password_list += random.choice(symbols)

    for char in range(nr_numbers):
      password_list += random.choice(numbers)

    random.shuffle(password_list)

    passwordOne = ""
    for char in password_list:
      passwordOne += char
    p_input.delete(0,'end')
    p_input.insert(0, passwordOne)
    pyperclip.copy(passwordOne)
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_text():
    website = w_input.get()
    password = p_input.get()
    email = e_input.get()
    new_data = {
        website: {
            "email" : email,
            "password" : password,
        }
    }
    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
    else:
        try:
            with open("data.json", mode="r") as file:
                data = json.load(file)
        except FileNotFoundError:
            with open("data.json", mode="w") as file:
                json.dump(new_data, file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", mode="w") as file:
                json.dump(data, file, indent=4)
        finally:
            w_input.delete(0, 'end')
            p_input.delete(0, 'end')

def search():
    try:
        website = w_input.get()
        with open("data.json", mode="r") as file:
            data = json.load(file)
            if website in data:
                password = data[website]["password"]
                email = data[website]["email"]
                messagebox.showinfo(title="Information", message=f"Email: {email}\nPassword: {password}")
            else :
                messagebox.showinfo(title="Error", message="Website Not Found in Manager")
    except KeyError:
       messagebox.showinfo(title="Error", message="Please enter a Website in Manager")
       w_input.delete(0, 'end')

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = Canvas(width=200, height=200)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100,100, image=lock_img)
canvas.grid(column=2, row=1)

website_label = Label(text="Website:")
website_label.grid(column=1, row=2)
website_label.focus()

email_label = Label(text="Email/Username:")
email_label.grid(column=1, row=3)

password_label = Label(text="Password:")
password_label.grid(column=1, row=4)

generate_button = Button(text="Generate Password", command=generate)
generate_button.grid(column=3, row=4, sticky=W)

add_button = Button(text="Add", width=30, command=save_text)
add_button.grid(column=2, row=5, columnspan=2)

search_button = Button(text="Search", command=search)
search_button.grid(column=3, row=2, sticky=W)

w_input = Entry(width=17)
w_input.grid(column=2, row=2)

e_input = Entry(width=35)
e_input.grid(column=2, row=3, columnspan=2)
e_input.insert(0, "anon@gmail.com")

p_input = Entry(width=17)
p_input.grid(column=2, row=4)

window.mainloop()