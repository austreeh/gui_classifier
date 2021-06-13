from os import chdir
from tkinter import *
from tkinter import ttk

from tkinter_custom_button import TkinterCustomButton

# класс - редактирование области значений признака
class edit_feature_window():

    global selected_item

    def __init__(self, db):
        self.db = db

    # интерфейсные штуки
    def __reload_window(self, window, new_title, new_width, new_height):
        for widgets in window.winfo_children():
            widgets.destroy()
        positionRight = int(window.winfo_screenwidth()/2 - new_width/2)
        positionDown = int(window.winfo_screenheight()/2 - new_height/2)
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

    def __create_entry_pair(self, window):
        frame = Frame(window, width = 37)
        ent1 = Entry(frame, textvariable="", width=16)
        ent1.grid(row=0, column=0)
        Label(frame, text="до", width=5).grid(row=0, column=1)
        ent2 = Entry(frame, textvariable="", width=16)
        ent2.grid(row=0, column=2)
        return frame

    def __fill_entry_pair(self, frame, value):
        childs = []
        for child in frame.winfo_children():
            childs.append(child)
        if value != "None":
            vals = value.split("-")
            childs[0].insert(0,vals[0])
            childs[2].insert(0,vals[1])

    # функциональные штуки
    def __fill_table(self, table, slice_int):
        table["column"]= self.db.columns_features()[:slice_int]
        table["show"]="headings"
        for column in table["column"]:
            table.heading(column, text=column)
        for row in self.db.fetch_features():
            table.insert("", END, values=row[:slice_int])

    def __fill_feats(self, table, input_str):
        table["column"]="значения"
        table["show"] = "headings"
        table.heading("значения", text="значения")
        if input_str != "None":
            values = list(map(str.strip, input_str.split(',')))
            for element in values:
                table.insert("", END, values=element)
    
    def __reload_table(self, table, slice_int, ship=0):
        for i in table.get_children(): 
            table.delete(i) 
        for row in self.db.fetch_features():
            table.insert("", END, values=row[:slice_int])

    def __add_to_table(self, table, value):
        curr_vals = []
        for line in table.get_children():
            for val in table.item(line)['values']:
                curr_vals.append(val)
        if value.isalpha():
            if value in curr_vals:
                self.__create_error("Значение уже в списке")
            else:
                table.insert("", END, values=value)
                self.__create_ok("Значение успешно добавлено")
        else:
            self.__create_error("Значение содержит недопустимые символы")

    def __del_from_table(self, table):
        item = table.selection()[0]
        if item:
            table.delete(item)

    def __select_item(self, event, table):
        global selected_item
        curr_item = table.focus()
        selected_item = table.item(curr_item)['values'][0:3]
        print(selected_item)

    def __update_feature_str(self, window, table, arguments):
        curr_vals = []
        for line in table.get_children():
            for val in table.item(line)['values']:
                curr_vals.append(val)
        self.__fit_database_str(arguments[0], curr_vals)
        if curr_vals == []:
            arguments[2] = None
        else:
            for i in range(1, len(curr_vals)):
                curr_vals[0] += ", "+curr_vals[i]
            arguments[2] = curr_vals[0]
        self.db.update_feature(arguments[0], arguments)
        
        self.__create_ok("Область значений обновлена")
        window.destroy()
        self.gen()

    def __update_feature_int(self, window, frame, arguments):
        # check values
        childs = []
        for child in frame.winfo_children():
            childs.append(child)
        if childs[0].get().isdigit() and childs[2].get().isdigit():
            if int(childs[0].get()) <= int(childs[2].get()):
                if int(childs[0].get()) >= 0 and int(childs[2].get()) >=0:
                    arguments[2] = childs[0].get() + "-" + childs[2].get()
                    self.__fit_database_int(int(childs[0].get()), int(childs[2].get()), arguments[0])
                    self.db.update_feature(arguments[0], arguments)
                    self.__create_ok("Область значений обновлена")
                    window.destroy()
                    self.gen()
                else:
                    self.__create_error("Отрицательные числа запрещены")
            else:
                self.__create_error("Левая граница больше правой")
        else:
            self.__create_error("Область значений должна содержать числа")
        

    def __clear_feature(self, arguments):
        arguments[2] = None
        self.db.update_feature(arguments[0], arguments)

    # затычки
    def fake_func(self, window):
        print("fake_func placed")
        pass

    # само окно генерации
    def gen(self):
        window = Tk()
        self.__reload_window(window, "Радактор области значений признаков", 620, 440)
        table = self.__create_table(window, 300, 580, 20, 20)
        self.__fill_table(table, 3)

        TkinterCustomButton(master=window,text="Редактировать область значений",corner_radius=20,
            height=30,width=280,fg_color="gray38",hover_color="SkyBlue4",
            command= lambda: self.__feature_editor(window)).place(x=315, y=340)

        TkinterCustomButton(master=window,text="Очистить область значений",corner_radius=20,
            height=30,width=280,fg_color="gray38",hover_color="SkyBlue4",
            command= lambda: self.__feature_deleter(window, table)).place(x=20, y=340)

        TkinterCustomButton(master=window,text="Назад",corner_radius=20,
            height=30,width=150,fg_color="gray26",hover_color="SkyBlue4",
            command= window.destroy).place(x=20, y=390)

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

    ## cut and to end
    def __feature_deleter(self, window, table):
        global selected_item
        try: 
            selected_item
        except NameError:
            self.__create_error("Выберите признак для редактирования")
        else:
            if selected_item != "":
                self.__clear_feature(selected_item)
                self.__create_ok("Область значений признака очищена")
                self.__reload_table(table, 3)
                self.__clear_database_f_name(selected_item[0])
                del selected_item
            else:
                self.__create_error("Выберите признак для редактирования")
    ## cut here

    def __edit_feature(self, window, arguments):
        if arguments[1] == "Перечислимый":
            self.__edit_str(window, arguments)
        else:
            self.__edit_int(window, arguments)

    def __edit_int(self, window, arguments):
        global selected_item
        del selected_item
        self.__reload_window(window, "Радактор интервального признака", 400, 230)
        Label(window, text="Название признака:").place(x=20, y=20)
        Label(window, text=arguments[0], font="Helvetica 14 bold").place(x=160, y=20)
        Label(window, text="Тип признака:").place(x=20, y=60)
        Label(window, text=arguments[1], font="Helvetica 14 bold").place(x=160, y=60)
        Label(window, text="Область значений:").place(x=20, y=100)
        entry_pair = self.__create_entry_pair(window)
        entry_pair.place(x=20, y=140)
        self.__fill_entry_pair(entry_pair, arguments[2])
        Label(window, text="[").place(x=10, y=140)
        Label(window, text="]").place(x=380, y=140)
        TkinterCustomButton(master=window,text="Назад",corner_radius=20,height=30,width=140,
            fg_color="gray26",hover_color="SkyBlue4",command=lambda: [window.destroy(), self.gen()]).place(x=20, y=180)
        TkinterCustomButton(master=window,text="Обновить",corner_radius=20,height=30,width=140,
            fg_color="gray38",hover_color="SkyBlue4",command=lambda: self.__update_feature_int(window, entry_pair, arguments)).place(x=240, y=180)

    def __edit_str(self, window, arguments):
        global selected_item
        del selected_item
        self.__reload_window(window, "Радактор перечислимого признака", 400, 400)
        Label(window, text="Название признака:").place(x=20, y=20)
        Label(window, text=arguments[0], font="Helvetica 14 bold").place(x=160, y=20)
        Label(window, text="Тип признака:").place(x=20, y=60)
        Label(window, text=arguments[1], font="Helvetica 14 bold").place(x=160, y=60)
        Label(window, text="Область значений:").place(x=20, y=100)
        table = self.__create_table(window, 200, 200, 20, 130)

        ent = Entry(window, textvariable="", width=14)
        ent.place(x=240, y=130)
        TkinterCustomButton(master=window,text="+",corner_radius=20,height=30,width=140,
            fg_color="gray38",hover_color="SkyBlue4",command=lambda: self.__add_to_table(table, ent.get())).place(x=240, y=170)
        TkinterCustomButton(master=window,text="удалить",corner_radius=20,height=30,width=140,
            fg_color="gray38",hover_color="SkyBlue4",command=lambda: self.__del_from_table(table)).place(x=240, y=210)
        TkinterCustomButton(master=window,text="Назад",corner_radius=20,height=30,width=140,
            fg_color="gray26",hover_color="SkyBlue4",command=lambda: [window.destroy(), self.gen()]).place(x=20, y=350)
        TkinterCustomButton(master=window,text="Подтвердить",corner_radius=20,height=30,width=140,
            fg_color="gray38",hover_color="SkyBlue4",command=lambda: self.__update_feature_str(window, table, arguments)).place(x=240, y=350)
        self.__fill_feats(table, arguments[2])

    def __fit_database_int(self, left_val, right_val, feature_name):

        print(left_val, right_val, feature_name)
        for row in self.db.fetch_classes():
            curr_val = self.db.select_Cfeature(row[0], feature_name)[0]

            if curr_val != None and curr_val != "None":
                parts = curr_val.split("-")
                if int(parts[0]) < left_val or int(parts[1]) > right_val:
                    self.db.update_Cfeature(row[0], feature_name, "None")
    
    def __fit_database_str(self, feature_name, new_vals):
        print(feature_name)
        for row in self.db.fetch_classes():
            curr_vals = self.db.select_Cfeature(row[0], feature_name)[0]
            
            if curr_vals != None and curr_vals != "None":
                curr_vals = curr_vals.split(",")
                print("class ",row[0], "curr_vals ",curr_vals, "new_vals ", new_vals)
                curr_vals = list(map(str.strip, curr_vals))
                if new_vals != None and new_vals != "None" and new_vals != []:
                    for element in curr_vals:
                        if element not in new_vals:
                            print("element to delete-"+element+"-",new_vals)
                            curr_vals.remove(element)
                    if curr_vals == []:
                        self.db.update_Cfeature(row[0], feature_name, "None")
                    else:
                        curr_vals = ", ".join(curr_vals)
                        self.db.update_Cfeature(row[0], feature_name, curr_vals)       
                else:
                    self.db.update_Cfeature(row[0], feature_name, "None")
    
    def __clear_database_f_name(self, feature_name):
        for row in self.db.fetch_classes():
            self.db.update_Cfeature(row[0], feature_name, "None")

    
