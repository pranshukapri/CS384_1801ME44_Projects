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
    
# Funtion for the quiz Selection Window...
def quiz_select(master):
    global quiz_no
    master.destroy()
    select = Tk()
    Label(select, text = "Choose the quiz you want to start: \n").pack(pady = 5, padx =10)
    
    quiz_name = StringVar()
    quiz_name.set(None)
    quizes = os.listdir("./quiz_wise_questions")
    i = 0
    for num in quizes:
        R = Radiobutton(select, text = num[:-4], variable=quiz_name, value = num)
        R.pack()
        i += 1
    Button(select, text = "OK", command = lambda : [select.destroy(), main_quiz(quiz_name.get())]).pack(pady = 20)
    select.mainloop()

# Main Function for the Realtime Quiz...   
def main_quiz(quiz_name):
    global ques_no
    global User_Name
    global User_Roll
    global quiz_no
    global marked
    global unatt
    quiz_no = quiz_name[:-4]
    
    quiz_window = Tk()
    #quiz_window.geometry("500x500")

    topframe = Frame(quiz_window)
    topframe.pack(side = TOP)
    midframe = Frame(quiz_window)
    midframe.pack(side = TOP)
    mid2frame = Frame(quiz_window)
    mid2frame.pack(side = TOP)
    bottomframe = Frame(quiz_window)
    bottomframe.pack(side = BOTTOM)

    #Binding Parameters
    quiz_window.bind('<Control-Alt-e>',database_to_csv_eventpress)
    quiz_window.bind('<Control-Alt-f>',end_quiz_eventpress)
    quiz_window.bind('<Control-Alt-u>',unattempted_ques_eventpress)

    with open("./quiz_wise_questions/" + quiz_name, 'r') as questions:
        read = csv.DictReader(questions, delimiter = ',')
        header = read.fieldnames
        list_ques = list(read)
        ques_no = 0
        q_no = []
        for x in range(len(list_ques)):
            marked.append(0)
            q_no.append(x+1)
        
        Q = Queue()
        max_time = re.search(r'=(\d+)', header[-1]).group(1)
        max_time = int(max_time) * 60
        t2 = threading.Thread(target=countdown, args=(max_time, Q))
        t2.start()
        
        selected_option = IntVar()
        selected_option.set(0)
        next_ques(list_ques, topframe, mid2frame, selected_option)
        Button(midframe, text = "Save & Next", command = lambda : next_ques(list_ques, topframe, mid2frame, selected_option)).pack(pady = 10, padx = 5, side = LEFT)
        Button(midframe, text = "Submit", command = lambda : end_quiz()).pack(pady = 10, padx = 5)
        
        var = IntVar()
        var.set(max_time)
        choice = IntVar()
        choice.set(0)
        unattempted = IntVar()
        Label(bottomframe, text = "Time Left: ").grid(row = 0, sticky = W)
        Label(bottomframe, textvariable = var).grid(row = 0, column = 1)
        Label(bottomframe, text = "Roll: ").grid(row = 1, sticky = W)
        Label(bottomframe, text = User_Roll).grid(row = 1, column = 1)
        Label(bottomframe, text = "Name: ").grid(row = 2, sticky = W)
        Label(bottomframe, text = User_Name).grid(row = 2, column = 1)
        Label(bottomframe, text = "Unattempted Questions: ").grid(row = 3, sticky = W)
        Label(bottomframe, textvariable = unattempted).grid(row = 3, column = 1)
        Label(bottomframe, text = "Goto Question: ").grid(row = 4, sticky = W)
        ttk.Combobox(bottomframe, values = q_no, textvariable=choice, width = 5).grid(row = 4, column = 1)
        Button(bottomframe, text = "Ok", command = lambda : goto_ques(list_ques, topframe, mid2frame, choice.get(), selected_option)).grid(row = 4, column = 2)
        
        keys_temp = list(list_ques[0].keys())
        del(keys_temp[-1])
        keys_temp.append("marked_choice")
        keys_temp.append("Total")
        keys_temp.append("Legend")
        with open("./individual_responses/" + quiz_no + "_" + User_Roll + ".csv", 'w', newline='') as indi:
            writer = csv.DictWriter(indi, fieldnames = keys_temp)
            writer.writeheader()
        
        while 1:
            var.set(Q.get())
            unattempted.set(unatt)
            try:
                quiz_window.update()
            except:
                break
            if stop_timer:
                break
        
        try:
            quiz_window.destroy()
        except:
            end_quiz()

