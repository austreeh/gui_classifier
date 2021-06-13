from os import error
from sqlite3.dbapi2 import Error
from tkinter import *
from tkinter import ttk
from typing import Container

from tkinter_custom_button import TkinterCustomButton

class solver():

    global selected_item

    def __init__(self, db):
        self.db = db

    # интерфейсные штуки
    def __reload_window(self, window, new_title, new_width, new_height):
        for widgets in window.winfo_children():
            widgets.destroy()

        positionRight = int(window.winfo_screenwidth()/2 - new_width/2)
        positionDown = int(window.winfo_screenheight()/2 - new_height/2)

        # создаём окно, центрируем
        window.title(new_title)
        window.geometry(f'{new_width}x{new_height}+{positionRight}+{positionDown}')
        window.pack_propagate(False)
        window.resizable(0,0)

    def __create_error(self, text):
        here = Tk()
        self.__reload_window(here, "Ошибка", 400, 100)
        Label(here, text=text).place(x=200, y=30, anchor=CENTER)
        button = TkinterCustomButton(master=here,text="Назад",corner_radius=20,
            height=30,width=100,fg_color="gray26",hover_color="SkyBlue4",
            command= here.destroy 
        ).place(x=150, y=50)
    
    # cut
    def __moron_check(self):
        for row in self.db.fetch_classes():
            for i in range(1, len(row)):
                if row[i] == "None" or row[i] == None or row[i] == ["None"] or row[i] == [None]:
                    return False
        return True
    # cut
        
    def __create_scrollable_frame(self, window, width, height, x, y, text):
        container = LabelFrame(window, text=text, width=width, height=height, bd=1)
        container.pack_propagate(False)
        canvas = Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        container.place(x=x, y=y)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        return scrollable_frame

    def __create_entry(self, element, frame):
        if element[1] == "Перечислимый":
            return ttk.Combobox(frame, state="readonly", values=list(map(str.strip, element[2].split(','))), width=18)
        else:
            return Entry(frame, textvariable="")

    def __create_inputs(self, entry_frame, error_frame, res_frame):
        features = self.db.fetch_features()
        entry_list = []
        fake_entry = Entry(entry_frame, textvariable="")

        Label(entry_frame, text="Название признака:", width=25, anchor="w").grid(row=0, column=0)
        Label(entry_frame, text="Значение:", width=25, anchor="w").grid(row=0, column=1)
        row_counter=1
        Label(entry_frame, text="", width=25).grid(row=row_counter, column=0)
        Label(entry_frame, text="", width=25).grid(row=row_counter, column=1)
        row_counter += 1
        for element in features:
            Label(entry_frame, text=element[0]+":", width=25, anchor="w").grid(row=row_counter, column=0)
            entry = self.__create_entry(element, entry_frame)
            entry.grid(row=row_counter, column=1, sticky="W")
            entry_list.append(entry)
            row_counter += 1
            if type(entry_list[-1]) == type(fake_entry):
                Label(entry_frame, text="", width=25).grid(row=row_counter, column=0)
                parts = element[2].split("-")
                Label(entry_frame, text="Введите значение от "+parts[0]+" до "+parts[1], width=25, fg="green4", anchor="w").grid(row=row_counter, column=1)
                row_counter += 1
            Label(entry_frame, text="", width=25).grid(row=row_counter, column=0)
            Label(entry_frame, text="", width=25).grid(row=row_counter, column=1)
            row_counter += 1
        TkinterCustomButton(master=entry_frame,text="Найти класс",corner_radius=20,
            height=30,width=150,fg_color="gray38",hover_color="SkyBlue4", 
            command=lambda: self.__guess_class(error_frame, entry_list, res_frame) ).grid(columnspan=2)

    def __guess_class(self, error_frame, entry_list, res_frame):
        for widget in error_frame.winfo_children():
            widget.destroy()

        for widget in res_frame.winfo_children():
            widget.destroy()

        fake_entry = Entry(error_frame, textvariable="")
        arguments = []
        is_ok = True
        for element in entry_list:
            if type(element) == type(fake_entry):
                if element.get().isdigit():
                    arguments.append(element.get())
                else:
                    if element.get() != "":
                        is_ok = False
                        self.__create_error("Tедопустимые символы в полях ввода")
                    else:
                        arguments.append("")
            else:
                arguments.append(element.get())
        if is_ok:
            self.__guess(error_frame, arguments, res_frame)

    def __guess(self, error_frame, arguments, res_frame):
        features = self.db.fetch_features() #
        true_classes = []

        for i in range(len(arguments)):
            if arguments[i] == "":
                Label(error_frame, text="Пропущен признак: "+features[i][0], fg="red").grid(sticky="W")

        for row in self.db.fetch_classes():
            errors = False
            for i in range(1, len(row)):
                if "-" in row[i]:
                    if arguments[i-1] != "":
                        parts = row[i].split("-")
                        if int(arguments[i-1]) < int(parts[0]) or int(arguments[i-1]) > int(parts[1]):
                            Label(error_frame, text="Класс "+row[0]+" не подходит по признаку "+features[i-1][0], fg="pink").grid(sticky="W")
                            errors = True
                else:
                    parts = list(map(str.strip, row[i].split(",")))
                    if arguments[i-1] != "":
                        if arguments[i-1] not in parts:
                            Label(error_frame, text="Класс "+row[0]+" не подходит по признаку "+features[i-1][0], fg="pink").grid(sticky="W")
                            errors = True
                if errors:
                    break
            if not errors:
                Label(error_frame, text="Класс "+row[0]+" подходит по всем признакам ", fg="gold").grid(sticky="W")
                true_classes.append(row[0])
        Label(error_frame, text="").grid()
        if true_classes != []:
            Label(res_frame, text="Подходящие классы: "+(", ".join(true_classes)),font="Helvetica 14 bold", fg="green3").grid(sticky="W")
        else:
            Label(res_frame, text="Все классы отвергнуты",font="Helvetica 14 bold", fg="orange").grid(sticky="W")

    # само окно генерации
    def gen(self):
        if self.__moron_check(): 
            window = Tk()
            self.__reload_window(window, "Решатель задач", 920, 440)
            entry_frame = self.__create_scrollable_frame(window, 460, 400, 20, 20, "Поля ввода значений признаков")
            error_frame = self.__create_scrollable_frame(window, 400, 300, 500, 20, "Информация")
            res_frame = self.__create_scrollable_frame(window, 400, 100, 500, 320, "Результат")
            self.__create_inputs(entry_frame, error_frame, res_frame)
        else:
            self.__create_error("Проверьте целостность базы знаний")
