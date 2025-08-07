import os
import re
import math
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from random_password_generator_CLI import *
from tkinter.filedialog import asksaveasfile


# Constants
FONT_LARGE = ('Noto Sans', 20)
FONT_MEDIUM = ('Noto Sans', 15)
FONT_NORMAL = ('Noto Sans', 12)
FONT_SMALL = ('Noto Sans', 10)
FONT_BOLD = ('Noto Sans', 12, 'bold')

COLOR_BACKGROUND = "#000000"
COLOR_FORGROUND = "#F0CF28"

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
buttons = {}
labels = {}


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


def get_spinbox_password_length() -> int | None:
    """
    Retrieve the password length form the spinbox.

    Returns:
        int: The selected password length.
    """
    return int(spinbox_password_length.get())


def is_valid_password_length(password_length: int) -> bool:
    """
    Checks if the password length is valid (between 8 and 30).

    Args:
        `password_length` (int): The length to validate.

    Returns:
        bool: True if valid, otherwise False.
    """
    return MIN_PASSWORD_LENGTH <= password_length <= MAX_PASSWORD_LENGTH


def set_password_length() -> None:
    """
    Sets the password length in the `password_option` dictionary if valid.
    Raises a ValueError if is invalid.

    Raises:
        ValueError: If the password length is invalid (e.g., below minimum or above maximum allowed).

    Side Effects:
        Updates global `password_option` if valid.

    Returns:
        None
    """
    password_length = get_spinbox_password_length()
    if not is_valid_password_length(password_length):
        raise ValueError
    password_option['password_length'] = password_length


def get_selected_password_length() -> int:
    """
    Evaluates the length of selected password from the combobox.
    
    Returns:
        int: Length of the selected password.
    """
    selection_password = combobox_generated_password.get()
    return len(selection_password)


def analyze_selected_password() -> dict:
    """
    Analyzes the selected password from the combobox and returns a dictionary of its features.

    Returns:
        dict: A dictionary indicating the presence of character types and password length.
    """
    
    selected_password = combobox_generated_password.get()
    length = get_selected_password_length()
    
    return {
        'password_length': length,
        'uppercase': bool(re.search(r"[A-Z]", selected_password)),
        'lowercase': bool(re.search(r"[a-z]", selected_password)),
        'digit': bool(re.search(r"[0-9]", selected_password)),
        'minus': bool(re.search(r"-", selected_password)),
        'underline': bool(re.search(r"_", selected_password)),
        'space': bool(re.search(r"\s", selected_password)),
        'symbol': bool(re.search(r"[!?@#$%&*^~/|:;.,'\"']", selected_password)),
        'bracket': bool(re.search(r"[{}\[\]()<>]", selected_password)),
    }


def calculate_password_range() -> int:
    """
    Calculates the total size of the character set based on selected password options.

    Returns:
        int: Total character set size for entropy calculation.
    """
    
    password_range = 0
    password_features = analyze_selected_password()
    
    for key, value in password_features.items():
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

    password_length = get_selected_password_length()

    password_pool_size = calculate_password_range()
    entropy = password_length * math.log2(password_pool_size)
    return entropy


def show_password_entropy(*args) -> None:
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
    labels['label_entropy_value'].config(text=f'{password_entropy_value:.2f} bits')


def evaluate_password_strength(password_entropy: float) -> dict:
    """
    Evaluates the strength of a password based on its entropy.

    Args:
        `password_entropy` (float): The entropy value of the password.

    Returns:
        dict: A dictionary containing the score, label and color representing the strength.
    """
    if password_entropy < 28:
        return {'score': 10, 'label': '🔴 Very Weak', 'color': STRENGTH_COLORS['very_weak']}
    elif password_entropy < 36:
        return {'score': 30, 'label': '🟠 Weak', 'color': STRENGTH_COLORS['weak']}
    elif password_entropy < 60:
        return {'score': 55, 'label': '🟡 Fair', 'color': STRENGTH_COLORS['fair']}
    elif password_entropy < 128:
        return {'score': 80, 'label': '🟣 Strong', 'color': STRENGTH_COLORS['strong']}
    else:
        return {'score': 100, 'label': '🟢 Perfect', 'color': STRENGTH_COLORS['perfect']}


def calculate_password_strength() -> tuple[int, str, str]:
    """
    Calculates the strength of a password.

    Returns:
        tuple: A tuple containing the `score` (int), `label` (str) and `color` (str) representing the password strength.
    """
    password_entropy = calculate_password_entropy()
    strength_date = evaluate_password_strength(password_entropy)
    return strength_date['score'], strength_date['label'], strength_date['color']


def update_password_strength_label() -> None:
    """
    Updates the password strength rating and its associated color in the GUI.

    Side Effects:
    1. Retrieves the strength level and color by calling `calculate_password_strength()`
    2. Updates the `label_show_strength` widget with:
       - Text: The strength level (e.g., "🔴 Very Weak")
       - Foreground color: The associated color code (e.g., "#f01010")

    Returns:
        None
    """
    _, strength_level, strength_color  = calculate_password_strength()
    labels['label_show_strength'].config(text=strength_level, fg=strength_color)


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
    combobox_generated_password.config(values=password_list)
    combobox_generated_password.set(password_list[-1])


