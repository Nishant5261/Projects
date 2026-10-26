from tkinter import *
from time import sleep
from tkinter import messagebox
from database import adm_check
from adm_dashboard import dash_board
d=0
def stf_login():
    login = Tk()
    login.geometry("400x500")
    login.title("JAYCEES PUBLIC SCHOOL")
    login.configure(bg="#ffffff")
    login.resizable(0,0)
    scl=PhotoImage(file="images\logo.png")
    bt=PhotoImage(file="images\login_but.png")
    hide=PhotoImage(file='images\hide.png')    
    show=PhotoImage(file='images\show.png')
    login.iconphoto(False,scl)
    def reset():
        entry1.delete(0,END)
        entry2.delete(0,END)
    def submit():
        user_name =entry1.get()
        password = entry2.get()
        res=adm_check(user_name,password)
        if (user_name == "" and password ==""):
            messagebox.showerror("Error","Please Type User ID and Password")
        elif (user_name == ""):
            messagebox.showerror("Error","Please Type your User ID")
        elif (password == ""):
            messagebox.showerror("Error","Please Type your Password")
        elif (res=='invalid id'):
            messagebox.showerror("Error","Please Type correct User ID")
        elif (res == "invalid pass"):
            messagebox.showerror("Error","Please Type correct Password")
        elif (res == 'loggedin'):
            reset()
            messagebox.showinfo("Notice","Succesfully Logged In \n Thank You :)")
            login.destroy()
            sleep(1)
            dash_board(user_name)
            
    def hide1(ev):
        show_.destroy()
        hide2=Button(login,image=hide,bd=0,relief=FLAT)
        hide2.place(x=335,y=274)   
    def show1(ev):
        global d
        if d==0:
            hide_['image']=show
            entry2['show']=''
            d=1
        else:
            hide_['image']=hide
            entry2['show']='*'
            d=0
    scl_logo=Label(login,image=scl,bd=0,bg='white').pack(pady=15,anchor=CENTER)
    label1 = Label(login, font = ("calibri", 18), text = "sign in to Account",bg='white').place(x=115,y=120)
    btn = Button(login,image=bt, border =0,cursor='hand2',command=submit,bg='white')
    btn.pack(side=BOTTOM,anchor=CENTER,pady=80)
    entry1=Entry(login,bd=2,highlightcolor='red',relief=GROOVE,width=23,font=('sans serif',20),bg='#e6ffe6')
    entry2=Entry(login,bd=2,highlightcolor='red',relief=GROOVE,width=23,font=('sans serif',20 )
                 ,show='*')
    entry1.place(x=25,y=180)
    entry2.place(x=25,y=270)
    user_name=Label(login,bg='#e6ffe6',bd=0,text="Staff ID",font=('calibri',14),fg='#ff0055').place(x=30,y=164)
    password=Label(login,bg='white',bd=0,text="Password",font=('calibri',14),fg='#2a8000').place(x=30,y=254)
    hide_=Button(login,image=hide,bd=0,cursor='hand2')
    hide_.place(x=335,y=274)
    hide_.bind('<Button>',show1)
    login.mainloop()


