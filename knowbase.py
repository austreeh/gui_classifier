from tkinter import *

from tkinter_custom_button import TkinterCustomButton

from edit_feature import *
from edit_class import *
from class_list import *
from features_list import *
from checker_win import *

from db import Database

db = Database("data.db")

class knowbase():
    def __init__(self):
        self.EF = edit_feature_window(db) 
        self.EC = edit_class_window(db)
        self.CL = class_list_window(db)
        self.FL = features_list_window(db)
        self.CH = checker_window(db)
        # self.Ch = checker()

    def generate(self):
        
        window = Tk()

        # задаём размеры окна
        window_width = 400
        window_height= 500

        # рассчитываем центр экрана
        positionRight = int(window.winfo_screenwidth()/2 - window_width/2)
        positionDown = int(window.winfo_screenheight()/2 - window_height/2)

        # создаём окно, центрируем
        window.title("Редактор базы знаний")
        window.geometry(f'{window_width}x{window_height}+{positionRight}+{positionDown}')
        window.pack_propagate(False)
        window.resizable(0,0)

        # добавляем кнопки
        edit_Flist_button = TkinterCustomButton(
            master=window,
            text="Список признаков",
            corner_radius=20,
            width=300,
            fg_color="gray38",
            hover_color="SkyBlue4",
            command=self.FL.gen
        )

        edit_Frang_button = TkinterCustomButton(
            master=window,
            text="Области значений признаков",
            corner_radius=20,
            width=300,
            fg_color="gray38",
            hover_color="SkyBlue4",
            command=self.EF.gen
        )

        edit_Clist_button = TkinterCustomButton(
            master=window,
            text="Список классов",
            corner_radius=20,
            width=300,
            fg_color="gray38",
            hover_color="SkyBlue4",
            command=self.CL.gen
        )

        edit_Cfeat_button = TkinterCustomButton(
            master=window,
            text="Значения признаков для классов",
            corner_radius=20,
            width=300,
            fg_color="gray38",
            hover_color="SkyBlue4",
            command=self.EC.gen
        )

        check_integrity_b = TkinterCustomButton(
            master=window,
            text="Проверить целостность",
            corner_radius=20,
            width=300,
            fg_color="gray38",
            hover_color="SkyBlue4",
            command=self.CH.gen
        )

        back_to_menu = TkinterCustomButton(
            master=window,
            text="Закрыть",
            corner_radius=20,
            width=150,
            fg_color="gray26",
            hover_color="SkyBlue4",
            command=window.destroy
        )

        # расставляем кнопки
        edit_Flist_button.place(relx=0.5, rely=0.15, anchor=CENTER)
        edit_Frang_button.place(relx=0.5, rely=0.29, anchor=CENTER)
        edit_Clist_button.place(relx=0.5, rely=0.43, anchor=CENTER)
        edit_Cfeat_button.place(relx=0.5, rely=0.57, anchor=CENTER)
        check_integrity_b.place(relx=0.5, rely=0.71, anchor=CENTER)
        back_to_menu.place(relx=0.5, rely=0.85, anchor=CENTER)


