from tkinter import *
from tkinter import ttk

from tkinter_custom_button import TkinterCustomButton

# класс - редактирование области значений признака
class edit_class_window():

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
        self.__reload_window(here, "Ошибка", 400, 100)
        Label(here, text=text).place(x=200, y=30, anchor=CENTER)
        button = TkinterCustomButton(master=here,text="Назад",corner_radius=20,
            height=30,width=100,fg_color="gray26",hover_color="SkyBlue4",
            command= here.destroy 
        ).place(x=150, y=50)
    
    def __create_ok(self, text):
        here = Tk()
        self.__reload_window(here, "Успешно", 300, 100)
        Label(here, text=text).place(x=150, y=30, anchor=CENTER)
        button = TkinterCustomButton(master=here,text="Ок",corner_radius=20,
            height=30,width=100,fg_color="gray38",hover_color="SkyBlue4",
            command= here.destroy 
        ).place(x=100, y=50)

    def __create_entry_pair(self, window):
        frame = Frame(window, width = 37)
        ent1 = Entry(frame, textvariable="", width=16)
        ent1.grid(row=0, column=0)
        Label(frame, text="до", width=5).grid(row=0, column=1)
        ent2 = Entry(frame, textvariable="", width=16)
        ent2.grid(row=0, column=2)
        return frame

    def __fill_entry_pair(self, frame, class_name, arguments):
        value = self.db.select_Cfeature(class_name, arguments[0])[0]
        childs = []
        for child in frame.winfo_children():
            childs.append(child)
        print(value)
        if value != None and value != 'None' and "," not in value:
            vals = value.split("-")
            childs[0].insert(0,vals[0])
            childs[2].insert(0,vals[1])

    # функциональные штуки
    def __fill_table(self, table, slice_int):
        table["column"]= self.db.columns_classes()[:slice_int]
        table["show"]="headings"
        for column in table["column"]:
            table.heading(column, text=column)
        for row in self.db.fetch_classes():
            table.insert("", END, values=row[:slice_int])

    def __fill_extra(self, table, class_name):
        table["column"] = self.db.columns_features()
        table["show"]="headings"
        class_val = self.db.get_class(class_name)
        for column in table["column"]:
            table.heading(column, text=column)
        i = 1
        for row in self.db.fetch_features():
            part = list(row[:2])
            part.append(class_val[i])
            table.insert("", END, values=tuple(part))
            i += 1

    def __reload_extra(self, table, class_name):
        for i in table.get_children(): 
            table.delete(i) 
        class_val = self.db.get_class(class_name)
        i = 1
        for row in self.db.fetch_features():
            part = list(row[:2])
            part.append(class_val[i])
            table.insert("", END, values=tuple(part))
            i += 1
        
    def __fill_feats(self, table, input_str):
        table["column"]="значения"
        table["show"] = "headings"
        table.heading("значения", text="значения")
        if input_str != "None" and input_str != None and "-" not in input_str:
            values = list(map(str.strip, input_str.split(',')))
            print(values)
            for element in values:
                table.insert("", END, values=element)

    def __select_item(self, event, table):
        global selected_item
        curr_item = table.focus()
        selected_item = table.item(curr_item)['values'][0:3]
        print(selected_item)

    def __update_feature_str(self, window, table, class_name, arguments):
        arguments = list(arguments)
        curr_vals = []
        for line in table.get_children():
            for val in table.item(line)['values']:
                curr_vals.append(val)
        if curr_vals == []:
            arguments[2] = None
        else:
            for i in range(1, len(curr_vals)):
                curr_vals[0] += ", "+curr_vals[i]
            arguments[2] = curr_vals[0]
        self.db.update_Cfeature(class_name, arguments[0], arguments[2])
        self.__create_ok("Область значений обновлена")
        self.__edit_class(window, [class_name])

    def __update_feature_int(self, window, frame, class_name, arguments, limits):
        if limits[2] == "None" or limits[2] == None:
            self.__create_error("Область значения признака не определена")
        else:
            parts = limits[2].split("-")
            arguments = list(arguments)
            childs = []
            for child in frame.winfo_children():
                childs.append(child)
            if childs[0].get().isdigit() and childs[2].get().isdigit():
                if int(childs[0].get()) <= int(childs[2].get()):
                    if int(parts[0]) <= int(childs[0].get()) and int(parts[1]) >= int(childs[2].get()):
                        arguments[2] = str(int(childs[0].get())) + "-" + str(int(childs[2].get()))
                        self.db.update_Cfeature(class_name, arguments[0], arguments[2])
                        self.__create_ok("Область значений обновлена")
                        self.__edit_class(window, [class_name])
                    else:
                        self.__create_error("Значения полей вне области значений признака")
                else:
                    self.__create_error("Левая граница больше правой")
            else:
                self.__create_error("Недопустимые символы в области значений")
        

    def __clear_classfeature(self, class_name, arguments):
        self.db.update_Cfeature(class_name, arguments[0], "None")

    def __pour_value(self, table_left, table_right):
        item = table_left.focus()
        if item:
            table_right.insert("", END, values=table_left.item(item)['values'][0])
            table_left.delete(item)
            
    def __clean_extra(self, table_left, table_right):
        val_list = []
        for line in table_right.get_children():
            for value in table_right.item(line)['values']:
                val_list.append(value)
        for line in table_left.get_children():
            for item in table_left.item(line)['values']:
                if item in val_list:
                    table_left.delete(line)

    # проверки полей

    # затычки
    def fake_func(self, window):
        print("fake_func placed")
        pass

    # само окно генерации
    def gen(self):
        window = Tk()
        self.__reload_window(window, "Радактор признаков классов", 290, 350)
        table = self.__create_table(window, 200, 250, 20, 20)
        self.__fill_table(table, 1)
        
        TkinterCustomButton(master=window,text="Редактировать признаки класса",corner_radius=20,
            height=30,width=250,fg_color="gray38",hover_color="SkyBlue4",
            command= lambda: self.__class_editor(window)).place(x=20, y=240)

        TkinterCustomButton(master=window,text="Назад",corner_radius=20,
            height=30,width=250,fg_color="gray26",hover_color="SkyBlue4",
            command= window.destroy).place(x=20, y=300)

    def __class_editor(self, window):
        global selected_item
        try: 
            selected_item
        except NameError:
            self.__create_error("Выберите класс для редактирования")
        else:
            if selected_item != "":
                self.__edit_class(window, selected_item)
                del selected_item
            else:
                self.__create_error("Выберите класс для редактирования")

    def __edit_class(self, window, selected_item):
        self.__reload_window(window, "Радактор класса "+selected_item[0], 580, 500)
        Label(window, text="Класс:").place(x=20, y=20)
        Label(window, text=selected_item[0], font="Helvetica 14 bold").place(x=160, y=20)
        Label(window, text="Таблица признаков:").place(x=20, y=60)
        table = self.__create_table(window, 300, 540, 20, 80)
        self.__fill_extra(table, selected_item[0])

        TkinterCustomButton(master=window,text="Редактировать значение признака",corner_radius=20,
            height=30,width=250,fg_color="gray38",hover_color="SkyBlue4",
            command= lambda: self.__classfeature_editor(window, selected_item[0])).place(x=310, y=400)

        TkinterCustomButton(master=window,text="Очистить значения признака",corner_radius=20,
            height=30,width=250,fg_color="gray38",hover_color="SkyBlue4",
            command= lambda: self.__classfeature_deleter(table, selected_item[0])).place(x=20, y=400)

        TkinterCustomButton(master=window,text="Назад",corner_radius=20,
            height=30,width=250,fg_color="gray26",hover_color="SkyBlue4",
            command= lambda: [window.destroy() , self.gen()]).place(x=20, y=450)

    ## cut and to end
    def __classfeature_deleter(self, table, class_name):
        global selected_item
        try: 
            selected_item
        except NameError:
            self.__create_error("Выберите признак для очистки")
        else:
            if selected_item != "":
                self.__clear_classfeature(class_name, selected_item)
                self.__create_ok("Область значений признака очищена")
                self.__reload_extra(table, class_name)
                del selected_item
            else:
                self.__create_error("Выберите признак для очистки")
    ## cut here

    def __classfeature_editor(self, window, class_name):
        global selected_item
        try: 
            selected_item
        except NameError:
            self.__create_error("Выберите признак для редактирования")
        else:
            if selected_item != "":
                if selected_item[1] == "Перечислимый":
                    self.__edit_str(window, class_name, selected_item)
                else:
                    self.__edit_int(window, class_name, selected_item)
                del selected_item
            else:
                self.__create_error("Выберите признак для редактирования")

    def __edit_int(self, window, class_name, arguments):
        global selected_item
        if selected_item:
            del selected_item
        self.__reload_window(window, "Радактор интервального признака", 400, 250)
        Label(window, text="Признак:").place(x=20, y=20)
        Label(window, text=arguments[0], font="Helvetica 14 bold").place(x=160, y=20)
        Label(window, text="Тип признака:").place(x=20, y=60)
        Label(window, text=arguments[1], font="Helvetica 14 bold").place(x=160, y=60)
        Label(window, text="Область значений:").place(x=20, y=100)
        entry_pair = self.__create_entry_pair(window)
        entry_pair.place(x=20, y=140)
        Label(window, text="[").place(x=10, y=140)
        Label(window, text="]").place(x=380, y=140)
        limits = self.db.get_feature(arguments[0])
        if limits[2] == "None" or limits[2] == None:
            Label(window, text="Область значений не определена", fg="red3").place(x=20, y=170)
        else:
            parts = limits[2].split("-")
            Label(window, text="Введите значение от "+parts[0]+" до "+parts[1]+" включительно", fg="green3").place(x=20, y=170)
        self.__fill_entry_pair(entry_pair, class_name, arguments)
        TkinterCustomButton(master=window,text="Назад",corner_radius=20,height=30,width=140,
            fg_color="gray26",hover_color="SkyBlue4",command= lambda: self.__edit_class(window, [class_name])).place(x=20, y=200)
        TkinterCustomButton(master=window,text="Подтвердить",corner_radius=20,height=30,width=140,
            fg_color="gray38",hover_color="SkyBlue4",command=lambda: self.__update_feature_int(window, entry_pair, class_name, arguments, limits)).place(x=240, y=200)

    def __edit_str(self, window, class_name, arguments):
        global selected_item
        del selected_item
        feature_list = self.db.get_feature(arguments[0])

        self.__reload_window(window, "Радактор перечислимого признака", 520, 400)
        Label(window, text="Класс:").place(x=20, y=20)
        Label(window, text=class_name, font="Helvetica 14 bold").place(x=160, y=20)
        Label(window, text="Признак:").place(x=20, y=60)
        Label(window, text=feature_list[0], font="Helvetica 14 bold").place(x=160, y=60)
        Label(window, text="Доступные признаки:").place(x=20, y=100)
        table_left = self.__create_table(window, 200, 200, 20, 130)
        Label(window, text="Признаки класса:").place(x=300, y=100)
        table_right = self.__create_table(window, 200, 200, 300, 130)

        TkinterCustomButton(master=window,text="->",corner_radius=20,height=30,width=40,
            fg_color="gray38",hover_color="SkyBlue4",command=lambda: self.__pour_value(table_left, table_right)).place(x=240, y=170)
        TkinterCustomButton(master=window,text="<-",corner_radius=20,height=30,width=40,
            fg_color="gray38",hover_color="SkyBlue4",command=lambda: self.__pour_value(table_right, table_left)).place(x=240, y=210)
        TkinterCustomButton(master=window,text="Назад",corner_radius=20,height=30,width=200,
            fg_color="gray26",hover_color="SkyBlue4",command=lambda: self.__edit_class(window, [class_name])).place(x=20, y=350)
        TkinterCustomButton(master=window,text="Подтвердить",corner_radius=20,height=30,width=200,
            fg_color="gray38",hover_color="SkyBlue4",command=lambda: self.__update_feature_str(window, table_right, class_name, feature_list)).place(x=300, y=350)
        self.__fill_feats(table_left, feature_list[2])
        self.__fill_feats(table_right, arguments[2])
        self.__clean_extra(table_left, table_right)



        