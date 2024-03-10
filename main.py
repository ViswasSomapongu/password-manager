from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
    'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 
    'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
    'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


    password_list = [] 
    nr_letters= random.randint(8,10)
    nr_symbols = random.randint(2,4)
    nr_numbers = random.randint(2,4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]

    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]

    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]
    # for char in range(nr_letters): 
    #     password_list.append(random.choice(letters))

    # for char in range(nr_symbols):
    #     password_list+=random.choice(symbols)
        
    # for char in range(nr_numbers):
    #     password_list+=random.choice(numbers)

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)


    Final_password = "".join(password_list)
    # for i in password_list:
    #     Final_password+=i
    # print(f"Here is your Password: {Final_password}")
    password_entry.insert(0,Final_password)
    pyperclip.copy(Final_password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website)==0 or len(password)==0:
        messagebox.showinfo(title="oops!", message="Please make sure you haven't left any fields empty. ")
    else:   
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered:\nEmail: {email} \nPassword: {password} \nIs it ok to save?")
        if is_ok:
            with open("data.txt","a") as data_file:
                data_file.write(f"{website} | {email} | {password}\n")
                website_entry.delete(0,END)
                password_entry.delete(0,END)
        try:
            with open("data.json","r") as data_file:
                #Reading old data
                data=json.load(data_file)
        except FileNotFoundError:
            with open("data.json","w") as data_file:
                #Updating old data with  new data
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("data.json","w") as data_file:
                #Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0,END)
            password_entry.delete(0,END)

# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open("data.json") as data_file:
            data=json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error",message="No Data File Found.")
    else:
        if website in data:
            email = data[website]["email"]
            passwor = data[website]["password"]
            messagebox.showinfo(title=website,message=f"Email: {email}\nPassword: {passwor}")
        else:
            messagebox.showinfo(title="Error",message=f"No details for {website} exists.")

# ---------------------------- UI SETUP -------------------------------#

windows = Tk()
windows.title("Password-Manager")
windows.config(padx=50, pady=50)

# Logo
canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=0, columnspan=3)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0, sticky="e")

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0, sticky="e")

password_label = Label(text="Password:")
password_label.grid(row=3, column=0, sticky="e")

# Entries
website_entry = Entry(width=21)
website_entry.grid(row=1, column=1, sticky="w")
website_entry.focus()

email_entry = Entry(width=40)
email_entry.grid(row=2, column=1, columnspan=2, sticky="w")
email_entry.insert(0,"Johndeo@gmail.com")

password_entry = Entry(width=21)
password_entry.grid(row=3, column=1, sticky="w")

# Buttons
search_button = Button(text = "Search",width=15,command=find_password)
search_button.grid(row=1,column=2, sticky="w")

generate_password_button = Button(text="Generate Password", width=15, command=generate_password)
generate_password_button.grid(row=3, column=2, sticky="w")

add_button = Button(text="Add", width=34,command = save)
add_button.grid(row=4, column=1, columnspan=2, sticky="w")

windows.mainloop()
