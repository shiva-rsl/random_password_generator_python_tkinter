import tkinter as tk
from tkinter import ttk

list_of_generated_passwords = []


window = tk.Tk()


window.geometry('800x640')
window.resizable(width=False, height=False)
window.title('Random Password Generator App')


# Label
label_password_length = tk.Label(master=window, text='Length')
label_password_length.grid()

label_password_length_numbers = tk.Label(master=window, text='(6 to 64 Chars)')
label_password_length_numbers.grid()

label_random_password = tk.Label(master=window, text='Random password')
label_random_password.grid()

label_generated_password = tk.Label(master=window, background='yellow')
label_generated_password.grid()

label_password_strength = tk.Label(master=window, text='Password strength')
label_password_strength.grid()

label_showing_password_strength = tk.Label(master=window,)
label_showing_password_strength.grid()

label_password_quantity = tk.Label(master=window, text='Quantity')
label_password_quantity.grid()

label_password_quantity_numbers = tk.Label(master=window, text='(1-100 Passwords)')
label_password_quantity_numbers.grid()

label_command = tk.Label(master=window, text='')



# Entry
entry_pass_length = tk.Entry(master=window, )
entry_pass_length.grid()

entry_password_numbers = tk.Entry(master=window, )
entry_password_numbers.grid()


# Checkbox
checkbox_uppercase = tk.Checkbutton(master=window, text='Uppercase')
checkbox_uppercase.grid()

checkbox_lowercase = tk.Checkbutton(master=window, text='Lowercase')
checkbox_uppercase.grid()

checkbox_number = tk.Checkbutton(master=window, text='Number')
checkbox_uppercase.grid()

checkbox_symbol = tk.Checkbutton(master=window, text='Symbol')
checkbox_uppercase.grid()

checkbox_space = tk.Checkbutton(master=window, text='Space')
checkbox_uppercase.grid()



# Combobox
combobox_genereted_passwords = ttk.Combobox(master=window, values=list_of_generated_passwords)
combobox_genereted_passwords.set(' ')
combobox_genereted_passwords.grid()


# Spinbox
spinbox_password_quantity = tk.Spinbox(master=window, from_=1, to=100, width=20,relief='sunken')
spinbox_password_quantity.grid()


# Button
button_save = tk.Button(master=window, text='Save password')
button_save.grid()

image_of_key = tk.PhotoImage(file='./Pictures/key.png')
button_generate = tk.Button(master=window, text='Generate password(s)', background='yellow', activebackground='yellow', image=image_of_key)
button_generate.grid()

button_copy_to_clipboard = tk.Button(master=window, text='Copy to clipboard')
button_copy_to_clipboard.grid()

button_close = tk.Button(master=window, text='Close')
button_close.grid()

button_about = tk.Button(master=window, text='About')
button_about.grid()



window.mainloop()

