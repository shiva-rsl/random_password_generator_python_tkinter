import os
import re
import tkinter as tk
import random_password_generator_CLI
from tkinter import ttk
from tkinter import E,W,S,N
from tkinter import messagebox
from random_password_generator_CLI import *
from tkinter.filedialog import asksaveasfile


DEFAULT_PASSWORD_LENGTH = 8
password_option_user = []
checkbox_variables = []
password_option = {}


# Functions
def clear_screen():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except:
        print('\n' * 100)
clear_screen()


def error_messagebox_function():
    messagebox.showinfo('Error', 'Please check at lease one checkbox to proceed.')
    

def generate_passowrd_function():

    try: 

        for _, (text, var) in enumerate(checkbox_options.items()):
            checkbox_name = re.sub(r"\s\(.*\)", '', text)
            password_option[checkbox_name.lower()] = var.get()

        password_option['password_length'] = int(spinbox_password_length.get())
        password_quantity = int(spinbox_password_quantity.get())

        for _ in range(password_quantity):
            generated_password = random_password_generator(password_option)
            entry_generated_password.insert(tk.END, generated_password+"\n")

    except IndexError:
        error_messagebox_function()
            
          
def button_show_copy_messege():
    
    password_count = int(spinbox_password_quantity.get())
    print(password_count)
    if password_count == 1:
        label_about['text'] = 'Password copied!'
        label_about['fg'] = 'green'
    else:
        label_about['text'] = 'Passwords copied!'
        label_about['fg'] = 'green'
    window.after(2000, lambda: label_about.config(text=''))


def copy_to_clipboard_function():
    labelframe_generated_password.clipboard_clear()
    labelframe_generated_password.clipboard_append(entry_generated_password.get('1.0', tk.END).rstrip())
    button_show_copy_messege()


def clear_function():
    entry_generated_password.delete(0.0, tk.END)


def about_function():
    text = """The Random Password Generator enables you to generate secure and highly
    unpredictable passwords through an optional mix of lowercase and uppercase letters,
    numbers and special characters."""
    if label_about['text'] == '':
        label_about['text'] = text
    else:
        label_about['text'] = ''


def save_password_function(passwrods):
    file = asksaveasfile(
            mode='w', 
            title='Save Passwords', 
            filetypes=[('Text Document','*.txt'), ('All Files', '*.*')], 
            defaultextension='.txt', 
        )

    if file:
        content = passwrods
        file.write(content)
        file.close()


def save_function():
    generated_passwrods = entry_generated_password.get('0.0', tk.END).rstrip()
    if generated_passwrods == '':
        messagebox.showinfo('Error', 'There is nothing to be saved')
        return
    save_password_function(generated_passwrods)
        

# Main window
window = tk.Tk()
window.geometry('700x925')
window.resizable(width=False, height=False)
window.title('Random Password Generator App')

window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=2)
window.columnconfigure(2, weight=1)
window.configure(bg="#DFE4E8")


# LabelFrames
labelframe_settings = tk.LabelFrame(
    master=window, 
    text='Password settings', 
    font=('Noto Sans', 20, ),
)
labelframe_settings.grid(row=2, column=0, columnspan=5, padx=(10, 10), pady=(10, 0), sticky='EW')

labelframe_settings.columnconfigure(0, weight=1)
labelframe_settings.columnconfigure(1, weight=1)
labelframe_settings.columnconfigure(2, weight=1)


labelframe_generated_password = tk.LabelFrame(
    master=window,
    text='Generated Password(s)',
    font=('Noto Sans', 20, ),
)
labelframe_generated_password.grid(row=3, column=0, ipadx=120, ipady=5, padx=(10, 10), pady=(10, 10))


labelframe_buttons = tk.LabelFrame(
    master=window,
)
labelframe_buttons.grid(row=4, column=0, ipadx=15, ipady=0, padx=(10, 10), pady=(5, 10))



# Labels

label_texts = {
    "title": "Random Password Generator",
    "subtitle": "A free tool to quickly create your password",
    "length": "Length of generated password: ",
    "length_note": "(8 to 30 Chars)",
    "quantity": "Number of Passwords: ",
    "quantity_note": "(1-100 Passwords)",
    "output": "Your Password: "
}


label_title = tk.Label(
    master=window, 
    text=label_texts['title'], 
    background='black', 
    foreground='yellow', 
    font=('Noto Sans', 20)
)
label_title.grid(row=0, column=0, columnspan=5, ipadx=250, ipady=15, sticky='NSEW')


label_title_definition = tk.Label(
    master=window,
    text=label_texts['subtitle'],
    background='black', 
    foreground='yellow', 
    font=('Noto Sans', 12),
)
label_title_definition.grid(row=1, column=0, columnspan=5, ipady=5, sticky='NEW')


label_password_length = tk.Label(
    master=labelframe_settings, 
    text=label_texts['length'],
    font=('Noto Sans', 10),
)
label_password_length.grid(row=0, column=0, padx=(10, 5), pady=(20, 0), sticky='w')


