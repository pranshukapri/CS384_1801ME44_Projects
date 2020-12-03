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