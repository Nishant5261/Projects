import mysql.connector as con
global cur
global sql
sql=con.connect(host="localhost",user="root",passwd="17aug2004")
cur=sql.cursor()
def data():
    cur.execute('CREATE DATABASE IF NOT  EXISTS school')
    cur.execute('USE school')
    cur.execute('SHOW tables')
    s=[]
    for i in cur:
        s+=i
    if 'user_info' not in s:
        col='''CREATE TABLE  IF NOT EXISTS user_info(
                    user_id  VARCHAR(10) PRIMARY KEY,
                    name VARCHAR(30),
                    class VARCHAR(5),
                    rollno VARCHAR(5),
                    dob VARCHAR(15),
                    gender VARCHAR(10),
                    house CHAR(10),
                    father CHAR(30),
                    mother VARCHAR(30),
                    mob VARCHAR(15),
                    add_ CHAR(30),
                    pin VARCHAR(8))'''
        cur.execute(col)
        sql.commit()
        cmd=f'''INSERT INTO user_info(user_id,name,class,rollno,dob,gender,house,father,mother,mob,add_,pin)
                VALUES (11638,'Nishant Giri','12E',28,'17-Aug-2005','Male','Tilak','Pramod Kumar','Sonu Devi','6398523347','Rudrapur',263153)'''
        cur.execute(cmd)
        sql.commit()
    if 'adm_info' not in s:
        col1='''CREATE TABLE IF NOT EXISTS adm_info (
                    id_ VARCHAR(10) PRIMARY KEY,
                    name_ VARCHAR(30),
                    dob VARCHAR(15),
                    gender VARCHAR(10),
                    qual_acad CHAR(30),
                    qual_prof CHAR(30),
                    mob VARCHAR(15),
                    add_ CHAR(30),
                    pin VARCHAR(10),
                    post VARCHAR(5),
                    YOJ VARCHAR(5),
                    class VARCHAR(20),
                    subject_ VARCHAR(20))'''
        cur.execute(col1)
        sql.commit()
        cmd='''INSERT INTO adm_info(id_,name_,dob,gender,qual_acad,qual_prof,mob,add_,pin,post,YOJ,class,subject_)
                VALUES ('JPS19', 'VIVEK DALAKOTI', '04-Feb-1971', 'Male', 'POST GRADUATE', 'PH.ED.', '0123456789', 'Rudapur', '263153', 'PGT', '2013', 'SR. SECONDARY', 'COMPUTER SCIENCE')'''
        cur.execute(cmd)
        sql.commit()
    if 'adm_login_info' not in s:
        col2='''CREATE TABLE IF NOT EXISTS adm_login_info (
                    id_ VARCHAR(10) PRIMARY KEY,
                    pass VARCHAR(20))'''
        cur.execute(col2)
        sql.commit()
        cur.execute("INSERT INTO adm_login_info(id_,pass) VALUES('JPS19','CS1234')")
        sql.commit()
    if 'login_info' not in s:
        col3='''CREATE TABLE IF NOT EXISTS login_info (
                    id_ VARCHAR(10) PRIMARY KEY,
                    pass VARCHAR(20))'''
        cur.execute(col3)
        sql.commit()
        cur.execute("INSERT INTO login_info(id_,pass) VALUES(11638,1234)")
        sql.commit()
def check_stu(id_):
    cur.execute("USE school")
    cur.execute('SELECT * FROM login_info')
    for i in cur:
        if id_ in i:
            return True
    return False        
def add_stu(a,b,c,d,e,f,g,h,i,j,k,l,m):
    cur.execute("USE school")
    cmd=f'''INSERT INTO user_info(user_id,name,class,rollno,dob,gender,house,father,mother,mob,add_,pin)
                VALUES ('{a}','{b}','{c}','{d}','{e}','{f}','{g}','{h}','{i}','{j}','{k}','{l}')'''
    cmd2=f"INSERT INTO login_info(id_,pass) VALUES('{a}','{m}')"
    cur.execute(cmd)
    sql.commit()
    cur.execute(cmd2)
    sql.commit()
def profile_info(id_):
    cur.execute("USE school")
    cur.execute(f"SELECT * FROM user_info WHERE user_id='{id_}' ")
    data=cur.fetchone()
    return data
def profile_info_stf(sid_):
    cur.execute("USE school")
    cur.execute(f"SELECT * FROM adm_info WHERE id_='{sid_}' ")
    data=cur.fetchone()
    return data

def check(user_id,password):
    cur.execute("USE school")
    cur.execute(f"SELECT * FROM login_info WHERE  id_ = '{user_id}' ")
    da=cur.fetchone()
    if da==None:
        return 'invalid id'
    elif password != da[1]:
        return'invalid pass'
    else:
        return'loggedin'
def exist(a_):
    cur.execute("USE school")
    id_=str(a_)
    cur.execute(f"SELECT * FROM login_info WHERE id_='{id_}'")
    all_=cur.fetchone()
    if all_==None:
        return False
    return True
def adm_check(user_id,password):
    cur.execute("USE school")
    cur.execute(f"SELECT * FROM adm_login_info WHERE  id_ = '{user_id}' ")
    da=cur.fetchone()
    if da==None:
        return 'invalid id'
    elif password != da[1]:
        return'invalid pass'
    else:
        return'loggedin'

