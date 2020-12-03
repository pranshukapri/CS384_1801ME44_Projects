import time 
import threading
import os
import csv
import re
import sqlite3
import hashlib
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
        m=c.execute(find_user,[(self.l_roll.get()),str(hashlib.sha256(self.password.get().encode('utf-8')).hexdigest())])
        
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
        c.execute(insert,[(self.n_username.get()),str(hashlib.sha256(self.n_password.get().encode('utf-8')).hexdigest()),(self.roll.get()),(self.whtsapp.get())])
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
    stop_timer = False
    while t: 
        mins, secs = divmod(t, 60) 
        timer = '{:02d}:{:02d}'.format(mins, secs)
        Q.append(timer)
        time.sleep(1) 
        t -= 1
        if stop_timer:
            break
    if t == 0:
        stop_timer = True
        
    #print("countdown")
        
# Function for initial Login/Signup...
def login_window():
    abc()
    #print("login window")
    
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
    #print("quiz select")

# Main Function for the Realtime Quiz...   
def main_quiz(quiz_name):
    global ques_no
    global User_Name
    global User_Roll
    global quiz_no
    global marked
    global unatt
    global stop_timer
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
        
        Q = []
        max_time = re.search(r'=(\d+)', header[-1]).group(1)
        max_time = int(max_time) * 60
        t2 = threading.Thread(target=countdown, args=(max_time, Q))
        t2.start()
        
        selected_option = IntVar()
        selected_option.set(0)
        next_ques(list_ques, topframe, mid2frame, selected_option)
        Button(midframe, text = "Save & Next", command = lambda : next_ques(list_ques, topframe, mid2frame, selected_option)).pack(pady = 10, padx = 5, side = LEFT)
        Button(midframe, text = "Submit", command = lambda : end_quiz(quiz_window)).pack(pady = 10, padx = 5)
        
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
            if len(Q) > 0:
                var.set(Q[0])
                Q.pop()
            unattempted.set(unatt)
            try:
                quiz_window.update()
            except:
                break
            if stop_timer:
                break
        
        end_quiz(quiz_window)
    
    #print("main quiz")

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
    
    #print("next ques")

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
    
    #print("goto ques")

# Function for Evaluating the final parameters and putting into the csv file...
def evalute():
    global marked
    global total_marks
    global quiz_no
    global User_Roll
    
    i = 0
    total_quiz_marks = 0
    dict_temp = {}
    list_ques = []
    
    with open("./quiz_wise_questions/" + quiz_no + ".csv", 'r') as questions:
        read = csv.DictReader(questions, delimiter = ',')
        list_ques = list(read)
    for row in list_ques:
        total = 0
        dict_temp = row
        dict_temp.popitem()
        dict_temp["marked_choice"] = marked[i]
        dict_temp["Total"] = 0
        dict_temp["Legend"] = "Unanswered"
    
        with open("./individual_responses/" + quiz_no + "_" + User_Roll + ".csv", 'a', newline='') as indi:
            writer = csv.DictWriter(indi, fieldnames = dict_temp.keys())
        
            if row["compulsory"] == 'y':
                if int(marked[i]) == int(row["correct_option"]):
                    total = int(row["marks_correct_ans"])
                    dict_temp["Legend"] = "Correct Choice"
                else:
                    total = int(row["marks_wrong_ans"])
                    if int(marked[i]):
                        dict_temp["Legend"] = "Wrong Choice"
                    else:
                        dict_temp["Legend"] = "Wrong Choice (Unattempted)"
            else:
                if int(marked[i]) == int(row["correct_option"]):
                    total = int(row["marks_correct_ans"])
                    dict_temp["Legend"] = "Correct Choice"
                elif int(marked[i]):
                    total = int(row["marks_wrong_ans"])
                    dict_temp["Legend"] = "Wrong Choice"
            dict_temp["Total"] = total
            total_marks = total_marks + total
            total_quiz_marks = total_quiz_marks + int(row["marks_correct_ans"])
            writer.writerow(dict_temp)
        i += 1
    
    with open("./individual_responses/" + quiz_no + "_" + User_Roll + ".csv", 'a', newline='') as indi:
        writer = csv.DictWriter(indi, fieldnames = dict_temp.keys())
        for key in dict_temp:
            dict_temp[key] = ""
        dict_temp["Total"] = total_marks
        dict_temp["Legend"] = "Marks Obtained"
        writer.writerow(dict_temp)
        dict_temp["Total"] = total_quiz_marks
        dict_temp["Legend"] = "Total Quiz Marks"
        writer.writerow(dict_temp)
        
    #print("evaluate")
    
