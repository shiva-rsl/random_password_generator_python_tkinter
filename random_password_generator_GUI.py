import os
import re
import math
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from random_password_generator_CLI import *
from tkinter.filedialog import asksaveasfile


DEFAULT_PASSWORD_LENGTH = 8

checkbox_variables = []
password_option = {}
passwords = []


# Functions
def clear_screen():
    """
    Clear the terminal screen.
    Uses 'cls' command on Windows and 'clear' on Unix-based systems.
    If the command fails, it prints multiple newlines as a fallback.
    """
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except:
        print('\n' * 100)

clear_screen()


def error_messagebox_function():
    """
    show an error popup if user has not checked any checkboxes.
    """
    messagebox.showinfo('Error', 'Please check at lease one checkbox to proceed.')


def password_range_calculation():
    """
    Calculate the total size of the character set based on selected password options.

    Returns:
        int: Total character set size for entropy calculation.
    """

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
    
    password_range = 0

    for key, value in password_option.items():
        if key == 'password_length':
            continue
        if value:
            password_range += password_option_range_size.get(key, 0)

    return password_range


def password_entropy_calculation():
    """
    Calculate the entropy of a password based on its length and character diversity.

    The entropy is calculated using the formula: 
    entropy = length * log2(character_pool_size)
    where character_pool_size is determined by password_range_calculation().

    Returns:
        float: The calculated password entropy in bits. A higher value indicates a stronger password.
    """
    selection_password = var.get()
    password_length = len(selection_password)
    password_range = password_range_calculation()
    entropy = password_length * math.log2(password_range)
    return entropy


def show_password_entropy():
    """
    Calculate and display the password entropy in the GUI label.

    This function:
    1. Calls password_entropy_calculation() to compute the entropy
    2. Formats the result to 2 decimal places
    3. Updates the text of label_entropy_value with the result

    Side Effects:
        Modifies the text property of the label_entropy_value widget.

    Returns:
        None: This function doesn't return anything; it updates the UI directly.
    """
    password_entropy_value = password_entropy_calculation()
    label_entropy_value['text'] = f'{password_entropy_value:.2f} bits'


def strength_password_calculation():
    """
    Evaluate password strength based on its entropy and return a rating with color coding.

    The strength is categorized into 5 levels according to the calculated entropy:
    - Very Weak (🔴): < 28 bits
    - Weak (🟠): 28-35 bits
    - Fair (🟡): 36-59 bits
    - Strong (🟣): 60-127 bits
    - Perfect (🟢): 128+ bits

    Returns:
        tuple: A tuple containing two elements:
            - str: Password strength level with emoji indicator
            - str: Hexadecimal color code corresponding to the strength level
    """
    
    strength_level = ''
    strength_color = ''

    password_entropy = password_entropy_calculation()
    
    if password_entropy < 28:
        strength_level = '🔴 Very Weak'
        strength_color = "#f01010"
    elif password_entropy < 36:
        strength_level = '🟠 Weak'
        strength_color = "#ed761c"
    elif password_entropy < 60:
        strength_level = '🟡 Fair'
        strength_color = "#EFE63E"
    elif password_entropy < 128:
        strength_level = '🟣 Strong'
        strength_color =  "#9b59b6"
    else:
        strength_level = '🟢 Perfect'
        strength_color = "#06be06"
    
    return strength_level, strength_color



def show_strength_password():
    """
    Display the password strength rating and its associated color in the GUI.

    This function:
    1. Retrieves the strength level and color by calling strength_password_calculation()
    2. Updates the label_show_strength widget with:
       - Text: The strength level (e.g., "🔴 Very Weak")
       - Foreground color: The associated color code (e.g., "#f01010")

    Side Effects:
        Modifies the text and foreground color properties of the label_show_strength widget.

    Returns:
        None
    """
    strength_level, strength_color  = strength_password_calculation()
    label_show_strength['text'] = strength_level
    label_show_strength['fg'] = strength_color


def generate_password():
    for _, (key, value) in enumerate(checkbox_options.items()):
        checkbox_name = re.sub(r'\s\(.*\)', '', key)
        password_option[checkbox_name.lower()] = value.get()

    password_option['password_length'] = int(spinbox_password_length.get())

    generated_password = random_password_generator(password_option)
    passwords.append(generated_password)
    combobox_generated_password['values'] = passwords
    combobox_generated_password.set(passwords[-1])



