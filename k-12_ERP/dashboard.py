from tkinter import *
import csv
from m import month_
from time import sleep,ctime
from tkinter import messagebox
from database import profile_info,exist
def mark(sr):
    mon_=month_()
    na=['NA','NA','NA','NA','NA']
    with open(f"res\marks{mon_}.csv",'r') as m:
        r=csv.reader(m)
        for i in r:
            if i[0]==sr:
                return list(i[1:])
        return na
def te_acher():
    global teach
    dash.withdraw()
    sleep(1)
    teach=Toplevel(dash,bg="#ecf9f2")
    teach.iconphoto(False,teacher_)
    teach.geometry(position)
    teach.resizable(0,0)
    teach.title('Teachers')
    teach.protocol("WM_DELETE_WINDOW", on_closing_te)
    Label(teach,bd=0,fg='white',bg='#418CF0',text=f"          Teachers of {info[2]}          ",font=('calibri',28,'bold')).place(x=0,y=0,anchor=NW)
    Label(teach,bd=0,fg='#400080',bg='#ecf9f2',text="  Name                         Subject",font=('calibri',24,'bold')).place(x=0,y=50,anchor=NW)
    with open(f"{info[2]}.csv",'r') as f:
        r=csv.reader(f)
        t=[]
        for i in r:
            t+=i
    Label(teach,bd=0,fg='#444422',bg='#ecf9f2',text=f"{t[0]}",font=('calibri',20,'bold')).place(x=15,y=120,anchor=NW)
    Label(teach,bd=0,fg='#444422',bg='#ecf9f2',text=f"{t[2]}",font=('calibri',20,'bold')).place(x=15,y=160,anchor=NW)
    Label(teach,bd=0,fg='#444422',bg='#ecf9f2',text=f"{t[4]}",font=('calibri',20,'bold')).place(x=15,y=200,anchor=NW)
    Label(teach,bd=0,fg='#444422',bg='#ecf9f2',text=f"{t[6]}",font=('calibri',20,'bold')).place(x=15,y=240,anchor=NW)
    Label(teach,bd=0,fg='#444422',bg='#ecf9f2',text=f"{t[8]}",font=('calibri',20,'bold')).place(x=15,y=280,anchor=NW)
    Label(teach,bd=0,fg='#444422',bg='#ecf9f2',text=f"{t[1]}",font=('calibri',20,'bold')).place(x=385,y=120,anchor=NE)
    Label(teach,bd=0,fg='#444422',bg='#ecf9f2',text=f"{t[3]}",font=('calibri',20,'bold')).place(x=385,y=160,anchor=NE)
    Label(teach,bd=0,fg='#444422',bg='#ecf9f2',text=f"{t[5]}",font=('calibri',20,'bold')).place(x=385,y=200,anchor=NE)
    Label(teach,bd=0,fg='#444422',bg='#ecf9f2',text=f"{t[7]}",font=('calibri',20,'bold')).place(x=385,y=240,anchor=NE)
    Label(teach,bd=0,fg='#444422',bg='#ecf9f2',text=f"{t[9]}",font=('calibri',20,'bold')).place(x=385,y=280,anchor=NE)       
