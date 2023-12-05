import pymongo
from tkinter import * 
from tkinter.ttk import Combobox 
from tkinter import scrolledtext 

client = pymongo.MongoClient('192.168.112.103')
database = client['22303']

Play = database["Dan_Play"]
Team = database["Dan_Team"]
# Play.delete_many({})
# Team.delete_many({})


def openn(entry_user, txt3):
	if entry_user.get()=='team' :
		openn2(txt3)
	else :
		openn1(txt3)

def openn1(txt3):
	window1 = Tk() 
	window1.title("вывод")
	window1.geometry("1500x600")
	group='$group'
	ty2='$avg'
	ty3="_id"
	s=''
	for qwe in Play.aggregate([{group:{"name" ,"city","coach" ,"players" , "reserve" }}]): #
		s+=str(qwe.values())+"\n"
	lb2 = Label(window1, text=s)  
	lb2.place(x=100, y=100)
	print(s)
	window1.mainloop()

def openn2(txt3):
	window1 = Tk() 
	window1.title("вывод")
	window1.geometry("1500x600")
	s=""
	ty='$group'
	ty2='$avg'
	ty3="_id"
	hg=txt3.get()
	for qwe in Team.aggregate(): #{ty:{ty2:txt3.get()},{ty3:0,}}
		s+=str(qwe.values())+"\n"
	scroll_bar = Scrollbar(window1)
  
	scroll_bar.pack( side = BOTTOM,
                fill = Y )
	lb2 = Label(window1, text=s)  
	lb2.place(x=10, y=10)	
	print(s)
	# scroll_bar.config( command = lb2.yview )
	window1.mainloop()
	


window = Tk() 
window.title("ЛАба 4.1")
window.geometry("800x500")
x=50
lb = Label(window, text="таблица")  
lb.place(x=100, y=x)
entry_user = Combobox(window)
entry_user['values']=("Play", "team")
entry_user.current(1)
entry_user.place(x=200, y=x)
x=x+75
lb3 = Label(window, text="вопрос")  
lb3.place(x=100, y=x)
txt3 = Entry(window, width=70)  
txt3.place(x=325, y=x)
x=x+75

my_button2 = Button(window, text="результат", command=lambda :openn(entry_user, txt3))
my_button2.place(x=500, y=x)

window.mainloop()