import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image,ImageTk
import sqlite3
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle
from reportlab.platypus import Image as Imagee
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import os,sys,shutil
import sys, os

def resource_path(relative_path):
    """ Get absolute path to resource (works for PyInstaller) """
    try:
        base_path = sys._MEIPASS  # Folder PyInstaller uses for temp files
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

import shutil, os

user_db = os.path.join(os.getenv("APPDATA"), "school_app", "school.db")

if not os.path.exists(user_db):
    os.makedirs(os.path.dirname(user_db), exist_ok=True)
    shutil.copy(resource_path("school.db"), user_db)

conn = sqlite3.connect(user_db)



cursor=conn.cursor()
cursor.execute("""CREATE table IF NOT EXISTS users(name text,
               password text )""")
cursor.execute("""CREATE table IF NOT EXISTS students1(
               Admission text primary key ,
               Name text,
               DOB date,
               Class text,
               Parent text,
               Photo text,
               Telephone text)"""
)
cursor.execute("""CREATE table IF NOT EXISTS finance(Admission text,Fees integer,Date date, 
               FOREIGN KEY (Admission) REFERENCES students1(Admission))
               """)
cursor.execute("""CREATE table IF NOT EXISTS teacher(Name text, Class text, 
               FOREIGN KEY (Class) REFERENCES students1(Class))
               """)
photo_path=None

#MAIN PAGE
class root(tk.Tk):
   def __init__(self, screenName = None, baseName = None, className = "Tk", useTk = True, sync = False, use = None):
      super().__init__(screenName, baseName, className, useTk, sync, use)
      self.geometry("900x500")
      self.title("STUDENT DATABASE")
      self.photo=Image.open(resource_path("images/pexels-olia-danilevich-5088008.jpg"))
      self.photo=self.photo.resize((900,500))
      self.mage=ImageTk.PhotoImage(self.photo)
      self.label1=tk.Label(self,image=self.mage).place(x=0,y=0,relheight=1,relwidth=1)
      self.label2=tk.Label(self,text="SCHOOL DATABASE MANAGEMENT SYSTEM",font=("Arial",16,"bold","underline"),foreground="blue")
      self.label2.pack()
      def add_user():
        window=tk.Toplevel(self)
        window.title("Add User")
        window.geometry("200x200")
        window.config(bg="grey")
        window.resizable(False,False)
        tk.Label(window,text="New User",foreground="blue").pack(pady=5)
        new_name=tk.Entry(window,foreground="blue")
        new_name.pack(pady=5)
        tk.Label(window,text="Password",foreground="blue").pack(pady=5)
        new_word=tk.Entry(window,foreground="blue")
        new_word.pack(pady=5)
        def submit_new():
          name=new_name.get()
          psw=new_word.get()
          if name and psw:
             cursor.execute("INSERT INTO users(name,password) VALUES(?,?)",(name,psw))
             conn.commit()
             messagebox.showinfo("NEW USER","New user created successfully")
             return
          else:
              messagebox.showerror("USER NOT CREATED","User not created.Check you have filled both fields")
              return
        btn=tk.Button(window,text="SUBMIT",command=submit_new)
        btn.pack()
      self.btn1=tk.Button(self,text="CREATE USER",width=30,foreground="blue",command=add_user)
      self.btn1.pack(pady=20)
      self.btn2=tk.Button(self,text="STUDENTS",foreground="blue",width=30,command=mwanafunzi)
      self.btn2.pack(pady=20)
      self.btn3=tk.Button(self,text="FINANCES",foreground="blue",width=30,command=student_finance)
      self.btn3.pack(pady=20)
      self.btn4=tk.Button(self,text="TEACHERS",foreground="blue",width=30,command=teacher_data)
      self.btn4.pack(pady=20)
#--END OF MAIN PAGE--#
#STUDENT FINANCE
def student_finance():
   finance=fees()
   finance.resizable(False,False)
   finance.mainloop()