def stu_result():
    global re_sult   
    dash.withdraw()
    sleep(1)
    re_sult=Toplevel(dash)
    re_sult.iconphoto(False,prof_)
    re_sult.geometry(position)
    re_sult.resizable(0,0)
    re_sult.title('PROFILE')
    re_sult.protocol("WM_DELETE_WINDOW", on_closing_res)
    out2=Canvas(re_sult,bg='#e6fff2',bd=0,height=500,width=400)
    out2.pack()
    out2.create_rectangle(0,0,400,40,fill='#418CF0',width=0)
    out2.create_rectangle(270,150,271,500,fill='#418CF0',width=0)
    out2.create_text(200,0,fill='white',text="Student Result",font=('Comic Sans MS',20),anchor=N)
    out2.create_rectangle(0,150,400,180,fill='#418CF0',width=0)
    out2.create_text(200,145,fill='white',text="Subject                   Marks",font=('Comic Sans MS',20),anchor=N)
    out2.create_text(10,60,text="Admission NO. :",font=('Berlin Sans FB',16,'underline'),anchor=W)
    out2.create_text(10,95,text="Name :",font=('Berlin Sans FB',18,'underline'),anchor=W)
    out2.create_text(10,130,text="Class :",font=('Berlin Sans FB',18,'underline'),anchor=W)
    out2.create_text(150,130,text="RollNo. :",font=('Berlin Sans FB',18,'underline'),anchor=W)
    out2.create_text(170,60,text=f"{info[0]}",font=('Berlin Sans FB',16),anchor=W,fill='#330099')
    out2.create_text(100,95,text=f"{info[1]}",font=('Berlin Sans FB',18),anchor=W,fill='#330099')
    out2.create_text(100,130,text=f"{info[2]}",font=('Berlin Sans FB',18),anchor=W,fill='#330099')
    out2.create_text(240,130,text=f"{info[3]}",font=('Berlin Sans FB',18),anchor=W,fill='#330099')
    #subjects
    out2.create_text(10,200,text="Physics",font=('Berlin Sans FB',20,),anchor=W)
    out2.create_text(10,240,text="Chemistry",font=('Berlin Sans FB',20,),anchor=W)
    out2.create_text(10,280,text="Maths",font=('Berlin Sans FB',20,),anchor=W)
    out2.create_text(10,320,text="English",font=('Berlin Sans FB',20,),anchor=W)
    out2.create_text(10,360,text="Computer science",font=('Berlin Sans FB',20,),anchor=W)
    mark_s=(mark(file))
    #marks
    out2.create_text(300,200,text=f"{mark_s[0]}",font=('Berlin Sans FB',20,),anchor=W)
    out2.create_text(300,240,text=f"{mark_s[1]}",font=('Berlin Sans FB',20,),anchor=W)
    out2.create_text(300,280,text=f"{mark_s[2]}",font=('Berlin Sans FB',20,),anchor=W)
    out2.create_text(300,320,text=f"{mark_s[3]}",font=('Berlin Sans FB',20,),anchor=W)
    out2.create_text(300,360,text=f"{mark_s[4]}",font=('Berlin Sans FB',20,),anchor=W)
    
def stu_profile():
    global pro_file
    dash.withdraw()
    sleep(1)
    pro_file=Toplevel(dash)
    pro_file.iconphoto(False,prof_)
    pro_file.geometry(position)
    pro_file.resizable(0,0)
    pro_file.title('PROFILE')
    pro_file.protocol("WM_DELETE_WINDOW", on_closing_prof)
    out2=Canvas(pro_file,bg='#e6fff2',bd=0,height=500,width=400)
    out2.pack()
    out2.create_rectangle(0,0,400,40,fill='#418CF0',width=0)
    out2.create_text(200,0,fill='white',text="Student Information",font=('Comic Sans MS',20),anchor=N)
    out2.create_rectangle(387,63,270,195,fill='#ff9933',width=0)
    out2.create_image(385,65,image=prof,anchor=NE)
    #labels
    out2.create_text(10,60,text="Admission NO. :",font=('Berlin Sans FB',16,'underline'),anchor=W)
    out2.create_text(10,95,text="Name :",font=('Berlin Sans FB',18,'underline'),anchor=W)
    out2.create_text(10,130,text="Class :",font=('Berlin Sans FB',18,'underline'),anchor=W)
    out2.create_text(150,130,text="RollNo. :",font=('Berlin Sans FB',18,'underline'),anchor=W)
    out2.create_text(10,170,text="DOB :",font=('Berlin Sans FB',18,'underline'),anchor=W)
    out2.create_text(10,205,text="Gender :",font=('Berlin Sans FB',18,'underline'),anchor=W)
    out2.create_text(10,240,text="House :",font=('Berlin Sans FB',18,'underline'),anchor=W)
    out2.create_text(10,275,text="Father Name :",font=('Berlin Sans FB',18,'underline'),anchor=W)
    out2.create_text(10,310,text="Mother Name :",font=('Berlin Sans FB',18,'underline'),anchor=W)
    out2.create_text(10,345,text="Mob No. :",font=('Berlin Sans FB',18,'underline'),anchor=W)
    out2.create_text(10,380,text="Address :",font=('Berlin Sans FB',18,'underline'),anchor=W)
    out2.create_text(10,415,text="Pin :",font=('Berlin Sans FB',18,'underline'),anchor=W)
    #information
    out2.create_text(170,60,text=f"{info[0]}",font=('Berlin Sans FB',16),anchor=W,fill='#330099')
    out2.create_text(100,95,text=f"{info[1]}",font=('Berlin Sans FB',18),anchor=W,fill='#330099')
    out2.create_text(100,130,text=f"{info[2]}",font=('Berlin Sans FB',18),anchor=W,fill='#330099')
    out2.create_text(240,130,text=f"{info[3]}",font=('Berlin Sans FB',18),anchor=W,fill='#330099')
    out2.create_text(100,170,text=f"{info[4]}",font=('Berlin Sans FB',18),anchor=W,fill='#330099')
    out2.create_text(100,205,text=f"{info[5]}",font=('Berlin Sans FB',18),anchor=W,fill='#330099')
    out2.create_text(100,240,text=f"{info[6]}",font=('Berlin Sans FB',18),anchor=W,fill='#330099')
    out2.create_text(170,275,text=f"{info[7]}",font=('Berlin Sans FB',18),anchor=W,fill='#330099')
    out2.create_text(170,310,text=f"{info[8]}",font=('Berlin Sans FB',18),anchor=W,fill='#330099')
    out2.create_text(170,345,text=f"{info[9]}",font=('Berlin Sans FB',18),anchor=W,fill='#330099')
    out2.create_text(110,380,text=f"{info[10]}",font=('Berlin Sans FB',18),anchor=W,fill='#330099')
    out2.create_text(100,415,text=f"{info[11]}",font=('Berlin Sans FB',18),anchor=W,fill='#330099')
                    
