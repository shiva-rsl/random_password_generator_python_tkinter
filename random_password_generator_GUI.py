import os
import re
import math
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from random_password_generator_CLI import *
from tkinter.filedialog import asksaveasfile


DEFAULT_TEXT_COLOR = "#000000"
ABOUT_TEXT = '''The Random Password Generator enables you to generate secure and highly
    unpredictable passwords through an optional mix of lowercase and uppercase letters,
    numbers and special characters.'''
STRENGTH_COLORS = {
    'very_weak': "#f01010",
    'weak': "#ed761c",
    'fair': "#EFE63E",
    'strong': "#e52bf2",
    'perfect': "#06be06"
}
PASSWORD_OPTION_RANGE_SIZE = {    
    'uppercase': 26, 
    'lowercase': 26, 
    'digit': 10, 
    'minus': 1, 
    'underline': 1, 
    'space': 1, 
    'symbol': 19, 
    'bracket': 8, 
}


checkbox_variables = []
password_option = {}
password_list = []


# Functions

def clear_screen() -> None:
    """
    Clears the terminal screen.

    Uses 'cls' command on Windows and 'clear' on Unix-based systems.
    If the command fails, it prints multiple newlines as a fallback.
    """
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except Exception:
        print('\n' * 100)

clear_screen()


def show_checkbox_error_message() -> None:
    """
    shows an error popup if user has not checked any checkboxes.
    """
    messagebox.showinfo('Error', 'Please check at lease one checkbox to proceed.')


def show_invalid_password_length_message() -> None:
    """
    Displays an error popup if the password length is not valid.
    """
    messagebox.showinfo(
        'Error', 
        f'Password length must be between {MIN_PASSWORD_LENGTH} and {MAX_PASSWORD_LENGTH} characters.'
    )


def is_valid_password_length(password_length: int) -> bool:
    """
    Checks if the password length is valid (between 8 and 30).

    Args:
        `password_length` (int): The length to validate.

    Returns:
        bool: True if valid, otherwise False.
    """
    return MIN_PASSWORD_LENGTH <= password_length <= MAX_PASSWORD_LENGTH


def set_password_length(password_length: int) -> None:
    """
    Sets the password length in the `password_option` dictionary if valid.
    Shows an error message if invalid.

    Args:
        `password_length` (int): The length to set.

    Side Effects:
        Updates global `password_option` if valid.
        Shows an error message if invalid.

    Returns:
        None
    """
    if is_valid_password_length(password_length):
        password_option['password_length'] = password_length
    else:
        show_invalid_password_length_message()


def calculate_password_range() -> int:
    """
    Calculates the total size of the character set based on selected password options.

    Returns:
        int: Total character set size for entropy calculation.
    """
    
    password_range = 0

    for key, value in password_option.items():
        if key == 'password_length':
            continue
        if value:
            password_range += PASSWORD_OPTION_RANGE_SIZE.get(key, 0)

    return password_range


def calculate_password_entropy() -> float:
    """
    Calculates the entropy of a password based on its length and character diversity.

    The entropy is calculated using the formula: 
        entropy = length * log2(character_pool_size)
    where `character_pool_size` is determined by `calculate_password_range()`.

    Returns:
        float: The calculated password entropy in bits. A higher value indicates a stronger password.
    """
    selection_password = var.get()
    password_length = len(selection_password)
    password_pool_size = calculate_password_range()
    entropy = password_length * math.log2(password_pool_size)
    return entropy


def show_password_entropy() -> None:
    """
    Calculates and displays the password entropy in the GUI label.

    Side Effects:
        - Calls `calculate_password_entropy()` to compute the entropy
        - Formats the result to 2 decimal places
        - Updates the text of `label_entropy_value` with the result

    Returns:
        None
    """
    password_entropy_value = calculate_password_entropy()
    label_entropy_value['text'] = f'{password_entropy_value:.2f} bits'