# Final Function for ending the quiz and the Final Result Window...
def end_quiz(quiz_window):
    global stop_timer
    global total_marks
    global quiz_no
    global User_Roll
    global subm_called
    
    if subm_called:
        return True
    else:
        subm_called += 1
    
    stop_timer = True
    try:
        quiz_window.destroy()
    except:
        pass
    evalute()
    subm_window = Tk()
    
    total_quiz_ques = 0
    ques_att = 0
    corr = 0
    wrong = 0
    
    with open("./individual_responses/" + quiz_no + "_" + User_Roll + ".csv", 'r') as indi:
        reader = csv.DictReader(indi, delimiter=',')
        
        for row in reader:
            total_quiz_ques += 1
            if row["Legend"] == "Correct Choice":
                corr += 1
                ques_att += 1
            if row["Legend"] == "Wrong Choice":
                wrong += 1
                ques_att += 1
        total_quiz_ques = total_quiz_ques - 2
            
    database_marks_sub()
    
    Label(subm_window, text = "Your Quiz has been Sucessfully Submitted!\n").grid(row = 0)
    Label(subm_window, text = "Total Quiz Questions: ").grid(row = 1, sticky = W)
    Label(subm_window, text = total_quiz_ques).grid(row = 1, column = 1)
    Label(subm_window, text = "Total Quiz Questions Attempted: ").grid(row = 2, sticky = W)
    Label(subm_window, text = ques_att).grid(row = 2, column = 1)
    Label(subm_window, text = "Total Correct Questions: ").grid(row = 3, sticky = W)
    Label(subm_window, text = corr).grid(row = 3, column = 1)
    Label(subm_window, text = "Total Wrong Questions: ").grid(row = 4, sticky = W)
    Label(subm_window, text = wrong).grid(row = 4, column = 1)
    Label(subm_window, text = "Total Marks Obtained: ").grid(row = 5, sticky = W)
    Label(subm_window, text = total_marks).grid(row = 5, column = 1)
    
    subm_window.mainloop()
    
    #print("end quiz")

def end_quiz_eventpress(event):
    global stop_timer
    global total_marks
    global quiz_no
    global User_Roll
    
    stop_timer = True
    
    evalute()
    subm_window = Tk()
    
    total_quiz_ques = 0
    ques_att = 0
    corr = 0
    wrong = 0
    
    with open("./individual_responses/" + quiz_no + "_" + User_Roll + ".csv", 'r') as indi:
        reader = csv.DictReader(indi, delimiter=',')
        
        for row in reader:
            total_quiz_ques += 1
            if row["Legend"] == "Correct Choice":
                corr += 1
                ques_att += 1
            if row["Legend"] == "Wrong Choice":
                wrong += 1
                ques_att += 1
        total_quiz_ques = total_quiz_ques - 2
    
    Label(subm_window, text = "Your Quiz has been Sucessfully Submitted!\n").grid(row = 0)
    Label(subm_window, text = "Total Quiz Questions: ").grid(row = 1, sticky = W)
    Label(subm_window, text = total_quiz_ques).grid(row = 1, column = 1)
    Label(subm_window, text = "Total Quiz Questions Attempted: ").grid(row = 2, sticky = W)
    Label(subm_window, text = ques_att).grid(row = 2, column = 1)
    Label(subm_window, text = "Total Correct Questions: ").grid(row = 3, sticky = W)
    Label(subm_window, text = corr).grid(row = 3, column = 1)
    Label(subm_window, text = "Total Wrong Questions: ").grid(row = 4, sticky = W)
    Label(subm_window, text = wrong).grid(row = 4, column = 1)
    Label(subm_window, text = "Total Marks Obtained: ").grid(row = 5, sticky = W)
    Label(subm_window, text = total_marks).grid(row = 5, column = 1)
    
    subm_window.mainloop()

