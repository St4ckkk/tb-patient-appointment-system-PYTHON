from tkinter import *
import sqlite3
import calendar
from datetime import datetime,date,timedelta
from tkinter import scrolledtext,messagebox,ttk
from tkcalendar import DateEntry


bl = "#1c9cd4"
bl1= "#0b96d3"
wh = 'white'

now = datetime.now()


def time_in_range(start, end, x):
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

class CalendarView:
    def __init__(self, parent,appointment):
        self.parent = parent
        self.appointment = appointment
        self.cal = calendar.TextCalendar(calendar.MONDAY)
        self.year = int(now.strftime('%Y'))
        self.month = int(now.strftime('%m'))
        self.wid = []
        
        self.setup(self.year, self.month)
    
    # Resets the buttons
    def clear(self):
        for w in self.wid[:]:
            w.grid_forget()
            self.wid.remove(w)
    
    # Moves to previous month/year on calendar
    def go_prev(self):
        if self.month > 1:
            self.month -= 1
        else:
            self.month = 12
            self.year -= 1
        self.clear()
        self.setup(self.year, self.month)
    
    # Moves to next month/year on calendar
    def go_next(self):
        if self.month < 12:
            self.month += 1
        else:
            self.month = 1
            self.year += 1
        
        self.clear()
        self.setup(self.year, self.month)
    
    # Called on date button press
    def selection(self, day,month,year):
        print(day,month,year)
        master = Toplevel()
        master.config(bg=bl)
        master.title('Daily View')
        h = master.winfo_screenheight() 
        w = master.winfo_screenwidth()
        master.resizable(0,0)
        canvas = Canvas(master, width=w-40, height=h-40,bg=bl)  # make canvas big enough to see the rectangles
        scrollbar = Scrollbar(master)
        scrollbar.config(command=canvas.yview)
        canvas.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right",fill=Y)
        canvas.pack(side="left",expand=YES,fill=BOTH)

        canvas.create_text(w/2-20,40,fill=wh,font="HELVETICA 24 bold",text=str(day)+'/'+str(month)+'/'+str(year))
        canvas.create_line(w/2-20,60,w/2-20,h,fill=wh)
        canvas.create_text(w/4,70,fill=wh,text='BED 1',font="HELVETICA 13 bold")
        canvas.create_text(w-300,70,fill=wh,text='BED 2',font="HELVETICA 13 bold")
        hours = [9,10,11,12,1,2,3,4,5,6]
        line = []
        text = []
        l = {}
        t = {}
        y_val = []
        y = 90
        for i in range(9,12):
            txt = canvas.create_text(20,y,fill=wh,text=str(i)+' AM')
            ln = canvas.create_line(60,y,w-40,y,fill=wh)
            y_val.append(y)
            line.append(ln)
            text.append(txt)
            l[i] = ln
            t[i] = txt
            y+=65
        txt = canvas.create_text(20,y,fill=wh,text=str(12)+' PM')
        ln = canvas.create_line(60,y,w-40,y,fill=wh)
        y_val.append(y)
        line.append(ln)
        text.append(txt)
        l[12] = ln
        t[12] = txt
        y+=65
        for i in range(1,7):
            txt = canvas.create_text(20,y,fill=wh,text=str(i)+' PM')
            ln = canvas.create_line(60,y,w-40,y,fill=wh)
            y_val.append(y)
            line.append(ln)
            text.append(txt)
            l[i] = ln
            t[i] = txt
            y+=65
        up = []

        for i in range(len(self.appointment)):
            if self.appointment[i][4] == str(year)+'-'+str(month).zfill(2)+'-'+str(day):
                try:
                    if int(self.appointment[i][5]) in hours and int(self.appointment[i][6]) in hours:
                        value = hours.index(int(self.appointment[i][5]))
                        new_y = y_val[value]
                        value1 = hours.index(int(self.appointment[i][6]))
                        new_y1 = y_val[value1]
                        
                        canvas.delete(l[int(self.appointment[i][5])])
                        canvas.delete(t[int(self.appointment[i][5])])
                        t.pop(int(self.appointment[i][5]))
                        l.pop(int(self.appointment[i][5]))

                        canvas.delete(l[int(self.appointment[i][6])])
                        canvas.delete(t[int(self.appointment[i][6])])
                        t.pop(int(self.appointment[i][6]))
                        l.pop(int(self.appointment[i][6]))

                        if self.appointment[i][-3] == 1:
                            if value < 3:
                                t1 = canvas.create_text(30,new_y,fill=wh,text=self.appointment[i][5]+' AM')
                                t2 = canvas.create_text(30,new_y1,fill=wh,text=self.appointment[i][6]+' AM')

                            else:
                                t1 = canvas.create_text(30,new_y,fill=wh,text=self.appointment[i][5]+' PM')
                                t2 = canvas.create_text(30,new_y1,fill=wh,text=self.appointment[i][6]+' PM')
                          
                            print('ff')
                            t3 = canvas.create_line(60,new_y,int(w)/2-20,new_y,fill=wh)
                            t4 = canvas.create_line(60,new_y1,int(w)/2-20,new_y1,fill=wh)
                            
                            canvas.create_text(140,y_val[value]+38,fill=wh,font="HELVETICA 10 bold",text='Patient Name: '+'\n\t'+self.appointment[i][1]+' '+self.appointment[i][2])

                        elif self.appointment[i][-3] == 2:
                            if value < 3:
                                t1 = canvas.create_text(int(w)/2,new_y,fill=wh,text=self.appointment[i][5]+' AM')
                                t2 = canvas.create_text(int(w)/2,new_y1,fill=wh,text=self.appointment[i][6]+' AM')
                            else:
                                t1 = canvas.create_text(int(w)/2,new_y,fill=wh,text=self.appointment[i][5]+' PM')
                                t2 =canvas.create_text(int(w)/2,new_y1,fill=wh,text=self.appointment[i][6]+' PM')

                            t3 = canvas.create_line(int(w)/2+20,new_y,int(w)-40,new_y,fill=wh)
                            t4 = canvas.create_line(int(w)/2+20,new_y1,int(w)-40,new_y1,fill=wh)

                            canvas.create_text(int(w)/2+150,y_val[value]+38,fill=wh,font="HELVETICA 10 bold",text='Patient Name: '+'\n\t'+self.appointment[i][1]+' '+self.appointment[i][2])

                        t[int(self.appointment[i][5])] = t1
                        t[int(self.appointment[i][6])] = t2

                        l[int(self.appointment[i][5])] = t3
                        l[int(self.appointment[i][6])] = t4
                        
                        up.append(value)
                        up.append(value1)
                except:
                    try:
                        if int(self.appointment[i][5]) in hours:
                            g = self.appointment[i][6].split(':')
                            try:
                                start_time = datetime.strptime(self.appointment[i][5], '%I:%M')
                            except:
                                start_time = datetime.strptime(self.appointment[i][5], '%I')
                            try:
                                stop_time = datetime.strptime(self.appointment[i][6], '%I:%M')
                            except:
                                stop_time = datetime.strptime(self.appointment[i][6], '%I')

                            datetime1 = datetime.combine(date.today(), start_time.time())
                            datetime2 = datetime.combine(date.today(), stop_time.time())
                            time_elapsed = datetime2 - datetime1
                            seconds = time_elapsed.total_seconds()
                            hour = seconds // 3600
                            minutes = (seconds % 3600) // 60
                            if int(hour) < 0:
                                hour+=12
                                
                            value = hours.index(int(self.appointment[i][5]))
                            new_y = y_val[value]
                            value1 = hours.index(int(g[0]))
                            new_y1 = y_val[value1]+70%int(g[1])
                            
                            canvas.delete(l[int(self.appointment[i][5])])
                            canvas.delete(t[int(self.appointment[i][5])])
                            t.pop(int(self.appointment[i][5]))
                            l.pop(int(self.appointment[i][5]))

                            canvas.delete(l[int(g[0])])
                            canvas.delete(t[int(g[0])])
                            t.pop(int(g[0]))
                            l.pop(int(g[0]))
            
                            if self.appointment[i][-3] == 1:
                                if value < 3:
                                    t1 = canvas.create_text(30,new_y,fill=wh,text=self.appointment[i][5]+' AM')
                                    t2 = canvas.create_text(30,new_y1,fill=wh,text=self.appointment[i][6]+' AM')
                                else:
                                    t1 = canvas.create_text(30,new_y,fill=wh,text=self.appointment[i][5]+' PM')
                                    t2 = canvas.create_text(30,new_y1,fill=wh,text=self.appointment[i][6]+' PM')
                                    
                                t3 = canvas.create_line(60,new_y,int(w)/2-20,new_y,fill=wh)
                                t4 = canvas.create_line(60,new_y1,int(w)/2-20,new_y1,fill=wh)
                                
                                canvas.create_text(140,y_val[value]+38,fill=wh,font="HELVETICA 10 bold",text='Patient Name: '+'\n\t'+self.appointment[i][1]+' '+self.appointment[i][2])

                            elif self.appointment[i][-3] == 2:
                                if value < 3:
                                    t1 = canvas.create_text(int(w)/2,new_y,fill=wh,text=self.appointment[i][5]+' AM')
                                    t2 = canvas.create_text(int(w)/2,new_y1,fill=wh,text=self.appointment[i][6]+' AM')
                                else:
                                    t1 = canvas.create_text(int(w)/2,new_y,fill=wh,text=self.appointment[i][5]+' PM')
                                    t2 = canvas.create_text(int(w)/2,new_y1,fill=wh,text=self.appointment[i][6]+' PM')
                                    
                                t3 = canvas.create_line(int(w)/2+20,new_y,int(w)-40,new_y,fill=wh)
                                t4 = canvas.create_line(int(w)/2+20,new_y1,int(w)-40,new_y1,fill=wh)

                                canvas.create_text(int(w)/2+150,y_val[value]+38,fill=wh,font="HELVETICA 10 bold",text='Patient Name: '+'\n\t'+self.appointment[i][1]+' '+self.appointment[i][2])
                                    
                            t[int(self.appointment[i][5])] = t1
                            t[int(g[0])] = t2

                            l[int(self.appointment[i][5])] = t3
                            l[int(g[0])] = t4

                            up.append(value)
                            up.append(value1)
                            
                    except:
                        try:
                            if int(self.appointment[i][6]) in hours:
                                g = self.appointment[i][5].split(':')
                                try:
                                    start_time = datetime.strptime(self.appointment[i][5], '%I:%M')
                                except:
                                    start_time = datetime.strptime(self.appointment[i][5], '%I')
                                try:
                                    stop_time = datetime.strptime(self.appointment[i][6], '%I:%M')
                                except:
                                    stop_time = datetime.strptime(self.appointment[i][6], '%I')

                                datetime1 = datetime.combine(date.today(), start_time.time())
                                datetime2 = datetime.combine(date.today(), stop_time.time())
                                time_elapsed = datetime2 - datetime1
                                seconds = time_elapsed.total_seconds()
                                hour = seconds // 3600
                                minutes = (seconds % 3600) // 60
                                if int(hour) < 0:
                                    hour+=12
                                value = hours.index(int(g[0]))
                                new_y = y_val[value]+70%int(g[1])


                                if int(hour) == 1 and int(minutes) > 0:
                                    value = hours.index(int(self.appointment[i][6]))
                                    new_y = y_val[value]
                                    value1 = hours.index(int(g[0]))
                                    new_y1 = y_val[value1]+70%int(g[1])
                                

                                    
                                    canvas.delete(l[int(self.appointment[i][6])])
                                    canvas.delete(t[int(self.appointment[i][6])])
                                    t.pop(int(self.appointment[i][6]))
                                    l.pop(int(self.appointment[i][6]))

                                    if self.appointment[i][-3] == 1:
                                        if value1 < 3:
                                            t1 = canvas.create_text(30,new_y1,fill=wh,text=self.appointment[i][5]+' AM')
                                            t2 = canvas.create_text(30,new_y,fill=wh,text=self.appointment[i][6]+' AM')
                                        else:
                                            t1 = canvas.create_text(30,new_y1,fill=wh,text=self.appointment[i][5]+' PM')
                                            t2 = canvas.create_text(30,new_y,fill=wh,text=self.appointment[i][6]+' PM')
                                            
                                        t3 = canvas.create_line(60,new_y,int(w)/2-20,new_y,fill=wh)
                                        t4 = canvas.create_line(60,new_y1,int(w)/2-20,new_y1,fill=wh)
                                        
                                        canvas.create_text(140,y_val[value1]+38,fill=wh,font="HELVETICA 10 bold",text='Patient Name: '+'\n\t'+self.appointment[i][1]+' '+self.appointment[i][2])

                                    elif self.appointment[i][-3] == 2:
                                        if value1 < 3:
                                            t1 = canvas.create_text(int(w)/2,new_y1,fill=wh,text=self.appointment[i][5]+' AM')
                                            t2 = canvas.create_text(int(w)/2,new_y,fill=wh,text=self.appointment[i][6]+' AM')
                                        else:
                                            t1 = canvas.create_text(int(w)/2,new_y1,fill=wh,text=self.appointment[i][5]+' PM')
                                            t2 = canvas.create_text(int(w)/2,new_y,fill=wh,text=self.appointment[i][6]+' PM')
                                            
                                        t3 = canvas.create_line(int(w)/2+20,new_y,int(w)-40,new_y,fill=wh)
                                        t4 = canvas.create_line(int(w)/2+20,new_y1,int(w)-40,new_y1,fill=wh)

                                        canvas.create_text(int(w)/2+150,y_val[value1]+38,fill=wh,font="HELVETICA 10 bold",text='Patient Name: '+'\n\t'+self.appointment[i][1]+' '+self.appointment[i][2])
                                
                                t[int(g[0])] = t1
                                t[int(self.appointment[i][6])] = t2

                                l[int(g[0])] = t3
                                l[int(self.appointment[i][6])] = t4
                                up.append(value)
                                up.append(value1)
                        except:
                            if len(up)==0:
                                g = self.appointment[i][5].split(':')
                                g1 = self.appointment[i][6].split(':')
                                res = int(g1[0])-int(g[0])
                                value = hours.index(int(g[0]))
                                value1 = hours.index(int(g1[0]))
                                new_y = y_val[value]+70%int(g[1])
                                new_y1 = y_val[value1]+70%int(g1[1])

                                canvas.delete(l[int(g1[0])])
                                canvas.delete(t[int(g1[0])])
                                t.pop(int(g1[0]))
                                l.pop(int(g1[0]))
                                
                                if res == 1:
                                    if self.appointment[i][-3] == 1:
                                        if value < 3:
                                            t1=canvas.create_text(30,new_y,fill=wh,text=self.appointment[i][5]+' AM')
                                            t2=canvas.create_text(30,new_y1,fill=wh,text=self.appointment[i][6]+' AM')
                                        else:
                                            t1=canvas.create_text(30,new_y,fill=wh,text=self.appointment[i][5]+' PM')
                                            t2=canvas.create_text(30,new_y1,fill=wh,text=self.appointment[i][6]+' PM')

                                        t3=canvas.create_line(60,new_y,int(w)/2-20,new_y,fill=wh)
                                        t4=canvas.create_line(60,new_y1,int(w)/2-20,new_y1,fill=wh)

                                        canvas.create_text(140,y_val[value]+63,fill=wh,font="HELVETICA 10 bold",text='Patient Name: '+'\n\t'+self.appointment[i][1]+' '+self.appointment[i][2])

                                    elif self.appointment[i][-3] == 2:
                                        if value < 3:
                                            t1=canvas.create_text(int(w)/2,new_y1,fill=wh,text=self.appointment[i][6]+' AM')
                                            t2=canvas.create_text(int(w)/2,new_y,fill=wh,text=self.appointment[i][5]+' AM')
                                        else:
                                            t1=canvas.create_text(int(w)/2,new_y,fill=wh,text=self.appointment[i][5]+' PM')
                                            t2=canvas.create_text(int(w)/2,new_y1,fill=wh,text=self.appointment[i][6]+' PM')
                                        
                                        t3=canvas.create_line(int(w)/2+20,new_y,int(w)-40,new_y,fill=wh)
                                        t4=canvas.create_line(int(w)/2+20,new_y1,int(w)-40,new_y1,fill=wh)
                                        val = hours.index(int(g[0]))
                                        canvas.create_text((w/2)+150,y_val[val]+63,fill=wh,font="HELVETICA 10 bold",text='Patient Name: '+'\n\t'+self.appointment[i][1]+' '+self.appointment[i][2])
                                elif res == 2:
                                   if self.appointment[i][-3] == 1:
                                        if value < 3:
                                            t1=canvas.create_text(30,new_y,fill=wh,text=self.appointment[i][5]+' AM')
                                            t2=canvas.create_text(30,new_y1,fill=wh,text=self.appointment[i][6]+' AM')
                                        else:
                                            t1=canvas.create_text(30,new_y,fill=wh,text=self.appointment[i][5]+' PM')
                                            t2=canvas.create_text(30,new_y1,fill=wh,text=self.appointment[i][6]+' PM')
                                            
                                        canvas.delete(int(g1[0])-1)
                                        canvas.delete(int(g1[0])-1)
                                        t.pop(int(g1[0]-1))
                                        l.pop(int(g1[0]-1))

                                        t3=canvas.create_line(60,new_y,int(w)/2-20,new_y,fill=wh)
                                        t4=canvas.create_line(60,new_y1,int(w)/2-20,new_y1,fill=wh)

                                        canvas.create_text(140,y_val[value]+63,fill=wh,font="HELVETICA 10 bold",text='Patient Name: '+'\n\t'+self.appointment[i][1]+' '+self.appointment[i][2])

                                   elif self.appointment[i][-3] == 2:
                                        if value < 3:
                                            t1=canvas.create_text(int(w)/2,new_y,fill=wh,text=self.appointment[i][5]+' AM')
                                            t2=canvas.create_text(int(w)/2,new_y1,fill=wh,text=self.appointment[i][6]+' AM')
                                        else:
                                            t1=canvas.create_text(int(w)/2,new_y,fill=wh,text=self.appointment[i][5]+' PM')
                                            t2=canvas.create_text(int(w)/2,new_y1,fill=wh,text=self.appointment[i][6]+' PM')
                                            
                                        
                                        canvas.delete(int(g1[0])-1)
                                        canvas.delete(int(g1[0])-1)
                                        t.pop(int(g1[0]-1))
                                        l.pop(int(g1[0]-1))
                                        l.pop(int(g1[0]))

                                        t3=canvas.create_line(int(w)/2+20,new_y,int(w)-40,new_y,fill=wh)
                                        t4=canvas.create_line(int(w)/2+20,new_y1,int(w)-40,new_y1,fill=wh)

                                        canvas.create_text(int(w)/2+150,y_val[value]+63,fill=wh,font="HELVETICA 10 bold",text='Patient Name: '+'\n\t'+self.appointment[i][1]+' '+self.appointment[i][2])
                                t[int(g[0])] = t1
                                t[int(g1[0])] = t2

                                l[int(g[0])] = t3
                                l[int(g1[0])] = t4
                                up.append(value)
                                up.append(value1)

        canvas.configure(scrollregion=canvas.bbox('all'))
        master.mainloop()
    
    def setup(self, y, m):
        left = Button(self.parent, text='<', command=self.go_prev,bg=bl1,font=("HELVETICA",20,'bold'),fg=wh)
        self.wid.append(left)
        left.grid(row=0, column=0)
        
        header = Label(self.parent,font=("HELVETICA",24,'bold'),fg=wh,bg=bl, text='{} {}'.format(calendar.month_abbr[m], str(y)))
        self.wid.append(header)
        header.grid(row=0, column=1, columnspan=5)
        
        right = Button(self.parent, text='>', command=self.go_next,bg=bl1,font=("HELVETICA",20,'bold'),fg=wh)
        self.wid.append(right)
        right.grid(row=0, column=6)
        
        days = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
        for num, name in enumerate(days):
            t = Label(self.parent, text=name[:3],bg=bl,font=("HELVETICA",15,'bold'),fg=wh)
            self.wid.append(t)
            t.grid(row=1, column=num,pady=(20,5))
            
        di = {}
        
        for w, week in enumerate(self.cal.monthdatescalendar(y, m), 2):
            for d, day in enumerate(week):
                btn = Button(self.parent, text=day.strftime('%d'), bg=bl1,width=16,height=4,fg=wh,
                   font=("ARIAL",10,'bold'),command=lambda day=day: self.selection(day.strftime('%d'),m,y))
                btn.grid(row=w, column=d, sticky='nsew')
                if day.month != m:
                    btn['bg'] = '#aaa'
                    btn['state'] = 'disabled'
                li = []
                for i in self.appointment:
                    if i[4] == day.strftime('%Y-%m-%d'):
                        if day.strftime('%Y-%m-%d') not in di:
                            di[day.strftime('%Y-%m-%d')] = i[1]
                        else:
                            get = di[day.strftime('%Y-%m-%d')]
                            if get not in li:
                                li.append(get)
                                li.append(i[1])
                            else:
                                li.append(i[1])
                            l2 = [x for x in li if type(x) == str]
                            di[day.strftime('%Y-%m-%d')] = l2
                        btn['bg'] = '#0d82b5'
                        if len(di[day.strftime('%Y-%m-%d')][0]) == 1:
                            btn['text'] = day.strftime('%d')+'\n'+di[day.strftime('%Y-%m-%d')]
                        else:
                            btn['text'] = day.strftime('%d')+'\n'+di[day.strftime('%Y-%m-%d')][0]+'\n+'+str(len(di[day.strftime('%Y-%m-%d')])-1)+' more'

                    self.wid.append(btn)
                    if day.month != m:
                        btn['bg'] = '#aaa'
                        btn['state'] = 'disabled'

