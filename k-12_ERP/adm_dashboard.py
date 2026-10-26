from tkinter import *
import csv
from m import month_
from time import sleep,ctime
from tkinter import messagebox
from database import profile_info_stf,exist,check_stu,add_stu
def stu_add():
    global add
    global a
    global b
    global c
    global d
    global e
    global f
    global g
    global h
    global i
    global j
    global k
    global l
    global m
    dash.withdraw()
    sleep(1)
    add=Toplevel(dash,bg='#eeeedd')
    add.iconphoto(False,student_)
    add.geometry(position)
    add.resizable(0,0)
    add.title('ADD STUDENT')
    add.protocol("WM_DELETE_WINDOW", on_closing_stu) 
    Label(add,bg='#418CF0',bd=0,text="                    ADD    STUDENT                  ",font=('calibri',20),fg='white').place(x=0,y=0)
    Label(add,bg='#eeeedd',bd=0,text="SRNO",font=('calibri',16,'bold'),fg='#008040').place(x=15,y=50)
    Label(add,bg='#eeeedd',bd=0,text="Password",font=('calibri',16,'bold'),fg='#008040').place(x=15,y=80)
    Label(add,bg='#eeeedd',bd=0,text="Name",font=('calibri',16,'bold'),fg='#008040').place(x=15,y=110)
    Label(add,bg='#eeeedd',bd=0,text="Class",font=('calibri',16,'bold'),fg='#008040').place(x=15,y=140)
    Label(add,bg='#eeeedd',bd=0,text="Rollno.",font=('calibri',16,'bold'),fg='#008040').place(x=15,y=170)
    Label(add,bg='#eeeedd',bd=0,text="DOB(DD-MMM-YYYY)",font=('calibri',16,'bold'),fg='#008040').place(x=15,y=200)
    Label(add,bg='#eeeedd',bd=0,text="Gender",font=('calibri',16,'bold'),fg='#008040').place(x=15,y=230)
    Label(add,bg='#eeeedd',bd=0,text="House",font=('calibri',16,'bold'),fg='#008040').place(x=15,y=260)
    Label(add,bg='#eeeedd',bd=0,text="Father Name",font=('calibri',16,'bold'),fg='#008040').place(x=15,y=290)
    Label(add,bg='#eeeedd',bd=0,text="Mother Name",font=('calibri',16,'bold'),fg='#008040').place(x=15,y=320)
    Label(add,bg='#eeeedd',bd=0,text="MOB.",font=('calibri',16,'bold'),fg='#008040').place(x=15,y=350)
    Label(add,bg='#eeeedd',bd=0,text="Address",font=('calibri',16,'bold'),fg='#008040').place(x=15,y=380)
    Label(add,bg='#eeeedd',bd=0,text="Pincode",font=('calibri',16,'bold'),fg='#008040').place(x=15,y=410)
    #entry
    a=Entry(add,bd=2,bg='#ffe6e6',relief=GROOVE,width=13,font=('sans serif',14) )
    a.place(x=380,y=50,anchor=NE)
    m=Entry(add,bd=2,bg='#ffe6e6',relief=GROOVE,width=13,font=('sans serif',14))
    b=Entry(add,bd=2,bg='#ffe6e6',relief=GROOVE,width=13,font=('sans serif',14))
    c=Entry(add,bd=2,bg='#ffe6e6',relief=GROOVE,width=13,font=('sans serif',14))
    d=Entry(add,bd=2,bg='#ffe6e6',relief=GROOVE,width=13,font=('sans serif',14))
    e=Entry(add,bd=2,bg='#ffe6e6',relief=GROOVE,width=13,font=('sans serif',14))
    f=Entry(add,bd=2,bg='#ffe6e6',relief=GROOVE,width=13,font=('sans serif',14))
    g=Entry(add,bd=2,bg='#ffe6e6',relief=GROOVE,width=13,font=('sans serif',14))
    h=Entry(add,bd=2,bg='#ffe6e6',relief=GROOVE,width=13,font=('sans serif',14))
    i=Entry(add,bd=2,bg='#ffe6e6',relief=GROOVE,width=13,font=('sans serif',14))
    j=Entry(add,bd=2,bg='#ffe6e6',relief=GROOVE,width=13,font=('sans serif',14))
    k=Entry(add,bd=2,bg='#ffe6e6',relief=GROOVE,width=13,font=('sans serif',14))
    l=Entry(add,bd=2,bg='#ffe6e6',relief=GROOVE,width=13,font=('sans serif',14))
    m.place(x=380,y=80,anchor=NE)
    b.place(x=380,y=110,anchor=NE)
    c.place(x=380,y=140,anchor=NE)
    d.place(x=380,y=170,anchor=NE)
    e.place(x=380,y=200,anchor=NE)
    f.place(x=380,y=230,anchor=NE)
    g.place(x=380,y=260,anchor=NE)
    h.place(x=380,y=290,anchor=NE)
    i.place(x=380,y=320,anchor=NE)
    j.place(x=380,y=350,anchor=NE)
    k.place(x=380,y=380,anchor=NE)
    l.place(x=380,y=410,anchor=NE)
    btn1= Button(add,image=add_, border =0,cursor='hand2',bg='#eeeedd',command=a_stu)
    btn1.place(x=140,y=445)
