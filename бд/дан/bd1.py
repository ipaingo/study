import redis
from tkinter import * 
from tkinter.ttk import Combobox 
from tkinter import scrolledtext 

color="black"
sh="Arial"
raz="16"
nach=""

def clicked(user, a, b, c, d, combo, combo1, spin, txt1,txt10, txt):
	client.set(f'{user}:color',a)
	client.set(f'{user}:family',b)
	client.set(f'{user}:size',c)
	client.set(f'{user}:nach',d)
	callback(user,combo, combo1, spin, txt1,txt10, txt)

def callback(user, combo, combo1, spin, txt1, txt10, txt):
	global color,sh,raz,nach
	color=str(client.get(f'{user}:color'))
	sh=str(client.get(f'{user}:family'))
	raz=int(client.get(f'{user}:size'))
	nach=str(client.get(f'{user}:nach'))

	combo.delete(0, len(combo.get()))
	combo.insert(0, sh)

	combo1.delete(0, len(combo1.get()))
	combo1.insert(0, color)

	spin.delete(0, len(spin.get()))
	spin.insert(0, raz)

	txt1.delete(0, len(txt1.get()))
	txt1.insert(0, nach)

	clicked1(txt10, txt)

def clicked1(txt10, text):
	global color,sh,raz,nach
	sr=""  
	sr=sh + " " + str(raz) + " " + nach
	print(sr+"dqwqwefw")
	if not sr:return
	txt10.configure(font = sr, fg = color)
	# txt10['font']=sh
	txt10.delete(1.0, END)
	txt10.insert(1.0,text)



client = redis.StrictRedis(charset="utf-8",decode_responses=True)
window = Tk() 
window.title("ЛАба 1")
window.geometry("1200x700")

# my_button1 = tk.Button(windowAccounts, text="Сбросить")
# my_button.place(x=50, y=50)
lbl = Label(window, text="Имя пользователя")  
lbl.place(x=50, y=100)
entry_user = Combobox(window)
entry_user['values']=("Ройтбурд Дан", "Анисиомв Никита", "Кошкарев Игорь", "Кручинин Никита")
entry_user.current(1)
entry_user.place(x=200, y=100)

lb2 = Label(window, text="Название шрифта")  
lb2.place(x=50, y=300)
combo = Entry(window, width=50)  
# combo['values'] = ("Master of Festival", "Minotaur Jugendstil", "Novartis Deco", "Proserpina Deco", "Odalisque Deco", "Rhythm and Jazz Decor", "Diplomatia Two", "Mysteria Nouveau", "Davida Decor", "Grotesque Bourgeoisie", "Sea Breez Swash")  
# combo.current(1)  # установите вариант по умолчанию  
combo.place(x=170, y=300)  

lb3 = Label(window, text="Размер шрифта")  
lb3.place(x=50, y=350)
spin = Entry(window, width=5)  
spin.place(x=170, y=350)

lb4 = Label(window, text="Цвет шрифта")  
lb4.place(x=50, y=400)
combo1 = Combobox(window)  
combo1['values'] = ("black", "blue", "red", "white", "green", "pink", "grey", "purple", "yellow", "orange")  
combo1.current(1)    
combo1.place(x=170, y=400)  


lb5 = Label(window, text="Начертания")  
lb5.place(x=50, y=450)
txt1 = Entry(window,width=50)  
txt1.place(x=170, y=450)

my_button = Button(window, text="Сохранить настройки", command=lambda : clicked(entry_user.get(), combo1.get(), combo.get(), spin.get(), txt1.get(), combo, combo1, spin, txt1,txt10, txt))
my_button.place(x=75, y=500)

lb3 = Label(window, text="текс")  
lb3.place(x=500, y=50)
txt2 = Entry(window, width=75)  
txt2.place(x=500, y=100,height=75)

lb10 = Label(window, text="перевод")  
lb10.place(x=500, y=350)
txt10 = Text(window, width=75)  
txt10.place(x=500, y=400,height=75)


entry_user.bind("<<ComboboxSelected>>", lambda e:callback(entry_user.get(), combo, combo1, spin, txt1,txt10, txt2.get()))
txt2.bind("<KeyRelease>",lambda e: clicked1(txt10, txt2.get()))
# entry_user.bind("<<FocusIn>>", lambda e: clicked1(txt10, txt2.get()))




my_button = Button(window, text="переделать", command=lambda : clicked1(txt10, txt2.get()))
my_button.place(x=600, y=50)

txt3 = Label(window, width=40, height=10)  
txt3.place(x=500, y=200)



window.mainloop()

if __name== '__main__':
	main()
# client.close()