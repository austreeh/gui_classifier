from tkinter import *
from knowbase import *
from tkinter_custom_button import TkinterCustomButton
from db import Database

from test_case import *

app = Tk()

# задаём размеры окна
app_width = 300
app_height= 200

# рассчитываем центр экрана
positionRight = int(app.winfo_screenwidth()/2 - app_width/2)
positionDown = int(app.winfo_screenheight()/2 - app_height/2)

# создаём окно, центрируем
app.title("Меню")
app.geometry(f'{app_width}x{app_height}+{positionRight}+{positionDown}')
app.pack_propagate(False)
app.resizable(0,0)
# класс для вызова

db = Database("data.db")

KB = knowbase()
S = solver(db)

# добавляем кнопки
knowbase_button = TkinterCustomButton(
    master=app,
    text="Редактор базы знаний", 
    corner_radius=20, 
    width=200,
    fg_color="gray38",
    hover_color="SkyBlue4", 
    command=KB.generate
    )
            
solver_button = TkinterCustomButton(
    master=app,
    text="Решатель задач",
    corner_radius=20,
    width=200,
    fg_color="gray38",
    hover_color="SkyBlue4",
    command = S.gen
    )

# располагаем кнопки
knowbase_button.place(relx=0.5, rely=0.3, anchor=CENTER)
solver_button.place(relx=0.5, rely=0.7, anchor=CENTER)

# луп
app.mainloop()



# 1. Диапазоны признаков интервальных, проверка и []
# 3. Разделить листинг и результаты