def show_password_strength_in_progressbar() -> None:
    """
    Updates the password strength progress bar's value and color based on password entropy.
    
    Side Effects:
        - Calls `calculate_password_entropy()` to compute the entropy of the current password.
        - Updates the progress bar value and color to visually reflect password strength.
        
    Returns:
        None
    """
    strength, _, color = calculate_password_strength()
    
    style.configure('strength.Horizontal.TProgressbar', background=color)
    progressbar_generated_password.config(value=strength)


def update_password_strength_display(*args) -> None:
    """
    Updates the entire password strength view, including:
        - Entropy display
        - Strength label
        - Progress bar
    """
    show_password_entropy()
    update_password_strength_label()
    show_password_strength_in_progressbar()


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

    try: 
        set_password_length()

        get_password_options_from_user()

        generate_password()
        
        show_generated_password_in_combobox()

        update_password_strength_display()

    except IndexError:
        show_checkbox_error_message()
    
    except ValueError:
        show_invalid_password_length_message()


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
            file.write("\n".join(password_list))
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
    labels['label_guidance_text'].config(
        text='Password copied!', 
        fg="#066A10"
    )
    window.after(2000, lambda: labels['label_guidance_text'].config(text=''))


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
    combobox_generated_password.config(values=())
    labels['label_entropy_value'].config(text='')
    labels['label_show_strength'].config(text='')
    progressbar_generated_password.config(value=0)


def toggle_about_text() -> None:
    """
    Displays or toggles the application description in the `label_guidance_text`.

    Side Effects:
        - Shows `ABOUT_TEXT` in black if the label is empty
        - Clears the Label if it already contains text
    """
    if not labels['label_guidance_text']['text'].strip():
        labels['label_guidance_text'].config(text=ABOUT_TEXT, fg=COLOR_BACKGROUND)
    else:
        labels['label_guidance_text'].config(text='')


def close_app() -> None:
    """
    Displays a confirmation dialog and closes the application if user confirms.
    """
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()


def _create_label(master, font, text=None, background=None, foreground=None, **grid_options):
    """
    Creates label widgets with the given options.

    Args:
        master (tk.Widget): The parent widget.
        font (tuple): Font settings for the label.
        text (str, optional): Text to display on the label.
        background (str, optional): Background color.
        foreground (str, optional): Text color (foreground).
        **grid_options: Additional keyword arguments for grid placement.

    Returns:
        tk.Label: The created Label widget.
    """
    
    label = tk.Label(
        master=master,
        text=text,
        font=font,
        background=background,
        foreground=foreground,
    )
    label.grid(**grid_options)
    return label


def _create_button(master, text, command, font=FONT_SMALL, background=None, activebackground=None, anchor=None, **grid_options):
    """
    Creates button widgets with the given options.

    Args:
        master (tk.Widget): The parent widget.
        text (str): Text to display on the button.
        command (function): The function to call when the button is clicked.
        font (tuple): Font settings for the button. Defaults to FONT_SMALL.
        background (str, optional): Background color.
        activebackground (str, optional): Background color when active.
        anchor (str, optional): Text alignment inside the button (e.g., 'w', 'center').
        **grid_options: Additional keyword arguments for grid placement.

    Returns:
        tk.Button: The created button widget.
    """
    button = tk.Button(
        master=master,
        text=text,
        command=command,
        font=font,
        background=background,
        activebackground=activebackground,
        anchor=anchor,
    )
    button.grid(**grid_options)
    return button


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
    font=FONT_LARGE,
)
labelframe_settings.grid(row=2, column=0, columnspan=5, padx=(10, 10), pady=(10, 0), sticky='EW')

labelframe_settings.columnconfigure(0, weight=1)
labelframe_settings.columnconfigure(1, weight=1)
labelframe_settings.columnconfigure(2, weight=1)


labelframe_generated_password = tk.LabelFrame(
    master=window,
    text='Generated Password(s)',
    font=FONT_LARGE,
)
labelframe_generated_password.grid(row=3, column=0, ipadx=120, ipady=5, padx=(10, 10), pady=(10, 10))


labelframe_buttons = tk.LabelFrame(
    master=window,
)
labelframe_buttons.grid(row=4, column=0, ipadx=15, ipady=0, padx=(10, 10), pady=(5, 10))


# Style
style = ttk.Style(labelframe_generated_password)


# Labels