def a_stu():
    a1=a.get()
    b1=b.get()
    c1=c.get()
    d1=d.get()
    e1=e.get()
    f1=f.get()
    g1=g.get()
    h1=h.get()
    i1=i.get()
    j1=j.get()
    k1=k.get()
    l1=l.get()
    m1=m.get()
    s=check_stu(a1)
    if a1=='' or b1=='' or c1=='' or d1=='' or e1=='' or f1=='' or g1=='' or h1=='' or i1=='' or j1=='' or k1=='' or l1=='' or m1 =='':
        messagebox.showerror('Error',"Fields can't be blank")
    elif a1.isdigit()==False:
        messagebox.showerror('Error',"Field SRNO must be numeric")
    elif d1.isdigit()==False:
        messagebox.showerror('Error',"Field Rollno. must be numeric")
    elif j1.isdigit()==False:
        messagebox.showerror('Error',"Field MOB. must be numeric")
    elif l1.isdigit()==False:
        messagebox.showerror('Error',"Field Pincode  must be numeric")
    if s==True:
        messagebox.showerror('Error',"Student already addded")
    else:
        a.delete(0,END)
        b.delete(0,END)
        c.delete(0,END)
        d.delete(0,END)
        e.delete(0,END)
        f.delete(0,END)
        g.delete(0,END)
        h.delete(0,END)
        i.delete(0,END)
        j.delete(0,END)
        k.delete(0,END)
        l.delete(0,END)
        m.delete(0,END)
        add_stu(a1,b1,c1,d1,e1,f1,g1,h1,i1,j1,k1,l1,m1)
        messagebox.showinfo('Success',"Uploaded Sucessfully")
