import tkinter as tk

parameters = open("parameters.txt", "r")
max_average_temperature = parameters.readline()
max_average_humidity = parameters.readline()
max_humidity_in_notch = parameters.readline()  # notch переводится как "бороздка"
parameters.close()

root = tk.Tk()
root.attributes("-fullscreen", True)
WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()
label_font = "Calibri 24 bold"
small_label_font = "Calibri 14 bold"
button_font = "Calibri 16"
settings_root = None
emergency_mode = False


def open_settings():
    global settings_root
    settings_root = tk.Tk()
    settings_root.attributes("-fullscreen", True)
    settings_frame = tk.Frame(settings_root, height=HEIGHT, width=WIDTH, bg="#008000")
    settings_frame.grid(row=0, column=0, rowspan=6, columnspan=2)

    settings_quit_button = tk.Button(settings_root, text="Назад", bg="white", height=7, width=30, font=button_font,
                                     command=settings_root.destroy)
    settings_quit_button.grid(row=5, column=1)

    settings_label = tk.Label(settings_root, text="Настройки", fg="white", font=label_font, bg="#008000")
    settings_label.grid(row=0, column=0, columnspan=2)

    temperature_label = tk.Label(settings_root, text="Температура, при которой возможно открытие форточек (°C)",
                                 fg="white", font=small_label_font, bg="#008000")
    humidity_label = tk.Label(settings_root, text="Влажность, при которой возможно открытие системы увлажнения (%)",
                              fg="white", font=small_label_font, bg="#008000")
    average_humidity_label = tk.Label(settings_root, text="Влажность в бороздке, при которой возможен её полив(%)",
                                      fg="white", font=small_label_font, bg="#008000")
    labels = [temperature_label, humidity_label, average_humidity_label]

    for i in range(3):
        labels[i].grid(row=i + 1, column=0, sticky=tk.E, padx=25)

    temperature_entry = tk.Entry(settings_root, width=50)
    humidity_entry = tk.Entry(settings_root, width=50)
    humidity_in_notch_entry = tk.Entry(settings_root, width=50)

    entries = [temperature_entry, humidity_entry, humidity_in_notch_entry]
    default_text = [max_average_temperature, max_average_humidity, max_humidity_in_notch]

    for i in range(3):
        entries[i].grid(row=i + 1, column=1, sticky=tk.W)
        entries[i].insert(0, default_text[i])

    save_button = tk.Button(settings_root, text="Сохранить", bg="white", height=7, width=30, font=button_font,
                            command=save)
    save_button.grid(row=5, column=0)

    text_for_emergency_button = "Включить экстренный режим"
    emergency_mode_button = tk.Button(settings_root, text=text_for_emergency_button, bg="white", height=4,
                                      width=30, font=button_font, command=switch_emergency_mode)
    emergency_mode_button.grid(row=4, column=0, columnspan=2)


def save():
    children = settings_root.winfo_children()
    temperature_entry = children[6]
    humidity_entry = children[7]
    humidity_in_notch_entry = children[8]

    new_temperature = temperature_entry.get()
    new_humidity = humidity_entry.get()
    new_humidity_in_notch = humidity_in_notch_entry.get()

    try:
        new_temperature, new_humidity, new_humidity_in_notch = map(float, [new_temperature, new_humidity,
                                                                           new_humidity_in_notch])
        global max_average_temperature, max_average_humidity, max_humidity_in_notch
        is_different = (new_temperature != max_average_temperature or new_humidity != max_average_humidity
                        or new_humidity_in_notch != max_humidity_in_notch)
        if is_different:
            to_write = [new_temperature, new_humidity, new_humidity_in_notch]
            parameters = open("parameters.txt", "w")
            for i in to_write:
                parameters.write(str(i) + "\n")
            show_success()
            parameters.close()

    except ValueError:
        show_error()


def switch_emergency_mode():
    global emergency_mode
    emergency_mode = not emergency_mode

    emergency_button = settings_root.winfo_children()[10]
    if emergency_mode:
        emergency_button.configure(text="Выключить экстренный режим")
    else:
        emergency_button.configure(text="Включить экстренный режим")


