import tkinter as tk
from get_patch import TempFromTH, HumidityFromTH, Hd, TempA, HumidityA, OpenFort, Watering, totalHum
from pytz import timezone
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib

timezone_msc = timezone("Europe/Moscow")
time_format = "%H:%M:%S"

parameters = open("parameters.txt", "r", encoding="utf-8")
min_average_temperature, max_average_humidity, max_humidity_in_notch = parameters.readline().split()
parameters.close()

root = tk.Tk()
WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()
root.geometry(f"{WIDTH}x{HEIGHT}")
root.title("Автоматическая теплица")
label_font = "Calibri 24 bold"
small_label_font = "Calibri 14 bold"
button_font = "Calibri 16"
settings_root = None
input_root = None
soil_input_root = None
emergency_mode = False
watering_root = None
image = tk.PhotoImage(file="greenhouse2.png", height=HEIGHT+500, width=WIDTH+500)
image_for_tab = tk.PhotoImage(file="green.png", height=HEIGHT+500, width=WIDTH+500)

current_temperatures = [[], [], [], []]
temperatures_humidities_dates = [[], [], [], []]
current_humidities = [[], [], [], []]
current_soil_humidities = [[], [], [], [], [], []]
soil_humidities_dates = [[], [], [], [], [], []]
average_temperatures = []
average_humidities = []
average_dates = []