def profile():
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
    out2.create_text(200,0,fill='white',text="Teacher Information",font=('Comic Sans MS',20),anchor=N)
    out2.create_rectangle(392,63,277,187,fill='#ff9933',width=0)
    out2.create_image(390,65,image=prof,anchor=NE)
    #labels
    out2.create_text(10,60,text="Teacher ID :",font=('Berlin Sans FB',16,'underline'),anchor=W)
    out2.create_text(10,95,text="Name :",font=('Berlin Sans FB',18,'underline'),anchor=W)
    out2.create_text(10,130,text="Gender :",font=('Berlin Sans FB',18,'underline'),anchor=W)
    out2.create_text(10,170,text="Post :",font=('Berlin Sans FB',18,'underline'),anchor=W)
    out2.create_text(10,205,text="Year Of Joining :",font=('Berlin Sans FB',18,'underline'),anchor=W)
    out2.create_text(10,240,text="DOB :",font=('Berlin Sans FB',18,'underline'),anchor=W)
    out2.create_text(10,275,text="Subject Taught :",font=('Berlin Sans FB',18,'underline'),anchor=W)
    out2.create_text(10,310,text="Class Taught :",font=('Berlin Sans FB',18,'underline'),anchor=W)
    out2.create_text(10,345,text="Qualification(acad):",font=('Berlin Sans FB',18,'underline'),anchor=W)
    out2.create_text(10,380,text="Qualification(prof) :",font=('Berlin Sans FB',18,'underline'),anchor=W)
    out2.create_text(10,415,text="Mob No. :",font=('Berlin Sans FB',18,'underline'),anchor=W)
    out2.create_text(10,450,text="Address :",font=('Berlin Sans FB',18,'underline'),anchor=W)
    out2.create_text(10,480,text="Pin :",font=('Berlin Sans FB',18,'underline'),anchor=W)
    #information
    out2.create_text(150,60,text=f"{info[0]}",font=('Berlin Sans FB',16),anchor=W,fill='#330099')
    out2.create_text(100,95,text=f"{info[1]}",font=('Berlin Sans FB',16),anchor=W,fill='#330099')
    out2.create_text(100,130,text=f"{info[3]}",font=('Berlin Sans FB',18),anchor=W,fill='#330099')
    out2.create_text(100,170,text=f"{info[9]}",font=('Berlin Sans FB',18),anchor=W,fill='#330099')
    out2.create_text(180,205,text=f"{info[10]}",font=('Berlin Sans FB',18),anchor=W,fill='#330099')
    out2.create_text(100,240,text=f"{info[2]}",font=('Berlin Sans FB',18),anchor=W,fill='#330099')
    out2.create_text(180,275,text=f"{info[12]}",font=('Berlin Sans FB',18),anchor=W,fill='#330099')
    out2.create_text(170,310,text=f"{info[11]}",font=('Berlin Sans FB',18),anchor=W,fill='#330099')
    out2.create_text(230,345,text=f"{info[4]}",font=('Berlin Sans FB',16),anchor=W,fill='#330099')
    out2.create_text(230,380,text=f"{info[5]}",font=('Berlin Sans FB',18),anchor=W,fill='#330099')
    out2.create_text(120,415,text=f"{info[6]}",font=('Berlin Sans FB',18),anchor=W,fill='#330099')
    out2.create_text(120,450,text=f"{info[7]}",font=('Berlin Sans FB',18),anchor=W,fill='#330099')
    out2.create_text(100,480,text=f"{info[8]}",font=('Berlin Sans FB',18),anchor=W,fill='#330099')
def upload():
    x=stat.get()
    date=ctime().split()
    user=entry.get()
    month=month_()
    a=exist(user)
    '''a_=open(f"rec\{user}_{month}.csv",'a')
    a_.close()'''
    if a==True:
        d=open(f'rec\{user}_{month}.csv','r')
        r=csv.reader(d)
        status__=[]
        data=''
        match=False
        for i in r:
            status__+=i
        d.close()
    if a==True:
        b=open(f'rec\{user}_{month}.csv','a',newline='')
        w=csv.writer(b)
        if x=='Absent':
            data='a'+date[2]
        elif x=='Leave':
            data='l'+date[2]
        elif x=='Present':
            data='p'+date[2]
        else:
            messagebox.showerror('Error',"Please Select Status")
        for j in status__:
            if date[2] ==j[1:]:
                match=True
        if match==False:
            c=[data]
            w.writerow(c)
            b.close()
        else:
            messagebox.showerror('Error',"Already Uploaded")
    else:
        messagebox.showerror("Error","Please Type correct SRNO.")    
def attendence():
    global stat
    global rollno
    global up
    global entry
    dash.withdraw()
    sleep(1)
    up=Toplevel(dash,bg="#e6ffff")
    out3=Canvas(up,bg='#e6ffff',bd=0,height=90,width=400)
    out3.place(x=0,y=0)
    out3.create_image(0,0,image=jps_,anchor=NW)
    up.protocol("WM_DELETE_WINDOW", on_closing_atten)
    up.title("Upload Attendance")
    up.iconphoto(False,atten_)
    up.geometry(position)
    up.resizable(0,0)
    entry=Entry(up,bd=2,bg='#ffffe6',relief=GROOVE,width=23,font=('sans serif',20))
    entry.place(x=30,y=150)
    Label(up,bg='#ffffe6',bd=0,text="Student SRNO",font=('calibri',14),fg='#ff5500').place(x=35,y=132)
    Label(up,bg='#e6ffff',bd=1,text="       Today's Status      ",font=('calibri',14),fg='#ff5500',relief=SOLID,height=2).place(x=35,y=245)
    stat=StringVar(up)
    stat.set('select')
    status=("Absent","Present","Leave")
    u=OptionMenu(up,stat,*status)
    u.config(activebackground='#ccffee',bg='#ffe6cc')
    u.place(x=230,y=250)
    btn = Button(up,image=bt, border =0,cursor='hand2',bg='white',command=upload)
    btn.place(x=150,y=360)