def unattempted_ques_eventpress(event):
    unattemp_ques=0
    for i in marked:
        if(i==0):
            unattemp_ques+=1

    #print(unattemp_ques)
    if(unattemp_ques==0):
        ms.showinfo('Unattempted Question',"Voila ! It seems you have attempted all questions")
    else:
        ms.showinfo('Unattempted Question',"You still havn't attempted "+str(unattemp_ques)+" questions")

def database_marks_sub():
    with sqlite3.connect('project1_quiz_cs384.db') as db:
        c = db.cursor()
    find_user_already_sub = ('SELECT Roll_No FROM project1_marks WHERE Roll_No = ? AND quiz_num = ?')
    c.execute(find_user_already_sub,[User_Roll,quiz_no])
    if c.fetchall():
        #ms.showerror('Error!','Roll No has already given the quiz.')
        #print("Already Submitted once but now it is modified")
        ft = ('DELETE FROM project1_marks WHERE Roll_No = ? AND quiz_num = ?')
        c.execute(ft,[User_Roll,quiz_no])
        db.commit()
        insert = 'INSERT INTO project1_marks(Roll_No,quiz_num,total_marks) VALUES(?,?,?)'
        c.execute(insert,[User_Roll,quiz_no,total_marks])
        db.commit()
        database_to_csv()
        
    else:
        #print("FIRST TIME QUIZ SUBMISSION")
        insert = 'INSERT INTO project1_marks(Roll_No,quiz_num,total_marks) VALUES(?,?,?)'
        c.execute(insert,[User_Roll,quiz_no,total_marks])
        db.commit()
        database_to_csv()
    
    #print("database marks sub")

def database_to_csv():
    with sqlite3.connect('project1_quiz_cs384.db') as db:
        curs = db.cursor()
    curs.execute("SELECT * FROM project1_marks")
    res=curs.fetchall()
    raw_quizes=[]
    for i in res:
        raw_quizes.append(i[1])
    uniq_quizes_name=list(set(raw_quizes))
    
    #print(uniq_quizes_name)
    for file_name in uniq_quizes_name:
        final_fname = "./quiz_wise_responses/" + "scores_" + file_name + ".csv"
        if(os.path.exists(final_fname)):
            os.remove(final_fname)
            with open(final_fname, 'w',newline='') as fily:
                writer=csv.writer(fily)
                newheader=['Roll No','Quiz No','Total Marks']
                writer.writerow(newheader)
                for p in res:
                    if(p[1]==file_name):
                        writer.writerow(list(p))
        else:
            with open(final_fname, 'w',newline='') as fily:
                writer=csv.writer(fily)
                newheader=['Roll No','Quiz No','Total Marks']
                writer.writerow(newheader)
                for p in res:
                    if(p[1]==file_name):
                        writer.writerow(list(p))
                        
    #print("database to csv")

def database_to_csv_eventpress(event):
    with sqlite3.connect('project1_quiz_cs384.db') as db:
        curs = db.cursor()
    curs.execute("SELECT * FROM project1_marks")
    res=curs.fetchall()
    raw_quizes=[]
    for i in res:
        raw_quizes.append(i[1])
    uniq_quizes_name=list(set(raw_quizes))
    
    #print(uniq_quizes_name)
    for file_name in uniq_quizes_name:
        trim_name=re.split(r'[q]',file_name)
        final_fname="quiz"+str(trim_name[1])+'.csv'
        if(os.path.exists(final_fname)):
            os.remove(final_fname)
            with open(final_fname, 'w',newline='') as fily:
                writer=csv.writer(fily)
                newheader=['Roll No','Quiz No','Total Marks']
                writer.writerow(newheader)
                for p in res:
                    if(p[1]==file_name):
                        writer.writerow(list(p))
        else:
            with open(final_fname, 'w',newline='') as fily:
                writer=csv.writer(fily)
                newheader=['Roll No','Quiz No','Total Marks']
                writer.writerow(newheader)
                for p in res:
                    if(p[1]==file_name):
                        writer.writerow(list(p))

# Driver Code Starts Here...
User_Name = ""
User_Roll = ""
quiz_no = ""
ques_no = 0
total_marks = 0
marked = []
unatt = 0
stop_timer = False
subm_called = 0
login_window()