def attendence_():
    y=ctime().split()
    year=y[-1]
    c_date=month()
    if c_date in ['01','03','05','07','08','10','12']:
        da=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
    elif c_date in ['04','06','09','11']:
        da=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
    else:
        if int(year)%4==0:
            da=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]
        else:
            da=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]
    attend=[]
    global Attend
    dash.withdraw()
    sleep(1)
    Attend=Toplevel(dash,bg='white')
    Attend.iconphoto(False,atten_)
    mon=month()
    rec=exist(file)
    if rec==True:
        atten=open(f"rec\{file}_{mon}.csv",'a')
        atten.close()        
    atten=open(f"rec\{file}_{mon}.csv",'r')
    r=csv.reader(atten)
    for i in r:
        attend+=i
    screen_width = Attend.winfo_screenwidth()
    screen_height = Attend.winfo_screenheight()
    center_x = int(screen_width/2 - 450/ 2)
    center_y = int(screen_height/2 - 320/ 2)
    position=f"450x320+{center_x}+{center_y}"
    Attend.geometry(position)
    Attend.title('Attendence')
    Attend.resizable(0,0)
    Label(Attend,text="     Attendence Of The Month    ",bg="silver",fg="greenyellow",font="algerian 22 ",
              relief=GROOVE,borderwidth=5).grid(row=0,column=0,columnspan=8,sticky=N)
    cl=1
    row=1
    present_count=0
    absent_count=0
    leave_count=0
    a=int(len(da))
    b=int(len(attend))
    for j in attend:
        s=j[0]
        i=j[1:]
        if s=='p':
            l=Label(Attend,text=f"{i}",bg="#ccff99",relief=GROOVE,borderwidth='5',padx=16,pady=10,width=3)
            l.grid(row=row,column=cl,sticky=NSEW)
            present_count+=1
            cl+=1
        if s=='a':
            l=Label(Attend,text=f"{i}",bg="#ffb399",relief=SUNKEN,borderwidth='5',padx=16,pady=10,width=3)
            l.grid(row=row,column=cl,sticky=NSEW)
            cl+=1
            absent_count+=1
        if s=='l':
            l=Label(Attend,text=f"{i}",bg="#99e6ff",relief=RAISED,borderwidth='5',padx=16,pady=10,width=3)
            l.grid(row=row,column=cl,sticky=NSEW)
            cl+=1
            leave_count+=1
        if cl==8:        
            row+=1
            cl=1
    if a>b:
        for i in range(b+1,a+1):
            l=Label(Attend,text=f"{i}",bg="white",relief=RAISED,borderwidth='5',padx=16,pady=10,width=3)
            l.grid(row=row,column=cl,sticky=NSEW)
            cl+=1
            if cl==8:        
                row+=1
                cl=1
    frame=Frame(Attend,bg="white")
    frame.place(x=210,y=240)
    Label(frame,text=f"~>Present : {present_count}",bg="white",fg="navy",font="arial 12 bold").grid(row=0,column=1)
    Label(frame,text=f"~>Absent  :{absent_count}",bg="white",fg="navy",font="arial 12 bold").grid(row=1, column=1)
    Label(frame,text=f"~>Leave :   {leave_count}",bg="white",fg="navy",font="arial 12 bold").grid(row=2,column=1)
    Button(Attend,text="Close",command=on_closing_atten,bg="tomato",fg="midnightblue",relief=RAISED,
          borderwidth=5,activebackground="bisque",font="calibri 12 bold").place(x=390,y=275)
    Label(frame,bg="#ccff99",text="  ").grid(row=0, column=0,ipadx=5)
    Label(frame,bg="#ffb399",text="  ").grid(row=1, column=0,ipadx=5)
    Label(frame,bg="#99e6ff",text="  ").grid(row=2, column=0,ipadx=5)
    Attend.protocol("WM_DELETE_WINDOW",on_closing_atten)