def up_result():
    s=sr_res.get()
    p=phy.get()
    c=chem.get()
    m=math.get()
    e=eng.get()
    cs_=cs.get()
    ex=exist(s)
    mon_=month_()
    exist_=False
    if s=='':
        messagebox.showerror('Error',"Please Enter The SRNO of Student")
    elif p=='' or c=='' or m=='' or e=='' or cs_=='':
        messagebox.showerror('Error','Enter Marks In The Fields')
    elif ex==False:
        messagebox.showerror('Error',"No student found with specified Srno.")
    elif p.isdigit() and c.isdigit() and m.isdigit() and e.isdigit() and cs_.isdigit():
        sr_res.delete(0,END)
        phy.delete(0,END)
        chem.delete(0,END)
        math.delete(0,END)
        eng.delete(0,END)
        cs.delete(0,END)
        with open(f'res\marks{mon_}.csv','r') as res__:
            r=csv.reader(res__)
            for i in r:
                if s in i:
                    exist_=True
        if exist_==False:
            with open(f'res\marks{mon_}.csv','a',newline='') as res_:
                w=csv.writer(res_)
                c=[s,p,c,m,e,cs_]
                w.writerow(c)
            messagebox.showinfo('Succes','Uploaded')
        else:
            messagebox.showerror('Error','Marks already uploaded of this child')
    else:
        messagebox.showerror('Error','Marks Should Be Numeric')        
def result():
    global Test
    global phy
    global chem
    global math
    global cs
    global eng
    global sr_res
    dash.withdraw()
    sleep(1)
    Test=Toplevel(dash,bg="#f7ffe6")
    Test.protocol("WM_DELETE_WINDOW", on_closing_test)
    Test.title("Upload Result")
    Test.iconphoto(False,test_)
    Test.geometry(position)
    Test.resizable(0,0)
    sr_res=Entry(Test,bd=2,bg='#ecffb3',relief=GROOVE,width=23,font=('sans serif',20))
    sr_res.place(x=30,y=50)
    Label(Test,bg='#ecffb3',bd=0,text="Student SRNO",font=('calibri',14),fg='#ff5500').place(x=35,y=32)
    Label(Test,bg='#b3e0ff',bd=0,text="    Subject                  Marks           ",font=('calibri',24),fg='#ff0080').place(x=0,y=132)
    Label(Test,bg='#ffcccc',bd=1,text="Physics",font=('calibri',20),fg='#ffffff',relief=SOLID).place(x=25,y=182)
    Label(Test,bg='#ffcccc',bd=1,text="Chemistry",font=('calibri',20),fg='#ffffff',relief=SOLID).place(x=25,y=222)
    Label(Test,bg='#ffcccc',bd=1,text="Maths",font=('calibri',20),fg='#ffffff',relief=SOLID).place(x=25,y=262)
    Label(Test,bg='#ffcccc',bd=1,text="English",font=('calibri',20),fg='#ffffff',relief=SOLID).place(x=25,y=302)
    Label(Test,bg='#ffcccc',bd=1,text="Computer",font=('calibri',20),fg='#ffffff',relief=SOLID).place(x=25,y=342)
    phy=Entry(Test,bd=2,bg='#f9ecf2',width=5,font=('sans serif',20))
    phy.place(x=290,y=182)
    chem=Entry(Test,bd=2,bg='#f9ecf2',width=5,font=('sans serif',20))
    chem.place(x=290,y=222)
    math=Entry(Test,bd=2,bg='#f9ecf2',width=5,font=('sans serif',20))
    math.place(x=290,y=262)
    eng=Entry(Test,bd=2,bg='#f9ecf2',width=5,font=('sans serif',20))
    eng.place(x=290,y=302)
    cs=Entry(Test,bd=2,bg='#f9ecf2',width=5,font=('sans serif',20))
    cs.place(x=290,y=342)
    submit_= Button(Test,image=bt, border =0,cursor='hand2',bg='white',command=up_result)
    submit_.place(x=150,y=400)
