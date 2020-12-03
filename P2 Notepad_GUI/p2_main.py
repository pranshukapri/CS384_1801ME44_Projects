from tkinter import *
from tkinter import filedialog
from tkinter import colorchooser
from tkinter import messagebox
import re
import platform
import os
import datetime
root=Tk()
root.geometry('500x500+0+0')
root.title('Notepad')

undoList=[]
redoList=[]
ovr_filename=''

#---------------------------------------------------FUNCTIONS--------------------------------------------------------------
# open file
def file():
	f=filedialog.askopenfilename()
	global ovr_filename
	ovr_filename=f
	fr=open(f,'r')
	t1.insert(END,fr.read())
# -----------------------------------------------	
# save file	
def save():
	s=filedialog.asksaveasfilename()
	global ovr_filename
	ovr_filename=s
	f1=open(s,'w')
	f1.write(t1.get('1.0','end-1c'))
	f1.close()
	print('File saved successfully')
# --------------------------------------------	
# save file shortcut
def save1(event):
	s=filedialog.asksaveasfilename()
	f1=open(s,'w')
	f1.write(t1.get('1.0','end-1c'))
	f1.close()
	print('File saved successfully')
# ------------------------------------------------			
# new file
def newFile():
	t1.delete('1.0',END)
# -------------------------------------------------	
# new file shortcut	
def newFile1(event):
	t1.delete('1.0',END)
# -------------------------------------------------		
# exit confirmation
def quit():
	m=messagebox.askyesno(title='Exit',message='Are you Sure?')
	if m:
		root.destroy()
# ---------------------------------------------------		
# theme color color
def col():
	c=colorchooser.askcolor()
	t1['background']=c[1]
# ----------------------------------------------------
#font menu
def fontWin():
	t=Toplevel(root)
	t.title('Font')
	def o(*args):
		reg=re.compile(r'\d\d')
		t1['font']=reg.sub(varSize.get(),t1['font'])
	# foreground color
	def colfg():
		c1=colorchooser.askcolor()
		t1['fg']=c1[1]
	# --------------------------------------	
	varSize=StringVar()
	varSize.set('1')
	varSize.trace("w", o)
	varFont=StringVar()
	varFont.set('abc')
	size=[]

	for i in range(18):
		size.append(str(i+1))
	sizeO=OptionMenu(t,varSize,*size).grid(row=0,column=0)
	fontList=['abc','bcd','efg']
	fontO=OptionMenu(t,varFont,*fontList).grid(row=0,column=1)
	b=Button(t,text='Color',fg='black',command=colfg).grid(row=0,column=2)
# ------------------------------------------------------------	
# key pressed event 
def press(event):
	undoList.append(t1.get('1.0','end-1c'))
# undo button
def undo():
	t1.delete('1.0',END)
	u=undoList.pop()
	redoList.append(u)
	t1.insert(END,u)
	print(redoList)
# ---------------------------------------------------------------------	
# redo button
def redo():
	t1.delete('1.0',END)
	r=redoList.pop()
	undoList.append(r)
	t1.insert(END,r)
	print(redoList)
# undo shortcut
def undo1(event):
	t1.delete('1.0',END)
	u=undoList.pop()
	redoList.append(u)
	t1.insert(END,u)
	print(redoList)
# ----------------------------------------------------------------------------
def Stats():
	modified_date=''
	creation_filedate=''
	countchar=len(t1.get('1.0','end-1c')) - t1.get('1.0','end-1c').count(" ")
	countwords=t1.get('1.0','end-1c')
	countwords = len(re.findall(r'\w+',countwords))
	if(ovr_filename==''):
		modified_date="File Hasnt been Saved"
		creation_filedate="File hasn't been Saved"
	else:
		modified_date=modification_date(ovr_filename)
		creation_filedate=datetime.datetime.fromtimestamp(creation_date(ovr_filename))
	m=messagebox.showinfo("Stats","No of Char = "+str(countchar)+'\n'+"No of Words = "+str(countwords)+'\n'+"Modified Date: "+str(modified_date)+'\n'+"Creation Date: "+str(creation_filedate))

def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

def creation_date(path_to_file):

    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime

def far():
	t2=Toplevel(root)
	t2.title('Find & Replace')
	t2.geometry('210x100+100+100')
	
	v1=StringVar()
	v2=StringVar()
	v3=StringVar()

	def find():
		reg1=re.compile(v1.get())
		s1=reg1.search(t1.get('1.0','end-1c'))
		count=len(s1.group())
		v3.set(str(count)+' matches')

	def rep():
		pass	

	l1=Label(t2,text='Find:').grid(row=0,column=0,sticky=W)
	l2=Label(t2,text='Replace:').grid(row=1,column=0)
	l3=Label(t2,textvariable=v3).grid(row=3,column=0)
	
	e1=Entry(t2,textvariable=v1).grid(row=0,column=1)
	e2=Entry(t2,textvariable=v2).grid(row=1,column=1)
	b1=Button(t2,text='Find',command=find).grid(row=2,column=0,sticky=E)
	b2=Button(t2,text='Replace',command=rep).grid(row=2,column=1)

# _______________________________________________________________________________________________________________________________
# -----------------------Text Widget--------------------------------------
t1=Text(root,font='Consolas 25')
t1.bind('<Key>',press)
t1.pack(expand=True,fill=BOTH)
# -------------------------------------------------------------------------

# -------------------------------Menu bar------------------------------------
menubar=Menu(root)
# file menu
fm=Menu(menubar,tearoff=0)
fm.add_command(label='New',command=newFile)
fm.add_command(label='Open',command=file)
fm.add_command(label='Save',command=save)
fm.add_command(label='Quit',command=quit)
menubar.add_cascade(label='File',menu=fm)

# Edit menu
em=Menu(menubar,tearoff=0)
em.add_command(label='Undo',command=undo)
em.add_command(label='Redo',command=redo)
em.add_command(label='Cut')
em.add_command(label='Copy')
em.add_command(label='Paste')
em.add_command(label='Delete')
em.add_command(label='Find & Replace',command=far)
menubar.add_cascade(label='Edit',menu=em)

# Format menu
fom=Menu(menubar,tearoff=0)
fom.add_command(label='Font',command=fontWin)
menubar.add_cascade(label='Format',menu=fom)

# Theme menu
fom=Menu(menubar,tearoff=0)
fom.add_command(label='Color',command=col)
menubar.add_cascade(label='Theme',menu=fom)

# Stats menu
fom=Menu(menubar,tearoff=0)
fom.add_command(label='Show Stats',command=Stats)
menubar.add_cascade(label='Stats',menu=fom,command=Stats)

root.config(menu=menubar)
# ------------------------------------------------------------------------------------------------
root.bind('<Control-s>',save1)
root.bind('<Control-n>',newFile1)
root.bind('<Control-z>',undo1)

root.mainloop()