def open_settings():
    global settings_root
    settings_root = tk.Toplevel()
    settings_root.geometry(f"{WIDTH}x{HEIGHT}")
    settings_root.title("Настройки")
    settings_frame = tk.Frame(settings_root, height=HEIGHT, width=WIDTH)
    settings_frame.grid(row=0, column=0, rowspan=6, columnspan=2)

    settings_background=tk.Canvas(settings_root, height=HEIGHT, width=WIDTH)
    settings_background.grid(row=0, column=0, columnspan=2, rowspan=6)
    settings_background.create_image(0,0, image=image_for_tab, anchor=tk.N + tk.W)

    settings_quit_button = tk.Button(settings_root, text="Назад", bg="white", height=5, width=30, font=button_font,
                                     command=settings_root.destroy)
    settings_quit_button.grid(row=5, column=1, sticky=tk.W)

    settings_background.create_text(WIDTH//2,  HEIGHT//6 - 75, text="Настройки", fill="white", font=label_font, anchor=tk.S)
    settings_background.create_text(WIDTH//2 - 100, HEIGHT//6 + HEIGHT//55, text="Минимальная температура, при которой возможно открытие форточек (°C)", fill="white", font=small_label_font, anchor=tk.E)
    settings_background.create_text(WIDTH//2 - 100, HEIGHT//6 + HEIGHT//15, text="Максимальная влажность, при которой возможно открытие системы увлажнения (%)", fill="white", font=small_label_font, anchor=tk.E)
    settings_background.create_text(WIDTH//2 - 100, HEIGHT//6 + HEIGHT//5, text="Максимальная влажность в бороздке, при которой возможен её полив(%)", fill="white", font=small_label_font, anchor=tk.E)

    temperature_entry = tk.Entry(settings_root, width=50)
    humidity_entry = tk.Entry(settings_root, width=50)
    humidity_in_notch_entry = tk.Entry(settings_root, width=50)

    entries = [temperature_entry, humidity_entry, humidity_in_notch_entry]
    default_text = [min_average_temperature, max_average_humidity, max_humidity_in_notch]

    for i in range(3):
        entries[i].grid(row=i + 1, column=1, sticky=tk.W)
        entries[i].insert(0, default_text[i])

    save_button = tk.Button(settings_root, text="Сохранить", bg="white", height=7, width=30, font=button_font,
                            command=save)
    save_button.grid(row=5, column=0)

    if emergency_mode:
        text_for_emergency_button = "Выключить экстренный режим"
    else:
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
        global min_average_temperature, max_average_humidity, max_humidity_in_notch
        is_different = float(new_temperature) != float(min_average_temperature) \
                       or float(new_humidity) != float(max_average_humidity) \
                       or float(new_humidity_in_notch) != float(max_humidity_in_notch)
        if is_different:
            min_average_temperature, max_average_humidity, max_humidity_in_notch = new_temperature, \
                                                                                   new_humidity, new_humidity_in_notch
            to_write = [new_temperature, new_humidity, new_humidity_in_notch]
            parameters = open("parameters.txt", "w")
            for i in to_write:
                parameters.write(str(i) + " ")
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
    global quit_button
    frame.grid(rowspan=7, columnspan=6)
    start_button.grid_remove()
    quit_button.grid_remove()

    main_menu_background.delete("main_menu_image")
    main_menu_background.create_image(0, 0, image=image, anchor=tk.N+tk.W)

    quit_button = tk.Button(root, text="Выход", command=root.destroy, height=5, width=30, font=button_font, bg="white")
    main_menu_background.create_window(WIDTH-500, 780, window=quit_button)

    settings = tk.Button(text="Настройки", height=5, width=30, font=button_font, bg="white", command=open_settings)
    main_menu_background.create_window(500, 780, window=settings)

    main_menu_background.create_text(WIDTH//2, 50, text="Просмотр", fill="white", font=label_font)

    temp_hum_sensors = tk.Button(text="Датчики температуры и влажности", height=5, width=30, font=button_font,
                                 bg="white", command=open_temperature_humidity_sensors)
    main_menu_background.create_window(300, 180, window=temp_hum_sensors)
    soil_hum_sensors = tk.Button(text="Датчики влажности почвы", height=5, width=30, font=button_font, bg="white",
                                 command=open_soil_humidity_sensors)
    main_menu_background.create_window(WIDTH//2, 180, window=soil_hum_sensors)
    average_temp_hum = tk.Button(text="Средняя влажность и температура", height=5, width=30, font=button_font,
                                 bg="white", command=open_average_humidity_and_temperature)
    main_menu_background.create_window(WIDTH-300, 180, window=average_temp_hum)

    main_menu_background.create_text(WIDTH//2, 280, text="Управление", fill="white", font=label_font)

    fork_opener = tk.Button(text="Открыть форточки", height=5, width=30, font=button_font, bg="white",
                            command=open_forks)
    main_menu_background.create_window(300, 405, window=fork_opener)
    fork_closer = tk.Button(text="Закрыть форточки", height=5, width=30, font=button_font, bg="white",
                            command=close_forks)
    main_menu_background.create_window(300, 580, window=fork_closer)
    watering_opener = tk.Button(text="Открыть/закрыть полив бороздок", height=5, width=30, font=button_font, bg="white",
                                command=open_watering_interface)
    main_menu_background.create_window(WIDTH//2, 405, window=watering_opener)
    humidifier_opener = tk.Button(text="Открыть систему общего увлажнения", height=5, width=50,
                                  font=button_font, bg="white", command=open_humidifiing_system)
    main_menu_background.create_window(WIDTH-300, 405, window=humidifier_opener)
    humidifier_closer = tk.Button(text="Закрыть систему общего увлажнения", height=5, width=50,
                                  font=button_font, bg="white", command=close_humidifiing_system)
    main_menu_background.create_window(WIDTH-300, 580, window=humidifier_closer)

    main_menu_background.create_text(300, 680, text="Текущее состояние: закрыты", fill="white", font=small_label_font,
                           tags="current_fork_state")
    main_menu_background.create_text(WIDTH-300, 680, text="Текущее состояние: закрыта", fill="white", font=small_label_font,
                           tags="current_hum_system_state")

def show_error():
    error_root = tk.Tk()
    error_root.title("Ошибка")
    error_root.resizable(False, False)
    error_frame = tk.Frame(error_root, bg="#ffffff", width=600, height=100)
    error_frame.grid(row=0, column=0, rowspan=2)
    error_label = tk.Label(error_root, text="Ошибка", font=label_font, fg="red", bg="white")
    error_label.grid(row=0, column=0, sticky=tk.W + tk.E + tk.S)
    text_for_hint = "Введите корректные числовые значения. Дробные числа вводите через точку."
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


def open_temperature_humidity_sensors():
    sensors_root = tk.Tk()
    sensors_root.title("Датчики температуры и влажности")
    sensors_root.geometry(f"{WIDTH}x{HEIGHT}")
    sensors_frame = tk.Frame(sensors_root, height=HEIGHT, width=WIDTH, bg="#008000")
    sensors_frame.grid(row=0, column=0, rowspan=6, columnspan=5)
    sensors_label = tk.Label(sensors_root, text="Датчики температуры и влажности", fg="white", bg="#008000",
                             font=label_font)
    sensors_label.grid(row=0, column=0, columnspan=5)

    commands = [build_temperature_humidity_plot_1, build_temperature_humidity_plot_2, build_temperature_humidity_plot_3, build_temperature_humidity_plot_4]

    for i in range(1, 5):
        label_with_number = tk.Label(sensors_root, text=str(i), bg="#008000", fg="white", font=label_font,
                                     highlightthickness=2, highlightbackground="white")
        label_with_number.grid(row=1, column=i, sticky=tk.E + tk.W + tk.N + tk.S)

        button_with_plot = tk.Button(sensors_root, command=commands[i-1], text="Посмотреть графики",
                                     bg="white", font=button_font, height=1, width=18)
        button_with_plot.grid(row=4, column=i)

    for i in range(2, 4):
        for j in range(1, 5):
            if i == 2:
                text = TempFromTH(j)
                current_temperatures[j-1].append(text)
                current_date = datetime.now(timezone_msc).strftime(time_format)
                temperatures_humidities_dates[j - 1].append(current_date)

            else:
                text = HumidityFromTH(j)
                current_humidities[j-1].append(text)

            label_with_data = tk.Label(sensors_root, text=text, bg="#008000", fg="white", font=label_font,
                                       highlightthickness=2, highlightbackground="white")
            label_with_data.grid(row=i, column=j, sticky=tk.E + tk.W + tk.N + tk.S)

    number_label = tk.Label(sensors_root, text="Номер устройства", bg="#008000", fg="white", font=label_font,
                            highlightthickness=2, highlightbackground="white")
    number_label.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
    temperature_label = tk.Label(sensors_root, text="Температура", bg="#008000", fg="white", font=label_font,
                                 highlightthickness=2, highlightbackground="white")
    temperature_label.grid(row=2, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
    humidity_label = tk.Label(sensors_root, text="Влажность", bg="#008000", fg="white", font=label_font,
                              highlightthickness=2, highlightbackground="white")
    humidity_label.grid(row=3, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

    sensors_quit_button = tk.Button(sensors_root, text="Назад", command=sensors_root.destroy, bg="white",
                                    font=button_font, height=1, width=7)
    sensors_quit_button.grid(row=5, column=0, columnspan=2)

    manual_input = tk.Button(sensors_root, text="Ввести данные вручную", bg="white", font=button_font, height=1, width=18, command=manual_temperature_humidity_input)
    manual_input.grid(row=5, column=3, columnspan=2)


def open_soil_humidity_sensors():
    humidity_root = tk.Tk()
    humidity_root.title("Датчики влажности почвы")
    humidity_root.geometry(f"{WIDTH}x{HEIGHT}")
    humidity_frame = tk.Frame(humidity_root, height=HEIGHT, width=WIDTH, bg="#008000")
    humidity_frame.grid(row=0, column=0, rowspan=5, columnspan=7)
    humidity_label = tk.Label(humidity_root, text="Датчики влажности почвы", fg="white", bg="#008000", font=label_font)
    humidity_label.grid(row=0, column=0, columnspan=7)

    commands = [build_soil_humidity_plot_1, build_soil_humidity_plot_2, build_soil_humidity_plot_3, build_soil_humidity_plot_4, build_soil_humidity_plot_5, build_soil_humidity_plot_6]

    for i in range(1, 7):
        label_with_number = tk.Label(humidity_root, text=str(i), bg="#008000", fg="white", font=label_font,
                                     highlightthickness=2, highlightbackground="white")
        label_with_number.grid(row=1, column=i, sticky=tk.E + tk.W + tk.N + tk.S)
        text = Hd(i)
        label_with_data = tk.Label(humidity_root, text=text, bg="#008000", fg="white", font=label_font,
                                   highlightthickness=2, highlightbackground="white")
        label_with_data.grid(row=2, column=i, sticky=tk.E + tk.W + tk.N + tk.S)
        button_with_plot = tk.Button(humidity_root, text="Посмотреть графики", bg="white", font=button_font, height=1, width=18, command=commands[i-1])
        button_with_plot.grid(row=3, column=i)
        current_soil_humidities[i-1].append(text)
        current_date = datetime.now(timezone_msc).strftime(time_format)
        soil_humidities_dates[i - 1].append(current_date)


    number_label = tk.Label(humidity_root, text="Номер устройства", bg="#008000", fg="white", font=label_font,
                            highlightthickness=2, highlightbackground="white")
    number_label.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
    soil_humidity_label = tk.Label(humidity_root, text="Влажность почвы", bg="#008000", fg="white", font=label_font,
                                   highlightthickness=2, highlightbackground="white")
    soil_humidity_label.grid(row=2, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

    sensors_quit_button = tk.Button(humidity_root, text="Назад", command=humidity_root.destroy, bg="white",
                                    font=button_font, height=1, width=9)
    sensors_quit_button.grid(row=4, column=0, columnspan=3)

    manual_input = tk.Button(humidity_root, text="Ввести данные вручную", bg="white",
                                    font=button_font, height=1, width=18, command=manual_soil_humidity_input)
    manual_input.grid(row=4, column=4, columnspan=3)


def open_average_humidity_and_temperature():
    average_parameters_root = tk.Tk()
    average_parameters_root.title("Средняя влажность и температура")
    average_parameters_root.geometry(f"{WIDTH}x{HEIGHT}")
    average_parameters_frame = tk.Frame(average_parameters_root, height=HEIGHT, width=WIDTH, bg="#008000")
    average_parameters_frame.grid(row=0, column=0, rowspan=4, columnspan=2)

    average_parameters_label = tk.Label(average_parameters_root, text="Средняя влажность и температура", fg="white",
                                        bg="#008000", font=label_font)
    average_parameters_label.grid(row=0, column=0, columnspan=2)

    average_temperature = round(TempA(), 2)
    average_temperature_text = "Средняя температура: " + str(average_temperature)
    average_temperature_label = tk.Label(average_parameters_root, text=average_temperature_text, fg="white",
                                         bg="#008000", font=label_font)
    average_temperature_label.grid(row=1, column=0, columnspan=2)
    average_temperatures.append(average_temperature)

    average_humidity = round(HumidityA(), 2)
    average_humidity_text = "Средняя влажность: " + str(average_humidity)
    average_humidity_label = tk.Label(average_parameters_root, text=average_humidity_text, fg="white",
                                      bg="#008000", font=label_font)
    average_humidity_label.grid(row=2, column=0, columnspan=2)
    average_humidities.append(average_humidity)

    current_date = datetime.now(timezone_msc).strftime(time_format)
    average_dates.append(current_date)

    quit_button = tk.Button(average_parameters_root, text="Назад", bg="white", font=button_font, height=1, width=7,
                            command=average_parameters_root.destroy)
    quit_button.grid(row=3, column=0, sticky=tk.E, padx=20)

    plot_button = tk.Button(average_parameters_root, text="Посмотреть графики", bg="white", font=button_font, height=1, width=15, command=build_average_parameters_plot)
    plot_button.grid(row=3, column=1, sticky=tk.W, padx=20)


def open_forks():
    global min_average_temperature
    current_average_temperature = TempA()
    if current_average_temperature > float(min_average_temperature) or emergency_mode:
        OpenFort(1)
        background.itemconfigure("current_fork_state", text="Текущее состояние: открыты")
    else:
        show_info_about_temperature()


def close_forks():
    background.itemconfigure("current_fork_state", text="Текущее состояние: закрыты")
    OpenFort(0)



def show_info_about_temperature():
    info_root = tk.Tk()
    info_root.title("Ошибка")
    info_root.resizable(False, False)
    info_frame = tk.Frame(info_root, height=150, width=800, bg="#008000")
    info_frame.grid(row=0, column=0, rowspan=2)
    info_label = tk.Label(info_root, text="Ошибка", fg="white", bg="#008000", font=label_font)
    info_label.grid(row=0, column=0)
    text_for_hint = "Температура в теплице недостаточна для того, чтобы открыть форточки."
    hint_label = tk.Label(info_root, text=text_for_hint, fg="white", bg="#008000", font=small_label_font)
    hint_label.grid(row=1, column=0)


def open_humidifiing_system():
    global max_average_humidity
    current_average_humidity = HumidityA()
    if current_average_humidity < float(max_average_humidity) or emergency_mode:
        background.itemconfigure("current_hum_system_state", text="Текущее состояние: открыта")
        totalHum(1)
    else:
        show_info_about_humidity()


def show_info_about_humidity():
    info_root = tk.Tk()
    info_root.title("Ошибка")
    info_root.resizable(False, False)
    info_frame = tk.Frame(info_root, height=150, width=800, bg="#008000")
    info_frame.grid(row=0, column=0, rowspan=2)
    info_label = tk.Label(info_root, text="Ошибка", fg="white", bg="#008000", font=label_font)
    info_label.grid(row=0, column=0)
    text_for_hint = "Влажность в теплице достаточна. Включать общую систему увлажнения не нужно."
    hint_label = tk.Label(info_root, text=text_for_hint, fg="white", bg="#008000", font=small_label_font)
    hint_label.grid(row=1, column=0)


def close_humidifiing_system():
    background.itemconfigure("current_hum_system_state", text="Текущее состояние: закрыта")
    totalHum(0)


def open_watering_interface():
    global watering_root
    watering_root = tk.Tk()
    watering_root.title("Настройки системы полива")
    watering_root.geometry(f"{WIDTH}x{HEIGHT}")
    watering_frame = tk.Frame(watering_root, height=HEIGHT, width=WIDTH, bg="#008000")
    watering_frame.grid(row=0, column=0, rowspan=6, columnspan=6)
    watering_label = tk.Label(watering_root, text="Настройки системы полива", fg="white", bg="#008000", font=label_font)
    watering_label.grid(row=0, column=0, columnspan=6)

    open_commands = [open_1, open_2, open_3, open_4, open_5, open_6]
    close_commands = [close_1, close_2, close_3, close_4, close_5, close_6]

    for i in range(6):
        label_with_number = tk.Label(watering_root, text=str(i + 1), bg="#008000", fg="white", font=label_font)
        label_with_number.grid(row=1, column=i, sticky=tk.S)
        button_open = tk.Button(watering_root, text="Открыть", bg="white", height=3, width=20, font=button_font,
                                command=open_commands[i])
        button_open.grid(row=2, column=i)
        button_close = tk.Button(watering_root, text="Закрыть", bg="white", height=3, width=20, font=button_font,
                                 command=close_commands[i])
        button_close.grid(row=3, column=i)
        current_state = tk.Label(watering_root, text="Текущее состояние: закрыта", bg="#008000", fg="white",
                                 font=small_label_font)
        current_state.grid(row=4, column=i, sticky=tk.N)

    quit_button = tk.Button(watering_root, text="Назад", bg="white", font=button_font, height=1, width=7,
                            command=watering_root.destroy)
    quit_button.grid(row=5, column=2, columnspan=2)


def open_1():
    global max_humidity_in_notch
    current_humidity_in_notch = Hd(1)
    if current_humidity_in_notch < float(max_humidity_in_notch) or emergency_mode:
        Watering(1, 1)
        global watering_root
        label = watering_root.winfo_children()[5]
        label.configure(text="Текущее состояние: открыта")
    else:
        show_info_about_humidity_in_notch()


def close_1():
    global watering_root
    label = watering_root.winfo_children()[5]
    Watering(0, 1)
    label.configure(text="Текущее состояние: закрыта")


def open_2():
    global max_humidity_in_notch
    current_humidity_in_notch = Hd(2)
    if current_humidity_in_notch < float(max_humidity_in_notch) or emergency_mode:
        Watering(1, 2)
        global watering_root
        label = watering_root.winfo_children()[9]
        label.configure(text="Текущее состояние: открыта")
    else:
        show_info_about_humidity_in_notch()


def close_2():
    global watering_root
    label = watering_root.winfo_children()[9]
    Watering(0, 2)
    label.configure(text="Текущее состояние: закрыта")


def open_3():
    global max_humidity_in_notch
    current_humidity_in_notch = Hd(3)
    if current_humidity_in_notch < float(max_humidity_in_notch) or emergency_mode:
        Watering(1, 3)
        global watering_root
        label = watering_root.winfo_children()[13]
        label.configure(text="Текущее состояние: открыта")
    else:
        show_info_about_humidity_in_notch()


def close_3():
    global watering_root
    label = watering_root.winfo_children()[13]
    Watering(0, 3)
    label.configure(text="Текущее состояние: закрыта")


def open_4():
    global max_humidity_in_notch
    current_humidity_in_notch = Hd(4)
    if current_humidity_in_notch < float(max_humidity_in_notch) or emergency_mode:
        Watering(1, 4)
        global watering_root
        label = watering_root.winfo_children()[17]
        label.configure(text="Текущее состояние: открыта")
    else:
        show_info_about_humidity_in_notch()


def close_4():
    global watering_root
    label = watering_root.winfo_children()[17]
    Watering(0, 4)
    label.configure(text="Текущее состояние: закрыта")


def open_5():
    global max_humidity_in_notch
    current_humidity_in_notch = Hd(5)
    if current_humidity_in_notch < float(max_humidity_in_notch) or emergency_mode:
        Watering(1, 5)
        global watering_root
        label = watering_root.winfo_children()[21]
        label.configure(text="Текущее состояние: открыта")
    else:
        show_info_about_humidity_in_notch()


def close_5():
    global watering_root
    label = watering_root.winfo_children()[21]
    Watering(0, 5)
    label.configure(text="Текущее состояние: закрыта")


def open_6():
    global max_humidity_in_notch
    current_humidity_in_notch = Hd(6)
    if current_humidity_in_notch < float(max_humidity_in_notch) or emergency_mode:
        Watering(1, 6)
        global watering_root
        label = watering_root.winfo_children()[25]
        label.configure(text="Текущее состояние: открыта")
    else:
        show_info_about_humidity_in_notch()


def close_6():
    global watering_root
    label = watering_root.winfo_children()[25]
    Watering(0, 6)
    label.configure(text="Текущее состояние: закрыта")


def show_info_about_humidity_in_notch():
    info_root = tk.Tk()
    info_root.title("Ошибка")
    info_root.resizable(False, False)
    info_frame = tk.Frame(info_root, height=150, width=800, bg="#008000")
    info_frame.grid(row=0, column=0, rowspan=2)
    info_label = tk.Label(info_root, text="Ошибка", fg="white", bg="#008000", font=label_font)
    info_label.grid(row=0, column=0)
    text_for_hint = "Влажность в этой бороздке достаточна. Включать систему полива не нужно."
    hint_label = tk.Label(info_root, text=text_for_hint, fg="white", bg="#008000", font=small_label_font)
    hint_label.grid(row=1, column=0)


def build_temperature_humidity_plot_1():
    if len(current_temperatures[0]) < 9:
        temperatures_of_sensor = current_temperatures[0]
        humidities_of_sensor = current_humidities[0]
        dates_of_sensor = temperatures_humidities_dates[0]
    else:
        first_index = len(current_temperatures[0]) - 8
        temperatures_of_sensor = current_temperatures[0][first_index:]
        humidities_of_sensor = current_humidities[0][first_index:]
        dates_of_sensor = temperatures_humidities_dates[0][first_index:]

    fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, num="Графики температуры и влажности", figsize=(13, 75))
    ax1.plot(dates_of_sensor, temperatures_of_sensor, linewidth=2)
    ax2.plot(dates_of_sensor, humidities_of_sensor, linewidth=2)

    plt.show()

def build_temperature_humidity_plot_2():
    if len(current_temperatures[1]) < 9:
        temperatures_of_sensor = current_temperatures[1]
        humidities_of_sensor = current_humidities[1]
        dates_of_sensor = temperatures_humidities_dates[1]
    else:
        first_index = len(current_temperatures[1]) - 8
        temperatures_of_sensor = current_temperatures[1][first_index:]
        humidities_of_sensor = current_humidities[1][first_index:]
        dates_of_sensor = temperatures_humidities_dates[1][first_index:]

    fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, num="Графики температуры и влажности", figsize=(13, 75))
    ax1.plot(dates_of_sensor, temperatures_of_sensor, linewidth=2)
    ax2.plot(dates_of_sensor, humidities_of_sensor, linewidth=2)

    plt.show()

def build_temperature_humidity_plot_3():
    if len(current_temperatures[2]) < 9:
        temperatures_of_sensor = current_temperatures[2]
        humidities_of_sensor = current_humidities[2]
        dates_of_sensor = temperatures_humidities_dates[2]
    else:
        first_index = len(current_temperatures[2]) - 8
        temperatures_of_sensor = current_temperatures[2][first_index:]
        humidities_of_sensor = current_humidities[2][first_index:]
        dates_of_sensor = temperatures_humidities_dates[2][first_index:]

    fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, num="Графики температуры и влажности", figsize=(13, 75))
    ax1.plot(dates_of_sensor, temperatures_of_sensor, linewidth=2)
    ax2.plot(dates_of_sensor, humidities_of_sensor, linewidth=2)

    plt.show()

def build_temperature_humidity_plot_4():
    if len(current_temperatures[3]) < 9:
        temperatures_of_sensor = current_temperatures[3]
        humidities_of_sensor = current_humidities[3]
        dates_of_sensor = temperatures_humidities_dates[3]
    else:
        first_index = len(current_temperatures[3]) - 8
        temperatures_of_sensor = current_temperatures[3][first_index:]
        humidities_of_sensor = current_humidities[3][first_index:]
        dates_of_sensor = temperatures_humidities_dates[3][first_index:]

    fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, num="Графики температуры и влажности", figsize=(13, 75))
    ax1.plot(dates_of_sensor, temperatures_of_sensor, linewidth=2)
    ax2.plot(dates_of_sensor, humidities_of_sensor, linewidth=2)

    plt.show()


def build_soil_humidity_plot_1():
    if len(current_soil_humidities[0]) < 9:
        humidities_of_sensor = current_soil_humidities[0]
        dates_of_sensor = soil_humidities_dates[0]
    else:
        first_index=len(current_soil_humidities[0]) - 8
        humiditries_of_sensor = current_soil_humidities[0][first_index:]
        dates_of_sensor = soil_humidities_dates[0][first_index:]
        
    
    fig, ax = plt.subplots(num="График влажности почвы", figsize=(13, 75))
    ax.plot(dates_of_sensor, humidities_of_sensor, linewidth=2)
    
    plt.show()


def build_soil_humidity_plot_2():
    if len(current_soil_humidities[1]) < 9:
        humidities_of_sensor = current_soil_humidities[1]
        dates_of_sensor = soil_humidities_dates[1]
    else:
        first_index=len(current_soil_humidities[1]) - 8
        humiditries_of_sensor = current_soil_humidities[1][first_index:]
        dates_of_sensor = soil_humidities_dates[1][first_index:]
        
    
    fig, ax = plt.subplots(num="График влажности почвы", figsize=(13, 75))
    ax.plot(dates_of_sensor, humidities_of_sensor, linewidth=2)
    
    plt.show()


def build_soil_humidity_plot_3():
    if len(current_soil_humidities[2]) < 9:
        humidities_of_sensor = current_soil_humidities[2]
        dates_of_sensor = soil_humidities_dates[2]
    else:
        first_index=len(current_soil_humidities[2]) - 8
        humiditries_of_sensor = current_soil_humidities[0][first_index:]
        dates_of_sensor = soil_humidities_dates[2][first_index:]
        
    
    fig, ax = plt.subplots(num="График влажности почвы", figsize=(13, 75))
    ax.plot(dates_of_sensor, humidities_of_sensor, linewidth=2)
    
    plt.show()


def build_soil_humidity_plot_4():
    if len(current_soil_humidities[3]) < 9:
        humidities_of_sensor = current_soil_humidities[3]
        dates_of_sensor = soil_humidities_dates[3]
    else:
        first_index=len(current_soil_humidities[3]) - 8
        humiditries_of_sensor = current_soil_humidities[3][first_index:]
        dates_of_sensor = soil_humidities_dates[3][first_index:]
        
    
    fig, ax = plt.subplots(num="График влажности почвы", figsize=(13, 75))
    ax.plot(dates_of_sensor, humidities_of_sensor, linewidth=2)
    
    plt.show()


def build_soil_humidity_plot_5():
    if len(current_soil_humidities[4]) < 9:
        humidities_of_sensor = current_soil_humidities[4]
        dates_of_sensor = soil_humidities_dates[4]
    else:
        first_index=len(current_soil_humidities[4]) - 8
        humiditries_of_sensor = current_soil_humidities[4][first_index:]
        dates_of_sensor = soil_humidities_dates[4][first_index:]
        
    
    fig, ax = plt.subplots(num="График влажности почвы", figsize=(13, 75))
    ax.plot(dates_of_sensor, humidities_of_sensor, linewidth=2)
    
    plt.show()


def build_soil_humidity_plot_6():
    if len(current_soil_humidities[5]) < 9:
        humidities_of_sensor = current_soil_humidities[5]
        dates_of_sensor = soil_humidities_dates[5]
    else:
        first_index=len(current_soil_humidities[5]) - 8
        humiditries_of_sensor = current_soil_humidities[5][first_index:]
        dates_of_sensor = soil_humidities_dates[5][first_index:]
        
    
    fig, ax = plt.subplots(num="График влажности почвы", figsize=(13, 75))
    ax.plot(dates_of_sensor, humidities_of_sensor, linewidth=2)
    
    plt.show()


def build_average_parameters_plot():
    if len(average_temperatures) < 9:
        temperatures = average_temperatures
        humidities = average_humidities
        dates = average_dates
    else:
        first_index = len(average_temperatures) - 8
        temperatures = average_temperatures[first_index:]
        humidities = average_humidities[first_index:]
        dates = average_dates[first_index:]

    fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, num="Средняя температура и влажность", figsize=(13, 75))
    ax1.plot(dates, temperatures, linewidth=2)
    ax2.plot(dates, humidities, linewidth=2)

    plt.show()


def manual_temperature_humidity_input():
    global soil_input_root
    input_root = tk.Tk()
    input_root.geometry(f"{WIDTH}x{HEIGHT}")
    input_root.title("Ручной ввод данных")
    input_frame = tk.Frame(input_root, height=HEIGHT, width=WIDTH, bg="#008000")
    input_frame.grid(row=0, column=0, rowspan=5, columnspan=2)

    input_label = tk.Label(input_root, text="Ручной ввод данных", bg="#008000", fg="white", font=label_font)
    input_label.grid(row=0, column=0, columnspan=2)

    number_label = tk.Label(input_root, text="Номер датчика (от 1 до 4):", bg="#008000", fg="white", font=small_label_font)
    number_label.grid(row=1, column=0, sticky=tk.E, padx=50)
    number_entry = tk.Entry(input_root, width=50)
    number_entry.grid(row=1, column=1, sticky=tk.W)

    temperature_label = tk.Label(input_root, text="Температура:", bg="#008000", fg="white", font=small_label_font)
    temperature_label.grid(row=2, column=0, sticky=tk.E, padx=50)
    temperature_entry = tk.Entry(input_root, width=50)
    temperature_entry.grid(row=2, column=1, sticky=tk.W)

    humidity_label = tk.Label(input_root, text="Влажность:", bg="#008000", fg="white", font=small_label_font)
    humidity_label.grid(row=3, column=0, sticky=tk.E, padx=50)
    humidity_entry = tk.Entry(input_root, width=50)
    humidity_entry.grid(row=3, column=1, sticky=tk.W)

    quit_button = tk.Button(input_root, text="Назад", bg="white", font=button_font, width=7, height=1, command=input_root.destroy)
    quit_button.grid(row=4, column=0)

    save_button = tk.Button(input_root, text="Сохранить", bg="white", font=button_font, width=7, height=1, command=save_manual_temperature_humidity)
    save_button.grid(row=4, column=1)


def save_manual_temperature_humidity():
    children = input_root.winfo_children()
    number = children[3].get()
    temperature = children[5].get()
    humidity = children[7].get()
    try:
        number = int(number)
        temperature, humidity = map(float, [temperature, humidity])
        current_temperatures[number-1].append(temperature)
        current_humidities[number-1].append(humidity)
        current_date =  datetime.now(timezone_msc).strftime(time_format)
        temperatures_humidities_dates[number-1].append(current_date)
        show_success()
    except ValueError:
        show_error()
    except IndexError:
        show_error()


def manual_soil_humidity_input():
    global soil_input_root
    soil_input_root = tk.Tk()
    soil_input_root.geometry(f"{WIDTH}x{HEIGHT}")
    soil_input_root.title("Ручной ввод данных")
    soil_input_frame = tk.Frame(soil_input_root, height=HEIGHT, width=WIDTH, bg="#008000")
    soil_input_frame.grid(row=0, column=0, rowspan=4, columnspan=2)

    soil_input_label = tk.Label(soil_input_root, text="Ручной ввод данных", bg="#008000", fg="white", font=label_font)
    soil_input_label.grid(row=0, column=0, columnspan=2)

    soil_number_label = tk.Label(soil_input_root, text="Номер датчика (от 1 до 6):", bg="#008000", fg="white", font=small_label_font)
    soil_number_label.grid(row=1, column=0, sticky=tk.E, padx=50)
    soil_number_entry = tk.Entry(soil_input_root, width=50)
    soil_number_entry.grid(row=1, column=1, sticky=tk.W)


    soil_humidity_label = tk.Label(soil_input_root, text="Влажность:", bg="#008000", fg="white", font=small_label_font)
    soil_humidity_label.grid(row=2, column=0, sticky=tk.E, padx=50)
    soil_humidity_entry = tk.Entry(soil_input_root, width=50)
    soil_humidity_entry.grid(row=2, column=1, sticky=tk.W)

    soil_quit_button = tk.Button(soil_input_root, text="Назад", bg="white", font=button_font, width=7, height=1, command=soil_input_root.destroy)
    soil_quit_button.grid(row=3, column=0)

    soil_save_button = tk.Button(soil_input_root, text="Сохранить", bg="white", font=button_font, width=7, height=1, command=save_manual_soil_humidity)
    soil_save_button.grid(row=3, column=1)


def save_manual_soil_humidity():
    children = soil_input_root.winfo_children()
    number = children[3].get()
    humidity = children[5].get()
    try:
        number = int(number)
        humidity = float(humidity)
        current_soil_humidities[number-1].append(humidity)
        current_date =  datetime.now(timezone_msc).strftime(time_format)
        soil_humidities_dates[number-1].append(current_date)
        show_success()
    except ValueError:
        show_error()
    except IndexError:
        show_error()

frame = tk.Frame(root, width=WIDTH, height=HEIGHT)
frame.grid(column=0, row=0, columnspan=3, rowspan=3)

main_menu_background = tk.Canvas(root, height=HEIGHT, width=WIDTH)
main_menu_background.grid(row=0, column=0, columnspan=3, rowspan=3)
main_menu_image = tk.PhotoImage(file="greenhouse.png", height=HEIGHT, width=WIDTH)
main_menu_background.create_image(0, 0, image=main_menu_image, anchor=tk.N+tk.W)
main_menu_background.create_text(WIDTH//2, HEIGHT//4, text="Автоматическая теплица", fill="white", font=label_font, tags="main_menu_image")

start_button = tk.Button(root, text="Начать", height=5, width=30, font=button_font, command=load_interface, bg="white")
start_button.grid(column=1, row=1)

quit_button = tk.Button(root, text="Выход", command=root.destroy, height=5, width=30, font=button_font, bg="white")
quit_button.grid(column=1, row=2)

root.mainloop()