def load_interface():
    frame.grid(rowspan=6, columnspan=6)
    start_button.grid_remove()
    start_label.grid_remove()
    quit_button.grid(column=3, columnspan=3, row=5)

    settings = tk.Button(text="Настройки", height=7, width=30, font=button_font, bg="white", command=open_settings)
    settings.grid(column=0, columnspan=3, row=5)

    watch_label = tk.Label(root, text="Просмотр", fg="white", font=label_font, bg="#008000")
    watch_label.grid(row=0, column=0, columnspan=6)

    temp_hum_sensors = tk.Button(text="Датчики температуры и влажности", height=7, width=30, font=button_font,
                                 bg="white")
    temp_hum_sensors.grid(column=0, columnspan=2, row=1)
    soil_hum_sensors = tk.Button(text="Датчики влажности почвы", height=7, width=30, font=button_font, bg="white")
    soil_hum_sensors.grid(column=2, columnspan=2, row=1)
    average_temp_hum = tk.Button(text="Средняя влажность и температура", height=7, width=30, font=button_font,
                                 bg="white")
    average_temp_hum.grid(column=4, columnspan=2, row=1)

    handle_label = tk.Label(root, text="Управление", fg="white", font=label_font, bg="#008000")
    handle_label.grid(row=2, column=0, columnspan=6)

    fork_opener = tk.Button(text="Открыть/закрыть форточки", height=7, width=30, font=button_font, bg="white")
    fork_opener.grid(column=0, columnspan=2, row=3)
    watering_opener = tk.Button(text="Открыть/закрыть полив бороздок", height=7, width=30, font=button_font, bg="white")
    watering_opener.grid(column=2, columnspan=2, row=3)
    humidifier_opener = tk.Button(text="Открыть/закрыть систему общего увлажнения", height=7, width=50,
                                  font=button_font, bg="white")
    humidifier_opener.grid(column=4, columnspan=2, row=3)

    current_fork_state_label = tk.Label(root, text="Текущее состояние: закрыты", fg="white", font=small_label_font,
                                        bg="#008000")
    current_fork_state_label.grid(row=4, column=0, columnspan=2)

    current_humidifier_state_label = tk.Label(root, text="Текущее состояние: закрыта", fg="white",
                                              font=small_label_font, bg="#008000")
    current_humidifier_state_label.grid(row=4, column=4, columnspan=2)


def show_error():
    error_root = tk.Tk()
    error_root.title("Ошибка")
    error_root.resizable(False, False)
    error_frame = tk.Frame(error_root, bg="#ffffff", width=600, height=100)
    error_frame.grid(row=0, column=0, rowspan=2)
    error_label = tk.Label(error_root, text="Ошибка", font=label_font, fg="red", bg="white")
    error_label.grid(row=0, column=0, sticky=tk.W + tk.E + tk.S)
    text_for_hint = "Введите числовые значения. Дробные числа вводите через точку."
    hint_label = tk.Label(error_root, text=text_for_hint, font=small_label_font, bg="white")
    hint_label.grid(row=1, column=0, sticky=tk.W + tk.E)


def show_success():
    success_root = tk.Tk()
    success_root.title("Данные успешно сохранены")
    success_root.resizable(False, False)
    success_frame = tk.Frame(success_root, width=400, height=100, bg="white")
    success_frame.grid(row=0, column=0, rowspan=2)
    success_label = tk.Label(success_root, text="Данные успешно сохранены.", font=small_label_font, bg="white",
                             fg="green")
    success_label.grid(row=0, column=0)
    ok_button = tk.Button(success_root, text="OK", command=success_root.destroy)
    ok_button.grid(column=0, row=1)


frame = tk.Frame(root, width=WIDTH, height=HEIGHT, bg="#008000")
frame.grid(column=0, row=0, columnspan=3, rowspan=3)

start_button = tk.Button(root, text="Начать", height=7, width=30, font=button_font, command=load_interface, bg="white")
start_button.grid(column=1, row=1)

quit_button = tk.Button(root, text="Выход", command=root.destroy, height=7, width=30, font=button_font, bg="white")
quit_button.grid(column=1, row=2)

start_label = tk.Label(root, text="Автоматическая теплица", fg="white", font=label_font, bg="#008000")
start_label.grid(row=0, column=0, columnspan=3)

root.mainloop()
