import sqlite3 as sql
from tkinter import *
from tkinter import ttk
import random

def getButton():
  if (got == False):
    getButton = Button(get, text = 'Get Activity', command = lambda: getAct())
    getButton.pack(fill = 'both', expand = 'yes', padx = 0, pady =10)
  #else:
  #  gtable.pack(anchor = CENTER) 
    
def insert():
  global activityid
  title = ineTitle.get()
  description = ineDesc.get()
  priority = inePriority.get()
  value = ineValue.get()
  
  with con:
    cur.execute("INSERT into Activities values (:aid, :atitle, :adesc, :apriority, :avalue)", {'aid': activityid, 'atitle': title, 'adesc': description, 'apriority': priority, 'avalue': value})
  
  activityid += 1
  #print(activityid)

def search():
  for i in stable.get_children():
    stable.delete(i)
    
  string ='%' + seString.get() + '%'
  cur.execute("SELECT * from Activities where description like :str or Title like :str", {'str': string})
  for i in cur.fetchall():
    stable.insert(parent ='', index='end', iid=i[0], text='', values = i)
    

def remove():
  reid = reEntry.get()
  cur.execute("SELECT * from Activities where activityid is :aid", {'aid': reid})
  act = cur.fetchone()
  print("***REMOVING {} ***\n".format(act))
  with con:
    cur.execute("DELETE from Activities where activityid is :reid",{'reid': reid})
 
def update():
  actid = upIDEntry.get()
  newval = upValEntry.get()
  newpty = upPEntry.get()
  cur.execute("SELECT * from Activities where activityid is :aid", {'aid': actid})
  act = cur.fetchone()
  
  print("***UPDATING {} ***\n".format(act))
  
  with con:
    cur.execute("UPDATE Activities SET priority = :prio where activityid = :actid", {'prio': newpty, 'actid': actid})
    cur.execute("UPDATE Activities SET value = :val where activityid = :actid", {'val': newval,'actid': actid})
  
  cur.execute("SELECT * from Activities where activityid is :aid", {'aid': actid})
  act = cur.fetchone()
  
  #print("***UPDATED {} ***\n".format(act))
  
def getAct():
	global got
	got = True
	pick = random.randint(0,activityid-1) 
	cur.execute("SELECT * from Activities where activityid is :pick", {'pick': pick})
	output = cur.fetchone()
	#print(output)
	getButton()
	gtable.pack(anchor = CENTER) 
	gtable.insert(parent='', index='end', iid=output[0], text='', values=output)


con = sql.connect('/home/chd/.bored.db')
cur = con.cursor()

try:
	cur.execute("CREATE TABLE Activities(activityid INT, title TEXT, description TEXT, priority INT, value INT)")
except :
	print("*** TABLES ALREADY EXIST ***")

try:
	activityid = int(cur.execute('SELECT max(activityid) from Activities').fetchone()[0]) + 1
except:
	activityid = 0



window = Tk()
window.geometry('1600x1200')
window.title('bored')

#labelframes
get = LabelFrame(window, text='Activity Getter')
get.pack(fill='both', expand='yes', padx=10, pady=10)


insertlf = LabelFrame(window, text='insert new activity')
insertlf.pack(fill = 'both', expand='yes', padx=10,pady=10)


display = LabelFrame(window, text = 'display of activities with remove update and search functions')
display.pack(fill='both', expand='yes', padx=10,pady=10)

table = LabelFrame(display, text = "Search Table").grid(row=3, column=1)

#Variables

got = False
inTitle = StringVar()
inDesc = StringVar()
inPriority = IntVar()
inValue = IntVar()
sestr = StringVar()
upID = IntVar()
upVal = IntVar()
upPriority = IntVar()
reID = IntVar()

#Labels and Entries 

