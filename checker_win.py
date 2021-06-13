from tkinter import *
from tkinter import ttk

from tkinter_custom_button import TkinterCustomButton

# класс - редактирование области значений признака
class checker_window():

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

    # функциональные штуки
    def __fill_table(self, table):
        table["column"]= self.db.columns_classes()
        table["show"]="headings"
        for column in table["column"]:
            table.heading(column, text=column)
        for row in self.db.fetch_classes():
            check_mass = []
            check_mass.append(row[0])
            for i in range(1, len(row)):
                if row[i] == "None" or row[i] == None or row[i] == ["None"] or row[i] == [None]:
                    check_mass.append("\u274c")
                else:
                    check_mass.append("\u2714")
            table.insert("", END, values=check_mass)
    
    def __select_item(self, event, table):
        global selected_item
        curr_item = table.focus()
        selected_item = table.item(curr_item)['values'][0:3]
        print(selected_item)

    # само окно генерации
    def gen(self):
        window = Tk()
        self.__reload_window(window, "Проверка целостности классов", 800, 370)
        table = self.__create_table(window, 300, 760, 20, 20)
        self.__fill_table(table)

        TkinterCustomButton(master=window,text="Назад",corner_radius=20,height=30,width=140,
            fg_color="gray26",hover_color="SkyBlue4",command=window.destroy).place(x=20, y=330)