def progressbar_password_strength_function():

    password_strength = password_entropy_calculation()

    if password_strength < 28:
        strength = 10
        style.configure('strength.Horizontal.TProgressbar', background="#f01010")
    elif password_strength < 36:
        strength = 30
        style.configure('strength.Horizontal.TProgressbar', background="#ed761c")
    elif password_strength < 60:
        strength = 55
        style.configure('strength.Horizontal.TProgressbar', background="#EFE63E")
    elif password_strength < 128:
        strength = 80
        style.configure('strength.Horizontal.TProgressbar', background="#e52bf2")
    else:
        strength = 100
        style.configure('strength.Horizontal.TProgressbar', background="#06be06")

    progressbar_generated_password['value'] = strength



def generate_passowrd_button_function():

    try: 
        
        generate_password()
        
        show_password_entropy()

        show_strength_password()

        progressbar_password_strength_function()
        

    except IndexError:
        error_messagebox_function()


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


def error_messagebox_save_function(password):
    """
    Show an error popup if no password is available for saving.

    Returns:
        bool: True if a password exists, False otherwise.
    """
    if not password:
        messagebox.showinfo('Error', 'There is nothing to be saved!')
        return False
    return True


def save_function():
    generated_passwrod = var.get()
    if error_messagebox_save_function(generated_passwrod):
        save_password_function(generated_passwrod)


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
    """
    Reset all password-related GUI elements to their default empty state.

    This function:
    1. Clears the global passwords list
    2. Resets the password combobox (current selection and dropdown values)
    3. Clears the entropy value display
    4. Resets the strength indicator text
    5. Sets the progress bar to 0

    Returns:
        None
    """
    global passwords
    passwords = []
    combobox_generated_password.set('')
    combobox_generated_password['values'] = ()
    label_entropy_value['text'] = ''
    label_show_strength['text'] = ''
    progressbar_generated_password['value'] = 0


def about_function():
    """
    Display or toggle the application description in the guidance text label.

    This function:
    1. Shows an informational paragraph about the password generator app
    2. Sets the text color to black
    3. Toggles the text display (shows if empty, hides if already showing)

    Returns:
        None
    """

    text = '''The Random Password Generator enables you to generate secure and highly
    unpredictable passwords through an optional mix of lowercase and uppercase letters,
    numbers and special characters.'''
    if label_guidance_text['text'] == '':
        label_guidance_text['text'] = text
        label_guidance_text['fg'] = 'black'
    else:
        label_guidance_text['text'] = ''


def close_function():
    """
    Display a confirmation dialog and close the application if user confirms.

    This function:
    1. Displays a modal dialog with "OK" and "Cancel" buttons
    2. Asks the user to confirm quitting the application
    3. If user confirms ("OK"), terminates the application by destroying the main window
    4. If user cancels, returns without taking any action

    Returns:
        None
    """
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()


# Main window
window = tk.Tk()
window.geometry('700x840')
window.resizable(width=False, height=False)
window.title('Random Password Generator App')

window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=2)
window.columnconfigure(2, weight=1)
window.configure(bg='#DFE4E8')


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


# Style
style = ttk.Style(labelframe_generated_password)


# Labels

label_texts = {
    'title': 'Random Password Generator',
    'subtitle': 'A free tool to quickly create your password',
    'length': 'Length of generated password: ',
    'length_note': '(8 to 30 Chars)',
    'output': 'Password: ',
    'entropy': 'Total Entropy:',
    'strength': 'Strength: ',
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


label_show_strength = tk.Label(
    master=labelframe_generated_password,
    font=('Noto Sans', 12, 'bold'),
)
label_show_strength.grid(row=1, column=2)


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
    """Symbol (!?@#$%&*^~/|\:;.,\'\')""": tk.BooleanVar(),
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
    command=generate_passowrd_button_function,
)
button_generate_password.grid(row=6, column=1, pady=20, ipady=7, sticky='W')


button_save = tk.Button(
    master=labelframe_buttons, 
    text='Save Password',
    font=('Noto Sans', 10),
    command=save_function,
)
button_save.grid(row=0, column=0, ipadx=15, ipady=10)


button_copy_to_clipboard = tk.Button(
    master=labelframe_buttons, 
    text='Copy to clipboard',
    font=('Noto Sans', 10),
    command=copy_to_clipboard_function,
)
button_copy_to_clipboard.grid(row=0, column=1, ipadx=15, ipady=10)


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
button_about.grid(row=0, column=3, ipadx=25, ipady=10)


button_close = tk.Button(
    master=labelframe_buttons, 
    text='Close',
    font=('Noto Sans', 10),
    command=close_function)
button_close.grid(row=0, column=4, ipadx=23, ipady=10)


# ProgressBar
progress_var = tk.DoubleVar()
progressbar_generated_password = ttk.Progressbar(
    master=labelframe_generated_password,
    style='strength.Horizontal.TProgressbar',
    # variable=progress_var,
)
progressbar_generated_password.grid(row=1, column=1, padx=5, pady=10, sticky='SNEW') 


window.mainloop()
