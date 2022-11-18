from tkinter import *
import sqlite3

root = Tk()
root.title("MyToDoList")

Connection = sqlite3.connect("myToDoListDB.db")

cursor = Connection.cursor()

cursor.execute("""
    CREATE TABLE if not exists myToDoListDB
    ( id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    description TEXT NOT NULL,
    completed BOOLEAN NOT NULL)
""")

Connection.commit()

def delDo(id):
    def _delDo():
        cursor.execute("DELETE FROM myToDoListDB WHERE id = ?", (id, ))
        Connection.commit()
        showToDo()
    return _delDo


#Currying 
def complete(id):
    def _complete():
        toDo = cursor.execute("SELECT * FROM myToDoListDB WHERE id = ?", (id, )).fetchone()
        cursor.execute("UPDATE myToDoListDB SET completed = ? WHERE id = ?", (not toDo[3], id))
        Connection.commit()
        showToDo()
        #print(id)
    return _complete

    

def showToDo():
    shows = cursor.execute("""
    SELECT * FROM myToDoListDB
    """).fetchall()
    #print(shows)
    for widget in frame.winfo_children():
        widget.destroy()

    for i in range(0, len(shows)):
        id = shows[i][0]
        completed = shows[i][3]
        description = shows[i][2]
        color = '#777' if completed else "#000"
        Check = Checkbutton(frame,text=description,fg = color, width=42, anchor=W, command=complete(id))
        Check.grid(row=i, column=0 )
        delButton = Button(frame, text='Delete', command=delDo(id))
        if completed: delButton.grid(row = i, column=1)
        Check.select() if completed else Check.deselect

def addToDo():
    toDo = newTask.get()
    if toDo:
        cursor.execute("""
        INSERT INTO myToDoListDB (description, completed) VALUES (?,?)
        """, (toDo, False))
        Connection.commit()
        newTask.delete(0, END)
        showToDo()
    else: 
        pass






doLabel = Label(root, text="Do")
doLabel.grid(row=0, column=0)

newTask = Entry(root, width=40)
newTask.grid(row=0,column=1)

addButton = Button(root, text='Add', command=addToDo)
addButton.grid(row=0,column=2)

frame = LabelFrame(root,text="My Do's", padx=5,pady=5)
frame.grid(row=1, column=0, columnspan=3, sticky='nswe', padx=5)

newTask.focus()
root.bind('<Return>', lambda x: addToDo())

showToDo()

root.mainloop()