inlTitle = Label(insertlf, text='Title').grid(row= 0 , column = 0)
inlDesc = Label(insertlf, text='Description').grid(row= 0, column = 1)
inlPriority = Label(insertlf, text='Priority').grid(row= 0 , column = 2)
inlValue = Label(insertlf, text='Value').grid(row= 0 , column = 3)

ineTitle = Entry(insertlf, textvariable = inTitle)
ineTitle.grid(row=1, column = 0)
ineDesc = Entry(insertlf, textvariable = inDesc)
ineDesc.grid(row=1, column = 1)
inePriority = Entry(insertlf, textvariable = inPriority)
inePriority.grid(row=1, column = 2)
ineValue = Entry(insertlf, textvariable = inValue)
ineValue.grid(row=1, column = 3)


seLabel = Label(display, text='search input: ')
seLabel.grid(row=0, column=0)
seString = Entry(display, textvariable = sestr)
seString.grid(row=0, column=1)

upIDLabel = Label(display, text='Update ID: ')
upIDLabel.grid(row=1, column=0)
upIDEntry = Entry(display, textvariable = upID)
upIDEntry.grid(row=2, column=0)
upValLabel = Label(display, text= 'Update Value to: ')
upValLabel.grid(row=1, column=1)
upValEntry = Entry(display, textvariable = upVal)
upValEntry.grid(row=2, column=1)
upPLabel = Label(display, text= 'Update Priority to: ')
upPLabel.grid(row=1, column=2)
upPEntry = Entry(display, textvariable = upPriority)
upPEntry.grid(row=2, column=2)

reLabel = Label(display , text = ' Remove ID: ')
reLabel.grid(row=3, column=0)
reEntry = Entry(display, textvariable = reID)
reEntry.grid(row=3, column=1)


#Buttons


inButton = Button(insertlf, text = 'Insert New Activity', command = lambda: insert())
inButton.grid(row=2, column= 2)

rmButton = Button(display, text = 'Remove Activity', command = lambda: remove())
rmButton.grid(row=3,column=2)

udButton = Button(display, text = 'Update Activity', command = lambda: update())
udButton.grid(row=2,column=4)

seButton = Button(display, text = 'Search for Acrivities', command = lambda: search())
seButton.grid(row=0, column=2)


#Tables


gtable = ttk.Treeview(get)
gtable['columns'] = ('ID', 'Title', 'Description', 'Priority', 'Value')
gtable['selectmode'] = 'extended'


gtable.column('#0', width = 0, minwidth = 25)
gtable.column("ID", anchor = W, width = 50)
gtable.column("Title", anchor = W, width = 200)
gtable.column("Description", anchor = W, width = 800)
gtable.column("Priority", anchor = W, width = 200)
gtable.column("Value", anchor = W, width = 200)

gtable.heading('#0', text = '', anchor = W)
gtable.heading('ID', text = 'ID', anchor = W)
gtable.heading('Title', text = 'Title', anchor = W)
gtable.heading('Description', text = 'Description', anchor = W)
gtable.heading('Priority', text = 'Priority', anchor = W)
gtable.heading('Value', text = 'Value', anchor = W)


stable = ttk.Treeview(table)
stable['columns'] = ('ID', 'Title', 'Description', 'Priority', 'Value')
stable['selectmode'] = 'extended'
stable.pack(anchor = CENTER)

stable.column('#0', width = 0, minwidth = 25)
stable.column("ID", anchor = W, width = 50)
stable.column("Title", anchor = W, width = 200)
stable.column("Description", anchor = W, width = 800)
stable.column("Priority", anchor = W, width = 200)
stable.column("Value", anchor = W, width = 200)

stable.heading('#0', text = '', anchor = W)
stable.heading('ID', text = 'ID', anchor = W)
stable.heading('Title', text = 'Title', anchor = W)
stable.heading('Description', text = 'Description', anchor = W)
stable.heading('Priority', text = 'Priority', anchor = W)
stable.heading('Value', text = 'Value', anchor = W)


getButton()

window.mainloop()


con.close()