class fees(tk.Toplevel):
   def __init__(self):
      super().__init__()
      self.title("STUDENT FINANCE")
      self.geometry("500x330")
      self.config(bg="grey")
      self.mage=Image.open(resource_path("images/finance.jpeg"))
      self.mage=self.mage.resize((500,330))
      self.image=ImageTk.PhotoImage(self.mage)
      self.imageLb=tk.Label(self,image=self.image)
      self.imageLb.place(x=0,y=0,relheight=1,relwidth=1)
      self.lb1=tk.Label(self,text="STUDENT FINANCE",font=("arial",12,"bold"))
      self.lb1.pack(pady=10)
      self.lb2=tk.Label(self,text="Student admission")
      self.lb2.pack(pady=10)
      self.entry1=tk.Entry(self)
      self.entry1.pack(pady=10)
      self.lb3=tk.Label(self,text="Fees paid")
      self.lb3.pack(pady=10)
      self.entry2=tk.Entry(self)
      self.entry2.pack(pady=10)
      self.lb4=tk.Label(self,text="Date")
      self.lb4.pack(pady=10)
      self.entry3=tk.Entry(self)
      self.entry3.pack(pady=10)
      self.frame1=tk.Frame(self,width=500,height=10,relief="solid",bg="grey")
      self.frame1.pack(side="bottom")
      self.btn3=tk.Button(self.frame1,text="CLOSE",command=lambda:self.destroy())
      self.btn3.grid(column=1,row=0,padx=50)
      #SUBMIT FEES
      def submit():
       adm=self.entry1.get()
       fees=self.entry2.get()
       date=self.entry3.get()
       if adm and fees:
           cursor.execute("INSERT INTO finance(Admission,Fees,Date) VALUES(?,?,?)",(adm,fees,date))
           conn.commit()
           messagebox.showinfo("SUCCESSFUL","SUBMITTED SUCCESSFULLY")
           return
       else:
            messagebox.showerror("ERROR","NOTHING TO SUBMIT")
            return
      self.btn1=tk.Button(self.frame1,text="SUBMIT",command=submit)
      self.btn1.grid(row=0,column=2,padx=50)
       # PRINT FEES REPORT
      def print_report():
         cursor.execute("SELECT students1.Name,students1.Admission,students1.class,finance.Fees,finance.Date FROM students1 JOIN finance ON students1.Admission=finance.Admission")
         rows=cursor.fetchall()
         file_path=filedialog.asksaveasfilename(defaultextension=".pdf",title="SAVE AS",filetypes=[("Pdf files","*.pdf")])
         if file_path:
          doc=SimpleDocTemplate(filename=file_path)
          elements=[] 
          styles=getSampleStyleSheet()
          image_path=resource_path("images/school.jpg")
          img=Imagee(image_path,width=500,height=100)
          elements.append(img)
          elements.append(Paragraph("SCHOOL FEES FOR 2025",styles["Title"]))
          table_data=[["STUDENT NAME","ADMISSION","CLASS","FEES","DATE"]]
          for row in rows:
            table_data.append(list(row))
          table=Table(table_data)
          style=TableStyle([
          ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4CAF50")),
          ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
          ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
          ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
          ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
          ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
          ('GRID', (0, 0), (-1, -1), 1, colors.black),])
          table.setStyle(style)
          elements.append(table)
          elements.append(Paragraph("Generated by Finance Office"))
          doc.build(elements)
          os.startfile(file_path)
         else:
            return
      self.btn2=tk.Button(self.frame1,text="PRINT REPORT",command=print_report)
      self.btn2.grid(column=0,row=0,padx=50)
      #END OF PRINT
# END OF FINANCES
#TEACHER
def teacher_data():
   tab=teacher()
   tab.resizable(False,False)
class teacher(tk.Toplevel):
   def __init__(self):
      super().__init__()
      self.geometry("500x300")
      self.title("TEACHERS")
      self.mage=Image.open(resource_path("images/teacher.jpeg"))
      self.mage=self.mage.resize((500,300))
      self.image=ImageTk.PhotoImage(self.mage)
      self.imageLb=tk.Label(self,image=self.image)
      self.imageLb.place(x=0,y=0,relheight=1,relwidth=1)
      self.lb=tk.Label(self,text="TEACHERS DATABASE",font=("arial",16,"bold"),fg="blue")
      self.lb.pack(pady=5)
      self.lb2=tk.Label(self,text="Teacher's name")
      self.lb2.pack(pady=10)
      self.entry1=tk.Entry(self)
      self.entry1.pack(pady=10)
      self.lb3=tk.Label(self,text="Class assigned")
      self.lb3.pack(pady=10)
      self.entry2=ttk.Combobox(self,values=["1-EAST","1-WEST","1-NORTH","2-EAST","2-WEST","2=NORTH","3-EAST","3-WEST","3-NORTH","4-EAST","4-WEST","4-NORTH"])
      self.entry2.set("Select One")
      self.entry2.pack(pady=10)
      # SUBMIT
      def submit():
         name=self.entry1.get()
         cl=self.entry2.get()
         if name and cl:
            cursor.execute("INSERT INTO teacher(Name,Class) VALUES(?,?)",(name,cl))
            conn.commit()
            messagebox.showinfo("DONE","SUBMITTED SUCCESSFULLY")
            return
         else:
            messagebox.showerror("ERROR","MISSING NAME OR CLASS")
      self.btn=tk.Button(self,text="SUBMIT",command=submit)
      self.btn.pack(side="bottom")

      


      
      
      