def on_closing_prof():
    pro_file.destroy()
    sleep(1)
    dash.deiconify()
def on_closing_te():
    teach.destroy()
    sleep(1)
    dash.deiconify()
def on_closing_res():
    re_sult.destroy()
    sleep(1)
    dash.deiconify()
def on_closing_atten():
    Attend.destroy()
    sleep(1)
    dash.deiconify()
def closing():
    a=messagebox.askokcancel('WARNING','YOU WILL BE LOGGED OUT')
    if a==True:
        dash.destroy()
        
def dash_board(id_):
    global file
    file=str(id_)
    global info
    global position
    global dash
    global prof_
    global atten_
    global teacher_
    global test_
    global prof
    global pass_
    info=profile_info(id_)
    dash=Tk()
    dash.protocol("WM_DELETE_WINDOW",closing)
    screen_width = dash.winfo_screenwidth()
    screen_height = dash.winfo_screenheight()
    center_x = int(screen_width/2 - 400/ 2)
    center_y = int(screen_height/2 - 500/ 2)
    position=f"400x500+{center_x}+{center_y}"
    dash.geometry(position)
    dash.title("JAYCEES PUBLIC SCHOOL")
    dash.resizable(0,0)
    dash.configure(bg="#ffffff")
    scl=PhotoImage(file="images\logo.png")
    prof=PhotoImage(file=f"profile\{id_}.png")
    prof_=PhotoImage(file="images\profile.png")
    test_=PhotoImage(file=r"images\result.png")
    atten_=PhotoImage(file=r"images\attendence.png")
    teacher_=PhotoImage(file=r'images\teacher.png')
    #pass_=PhotoImage(file=r"images\ch_.png")
    dash.iconphoto(False,scl)
    out1=Canvas(dash,bg='white',bd=0,height=500,width=400)
    out1.pack(side=TOP)
    out1.create_line(0,150,400,150,fill='#ffffe6',width=2)
    out1.create_rectangle(0,0,400,148,fill='#418CF0',width=0)
    out1.create_image(390,10,image=prof,anchor=NE)
    out1.create_text(140,20,fill='white',text=f"{info[1]}",font=('Comic Sans MS',20),anchor=N)
    out1.create_text(140,70,fill='white',text=f"{info[2]}",font=('calibri',16,'bold'),anchor=N)
    out1.create_text(140,100,fill='white',text=f"{info[4]}",font=('calibri',16,'bold'),anchor=N)
    #profile
    profile_=Button(dash,image=prof_,bd=1,bg='white',activebackground='#f9ffe6',cursor='hand2'
                   ,relief=SOLID,height=140,anchor=S,command=stu_profile)
    profile_.place(x=35,y=160)
    profile1_=Label(dash,text="PROFILE",bd=0,font=('calibri',16),bg='white')
    profile1_.place(x=45,y=148)
    #attendence
    attend=Button(dash,image=atten_,bd=1,bg='white',activebackground='#f9ffe6',cursor='hand2'
                  ,relief=SOLID,height=140,anchor=S,command=attendence_)
    attend.place(x=225,y=160)
    attend_=Label(dash,text="ATTENDENCE",bd=0,font=('calibri',14),bg='white')
    attend_.place(x=235,y=148)
    #result
    test=Button(dash,image=test_,bd=1,bg='white',activebackground='#f9ffe6',cursor='hand2'
                ,relief=SOLID,height=140,anchor=S,command=stu_result)
    test.place(x=35,y=330)
    test_t=Label(dash,text="RESULT",bd=0,font=('calibri',16),bg='white')
    test_t.place(x=40,y=315)
    #teachers
    teacher=Button(dash,image=teacher_,bd=1,bg='white',activebackground='#f9ffe6',cursor='hand2'
                ,relief=SOLID,height=140,anchor=S,command=te_acher)
    teacher.place(x=225,y=330)
    teach=Label(dash,text="TEACHERS",bd=0,font=('calibri',16),bg='white')
    teach.place(x=235,y=315)
    dash.mainloop()
