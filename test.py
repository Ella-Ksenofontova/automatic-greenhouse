import tkinter as tk
root = tk.Tk()
root.attributes("-fullscreen", True)
WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()
label_font = "Calibri 24 bold"
button_font = "Calibri 16"

def load_interface():
    pass



frame = tk.Frame(root, width=WIDTH, height=HEIGHT)
frame.grid(column=0, row=0, columnspan=3, rowspan=3)

start_button = tk.Button(root, text="Начать", height=7, width=30, font=button_font, command = load_interface)
start_button.grid(column=1, row=1)


quit_button = tk.Button(root, text="Выход", command=root.destroy, height=7, width=30, font=button_font)
quit_button.grid(column=1, row=2)


start_label = tk.Label(root, text="Автоматическая теплица", fg = "white", font=label_font)
start_label.grid(row=0, column=0, columnspan=3)