label_configs = [
    {
        'name': 'label_title',
        'master': window,
        'text': 'Random Password Generator',
        'font': FONT_LARGE,
        'background': COLOR_BACKGROUND,
        'foreground': COLOR_FORGROUND,
        'grid': {'row':0, 'column':0, 'columnspan':5, 'ipadx':250, 'ipady':15, 'sticky':'NSEW'},
    },
    {
        'name': 'label_subtitle',
        'master': window,
        'text': 'A free tool to quickly create your password',
        'font': FONT_NORMAL,
        'background': COLOR_BACKGROUND,
        'foreground': COLOR_FORGROUND,
        'grid': {'row':1, 'column':0, 'columnspan':5, 'ipady':5, 'sticky':'NEW',},
    },
    {
        'name': 'label_password_length',
        'master': labelframe_settings,
        'text': 'Length of generated password: ',
        'font': FONT_SMALL,
        'grid': {'row':0, 'column':0, 'padx':(30, 0), 'pady':(30, 30), 'sticky':'w'},
    },
    {
        'name': 'label_password_length_numbers',
        'master': labelframe_settings,
        'text': '(8 to 30 Chars)',
        'font': FONT_SMALL,
        'grid': {'row':0, 'column':2, 'padx':(0, 80), 'pady':(30, 30), 'sticky':'w'},
    },
    {
        'name': 'label_random_password',
        'master': labelframe_generated_password,
        'text': 'Password: ',
        'font': FONT_MEDIUM,
        'grid': {'row':0, 'column':0, 'padx':20, 'pady':30, 'sticky':'E'},
    },
    {
        'name': 'label_password_strength',
        'master': labelframe_generated_password,
        'text': 'Strength: ',
        'font': FONT_SMALL,
        'grid': {'row':1, 'column':0, 'pady':10},
    },
    {
        'name': 'label_show_strength',
        'master': labelframe_generated_password,
        'font': FONT_BOLD,
        'grid': {'row':1, 'column':2,},

    },
    {
        'name': 'label_entropy_calc',
        'master': labelframe_generated_password,
        'text': 'Total Entropy:',
        'font': FONT_SMALL,
        'grid': {'row':2, 'column':0, 'pady':10},
    },
    {
        'name': 'label_entropy_value',
        'master': labelframe_generated_password,
        'font': FONT_BOLD,
        'grid': {'row':2, 'column':1, 'sticky':'w'},
    },
    {
        'name': 'label_guidance_text',
        'master': window,
        'font': FONT_SMALL,
        'background': "#DFE4E8",
        'grid': {'row':9, 'column':0, 'columnspan':3,},
    },
]


for config in label_configs:
    label = _create_label(
        master=config['master'],
        font=config['font'],
        text=config.get('text'),
        background=config.get('background'),
        foreground=config.get('foreground'),
        **config['grid']
    )
    labels[config['name']] = label


# Combobox
var = tk.StringVar()
combobox_generated_password = ttk.Combobox(
    master=labelframe_generated_password,
    width=28,
    font=FONT_MEDIUM,
    values=password_list,
    textvariable=var,
)
combobox_generated_password.grid(row=0, column=1, padx=5)
combobox_generated_password.bind("<<ComboboxSelected>>", update_password_strength_display)


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

button_configs = [
    {
        'name': 'button_generate_password',
        'master': labelframe_settings,
        'text': 'Generate Password',
        'command': on_generate_password_click,
        'background': 'yellow', 
        'activebackground': 'yellow',
        'anchor': 'center',
        'grid': {'row':6, 'column':1, 'pady':20, 'ipady':7, 'sticky':'W'}
    },
    {
        'name': 'button_save',
        'master': labelframe_buttons,
        'text': 'Save Password',
        'command': handle_save_password,
        'grid': {'row':0, 'column':0, 'ipadx':15, 'ipady':10}
    },
    {
        'name': 'button_copy_to_clipboard',
        'master': labelframe_buttons,
        'text': 'Copy to clipboard',
        'command': copy_to_clipboard,
        'grid': {'row':0, 'column':1, 'ipadx':15, 'ipady':10}
    },
    {
        'name': 'button_clear',
        'master': labelframe_buttons,
        'text': 'Clear',
        'command': reset_password_ui,
        'grid': {'row':0, 'column':2, 'ipadx':25, 'ipady':10}
    },
    {
        'name': 'button_about',
        'master': labelframe_buttons,
        'text': 'About',
        'command': toggle_about_text,
        'grid': {'row':0, 'column':3, 'ipadx':25, 'ipady':10}
    },
    {
        'name': 'button_close',
        'master': labelframe_buttons,
        'text': 'Close',
        'command': close_app,
        'grid': {'row':0, 'column':4, 'ipadx':23, 'ipady':10}
    },
]


for config in button_configs:
    button = _create_button(
        master=config['master'],
        text=config['text'],
        command=config['command'],
        background=config.get('background'),
        activebackground=config.get('activebackground'),
        anchor=config.get('anchor'),
        **config['grid'],
    )
    buttons[config['name']] = button


# ProgressBar
progress_var = tk.DoubleVar()
progressbar_generated_password = ttk.Progressbar(
    master=labelframe_generated_password,
    style='strength.Horizontal.TProgressbar',
    # variable=progress_var,
)
progressbar_generated_password.grid(row=1, column=1, padx=5, pady=10, sticky='SNEW') 


window.mainloop()
