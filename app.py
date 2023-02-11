import tkinter as tk
root = tk.Tk()
root.attributes("-fullscreen", True)
WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()
label_font = "Calibri 24 bold"
small_label_font = "Calibri 14"
button_font = "Calibri 16"


def load_interface():
    frame.grid(rowspan=6, columnspan=6)
    start_button.grid_remove()
    start_label.grid_remove()
    quit_button.grid(column=3, columnspan=3, row=5)

    settings = tk.Button(text="Настройки", height=7, width=30, font=button_font)
    settings.grid(column=0, columnspan=3, row=5)

    watch_label = tk.Label(root, text="Просмотр", fg = "white", font=label_font)
    watch_label.grid(row=0, column=0, columnspan=6)

    temp_hum_sensors = tk.Button(text="Датчики температуры и влажности", height=7, width=30, font=button_font)
    temp_hum_sensors.grid(column=0, columnspan=2, row=1)
    soil_hum_sensors = tk.Button(text="Датчики влажности почвы", height=7, width=30, font=button_font)
    soil_hum_sensors.grid(column=2, columnspan=2, row=1)
    average_temp_hum = tk.Button(text="Средняя влажность и температура", height=7, width=30, font=button_font)
    average_temp_hum.grid(column=4, columnspan=2, row=1)

    handle_label = tk.Label(root, text="Управление", fg = "white", font=label_font)
    handle_label.grid(row=2, column=0, columnspan=6)

    fork_opener = tk.Button(text="Открыть/закрыть форточки", height=7, width=30, font=button_font)
    fork_opener.grid(column=0, columnspan=2, row=3)
    watering_opener = tk.Button(text="Открыть/закрыть полив бороздок", height=7, width=30, font=button_font)
    watering_opener.grid(column=2, columnspan=2, row=3)
    humidifier_opener = tk.Button(text="Открыть/закрыть систему общего увлажнения", height=7, width=50, font=button_font)
    humidifier_opener.grid(column=4, columnspan=2, row=3)


    current_fork_state_label = tk.Label(root, text="Текущее состояние: закрыты", fg = "white", font=small_label_font)
    current_fork_state_label.grid(row=4, column=0, columnspan=2)

    current_humidifier_state_label = tk.Label(root, text="Текущее состояние: закрыта", fg = "white", font=small_label_font)
    current_humidifier_state_label.grid(row=4, column=4, columnspan=2)


frame = tk.Frame(root, width=WIDTH, height=HEIGHT)
frame.grid(column=0, row=0, columnspan=3, rowspan=3)

start_button = tk.Button(root, text="Начать", height=7, width=30, font=button_font, command = load_interface)
start_button.grid(column=1, row=1)


quit_button = tk.Button(root, text="Выход", command=root.destroy, height=7, width=30, font=button_font)
quit_button.grid(column=1, row=2)


start_label = tk.Label(root, text="Автоматическая теплица", fg = "white", font=label_font)
start_label.grid(row=0, column=0, columnspan=3)

root.mainloop()
