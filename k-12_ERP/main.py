from tkinter import *
import time as t
from database import data
from login_stu import stu_login
from login_stf import stf_login
global main
data()
def intro(event):
    t.sleep(1)
    lb1=Label(main,text="W E L C O M E ",font=('chiller',30,'bold'),border=0
              ,bg='white',fg='purple').place(x=110,y=110)
    login1=Button(main,image=stu,bd=4,cursor='hand2',bg='#aaff00'
                  ,activebackground='#ff1a1a',command=student).place(x=40,y=190)
    login2=Button(main,image=stf,bd=4,cursor='hand2',bg='#aaff00'
                  ,activebackground='#ff1a1a',command=staff).place(x=240,y=190)
def student():
    main.destroy()    
    stu_login()
def staff():
    main.destroy()
    stf_login()
main=Tk()
global stu
global stf
logo=PhotoImage(file="images\logo.png")
main.iconphoto(False,logo)
stu=PhotoImage(file="images\stu_login.png")
stf=PhotoImage(file="images\stf_login.png")
title_logo=PhotoImage(file="images\jps.png")
main.config(background='white')
main.title("Jaycees Public School")
main.geometry("425x400")
main.resizable(0,0)
head=Label (main, image=title_logo,border=0,bg='white')
head.place(x=0,y=0)
head.bind( "<Button>", intro )
main.mainloop()