def Database():
    global conn, cursor
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `user` (user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, admin_name TEXT, username TEXT, password TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS `appointment` (app_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, firstname TEXT, surname TEXT, phone INTEGER, date DATE, start_time TEXT, end_time TEXT, bed INTEGER, sessions INTEGER, notes TEXT)")

def Login(event=None):
    Database()
    if username.get() == "" or password.get() == "":
        lbl_text.config(text="Please fill all the fields!", fg="red")
    else:
        cursor.execute("SELECT * FROM `user` WHERE `username` = ? AND `password` = ?", (username.get(), password.get()))
        if cursor.fetchone() is not None:
            HomeWindow()
            username.set("")
            password.set("")
            lbl_text.config(text="")
        else:
            lbl_text.config(text="Invalid username or password", fg="red")
            username.set("")
            password.set("")   
    cursor.close()
    conn.close()

    
def Register():

    def register_a():
        Database()
        if name.get() == "" or username1.get() == "" or password1.get() == "":
            lbl_text2.config(text="Please fill all the fields!", fg="red")
        else:
            cursor.execute("SELECT * FROM `user` WHERE `username` = ?", (username1.get(),))
            if cursor.fetchone() is not None:
                lbl_text2.config(text='Username Already Exists. Please Try a New Username',fg='red')
                username.set("")
            else:
                cursor.execute("INSERT INTO `user` (admin_name, username, password) VALUES(?, ?, ?)",(name.get(),username1.get(),password1.get()))
                conn.commit()
            cursor.execute("SELECT * FROM `user` WHERE `username` = ? AND `password` = ?", (username1.get(), password1.get()))
        cursor.close()
        conn.close()
        messagebox.showinfo('Successful!','You are successfully registered!')
        reg.destroy()
    
    def Back2():
        reg.destroy()
        root.deiconify()

    root.withdraw()
    reg = Toplevel()
    reg.title('Register')
    reg.config(bg=bl)
    reg.resizable(0,0)

    head = Label(reg,text='ADMIN REGISTRATION',bg=bl, fg=wh, font=('HELVETICA',24,'bold'))
    head.grid(row=0,column=0,padx=10,pady=10,columnspan=2)

    n_lbl = Label(reg,text='Admin Name',bg=bl,fg=wh,font=("HELVETICA",14,'bold'))
    n_lbl.grid(row=1,column=0,padx=10,pady=10)

    name = Entry(reg,width=20,font=("ARIAL",12))
    name.grid(row=1,column=1,pady=10,padx=(0,20))

    u_lbl = Label(reg,text='Username',bg=bl,fg=wh,font=("ARIAL",14,'bold'))
    u_lbl.grid(row=2,column=0,padx=10,pady=10)

    username1 = Entry(reg,width=20,font=("ARIAL",12))
    username1.grid(row=2,column=1,pady=10,padx=(0,20))

    pa_lbl = Label(reg,text='Password',bg=bl,fg=wh,font=("ARIAL",14,'bold'))
    pa_lbl.grid(row=3,column=0,padx=10,pady=10)

    password1 = Entry(reg,width=20,show='*',font=("ARIAL",12))
    password1.grid(row=3,column=1,pady=10,padx=(0,20))

    regist = Button(reg,text='Register',font=('HELVETICA',16,'bold'),width=12,fg=wh,bg=bl1,bd=4,relief=RAISED,command=register_a)
    regist.grid(row=4,column=0,columnspan=2,padx=10,pady=10)

    lbl_text2 = Label(reg,bg=bl,font=('arial',12,'bold'))
    lbl_text2.grid(row=7,column=0,columnspan=2,padx=10,pady=(5,20))

    lbl_text3 = Label(reg,bg=bl,font=('arial',12,'bold'),text='OR')
    lbl_text3.grid(row=5,column=0,columnspan=2,padx=10,pady=5)

    btn_reg = Button(reg, text="Login", font=('arial',14,'bold'), command=Back2,bg=bl1,fg=wh,width=12,bd=4,relief=RAISED)
    btn_reg.grid(pady=10, row=6,column=0, columnspan=2,padx=10)
 
def Back():
    Home.destroy()
    username.set("")
    password.set("")
    root.deiconify()

def HomeWindow():
   
    def add_app():
        def conf():
            try:
                start_time = datetime.strptime(start.get(), '%I:%M').time()
            except:
                start_time = datetime.strptime(start.get(), '%I').time()
            try:
                stop_time = datetime.strptime(end.get(), '%I:%M').time()
            except:
                stop_time = datetime.strptime(end.get(), '%I').time()
                
            datetime1 = datetime.combine(date.today(), start_time)
            datetime2 = datetime.combine(date.today(), stop_time)
            time_elapsed = datetime2 - datetime1

            seconds = time_elapsed.total_seconds()
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            if int(hours) < 0:
                hours+=12
            start1 = start_time
            end1 = stop_time

            Database()
            cursor.execute("SELECT start_time,end_time,bed from `appointment` WHERE date = ?",(cal.get_date(),))
            tim = cursor.fetchall()

            if int(hours) >= 2 and int(minutes) > 0:
                messagebox.showerror('Timing Error!','The maximum time of appointment can be 2 hours only!')               

            else:
                if len(tim) == 0:
                    Database()
                    cursor.execute("INSERT INTO `appointment` (firstname, surname, phone, date, start_time, end_time, bed, sessions, notes) VALUES(?,?,?,?,?,?,?,?,?)",(f_name.get(),s_name.get(),phone.get(),cal.get_date(),start.get(),end.get(),beds.get(),sessions.get(),notes.get("1.0",'end-1c')))
                    conn.commit()
                    messagebox.showinfo('Successful!','Appointment is added successfully!')
                    f_name.delete(0,END)
                    s_name.delete(0,END)
                    phone.delete(0,END)
                    start.delete(0,END)
                    end.delete(0,END)
                    sessions.set(0)
                    notes.delete('0.0',END)
                    root2.destroy()
                else:
                    ti = {}
                    li = []
                    for i in tim:
                        try:
                            first = datetime.strptime(str(i[0]), '%I:%M').time()
                        except:
                            first = datetime.strptime(str(i[0]), '%I').time()
                        try:
                            second = datetime.strptime(str(i[1]), '%I:%M').time()
                        except:
                            second = datetime.strptime(str(i[1]), '%I').time()


                        if (time_in_range(first, second, end1) == True or time_in_range(first, second, start1) == True):
                            if False not in ti:
                                ti[False] = i[2]
                            else:
                                get = ti[False]
                                if get not in li:
                                    li.append(get)
                                    li.append(i[2])
                                else:
                                    li.append(i[2])
                                ti[False] = li
                        else:
                            ti[True] = i[2]
                    if False in ti:
                        find = ti[False]
                        try:
                            if 1 in find and 2 in find:
                                messagebox.showerror('Sorry','There are already 2 appointments at this time.')

                            elif beds.get() in find:
                                messagebox.showerror('Not available','This bed is not available. Try selecting the other')
                            else:
                                Database()
                                cursor.execute("INSERT INTO `appointment` (firstname, surname, phone, date, start_time, end_time, bed, sessions, notes) VALUES(?,?,?,?,?,?,?,?,?)",(f_name.get(),s_name.get(),phone.get(),cal.get_date(),start.get(),end.get(),beds.get(),sessions.get(),notes.get("1.0",'end-1c')))
                                conn.commit()
                                messagebox.showinfo('Successful!','Appointment is added successfully!')
                                f_name.delete(0,END)
                                s_name.delete(0,END)
                                phone.delete(0,END)
                                start.delete(0,END)
                                end.delete(0,END)
                                sessions.set(0)
                                notes.delete('0.0',END)
                                root2.destroy()
                        except:
                            if beds.get() == find:
                                messagebox.showerror('Not available','This bed is not available. Try selecting the other')
                            else:
                                Database()
                                cursor.execute("INSERT INTO `appointment` (firstname, surname, phone, date, start_time, end_time, bed, sessions, notes) VALUES(?,?,?,?,?,?,?,?,?)",(f_name.get(),s_name.get(),phone.get(),cal.get_date(),start.get(),end.get(),beds.get(),sessions.get(),notes.get("1.0",'end-1c')))
                                conn.commit()
                                messagebox.showinfo('Successful!','Appointment is added successfully!')
                                f_name.delete(0,END)
                                s_name.delete(0,END)
                                phone.delete(0,END)
                                start.delete(0,END)
                                end.delete(0,END)
                                sessions.set(0)
                                notes.delete('0.0',END)
                                root2.destroy()
                    elif True in ti:
                        Database()
                        cursor.execute("INSERT INTO `appointment` (firstname, surname, phone, date, start_time, end_time, bed, sessions, notes) VALUES(?,?,?,?,?,?,?,?,?)",(f_name.get(),s_name.get(),phone.get(),cal.get_date(),start.get(),end.get(),beds.get(),sessions.get(),notes.get("1.0",'end-1c')))
                        conn.commit()
                        messagebox.showinfo('Successful!','Appointment is added successfully!')
                        f_name.delete(0,END)
                        s_name.delete(0,END)
                        phone.delete(0,END)
                        start.delete(0,END)
                        end.delete(0,END)
                        sessions.set(0)
                        notes.delete('0.0',END)
                        root2.destroy()
                Home.destroy()
                HomeWindow()
               
        root2 = Toplevel()
        root2.config(bg=bl)
        root2.resizable(0,0)

        beds = IntVar()
        sessions = IntVar()
        sessions.set(0)
        
        head = Label(root2,text="ADD APPOINTMENT",font=("HELVETICA",23,'bold'),bg=bl,fg=wh)
        head.grid(row=0,column=0,padx=10,pady=10,columnspan=2)

        f_lbl = Label(root2,text='First Name',bg=bl,fg=wh,font=("HELVETICA",14,'bold'))
        f_lbl.grid(row=1,column=0,padx=10,pady=10)

        f_name = Entry(root2,width=20,font=("HELVETICA",12))
        f_name.grid(row=1,column=1,pady=10,padx=(0,20))

        s_lbl = Label(root2,text='Surname',bg=bl,fg=wh,font=("HELVETICA",14,'bold'))
        s_lbl.grid(row=2,column=0,padx=10,pady=10)

        s_name = Entry(root2,width=20,font=("HELVETICA",12))
        s_name.grid(row=2,column=1,pady=10,padx=(0,20))

        p_lbl = Label(root2,text='Phone Number',bg=bl,fg=wh,font=("HELVETICA",14,'bold'))
        p_lbl.grid(row=3,column=0,padx=10,pady=10)

        phone = Entry(root2,width=20,font=("HELVETICA",12))
        phone.grid(row=3,column=1,pady=10,padx=(0,20))

        d_lbl = Label(root2,text='Select Date',bg=bl,fg=wh,font=("HELVETICA",14,'bold'))
        d_lbl.grid(row=4,column=0,padx=10,pady=10)

        cal = DateEntry(root2, width=20,background=bl1,date_pattern='dd/mm/yyyy')
        cal.grid(row=4,column=1,pady=10,padx=(0,20))
        
        s_lbl = Label(root2,text='Start Time',bg=bl,fg=wh,font=("HELVETICA",14,'bold'))
        s_lbl.grid(row=5,column=0,padx=10,pady=10)

        start = Entry(root2,width=20,font=("HELVETICA",12))
        start.grid(row=5,column=1,pady=10,padx=(0,20))

        e_lbl = Label(root2,text='End Time',bg=bl,fg=wh,font=("HELVETICA",14,'bold'))
        e_lbl.grid(row=6,column=0,padx=10,pady=10)

        end = Entry(root2,width=20,font=("HELVETICA",12))
        end.grid(row=6,column=1,pady=10,padx=(0,20))

        b_lbl = Label(root2,text='Bed',bg=bl,fg=wh,font=("HELVETICA",14,'bold'))
        b_lbl.grid(row=7,column=0,padx=10,pady=10)

        bed1 = Radiobutton(root2,font=("HELVETICA",12),variable=beds,text='1',value=1,bg=bl,fg=wh,selectcolor=bl,activebackground=bl,activeforeground=wh, tristatevalue=0)
        bed1.grid(row=7,column=1,pady=10,padx=(0,120))
        
        bed2 = Radiobutton(root2,font=("HELVETICA",12),variable=beds,text='2',value=2,bg=bl,fg=wh,selectcolor=bl,activebackground=bl,activeforeground=wh, tristatevalue=0)
        bed2.grid(row=7,column=1,pady=10,padx=(100,20))
        bed1.select()
        
        session = Label(root2,text='Select Session',bg=bl,fg=wh,font=("HELVETICA",14,'bold'))
        session.grid(row=8,column=0,pady=10)

        om = OptionMenu(root2, sessions, 1,5,10)
        om.grid(row=8,column=1,pady=10,padx=(0,20))

        note = Label(root2,text='Add Notes',bg=bl,fg=wh,font=("HELVETICA",14,'bold'))
        note.grid(row=9,column=0,pady=10)

        notes = scrolledtext.ScrolledText(root2,wrap = WORD,width = 20, height = 4, font = ("ARIAL",13))
        notes.grid(row=9,column=1,pady=10,padx=(0,20))

        confirm = Button(root2,text='Confirm',font=("HELVETICA",14,'bold'),width=13,bg=bl1,fg=wh,command=conf)
        confirm.grid(row=10,columnspan=2,pady=10,padx=10)
        
    def edit_app():
        edit = Toplevel()
        edit.title('Edit Appointment')
        edit.config(bg=bl)
        edit.resizable(0,0)
        h = edit.winfo_screenheight() 
        w = edit.winfo_screenwidth()
        edit.geometry("{}x{}".format(w-100, h-150))

        def selectItem(a):
            ask = messagebox.askquestion ('Confirmation','Are You sure you want to Edit this appointment?')
            if ask == 'yes':
                curItem = tree.focus()
                data = tree.item(curItem)['values']
                item = tree.item(curItem)
                new = Toplevel()
                new.resizable(0,0)
                new.title('Edit Appointment')
                new.config(bg=bl)

                def conf():
                    try:
                        start_time = datetime.strptime(start.get(), '%I:%M').time()
                    except:
                        start_time = datetime.strptime(start.get(), '%I').time()
                    try:
                        stop_time = datetime.strptime(end.get(), '%I:%M').time()
                    except:

                        stop_time = datetime.strptime(end.get(), '%I').time()
                        
                    datetime1 = datetime.combine(date.today(), start_time)
                    datetime2 = datetime.combine(date.today(), stop_time)
                    time_elapsed = datetime2 - datetime1

                    seconds = time_elapsed.total_seconds()
                    hours = seconds // 3600
                    minutes = (seconds % 3600) // 60
                    if int(hours) < 0:
                        hours+=12
                    start1 = start_time
                    end1 = stop_time

                    Database()
                    cursor.execute("SELECT app_id,start_time,end_time from `appointment` WHERE date = ?",(cal.get_date(),))
                    tim = cursor.fetchall()

                    if int(hours) >= 2 and int(minutes) > 0:
                        messagebox.showerror('Timing Error!','The maximum time of appointment can be 2 hours only!')               

                    else:
                        for i in tim:
                            if int(idd.get()) == int(i[0]):
                                try:
                                    first = datetime.strptime(i[1], '%I:%M').time()
                                except:
                                    first = datetime.strptime(i[1], '%I').time()
                                try:
                                    second = datetime.strptime(i[2], '%I:%M').time()
                                except:
                                    second = datetime.strptime(i[2], '%I').time()

                                if first == start1 and second == end1:
                                    Database()
                                    cursor.execute("UPDATE `appointment` SET firstname = ?, surname = ?, phone = ?, date = ?, start_time = ?, end_time = ?, sessions = ?, notes = ? WHERE app_id = ?",(f_name.get(),s_name.get(),phone.get(),cal.get_date(),start.get(),end.get(),sessions.get(),notes.get("1.0",'end-1c'),idd.get()))
                                    conn.commit()
                                    messagebox.showinfo('Successful!','Appointment is Edited successfully!')
                                    res = []
                                    res.append(int(idd.get()))
                                    res.append(f_name.get())
                                    res.append(s_name.get())
                                    res.append(int(phone.get()))
                                    res.append(cal.get_date().strftime('%Y-%m-%d'))
                                    res.append(int(start.get()))
                                    res.append(int(end.get()))
                                    res.append(int(sessions.get()))
                                    res.append(notes.get("1.0",'end-1c'))
                                    item['values']=res
                                    tree.insert('', str(curItem)[1:], values=(res), tags='T')
                                    tree.delete(curItem)
                                    new.withdraw()
                                    
                                elif time_in_range(first, second, end1) == True or time_in_range(first, second, start1) == True:
                                    messagebox.showerror('Timing Error!','There is already an appointment at this time.')

                                else:
                                    Database()
                                    cursor.execute("UPDATE `appointment` SET firstname = ?, surname = ?, phone = ?, date = ?, start_time = ?, end_time = ?, sessions = ?, notes = ? WHERE app_id = ?",(f_name.get(),s_name.get(),phone.get(),cal.get_date(),start.get(),end.get(),sessions.get(),notes.get("1.0",'end-1c'),idd.get()))
                                    conn.commit()
                                    messagebox.showinfo('Successful!','Appointment is Edited successfully!')
                                    res = []
                                    res.append(int(idd.get()))
                                    res.append(f_name.get())
                                    res.append(s_name.get())
                                    res.append(int(phone.get()))
                                    res.append(cal.get_date().strftime('%Y-%m-%d'))
                                    res.append(int(start.get()))
                                    res.append(int(end.get()))
                                    res.append(int(sessions.get()))
                                    res.append(notes.get("1.0",'end-1c'))
                                    item['values']=res
                                    tree.insert('', str(curItem)[1:], values=(res), tags='T')
                                    tree.delete(curItem)
                                    new.withdraw()
                         

                sessions = IntVar()

                h = Label(new,text="EDIT APPOINTMENT",font=("HELVETICA",20,'bold'),bg=bl,fg=wh)
                h.grid(row=0,column=0,columnspan=2,padx=10,pady=10)

                i_lbl = Label(new,text='Appointment ID',bg=bl,fg=wh,font=("HELVETICA",14,'bold'))
                i_lbl.grid(row=1,column=0,padx=10,pady=10)

                idd = Entry(new,width=20,font=("HELVETICA",12))
                idd.grid(row=1,column=1,pady=10,padx=(0,20))

                f_lbl = Label(new,text='First Name',bg=bl,fg=wh,font=("HELVETICA",14,'bold'))
                f_lbl.grid(row=2,column=0,padx=10,pady=10)

                f_name = Entry(new,width=20,font=("HELVETICA",12))
                f_name.grid(row=2,column=1,pady=10,padx=(0,20))

                s_lbl = Label(new,text='Surname',bg=bl,fg=wh,font=("HELVETICA",14,'bold'))
                s_lbl.grid(row=3,column=0,padx=10,pady=10)

                s_name = Entry(new,width=20,font=("HELVETICA",12))
                s_name.grid(row=3,column=1,pady=10,padx=(0,20))

                p_lbl = Label(new,text='Phone Number',bg=bl,fg=wh,font=("HELVETICA",14,'bold'))
                p_lbl.grid(row=4,column=0,padx=10,pady=10)

                phone = Entry(new,width=20,font=("HELVETICA",12))
                phone.grid(row=4,column=1,pady=10,padx=(0,20))

                d_lbl = Label(new,text='Select Date',bg=bl,fg=wh,font=("HELVETICA",14,'bold'))
                d_lbl.grid(row=5,column=0,padx=10,pady=10)

                cal = DateEntry(new, width=20,background=bl1,date_pattern='dd/mm/yyyy')
                cal.grid(row=5,column=1,pady=10,padx=(0,20))
                
                s_lbl = Label(new,text='Start Time',bg=bl,fg=wh,font=("HELVETICA",14,'bold'))
                s_lbl.grid(row=6,column=0,padx=10,pady=10)

                start = Entry(new,width=20,font=("HELVETICA",12))
                start.grid(row=6,column=1,pady=10,padx=(0,20))

                e_lbl = Label(new,text='End Time',bg=bl,fg=wh,font=("HELVETICA",14,'bold'))
                e_lbl.grid(row=7,column=0,padx=10,pady=10)

                end = Entry(new,width=20,font=("HELVETICA",12))
                end.grid(row=7,column=1,pady=10,padx=(0,20))

                session = Label(new,text='Select Session',bg=bl,fg=wh,font=("HELVETICA",14,'bold'))
                session.grid(row=8,column=0,pady=10)

                om = OptionMenu(new, sessions, 1,5,10)
                om.grid(row=8,column=1,pady=10,padx=(0,20))

                note = Label(new,text='Add Notes',bg=bl,fg=wh,font=("HELVETICA",14,'bold'))
                note.grid(row=9,column=0,pady=10)

                notes = scrolledtext.ScrolledText(new,wrap = WORD,width = 20, height = 4, font = ("ARIAL",13))
                notes.grid(row=9,column=1,pady=10,padx=(0,20))

                idd.insert(END,data[0])
                idd.config(state='disabled')
                f_name.insert(END,data[1])
                s_name.insert(END,data[2])
                phone.insert(END,data[3])
                cal.delete(0,END)
                cal.insert(END,data[4])
                start.insert(END,data[5])
                end.insert(END,data[6])
                sessions.set(data[7])
                notes.insert(END,data[8])

                confirm = Button(new,text='Confirm',font=("HELVETICA",14,'bold'),width=13,bg=bl1,fg=wh,command=conf)
                confirm.grid(row=10,columnspan=2,pady=10,padx=10)
        
        head = Label(edit,text="EDIT APPOINTMENT",font=("HELVETICA",23,'bold'),bg=bl,fg=wh)
        head.pack(pady=30,padx=10)

        Database()
        cursor.execute("SELECT * FROM `appointment`")
        names = [description[0] for description in cursor.description]
        apps = cursor.fetchall()

        style = ttk.Style(edit)
        style.theme_use("clam")
        style.configure('Treeview', rowheight=40)

        tree= ttk.Treeview(edit,show='headings', selectmode="browse")
        tree["columns"] = names
        tree["displaycolumns"] = names
        for head in names:
            tree.heading(head, text=head, anchor=CENTER)
            tree.column(head, anchor=CENTER, stretch=True)

        for row in apps:
            tree.insert('', END, values=tuple(row), tags='T')

        scrolltable1 = Scrollbar(edit, command=tree.yview, orient='vertical')
        scrolltable2 = Scrollbar(edit, command=tree.xview, orient='horizontal')
        tree.configure(yscrollcommand=scrolltable1.set,xscrollcommand=scrolltable2.set)
        scrolltable1.pack(side=RIGHT, fill=Y)
        scrolltable2.pack(side=BOTTOM,fill=X)
        tree.tag_configure('T', font='Arial 13')
        tree.pack(fill=BOTH,expand=YES)
        tree.bind('<ButtonRelease-1>', selectItem)
        
    
    def del_app():
        
        dele = Toplevel()
        dele.title('Delete Appointment')
        dele.config(bg=bl)
        dele.resizable(0,0)
        h = dele.winfo_screenheight() 
        w = dele.winfo_screenwidth()
        dele.geometry("{}x{}".format(w-100, h-150))

        def selectItem(a):
            ask = messagebox.askquestion ('Confirmation','Are You sure you want to delete this appointment?')
            if ask == 'yes':
                curItem = tree.focus()
                data =tree.item(curItem)['values'] 
                cursor.execute("DELETE FROM `appointment` WHERE app_id = ?",(data[0],))
                conn.commit()
                messagebox.showinfo("Deletion Successful",("The Appointment number "+str(data[0])+' has been deleted'))
            cursor.close()
            conn.close()
            curItem = tree.focus()
            tree.delete(curItem)
        
        head = Label(dele,text="DELETE APPOINTMENT",font=("HELVETICA",23,'bold'),bg=bl,fg=wh)
        head.pack(pady=30,padx=10)

        Database()
        cursor.execute("SELECT * FROM `appointment`")
        names = [description[0] for description in cursor.description]
        apps = cursor.fetchall()

        style = ttk.Style(dele)
        style.theme_use("clam")
        style.configure('Treeview', rowheight=40)

        tree= ttk.Treeview(dele,show='headings', selectmode="browse")
        tree["columns"] = names
        tree["displaycolumns"] = names
        for head in names:
            tree.heading(head, text=head, anchor=CENTER)
            tree.column(head, anchor=CENTER, stretch=True)

        for row in apps:
            tree.insert('', END, values=tuple(row), tags='T')

        scrolltable1 = Scrollbar(dele, command=tree.yview, orient='vertical')
        scrolltable2 = Scrollbar(dele, command=tree.xview, orient='horizontal')
        tree.configure(yscrollcommand=scrolltable1.set,xscrollcommand=scrolltable2.set)
        scrolltable1.pack(side=RIGHT, fill=Y)
        scrolltable2.pack(side=BOTTOM,fill=X)
        tree.tag_configure('T', font='Arial 13')
        tree.pack(fill=BOTH,expand=YES)
        tree.bind('<ButtonRelease-1>', selectItem)
        

    global Home
    root.withdraw()
    Home = Toplevel()
    Home.title("Appointment Booking System")
    Home.config(bg=bl)
    Home.state('zoomed')
    Home.resizable(0,0)
    head = Label(Home, text="TB APPOINTMENT", font=('HELVETICA', 24,'bold'),bg=bl,fg=wh)
    head.grid(row=0,column=0,padx=10,columnspan=7)

    Database()
    cursor.execute("SELECT `admin_name` FROM `user` WHERE `username` = ?", (username.get(),))
    name = cursor.fetchone()
    
    lbl_home = Label(Home, text="WELCOME "+name[0].upper(), font=('HELVETICA', 20,'bold'),bg=bl,fg=wh)
    lbl_home.grid(row=1,column=0,padx=10,columnspan=7)

    year = int(now.strftime('%Y'))

    cursor.execute("SELECT * FROM `appointment`")
    appointment = cursor.fetchall()

    global calendarViewFrame
    calendarViewFrame = Frame(Home, borderwidth=5, bg=bl)
    calendarViewFrame.grid(row=2, column=0, columnspan=7,rowspan=6)
    viewCalendar = CalendarView(calendarViewFrame,appointment)


    add = Button(Home, text='ADD APPOINTMENT', command=add_app,bg=bl1,fg=wh,width=20,height=2,font=("HELVETICA",15,'bold'))
    add.grid(row=4,column=8,pady=5,padx=(40,10))

    edit = Button(Home, text='EDIT APPOINTMENT', command=edit_app,bg=bl1,fg=wh,width=20,height=2,font=("HELVETICA",15,'bold'))
    edit.grid(row=5,column=8,pady=5,padx=(40,10))

    delete = Button(Home, text='DELETE APPOINTMENT', command=del_app,bg=bl1,fg=wh,width=20,height=2,font=("HELVETICA",15,'bold'))
    delete.grid(row=6,column=8,pady=5,padx=(40,10))  
    
    logout = Button(Home, text='LOGOUT', command=Back,bg=bl1,fg=wh,width=20,height=2,font=("HELVETICA",15,'bold'))
    logout.grid(row=7,column=8,pady=20,padx=(40,10))

    Home.mainloop()



root = Tk()
root.title("Login Page")
root.resizable(0, 0)
root.config(bg=bl)

username = StringVar()
password = StringVar()
 
lbl_title = Label(root, text = "LOG IN", font=('HELVETICA', 25,'bold'),bg=bl,fg=wh)
lbl_title.grid(row=0,column=0,padx=10,pady=10,columnspan=2)

lbl_username = Label(root, text = "Username:", font=('arial', 14),bg=bl,fg=wh)
lbl_username.grid(row=1,column=0, sticky="e",padx=(70,10),pady=(30,10))

username1 = Entry(root, textvariable=username, font=(14))
username1.grid(row=1, column=1,padx=(10,70),pady=(30,10))

lbl_password = Label(root, text = "Password:", font=('arial', 14),bg=bl,fg=wh)
lbl_password.grid(row=2,column=0, sticky="e",padx=(70,10),pady=10)

password1 = Entry(root, textvariable=password, show="*", font=(14))
password1.grid(row=2, column=1,padx=(10,70),pady=10)

btn_login = Button(root, text="Login", font=('arial',14,'bold'), command=Login,bg=bl1,fg=wh,width=12,bd=4,relief=RAISED)
btn_login.grid(pady=(30,10), row=3,column=0, columnspan=2,padx=10)
btn_login.bind('<Return>', Login)

lbl_text1 = Label(root,bg=bl,font=('arial',12,'bold'),text='OR')
lbl_text1.grid(row=4,column=0,columnspan=2,padx=10,pady=5)

btn_reg = Button(root, text="Register", font=('arial',14,'bold'), command=Register,bg=bl1,fg=wh,width=12,bd=4,relief=RAISED)
btn_reg.grid(pady=10, row=5,column=0, columnspan=2,padx=10)

lbl_text = Label(root,bg=bl,font=('arial',12,'bold'))
lbl_text.grid(row=6,column=0,columnspan=2,padx=10,pady=(5,20))

if __name__ == '__main__':
    root.mainloop()
