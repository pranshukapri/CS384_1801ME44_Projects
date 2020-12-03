import time 
import threading
import os
import csv
import re
import sqlite3
from tkinter import *
from tkinter import ttk
from queue import Queue
from tkinter import messagebox as ms
with sqlite3.connect('project1_quiz_cs384.db') as db:
    c = db.cursor()
    
c.execute('CREATE TABLE IF NOT EXISTS project1_registration (Name TEXT NOT NULL PRIMARY KEY,password TEXT NOT NULL,Roll_No TEXT,Whatsapp_No TEXT)')
c.execute('CREATE TABLE IF NOT EXISTS project1_marks (Roll_No TEXT NOT NULL,quiz_num TEXT NOT NULL,total_marks REAL)')
db.commit()
db.close()

class abc():
    def __init__(self):
    	# Window 
        
        self.rootabc = Tk()
        self.master=self.rootabc
        # Some Usefull variables
        self.roll=StringVar()
        self.l_roll=StringVar()
        self.whtsapp=StringVar()
        self.Name = StringVar()
        self.password = StringVar()
        self.n_username = StringVar()
        self.n_password = StringVar()
        #Create Widgets
        self.widgets()
        self.rootabc.mainloop()
    def quit(self):
        self.rootabc.destroy()
        
    #Login Function
    def login(self):
    	#Establish Connection
        with sqlite3.connect('project1_quiz_cs384.db') as db:
            c = db.cursor()

        #Find project1_registration If there is any take proper action
        find_user = ('SELECT * FROM project1_registration WHERE Roll_No = ? and password = ?')
        m=c.execute(find_user,[(self.l_roll.get()),(self.password.get())])
        
        result = c.fetchall()
        
        ###GOTO NEXT WINDOW
        if result:
            #print("Success")
            self.logf.pack_forget()
            global User_Roll
            global User_Name
            User_Roll=result[0][2]
            User_Name=result[0][0]
            quiz_select(self.master)
        else:
            ms.showerror('Oops!','Some fields are either invalid or user not registered.')
            
    def new_user(self):
    	#Establish Connection
        with sqlite3.connect('project1_quiz_cs384.db') as db:
            c = db.cursor()

        #Find Existing Name if any take proper action
        find_user = ('SELECT Roll_No FROM project1_registration WHERE Roll_No = ?')
        c.execute(find_user,[(self.roll.get())])        
        if c.fetchall():
            ms.showerror('Error!','Roll No Already exists.')
        else:
            ms.showinfo('Success!','Account Created!')
            self.log()
        #Create New Account 
        insert = 'INSERT INTO project1_registration(Name,password,Roll_No,Whatsapp_No) VALUES(?,?,?,?)'
        c.execute(insert,[(self.n_username.get()),(self.n_password.get()),(self.roll.get()),(self.whtsapp.get())])
        db.commit()

        #Frame Packing Methords
    def log(self):
        self.Name.set('')
        self.password.set('')
        self.crf.pack_forget()
        self.head['text'] = 'LOGIN'
        self.logf.pack()
    def cr(self):
        self.n_username.set('')
        self.n_password.set('')
        self.logf.pack_forget()
        self.head['text'] = 'Create Account'
        self.crf.pack()
        
    #Draw Widgets
    def widgets(self):
        self.head = Label(self.master,text = 'LOGIN',font = ('',35),pady = 10)
        self.head.pack()
        self.logf = Frame(self.master,padx =10,pady = 10)
        Label(self.logf,text = 'Roll No: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.logf,textvariable = self.l_roll,bd = 5,font = ('',15)).grid(row=0,column=1)
        Label(self.logf,text = 'Password: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.logf,textvariable = self.password,bd = 5,font = ('',15),show = '*').grid(row=1,column=1)
        Button(self.logf,text = ' Login ',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.login).grid()
        Button(self.logf,text = ' Create Account ',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.cr).grid(row=2,column=1)
        self.logf.pack()
        
        self.crf = Frame(self.master,padx =10,pady = 10)
        Label(self.crf,text = 'Name: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.crf,textvariable = self.n_username,bd = 5,font = ('',15)).grid(row=0,column=1)
        Label(self.crf,text = 'Password: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.crf,textvariable = self.n_password,bd = 5,font = ('',15),show = '*').grid(row=1,column=1)

        Label(self.crf,text = 'Roll No: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.crf,textvariable = self.roll,bd = 5,font = ('',15)).grid(row=2,column=1)
        Label(self.crf,text = 'Whatsapp_No: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.crf,textvariable = self.whtsapp,bd = 5,font = ('',15)).grid(row=3,column=1)


        Button(self.crf,text = 'Create Account',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.new_user).grid()
        Button(self.crf,text = 'Go to Login',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.log).grid(row=4,column=1)
        
# Countdowm Function for Timer...
def countdown(t,Q): 
    global stop_timer
    while t: 
        mins, secs = divmod(t, 60) 
        timer = '{:02d}:{:02d}'.format(mins, secs)
        Q.put(timer)
        time.sleep(1) 
        t -= 1
        if stop_timer:
            break
    if t == 0:
        end_quiz()

# Function for initial Login/Signup...
def login_window():
    win=abc()