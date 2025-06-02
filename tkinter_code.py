import tkinter as tk
from tkinter import ttk
from tkinter import E,W,S,N


# Main window
window = tk.Tk()
window.geometry('700x660')
window.resizable(width=False, height=False)
window.title('Random Password Generator App')

window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=2)
window.columnconfigure(2, weight=1)


# LabelFrame
labelframe_settings = tk.LabelFrame(
    master=window, 
    text='Password settings', 
    font=('Noto Sans', 20, )
)
labelframe_settings.grid(row=2, column=0, columnspan=50, padx=(10, 10), pady=(20, 100), sticky='EW')

labelframe_settings.columnconfigure(0, weight=1)
labelframe_settings.columnconfigure(1, weight=1)
labelframe_settings.columnconfigure(2, weight=1)
labelframe_settings.columnconfigure(3, weight=1)
labelframe_settings.columnconfigure(4, weight=1)


# Labels

label_title = tk.Label(
    master=window, 
    text="Random Password Generator", 
    background='black', 
    foreground='yellow', 
    font=('Noto Sans', 20)
)
label_title.grid(row=0, column=0, columnspan=50, ipadx=250, ipady=15, sticky='NSEW')


label_title_definition = tk.Label(
    master=window,
    text='A free tool to quickly create your password',
    background='black', 
    foreground='yellow', 
    font=('Noto Sans', 12),
)
label_title_definition.grid(row=1, column=0, columnspan=50, ipady=5, sticky='NEW')


label_password_length_numbers = tk.Label(
    master=labelframe_settings, 
    text='Length of generated password',
    font=('Noto Sans', 10)
)
label_password_length_numbers.grid(row=0, column=0, pady=(20, 0),)

# label_password_length_numbers = tk.Label(master=window, text='(6 to 64 Chars)')
# label_password_length_numbers.grid()

# label_symbol = tk.Label(master=window, text='(!@#$%^&*<>+=)')
# label_symbol.grid()

# label_random_password = tk.Label(master=window, text='Random password')
# label_random_password.grid()

# label_generated_password = tk.Label(master=window, background='yellow')
# label_generated_password.grid()

# label_password_strength = tk.Label(master=window, text='Password strength')
# label_password_strength.grid()

# label_showing_password_strength = tk.Label(master=window,)
# label_showing_password_strength.grid()

# label_password_quantity = tk.Label(master=window, text='Quantity')
# label_password_quantity.grid()

label_password_quantity_numbers = tk.Label(
    master=labelframe_settings, 
    text='(1-100 Passwords)',
    font=('Noto Sans', 10),
)
label_password_quantity_numbers.grid(row=0, column=2, pady=(20, 0), padx=(0, 0), sticky='w')

# label_include_user_charatcers = tk.Label(master=window, text='Also include the following charatcers:')
# label_include_user_charatcers.grid()



# Entries
# entry_pass_length = tk.Entry(master=window, )
# entry_pass_length.grid()

# entry_password_numbers = tk.Entry(master=window, )
# entry_password_numbers.grid()

# entry_include_user_characters = tk.Entry(master=window, )
# entry_include_user_characters.grid()


# Checkboxs

checkbox_uppercase = tk.Checkbutton(
    master=labelframe_settings, 
    text=' Uppercase (A, B, C, ...)', 
    font=('Noto Sans', 10),
)
checkbox_uppercase.grid(row=1, column=0, padx=(45, 0), pady=(35, 0), sticky='w')

checkbox_lowercase = tk.Checkbutton(
    master=labelframe_settings, 
    text=' Lowercase (a, b, c, ...)',
    font=('Noto Sans', 10),
)
checkbox_lowercase.grid(row=2, column=0, padx=(45, 0), pady=(15, 0), sticky='w')

checkbox_digit = tk.Checkbutton(
    master=labelframe_settings, 
    text=' Digits (0, 1, 2, ...)',
    font=('Noto Sans', 10),
)
checkbox_digit.grid(row=1, column=1, padx=(45, 0), pady=(35, 0), sticky='W')

checkbox_minus = tk.Checkbutton(
    master=labelframe_settings, 
    text=' Minus (-)',
    font=('Noto Sans', 10),
)
checkbox_minus.grid(row=3, column=1, padx=(45, 0), pady=(15, 0), sticky='W')

checkbox_underline = tk.Checkbutton(
    master=labelframe_settings, 
    text=' Underline (_)', 
    font=('Noto Sans', 10),
)
checkbox_underline.grid(row=2, column=1, padx=(45, 0), pady=(15, 0), sticky='W')

checkbox_space = tk.Checkbutton(
    master=labelframe_settings, 
    text=' Space ()',
    font=('Noto Sans', 10),
)
checkbox_space.grid(row=4, column=1, padx=(45, 0), pady=(15, 0), sticky='W')

checkbox_symbol = tk.Checkbutton(
    master=labelframe_settings, 
    text=' Symbol ( !@#$%^&*<>+= )',
    font=('Noto Sans', 10),
)
checkbox_symbol.grid(row=3, column=0, padx=(45, 0), pady=(15, 0), sticky='w')

checkbox_brackets = tk.Checkbutton(
    master=labelframe_settings, 
    text=' Brackets ([, ], {, }, (, ), <, >)',
    font=('Noto Sans', 10),
)
checkbox_brackets.grid(row=4, column=0, padx=(45, 0), pady=(15, 0), sticky='w')



# Comboboxes
# combobox_genereted_passwords = ttk.Combobox(master=window)
# combobox_genereted_passwords.set(' ')
# combobox_genereted_passwords.grid()


# Spinbox

spinbox_password_quantity = tk.Spinbox(
    master=labelframe_settings, 
    from_=1, 
    to=100, 
    width=20,
    relief='sunken',
)
spinbox_password_quantity.grid(row=0, column=1, pady=(20, 0), padx=(0, 0), sticky='E', ipadx=10, ipady=5)


# Buttons
# button_save = tk.Button(master=window, text='Save password')
# button_save.grid()

# # image_of_key = tk.PhotoImage(file='./Pictures/key.png')
# # button_generate = tk.Button(master=window, text='Generate password(s)', background='yellow', activebackground='yellow', image=image_of_key)
# # button_generate.grid()

# button_copy_to_clipboard = tk.Button(master=window, text='Copy to clipboard')
# button_copy_to_clipboard.grid()

button_close = tk.Button(master=window, text='Close', command=window.destroy)
button_close.grid(row=20, column=5, padx=100, pady=55, ipadx=20, ipady=5, sticky=(tk.E))

# button_about = tk.Button(master=window, text='About')
# button_about.grid()



# ProgressBar
progressbar_generated_password = ttk.Progressbar()
# progressbar_generated_password.grid() 



window.mainloop()