# Function for the Save & Next Button Working...
def next_ques(list_ques, topframe, mid2frame, selected_option):
    global ques_no
    global total_marks
    global User_Roll
    global marked
    global unatt
    
    for widget in topframe.winfo_children():
       widget.destroy()
    
    if ques_no > 0 and len(list_ques) >= ques_no:
        marked[ques_no - 1] = int(selected_option.get())
    
    if len(list_ques) == ques_no:
        ques_no -= 1
    
    selected_option.set(marked[ques_no])
    Label(topframe, text = str(ques_no+1) + ". " + list_ques[ques_no]["question"] + "\n").pack(anchor = NW)
    R1 = Radiobutton(topframe, text=list_ques[ques_no]["option1"], variable=selected_option, value=1)
    R1.pack()
    R2 = Radiobutton(topframe, text=list_ques[ques_no]["option2"], variable=selected_option, value=2)
    R2.pack()
    R3 = Radiobutton(topframe, text=list_ques[ques_no]["option3"], variable=selected_option, value=3)
    R3.pack()
    R4 = Radiobutton(topframe, text=list_ques[ques_no]["option4"], variable=selected_option, value=4)
    R4.pack()
    
    Label(mid2frame, text = "Correct Ans: ").grid(row = 0, sticky = W)
    Label(mid2frame, text = list_ques[ques_no]["marks_correct_ans"]).grid(row = 0, column = 1)
    Label(mid2frame, text = "Wrong Ans: ").grid(row = 1, sticky = W)
    Label(mid2frame, text = list_ques[ques_no]["marks_wrong_ans"]).grid(row = 1, column = 1)
    Label(mid2frame, text = "Is Compulsory: ").grid(row = 2, sticky = W)
    Label(mid2frame, text = list_ques[ques_no]["compulsory"]).grid(row = 2, column = 1)
    Label(mid2frame, text = "").grid(row = 3)
    
    unatt = 0
    for i in marked:
        if not i:
            unatt += 1
    ques_no += 1

# Function for Goto Option (Called after clicking "OK" button)...
def goto_ques(list_ques, topframe, mid2frame, choice, selected_option):
    global ques_no
    global marked
    ques_no = choice - 1
    selected_option.set(marked[ques_no])
    
    for widget in topframe.winfo_children():
       widget.destroy()
    
    Label(topframe, text = str(ques_no+1) + ". " + list_ques[ques_no]["question"] + "\n").pack(anchor = NW)
    R1 = Radiobutton(topframe, text=list_ques[ques_no]["option1"], variable=selected_option, value=1)
    R1.pack()
    R2 = Radiobutton(topframe, text=list_ques[ques_no]["option2"], variable=selected_option, value=2)
    R2.pack()
    R3 = Radiobutton(topframe, text=list_ques[ques_no]["option3"], variable=selected_option, value=3)
    R3.pack()
    R4 = Radiobutton(topframe, text=list_ques[ques_no]["option4"], variable=selected_option, value=4)
    R4.pack()
    
    Label(mid2frame, text = "Correct Ans: ").grid(row = 0, sticky = W)
    Label(mid2frame, text = list_ques[ques_no]["marks_correct_ans"]).grid(row = 0, column = 1)
    Label(mid2frame, text = "Wrong Ans: ").grid(row = 1, sticky = W)
    Label(mid2frame, text = list_ques[ques_no]["marks_wrong_ans"]).grid(row = 1, column = 1)
    Label(mid2frame, text = "Is Compulsory: ").grid(row = 2, sticky = W)
    Label(mid2frame, text = list_ques[ques_no]["compulsory"]).grid(row = 2, column = 1)
    Label(mid2frame, text = "").grid(row = 3)
    
    ques_no += 1
