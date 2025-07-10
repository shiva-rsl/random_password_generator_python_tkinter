import os
import re
import math
import tkinter as tk
from tkinter import ttk
from tkinter import E,W,S,N
from tkinter import messagebox
from random_password_generator_CLI import *
from tkinter.filedialog import asksaveasfile


DEFAULT_PASSWORD_LENGTH = 8


checkbox_variables = []
password_option = {}
passwords = []


# Functions
def clear_screen():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except:
        print('\n' * 100)
clear_screen()


def error_messagebox_function():
    messagebox.showinfo('Error', 'Please check at lease one checkbox to proceed.')


def get_index(*args):
    print(var.get())


def selection_generated_password():
    return var.trace('w', get_index)


def password_range_calculation():
    password_range = 0

    password_option_range_size = {    
    'uppercase': 26, 
    'lowercase': 26, 
    'digit': 10, 
    'minus': 1, 
    'underline': 1, 
    'space': 1, 
    'symbol': 19, 
    'bracket': 8, 
    }
    
    for key, value in password_option.items():
        if key == 'password_length':
            continue
        if value:
            password_range += password_option_range_size.get(key, 0)

    return password_range


def password_entropy_calculation():
    selection_password = var.get()
    password_length = len(selection_password)
    password_range = password_range_calculation()
    entropy = password_length * math.log2(password_range)
    return entropy


def show_password_entropy():
    password_entropy_value = password_entropy_calculation()
    label_entropy_value['text'] = f'{password_entropy_value:.2f} bits'


def generate_passowrd_function():

    try: 
        
        for _, (key, value) in enumerate(checkbox_options.items()):
            checkbox_name = re.sub(r"\s\(.*\)", '', key)
            password_option[checkbox_name.lower()] = value.get()

        password_option['password_length'] = int(spinbox_password_length.get())

        generated_password = random_password_generator(password_option)
        passwords.append(generated_password)
        combobox_generated_password['values'] = passwords
        combobox_generated_password.set(passwords[-1])

        selection_password = var.get()
        password_length = len(selection_password)
        print(password_length)

        show_password_entropy()
        

    except IndexError:
        error_messagebox_function()


def show_copy_messege():
    label_guidance_text['text'] = 'Password copied!'
    label_guidance_text['fg'] = 'green' 
    window.after(2000, lambda: label_guidance_text.config(text=''))


def copy_to_clipboard_function():
    
    generated_passwrods = var.get()

    if generated_passwrods == '':
        messagebox.showinfo('Error', 'There is nothing to be copied!')
        return
    
    labelframe_generated_password.clipboard_clear()
    labelframe_generated_password.clipboard_append(generated_passwrods)
    show_copy_messege()


def clear_function():
    global passwords
    passwords = []
    combobox_generated_password.set('')
    combobox_generated_password['values'] = ()
    label_entropy_value['text'] = ''


def about_function():
    text = """The Random Password Generator enables you to generate secure and highly
    unpredictable passwords through an optional mix of lowercase and uppercase letters,
    numbers and special characters."""
    if label_guidance_text['text'] == '':
        label_guidance_text['text'] = text
        label_guidance_text['fg'] = 'black'
    else:
        label_guidance_text['text'] = ''


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
    generated_passwrods = var.get()
    if generated_passwrods == '':
        messagebox.showinfo('Error', 'There is nothing to be saved!')
        return
    save_password_function(generated_passwrods)
        

# Main window
window = tk.Tk()
window.geometry('700x840')
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
    "output": "Password: ",
    "entropy": "Total Entropy:",
    "strength": "Strength: ",
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
label_password_length.grid(row=0, column=0, padx=(30, 0), pady=(30, 30), sticky='w')


label_password_length_numbers = tk.Label(
    master=labelframe_settings, 
    text=label_texts['length_note'],
    font=('Noto Sans', 10),
)
label_password_length_numbers.grid(row=0, column=2, padx=(0, 80), pady=(30, 30), sticky='w')


label_random_password = tk.Label(
    master=labelframe_generated_password, 
    text=label_texts['output'],
    font=('Noto Sans', 15),
    anchor='center'
)
label_random_password.grid(row=0, column=0, padx=20, pady=30, sticky='E', )


label_password_strength = tk.Label(
    master=labelframe_generated_password,
    font=('Noto Sans', 12), 
    text=label_texts['strength'],
)
label_password_strength.grid(row=1, column=0, pady=10)


label_entropy_calc = tk.Label(
    master=labelframe_generated_password,
    font=('Noto Sans', 12),
    text=label_texts['entropy']
)
label_entropy_calc.grid(row=2, column=0, pady=10)


label_entropy_value = tk.Label(
    master=labelframe_generated_password,
    font=('Noto Sans', 12, 'bold'),
)
label_entropy_value.grid(row=2, column=1, sticky='w')


label_guidance_text = tk.Label(
    master=window,
    background='#DFE4E8',
)
label_guidance_text.grid(row=9, column=0, columnspan=3, )


# Combobox
var = tk.StringVar()
combobox_generated_password = ttk.Combobox(
    master=labelframe_generated_password,
    width=28,
    font=('Noto Sans', 15),
    values=passwords,
    textvariable=var
)
combobox_generated_password.grid(row=0, column=1, padx=5)


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


for index, (text, checkbox_var) in enumerate(checkbox_options.items()):
    
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
spinbox_password_length.grid(row=0, column=1, pady=(30, 30), ipadx=10, ipady=5, sticky='w')


# Buttons
button_generate_password = tk.Button(
    master=labelframe_settings, 
    text='Generate Password', 
    background='yellow', 
    activebackground='yellow',
    anchor='center',
    font=('Noto Sans', 10),
    command=generate_passowrd_function,
)
button_generate_password.grid(row=6, column=1, pady=20, ipady=7, sticky='W')


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


selection_generated_password()
print(password_option)
window.mainloop()
