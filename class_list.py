from tkinter import *
from tkinter import ttk

from tkinter_custom_button import TkinterCustomButton

# класс - редактирование области значений признака
class class_list_window():

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

    def __create_table(self, window, height, width, x, y):
        table_frame = LabelFrame(window, text="")
        table = ttk.Treeview(table_frame)
        table.place(relheight=1, relwidth=1)
        table_frame.place(height=height, width=width, x=x, y=y)
        table.bind('<ButtonRelease-1>', lambda event, table=table: self.__select_item(event, table))
        return table

    def __create_error(self, text):
        here = Tk()
        self.__reload_window(here, "Ошибка", 300, 100)
        Label(here, text=text).place(x=150, y=30, anchor=CENTER)
        button = TkinterCustomButton(master=here,text="Назад",corner_radius=20,
            height=30,width=100,fg_color="gray38",hover_color="SkyBlue4",
            command= here.destroy 
        ).place(x=100, y=50)
    
    def __create_ok(self, text):
        here = Tk()
        self.__reload_window(here, "Успешно", 300, 100)
        Label(here, text=text).place(x=150, y=30, anchor=CENTER)
        button = TkinterCustomButton(master=here,text="Ок",corner_radius=20,
            height=30,width=100,fg_color="gray38",hover_color="SkyBlue4",
            command= here.destroy 
        ).place(x=100, y=50)

    # функциональные штуки
    def __fill_table(self, table, slice_int):
        table["column"]= self.db.columns_classes()[:slice_int]
        table["show"]="headings"
        for column in table["column"]:
            table.heading(column, text=column)
        for row in self.db.fetch_classes():
            table.insert("", END, values=row[:slice_int])
    
    def __val_in_table(self, table, value):
        curr_vals = []
        for line in table.get_children():
            for val in table.item(line)['values']:
                curr_vals.append(val)
        return value in curr_vals

    def __reload_table(self, table, slice_int, ship=0):
        for i in table.get_children(): 
            table.delete(i) 
        for row in self.db.fetch_classes():
            table.insert("", END, values=row[:slice_int])

    def __select_item(self, event, table):
        global selected_item
        curr_item = table.focus()
        selected_item = table.item(curr_item)['values'][0:3]
        print(selected_item)        

    # само окно генерации
    def gen(self):
        window = Tk()
        self.__reload_window(window, "Радактор списка классов", 500, 290)
        table = self.__create_table(window, 200, 250, 20, 20)
        self.__fill_table(table, 1)
        Label(window, text="Новый класс").place(x=290, y=20)
        entry = Entry(window, textvariable="", width=20)
        entry.place(x=290, y=50)

        TkinterCustomButton(master=window,text="Удалить класс", corner_radius=20,height=30,width=190,
            fg_color="gray38",hover_color="SkyBlue4",command= lambda: self.__class_deleter(table)).place(x=290, y=190)
        
        TkinterCustomButton(master=window,text="Добавить класс", corner_radius=20,height=30,width=190,
            fg_color="gray38",hover_color="SkyBlue4",command=lambda: self.__class_adder(table, entry)).place(x=290, y=90)
        
        TkinterCustomButton(master=window,text="Назад", corner_radius=20,height=30,width=150,
            fg_color="gray26",hover_color="SkyBlue4",command=window.destroy).place(x=20, y=240)

    def __class_adder(self, table, entry):
        value = entry.get()
        args_number = len(self.db.columns_classes())
        arguments = []
        arguments.append(value)
        for i in range(1,args_number):
            arguments.append(None)
        if value.isalpha():
            if self.__val_in_table(table, value):
                self.__create_error("Класс уже существует")
            else:    
                self.db.insert_class(arguments)
                self.__create_ok("Класс добавлен")
                self.__reload_table(table, 1)
        else:
            if value == "":
                self.__create_error("Введите название класса")
            else:
                self.__create_error("Недопустимые символы в названиии класса")

    def __class_deleter(self, table):
        global selected_item
        try: 
            selected_item
        except NameError:
            self.__create_error("Выберите класс для удаления")
        else:
            if selected_item != "":
                self.db.remove_class(selected_item[0])
                self.__create_ok("Класс удалён")
                self.__reload_table(table, 1)
                del selected_item
            else:
                self.__create_error("Выберите класс для удаления")