def strength_password_calculation() -> tuple[str, str]:
    """
    Evaluates password strength based on its entropy and returns a rating with color coding.

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

    password_entropy = calculate_password_entropy()
    
    if password_entropy < 28:
        return '🔴 Very Weak', STRENGTH_COLORS['very weak']
    elif password_entropy < 36:
        return '🟠 Weak', STRENGTH_COLORS['weak']
    elif password_entropy < 60:
        return '🟡 Fair', STRENGTH_COLORS['fair']
    elif password_entropy < 128:
        return '🟣 Strong', STRENGTH_COLORS['strong']
    else:
        return '🟢 Perfect', STRENGTH_COLORS['perfect']


def show_password_strength() -> None:
    """
    Displays the password strength rating and its associated color in the GUI.

    Side Effects:
    1. Retrieves the strength level and color by calling `strength_password_calculation()`
    2. Updates the `label_show_strength` widget with:
       - Text: The strength level (e.g., "🔴 Very Weak")
       - Foreground color: The associated color code (e.g., "#f01010")

    Returns:
        None
    """
    strength_level, strength_color  = strength_password_calculation()
    label_show_strength['text'] = strength_level
    label_show_strength['fg'] = strength_color


def get_password_options_from_user() -> None:
    """
    Updates the global `password_option` dictionary based on the current user-selected checkbox values.


    Side Effects:
        - Modifies the global `password_option` dictionary by extracting checkbox states from `checkbox_options`.
    
    Returns:
        None
    """
    for _, (key, value) in enumerate(checkbox_options.items()):
        checkbox_name = re.sub(r'\s\(.*\)', '', key)
        password_option[checkbox_name.lower()] = value.get()


def generate_password() -> None:
    """
    Generates a random password based on the options selected by the user.

    Side Effects:
        - Calls the `random_password_generator()` to generate password.
        - Appends the generated password to the global `password_list`.

    Returns:
        None
    """
    generated_password = random_password_generator(password_option)
    password_list.append(generated_password)


def show_generated_password_in_combobox() -> None:
    """
    Displays the list of generated passwords in the combobox widget.
    
    Side Effects:
        - Updates the values of `combobox_generated_password` with the current `password_list`.
        - Sets the combobox selection to the most recently generated password.

    Returns:
        None
    """
    combobox_generated_password['values'] = password_list
    combobox_generated_password.set(password_list[-1])


def password_strength_calculation(entropy: float) -> tuple[int, str]:
    """
    Calculates the password strength score and corresponding color based on entropy.

    Args:
        entropy (float): The entropy value of the password.

    Returns:
        tuple[int, str]: A tuple containing the strength score (as an integer) 
        and the associated color code (as a hex string).
    """

    if entropy < 28:
        return 10, STRENGTH_COLORS['very weak']
    elif entropy < 36:
        return 30, STRENGTH_COLORS['weak']
    elif entropy < 60:
        return 55, STRENGTH_COLORS['fair']
    elif entropy < 128:
        return 80, STRENGTH_COLORS['strong']
    else:
        return 100, STRENGTH_COLORS['perfect']


def update_password_strength_progressbar() -> None:
    """
    Updates the password strength progress bar's value and color based on password entropy.
    
    Side Effects:
        - Calls `calculate_password_entropy()` to compute the entropy of the current password.
        - Updates the progress bar value and color to visually reflect password strength.
        
    Returns:
        None
    """
    entropy = calculate_password_entropy()
    strength, color = password_strength_calculation(entropy)
    
    style.configure('strength.Horizontal.TProgressbar', background=color)
    progressbar_generated_password['value'] = strength


def on_generate_password_click() -> None:
    """
    Handles the event triggered by the 'Generate Password' button.

    Steps performed:
        1. Retrives and validates the user_specified password length.
        2. Updates `password_option` based on user selections.
        3. Generates a password using the specified options.
        4. Displays the generated password in the combobox.
        5. Shows the password entropy.
        6. Shows the textual strength indicator.
        7. Updates the progress bar based on password strength.
    
    Handles:
        - IndexError by showing a checkbox selection error message.

    Returns:
        None
    """
    password_length = int(spinbox_password_length.get())

    try: 
        set_password_length(password_length)

        get_password_options_from_user()

        generate_password()
        
        show_generated_password_in_combobox()
        
        show_password_entropy()

        show_password_strength()

        update_password_strength_progressbar()
        

    except IndexError:
        show_checkbox_error_message()


def save_password_to_file(password: str) -> None:
    """
    Prompts the user with a file save dialog and writes the given password.
    
    Args:
        password (str): The password to save.

    Side Effects:
        - Opens a file dialog to select the save location.
        - Writes the password content to the selected file.

    Returns:
        None
    """

    file = asksaveasfile(
            mode='w', 
            title='Save Passwords', 
            filetypes=[('Text Document','*.txt'), ('All Files', '*.*')], 
            defaultextension='.txt', 
        )

    if file:
        try:
            file.write(password)
        finally:
            file.close()


def show_save_error_if_empty(password: str) -> bool:
    """
    Validates if a password is available for saving.
    
    Args:
        password (str): The password to validate.

    Side Effects:
        Shows a messagebox if the password is empty.

    Returns:
        bool: True if a password exists, False otherwise.
    """
    if not password:
        messagebox.showinfo('Error', 'There is nothing to be saved!')
        return False
    return True


def handle_save_password() -> None:
    """
    Validates and saves the generated password to a user-specified file.
    
    Side Effects:
        Shows error popup if no password is availabel.
        Opens a file dialog for saving the password.

    Return:
        None
    """
    generated_password = var.get()
    if show_save_error_if_empty(generated_password):
        save_password_to_file(generate_password)
    

def show_copy_error_if_empty(generated_password: str) -> bool:
    """
    Checks if the generated password is empty. if so, shows an error messagebox.
    
    Args:
        `generated_password` (str): The password string to check.

    Side Effects:
        Displays a messagebox if the password is empty.

    Returns:
        bool: True if an error was shown, False otherwise.
    """
    if not generated_password:
        messagebox.showinfo('Error', 'There is nothing to be copied!')
        return True
    return False


def show_copy_message() -> None:
    """
    Displays a confirmation message 'Password copied!' in `label_guidance_text`,
    then clears the message after 2 seconds.

    Side Effects:
        - Modifies the label text of `label_guidance_text`.
        - Uses `after()` to clear it after 2 seconds.

    Returns:
        None
    """
    label_guidance_text.config(
        text='Password copied!', 
        fg="#066A10"
    )
    window.after(2000, lambda: label_guidance_text.config(text=''))


def copy_to_clipboard() -> None:
    """
    Copies the generated password to clipboard.
    Shows an error if password is empty.

    Side Effects:
        - Displays an error popup if the password is empty.
        - Copies the password to the system clipboard.
        - Updates the `label_guidance_text` to show a confirmation message.

    Returns:
        None
    """
    generated_password = var.get()

    if show_copy_error_if_empty(generated_password):
        return
    
    labelframe_generated_password.clipboard_clear()
    labelframe_generated_password.clipboard_append(generated_password)
    
    show_copy_message()


def reset_password_ui() -> None:
    """
    Resets all password-related GUI elements to their default empty state.

    Side Effects:
        - Clears the global `password_list`
        - Resets the password combobox (current selection and dropdown values)
        - Clears the entropy value display
        - Resets the strength indicator text
        - Sets the progress bar to 0

    Returns:
        None
    """
    global password_list
    password_list.clear()
    combobox_generated_password.set('')
    combobox_generated_password['values'] = ()
    label_entropy_value['text'] = ''
    label_show_strength['text'] = ''
    progressbar_generated_password['value'] = 0


def toggle_about_text() -> None:
    """
    Displays or toggles the application description in the `label_guidance_text`.

    Side Effects:
        - Shows `ABOUT_TEXT` in black if the label is empty
        - Clears the Label if it already contains text
    """
    if not label_guidance_text['text'].strip():
        label_guidance_text.config(text=ABOUT_TEXT, fg=DEFAULT_TEXT_COLOR)
    else:
        label_guidance_text.config(text='')


def close_app() -> None:
    """
    Displays a confirmation dialog and closes the application if user confirms.
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
    values=password_list,
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
    command=on_generate_password_click,
)
button_generate_password.grid(row=6, column=1, pady=20, ipady=7, sticky='W')


button_save = tk.Button(
    master=labelframe_buttons, 
    text='Save Password',
    font=('Noto Sans', 10),
    command=handle_save_password,
)
button_save.grid(row=0, column=0, ipadx=15, ipady=10)


button_copy_to_clipboard = tk.Button(
    master=labelframe_buttons, 
    text='Copy to clipboard',
    font=('Noto Sans', 10),
    command=copy_to_clipboard,
)
button_copy_to_clipboard.grid(row=0, column=1, ipadx=15, ipady=10)


button_clear = tk.Button(
    master=labelframe_buttons, 
    text='Clear',
    font=('Noto Sans', 10),
    command=reset_password_ui,
)
button_clear.grid(row=0, column=2, ipadx=25, ipady=10)


button_about = tk.Button(
    master=labelframe_buttons, 
    text='About',
    font=('Noto Sans', 10),
    command=toggle_about_text,
)
button_about.grid(row=0, column=3, ipadx=25, ipady=10)


button_close = tk.Button(
    master=labelframe_buttons, 
    text='Close',
    font=('Noto Sans', 10),
    command=close_app)
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