def on_closing_prof():
    pro_file.destroy()
    sleep(1)
    dash.deiconify()
def on_closing_stu():
    add.destroy()
    sleep(1)
    dash.deiconify()
def on_closing_test():
    Test.destroy()
    sleep(1)
    dash.deiconify()
def on_closing_atten():
    up.destroy()
    sleep(1)
    dash.deiconify()
def closing():
    a=messagebox.askokcancel('WARNING','YOU WILL BE LOGGED OUT')
    if a==True:
        dash.destroy()        
def dash_board(id_):
    global file
    file=id_
    global info
    global position
    global dash
    global prof_
    global atten_
    global student_
    global test_
    global prof
    global jps_
    global bt
    global add_
    info=profile_info_stf(id_)
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
    prof=PhotoImage(file=f"profile_teacher\{id_}.png")
    prof_=PhotoImage(file="images\pro.png")
    jps_=PhotoImage(file="images\jps2.png")
    test_=PhotoImage(file=r"images\up_result.png")
    atten_=PhotoImage(file=r"images\att_.png")
    bt=PhotoImage(file='images\submit_but.png')
    student_=PhotoImage(file=r'images\add_stu.png')
    add_=PhotoImage(file=r'images\add.png')
    dash.iconphoto(False,scl)
    out1=Canvas(dash,bg='white',bd=0,height=500,width=400)
    out1.pack(side=TOP)
    out1.create_line(0,150,400,150,fill='#ffffe6',width=2)
    out1.create_rectangle(0,0,400,148,fill='#418CF0',width=0)
    out1.create_image(390,10,image=prof,anchor=NE)
    out1.create_text(140,20,fill='white',text=f"{info[1]}",font=('Comic Sans MS',20),anchor=N)
    out1.create_text(140,70,fill='white',text=f"{info[12]}",font=('calibri',16,'bold'),anchor=N)
    out1.create_text(140,100,fill='white',text=f"{info[2]}",font=('calibri',16,'bold'),anchor=N)
    #profile
    profile_=Button(dash,image=prof_,bd=1,bg='white',activebackground='#f9ffe6',cursor='hand2'
                   ,relief=SOLID,height=140,anchor=S,command=profile)
    profile_.place(x=35,y=160)
    profile1_=Label(dash,text="PROFILE",bd=0,font=('calibri',16),bg='white')
    profile1_.place(x=45,y=148)
    #attendence
    attend=Button(dash,image=atten_,bd=1,bg='white',activebackground='#f9ffe6',cursor='hand2'
                  ,relief=SOLID,height=140,anchor=S,command=attendence)
    attend.place(x=225,y=160)
    attend_=Label(dash,text="UPLOAD ATTENDENCE",bd=0,font=('calibri',10),bg='white',anchor=W)
    attend_.place(x=228,y=150)
    #result
    test=Button(dash,image=test_,bd=1,bg='white',activebackground='#f9ffe6',cursor='hand2'
                ,relief=SOLID,height=140,anchor=S,command=result)
    test.place(x=35,y=330)
    test_t=Label(dash,text="UPLOAD RESULT",bd=0,font=('calibri',13),bg='white')
    test_t.place(x=40,y=315)
    #add_student
    student=Button(dash,image=student_,bd=1,bg='white',activebackground='#f9ffe6',cursor='hand2'
                ,relief=SOLID,height=140,anchor=S,command=stu_add)
    student.place(x=225,y=330)
    stu=Label(dash,text="ADD STUDENT",bd=0,font=('calibri',14),bg='white')
    stu.place(x=233,y=315)
    dash.mainloop()