#--END OF ADD NEW USER--#         
        
#STUDENTS
def mwanafunzi():
     window1=tk.Toplevel()
     window1.title("STUDENTS")
     window1.geometry("500x250")
     mage=Image.open(resource_path("images/pic1.jpeg"))
     mage=mage.resize((500,250))
     mage_photo=ImageTk.PhotoImage(mage)
     IL=tk.Label(window1,image=mage_photo)
     IL.image=mage_photo
     IL.place(x=0,y=0,relheight=1,relwidth=1)
     tk.Label(window1,text="STUDENT SECTION",foreground="blue",font=("Arial",16,"bold","underline")).pack()
     tk.Button(window1,text="ADD STUDENT",command=add_mwanafunzi).pack(side="left",padx=10)
     tk.Button(window1,text="SEARCH FOR A STUDENT",command=search_one).pack(side="left",padx=50)
     tk.Button(window1,text="ALL STUDENTS",command=search_all).pack(side="right",padx=10)

def add_mwanafunzi():
   window=tk.Toplevel()
   window.geometry("250x700")
   window.config(bg="grey")
   tk.Label(window,text="ADD A STUDENT",foreground="purple",font=("Arial",16,"bold")).pack(pady=10)
#ADDING AN IMAGE
   tk.Label(window,text="STUDENT IMAGE").pack()
   image_label=tk.Label(window,text="Image will appear here once added")
   image_label.pack(pady=10)
   def add_image():
    global photo_path
    filepath=filedialog.askopenfilename(
      title="Open student image",
      filetypes=[("Image files","*.jpeg *.jpg *.ico")]
    )
    photo_path=filepath
    mage=Image.open(filepath)
    mage=mage.resize((150,150))
    mage_photo=ImageTk.PhotoImage(mage)
    image_label.image=mage_photo
    image_label.config(image=mage_photo)
#--END OF ADD IMAGE--#
   tk.Button(window,text="ADD IMAGE",command=add_image).pack(pady=10)
   tk.Label(window,text="Student Name",fg="blue").pack()
   entry1=tk.Entry(window)
   entry1.pack(pady=10)
   tk.Label(window,text="Admission Number",fg="blue").pack()
   entry2=tk.Entry(window)
   entry2.pack(pady=10)
   tk.Label(window,text="Date Of Birth",fg="blue").pack()
   entry3=tk.Entry(window)
   entry3.pack(pady=10)
   tk.Label(window,text="Parent's Name",fg="blue").pack()
   entry4=tk.Entry(window)
   entry4.pack(pady=10)
   tk.Label(window,text="Telephone",fg="blue").pack()
   entry5=tk.Entry(window)
   entry5.pack(pady=10)
   tk.Label(window,text="Class",fg="blue").pack()
   entry6=ttk.Combobox(window,state="readonly",values=["1-EAST","1-WEST","1-NORTH","2-EAST","2-WEST","2-NORTH","3-EAST","3-WEST","3-NORTH","4-EAST","4-WEST","4-NORTH"])
   entry6.set("Select one")
   entry6.pack()
   def submit_student():
       global photo_path
       student_name=entry1.get()
       adm=entry2.get()
       date=entry3.get()
       parent=entry4.get()
       tel=entry5.get()
       stream=entry6.get()
       photo=photo_path
       cursor.execute("INSERT INTO students1(Admission,Name,DOB,Parent,Telephone,Class,Photo) VALUES(?,?,?,?,?,?,?)",(adm,student_name,date,parent,tel,stream,photo))
       conn.commit()
       cursor.execute("SELECT * FROM students1")
       row=cursor.fetchall()
       print(row)
       messagebox.showinfo("Action successful","Student added successfully")
       entry1.delete(0,tk.END)
       entry2.delete(0,tk.END)
       entry3.delete(0,tk.END)
       entry4.delete(0,tk.END)
       entry5.delete(0,tk.END)
       entry6.delete(0,tk.END)
       image_label.config(text="Image will appear here once added")
   btn1=tk.Button(window,text="SUBMIT",command=submit_student)
   btn1.pack(pady=10)
   btn2=tk.Button(window,text="CLOSE",command=lambda:window.destroy())
   btn2.pack()
