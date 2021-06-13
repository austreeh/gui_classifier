from tkinter import *
from tkinter import ttk

from tkinter_custom_button import TkinterCustomButton

# класс - редактирование области значений признака
class features_list_window():

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
        table["column"] = self.db.columns_features()[:slice_int]
        table["show"]="headings"
        for column in table["column"]:
            table.heading(column, text=column)
        for row in self.db.fetch_features():
            table.insert("", END, values=row[:slice_int])
    
    def __reload_table(self, table, slice_int, ship=0):
        for i in table.get_children(): 
            table.delete(i) 
        for row in self.db.fetch_features():
            table.insert("", END, values=row[:slice_int])

    def __select_item(self, event, table):
        global selected_item
        curr_item = table.focus()
        selected_item = table.item(curr_item)['values'][0:3]
        print(selected_item)

    # само окно генерации
    def gen(self):
        window = Tk()
        self.__reload_window(window, "Радактор списка признаков", 580, 340)
        table = self.__create_table(window, 250, 400, 20, 20)
        self.__fill_table(table, 2)
        #
        TkinterCustomButton(master=window,text="Добавить",corner_radius=20,height=30,width=120,fg_color="gray38",
            hover_color="SkyBlue4",command=lambda: self.__feature_adder(window)).place(x=440, y=20)

        TkinterCustomButton(master=window,text="Удалить",corner_radius=20,height=30,width=120,fg_color="gray38",
            hover_color="SkyBlue4",command=lambda: self.__feature_deleter(table)).place(x=440, y=70)

        TkinterCustomButton(master=window,text="Редактировать",corner_radius=20,height=30,width=120,fg_color="gray38",
            hover_color="SkyBlue4",command=lambda: self.__feature_editor(window)).place(x=440, y=120)

        TkinterCustomButton(master=window,text="Назад",corner_radius=20,height=30,width=120,fg_color="gray26",
            hover_color="SkyBlue4",command=window.destroy).place(x=20, y=290)

    def __feature_deleter(self, table):
        global selected_item
        try: 
            selected_item
        except NameError:
            self.__create_error("Выберите признак для удаления")
        else:
            if selected_item != "":
                self.db.remove_feature(selected_item[0])
                self.__create_ok("Признак удалён")
                self.__reload_table(table, 2)
                del selected_item
            else:
                self.__create_error("Выберите признак для удаления")

    def __feature_adder(self, window):
        self.__reload_window(window, "Создание нового признака", 390, 190)
        Label(window, text="Введите название:").place(x=20, y=20)
        Label(window, text="Выберите тип:").place(x=20, y=80)

        ent = Entry(window, textvariable="", width=20)
        ent.place(x=180, y=20)
        combobox = ttk.Combobox(window, state="readonly", values=["Перечислимый","Интервальный"], width=18)
        combobox.place(x=180, y=80)

        TkinterCustomButton(master=window,text="Добавить",corner_radius=20,height=30,width=150,fg_color="gray38",
            hover_color="SkyBlue4",command=lambda: self.__add_feature(window, ent, combobox)).place(x=220, y=140)

        TkinterCustomButton(master=window,text="Назад",corner_radius=20,height=30,width=150,fg_color="gray26",
            hover_color="SkyBlue4",command=lambda: [self.gen(), window.destroy()]).place(x=20, y=140)

    def __add_feature(self, window, ent, combobox):
        name = ent.get()
        c_name = combobox.get()
        if name.isalpha():
            if name in self.db.columns_classes():
                self.__create_error("Признак с таким названием уже существует")
            else:
                if c_name == "":
                    self.__create_error("Выберите тип признака")
                else:
                    self.db.insert_feature([name, c_name, None])
                    self.__create_ok("Признак добавлен")
                    window.destroy()
                    self.gen()
        else:
            if name == "":
                self.__create_error("Введите название признака")
            else:    
                self.__create_error("Недопустимые символы в названии признака")

    def __feature_editor(self, window):
        global selected_item
        try: 
            selected_item
        except NameError:
            self.__create_error("Выберите признак для редактирования")
        else:
            if selected_item != "":
                self.__edit_feature(window, selected_item)
                del selected_item
            else:
                self.__create_error("Выберите признак для редактирования")

    def __edit_feature(self, window, args):
        prev_name = args[0]
        prev_cbox = args[1]
        self.__reload_window(window, "Редактирование признака", 390, 190)
        Label(window, text="Введите название:").place(x=20, y=20)
        Label(window, text="Выберите тип:").place(x=20, y=80)

        ent = Entry(window, textvariable="", width=20)
        ent.insert(0, prev_name)
        ent.place(x=180, y=20)

        combobox = ttk.Combobox(window, state="readonly", values=["Перечислимый","Интервальный"], width=18)
        combobox.current(["Перечислимый","Интервальный"].index(prev_cbox))
        combobox.place(x=180, y=80)

        TkinterCustomButton(master=window,text="Обновить",corner_radius=20,height=30,width=150,fg_color="gray38",
            hover_color="SkyBlue4",command=lambda: self.__update_feature(window, prev_name, prev_cbox, ent, combobox)).place(x=220, y=140)

        TkinterCustomButton(master=window,text="Назад",corner_radius=20,height=30,width=150,fg_color="gray26",
            hover_color="SkyBlue4",command=lambda: [self.gen(), window.destroy()]).place(x=20, y=140)

    def __update_feature(self, window, old_name, old_cbox, ent, combobox):
        name = ent.get()
        cbox = combobox.get()
        
        if name.isalpha():
                if cbox == old_cbox:
                    val = self.db.get_feature(old_name)[2]
                else:
                    val = None
                self.db.update_feature(old_name, [name, cbox, val])
                self.__create_ok("Признак обновлён")
                window.destroy()
                self.gen()
        else:
            if name == "":
                self.__create_error("Введите название признака")
            else:    
                self.__create_error("Недопустимые символы в названии признака")