label_password_length_numbers = tk.Label(
    master=labelframe_settings, 
    text=label_texts['length_note'],
    font=('Noto Sans', 10),
)
label_password_length_numbers.grid(row=0, column=2, padx=(5, 10), pady=(20, 0), sticky='w')

label_password_quantity = tk.Label(
    master=labelframe_settings, 
    text=label_texts['quantity'],
    font=('Noto Sans', 10),
)
label_password_quantity.grid(row=1, column=0, padx=(10, 5), pady=(20, 30), sticky='w')

label_password_quantity_numbers = tk.Label(
    master=labelframe_settings, 
    text=label_texts['quantity_note'],
    font=('Noto Sans', 10),
)
label_password_quantity_numbers.grid(row=1, column=2, padx=(5, 10), pady=(20, 30), sticky='w')


label_random_password = tk.Label(
    master=labelframe_generated_password, 
    text='Your Password(s): ',
    font=('Noto Sans', 15),
    anchor='center'
)
label_random_password.grid(row=0, column=0, padx=20, pady=30, sticky='E', )


label_about = tk.Label(
    master=window,
    background='#DFE4E8',
)
label_about.grid(row=9, column=0, columnspan=3, )


label_password_strength = tk.Label(
    master=labelframe_generated_password,
    font=('Noto Sans', 10), 
    text='Password strength:',
)
label_password_strength.grid(row=1, column=0, )


# texts

entry_generated_password = tk.Text(
    master=labelframe_generated_password,
    height=10,
    width=55,

)
entry_generated_password.grid(row=0, column=1, pady=5, )


# Checkboxs
checkbox_options = {
    'Uppercase (A, B, C, ...)': tk.BooleanVar(),
    'Lowercase (a, b, c, ...)': tk.BooleanVar(),
    'Digit (0, 1, 2, ...)': tk.BooleanVar(),
    'Minus (-)': tk.BooleanVar(),
    'Underline (_)': tk.BooleanVar(),
    'Space ( )': tk.BooleanVar(),
    "Symbol (!?@#$%&*^~/|\:;.,\"\')": tk.BooleanVar(),
    'Bracket ([, ], {, }, (, ), <, >)': tk.BooleanVar()
}


for index, (text, var) in enumerate(checkbox_options.items()):
    
    vars = tk.BooleanVar()
    checkbox_variables.append(vars)
    checkbox_options[text] = vars

    row = index // 2
    col = index % 2
    cb = tk.Checkbutton(
        master=labelframe_settings,
        text=text,
        variable=vars,
        font=('Noto Sans', 10),
    )
    cb.grid(row=2 + row, column=col, sticky='w', padx=20, pady=5)


# Spinbox

spinbox_password_length = tk.Spinbox(
    master=labelframe_settings, 
    from_=8, 
    to=30, 
    width=20,
    relief='sunken',
)
spinbox_password_length.grid(row=0, column=1, pady=(20, 0),  ipadx=10, ipady=5, sticky='w')

spinbox_password_quantity = tk.Spinbox(
    master=labelframe_settings, 
    from_=1, 
    to=100, 
    width=20,
    relief='sunken',
)
spinbox_password_quantity.grid(row=1, column=1, pady=(20, 30),  ipadx=10, ipady=5, sticky='w')


# Buttons
button_generate = tk.Button(
    master=labelframe_settings, 
    text='Generate Password', 
    background='yellow', 
    activebackground='yellow',
    anchor='center',
    font=('Noto Sans', 10),
    command=generate_passowrd_function,
)
button_generate.grid(row=6, column=1, pady=20, ipady=7, sticky='W')


button_save = tk.Button(
    master=labelframe_buttons, 
    text='Save Password(s)',
    font=('Noto Sans', 10),
    command=save_function,
)
button_save.grid(row=0, column=0, ipadx=12, ipady=10)


button_copy_to_clipboard = tk.Button(
    master=labelframe_buttons, 
    text='Copy to clipboard',
    font=('Noto Sans', 10),
    command=copy_to_clipboard_function,
)
button_copy_to_clipboard.grid(row=0, column=1, ipadx=12, ipady=10)


button_clear = tk.Button(
    master=labelframe_buttons, 
    text='Clear',
    font=('Noto Sans', 10),
    command=clear_function,
)
button_clear.grid(row=0, column=2, ipadx=25, ipady=10)


button_about = tk.Button(
    master=labelframe_buttons, 
    text='About',
    font=('Noto Sans', 10),
    command=about_function,
)
button_about.grid(row=0, column=3, ipadx=23, ipady=10)


button_close = tk.Button(
    master=labelframe_buttons, 
    text='Close',
    font=('Noto Sans', 10),
    command=window.destroy)
button_close.grid(row=0, column=4, ipadx=23, ipady=10)


# ProgressBar
progressbar_generated_password = ttk.Progressbar(
    master=labelframe_generated_password,
)
progressbar_generated_password.grid(row=1, column=1, padx=5, pady=10, sticky='SNEW') 


window.mainloop()
