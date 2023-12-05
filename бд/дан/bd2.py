from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import redis

def clicked(txt, txt1, txt2, tree):
	try:
		p=int(txt2.get())
		if p<0:
			messagebox.showerror("Ошибка","Надо положительное число")	
			return
	except:
		messagebox.showerror("Ошибка","Надо число")
		return

	user=txt1.get()
	user1=txt.get()
	a=txt2.get()
	if a is None:
		a=0
	b=a
	# print("а="+str(a)+" "+"user="+user+" "+"user1="+user1)
	c=client.get(f'{user}:{user1}')
	if c is None:
		c=0
	a=int(a)+int(c)
	client.set(f'{user}:{user1}',str(a))
	c=client.get(f'{user}:summ')
	if c is None:
		c=0
	b=int(b)+int(c)
	client.set(f'{user}:summ',str(b))
	txt.delete(0, len(txt.get()))
	txt1.delete(0, len(txt1.get()))
	txt2.delete(0, len(txt2.get()))

	clicked1(tree)


def clicked1(tree):	
	tree.delete(*tree.get_children())
	a=int(client.get(f'Игорь:жюри 1'))+int(client.get(f'Игорь:жюри 2'))+int(client.get(f'Игорь:жюри 3'))+int(client.get(f'Игорь:жюри 4'))
	b=int(client.get(f'Дан:жюри 1'))+int(client.get(f'Дан:жюри 2'))+int(client.get(f'Дан:жюри 3'))+int(client.get(f'Дан:жюри 4'))
	c=int(client.get(f'Никита:жюри 1'))+int(client.get(f'Никита:жюри 2'))+int(client.get(f'Никита:жюри 3'))+int(client.get(f'Никита:жюри 4'))
	d=int(client.get(f'Кирилл:жюри 1'))+int(client.get(f'Кирилл:жюри 2'))+int(client.get(f'Кирилл:жюри 3'))+int(client.get(f'Кирилл:жюри 4'))
	# people =[("Игорь", 0, 0, 0, 0, 0),("Дан", 0, 0, 0, 0, 0),("Никита", 0, 0, 0, 0, 0),("Кирилл", 0, 0, 0, 0, 0)]
	people=[("Игорь", client.get(f'Игорь:жюри 1'), client.get(f'Игорь:жюри 2'), client.get(f'Игорь:жюри 3'), client.get(f'Игорь:жюри 4'), int(a)), 
	("Дан", client.get(f'Дан:жюри 1'), client.get(f'Дан:жюри 2'), client.get(f'Дан:жюри 3'), client.get(f'Дан:жюри 4'),int(b)),
	("Никита", client.get(f'Никита:жюри 1'), client.get(f'Никита:жюри 2'), client.get(f'Никита:жюри 3'), client.get(f'Никита:жюри 4'), int(c)),
	("Кирилл", client.get(f'Кирилл:жюри 1'), client.get(f'Кирилл:жюри 2'), client.get(f'Кирилл:жюри 3'), client.get(f'Кирилл:жюри 4'), int(d)),
	]
	people.sort(key=lambda x: -x[5])
	for person in people:
		tree.insert("", END, values=person)


client = redis.StrictRedis(charset="utf-8",decode_responses=True) 
root = Tk()
root.title("Лаба 2")
root.geometry("1200x400") 

people =[("Игорь", 0, 0, 0, 0, 0),("Дан", 0, 0, 0, 0, 0),("Никита", 0, 0, 0, 0, 0),("Кирилл", 0, 0, 0, 0, 0)]

columns = ("name", "age1", "age2", "age3", "age4", "age5")
 
tree = ttk.Treeview(columns=columns, show="headings")
# tree.pack(fill=BOTH, expand=1)
tree.grid(column=0, row=0) 
tree.heading("name", text="Имя")
tree.heading("age1", text="жюри 1")
tree.heading("age2", text="жюри 2")
tree.heading("age3", text="жюри 3")
tree.heading("age4", text="жюри 4")
tree.heading("age5", text="сумма") 
# добавляем данные
for person in people:
    tree.insert("", END, values=person)
clicked1(tree)

lbl = ttk.Label(text="Жюри")  
lbl.grid(column=0, row=1)  
txt = ttk.Entry(width=10)  
txt.grid(column=0, row=2)


lbl1 = ttk.Label(text="Спортсмен")  
lbl1.grid(column=0, row=3)
txt1 = ttk.Entry(width=10)  
txt1.grid(column=0, row=4)


lbl = ttk.Label(text="Баллы")  
lbl.grid(column=0, row=5)
txt2 = ttk.Entry(width=10)  
txt2.grid(column=0, row=6)

my_button = ttk.Button(text="Сохранить результаты", command=lambda : clicked(txt, txt1, txt2, tree))
my_button.grid(column=0, row=7)

 
root.mainloop()