import tkinter as tk

window = tk.Tk()


window.geometry('800x640')
window.resizable(width=False, height=False)
window.title('Random Password Generator App')

# Label
label_pass_length = tk.Label(master=window, text='Length')
label_pass_length.grid()


# Entry
entry_pass_length = tk.Entry(master=window, )
entry_pass_length.grid()


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


# Button
button_save = tk.Button(master=window, text='Save password')
button_save.grid()

button_generate = tk.Button(master=window, text='Generate')
button_generate.grid()




window.mainloop()