#--END OF ADD STUDENT WINDOW--#
#SEARCH STUDENT
def search_all():
       cursor.execute("SELECT students1.Admission,students1.Name,students1.DOB,students1.Class,students1.Parent,students1.Photo,students1.Telephone,teacher.Name FROM students1 JOIN teacher ON students1.Class=teacher.Class")
       data=cursor.fetchall()
       show=tk.Toplevel()
       show.title("RECORDS")
       show.geometry("500x700")
       cols=["Admission"," Name","DOB","Class","Parent","Photo","Telephone","Teacher"]
       tree=ttk.Treeview(show,show="headings",columns=cols)
       
       for col in cols:
          tree.heading(col,text=col)
          tree.column(col,width=62,anchor="center")
       for row in data:
          tree.insert("",tk.END,values=row)
       tree.pack(expand=True,fill="both")

def search_one():
   window=tk.Toplevel()
   window.geometry("500x200")
   window.config(background="grey")
   window.resizable(False,False)
   tk.Label(window,text="SEARCH",font=("arial",14,"bold")).pack(pady=10)
   tk.Label(window,text="SEARCH BY ADM").pack(pady=10)
   h=tk.Entry(window)
   h.pack()
   def cheki():
      adm=h.get().strip()
      cursor.execute("SELECT * FROM students1 WHERE Admission=?",(adm,))
      rows=cursor.fetchone()
      if rows:
         Admission,Name,DOB,Class,Parent,Photo,Telephone=rows
         messagebox.showinfo("SUCCESSFUL","STUDENT FOUND")
         win=tk.Toplevel()
         win.geometry("500x400")
         win.config(bg="grey")
         win.resizable(False,False)
         tk.Label(win,text=f"Name : {Name}",font=("Arial", 12, "bold")).pack(pady=5)
         tk.Label(win,text=f"Admission : {Admission}",font=("Arial", 12, "bold")).pack()
         tk.Label(win,text=f"DOB : {DOB}",font=("Arial", 12, "bold")).pack(pady=5)
         tk.Label(win,text=f"Parent : {Parent}",font=("Arial", 12, "bold")).pack()
         tk.Label(win,text=f"Telephone : {Telephone}",font=("Arial", 12, "bold")).pack(pady=5)
         tk.Label(win,text=f"Class : {Class}",font=("Arial", 12, "bold")).pack(pady=5)
         pth=resource_path(Photo)
         img=Image.open(pth).resize((150,150))
         f_img=ImageTk.PhotoImage(img)
         lb=tk.Label(win,image=f_img)
         lb.image=f_img
         lb.pack()
      else:
         messagebox.showerror("ERROR","STUDENT NOT FOUND")

   tk.Button(window,text="SEARCH",command=cheki).pack(side="bottom")
       
#--END OF SEARCH STUDENT--#
#LOGIN PAGE SUBMIT
def submit():
    ame=username.get()
    ord=password.get()
    cursor.execute("SELECT password FROM users WHERE name=?",(ame,))
    user=cursor.fetchone()
    if ord==user[0]:
        messagebox.showinfo("Login","Login was successful")
        page.destroy()
        main=root()
        main.resizable(False,False)
        main.mainloop()
    else:
        messagebox.showerror("Login","Wrong password or username")
#--END OF LOGIN PAGE FUNCTION--#

#LOGIN PAGE
page=tk.Tk()
page.title("LOGIN PAGE")
page.geometry("500x250")
page.config(background="grey")
tk.Label(page,text="Username",foreground="blue",font=("Arial",13,"bold")).pack()
username=tk.Entry(page,foreground="blue")
username.pack(pady=10)
tk.Label(page,text="Password",foreground="blue",font=("Arial",13,"bold")).pack(pady=10)
password=tk.Entry(page,foreground="blue",show="*")
password.pack()
tk.Button(page,text="SUBMIT",foreground="blue",command=submit).pack(side="bottom")
page.resizable(False,False)
page.mainloop()