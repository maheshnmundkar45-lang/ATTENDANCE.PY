import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
from datetime import datetime

class AttendanceRegister:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Entry Register")


        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.width}x{self.height}+0+0")

    
        titleLbl = tk.Label(self.root, text="Attendance Entry Register",
                            bg="dark red", fg="white", bd=4, relief="groove",
                            font=("Arial", 45, "bold"))
        titleLbl.pack(side="top", fill="x")


        inFrame = tk.Frame(self.root, bg="light yellow", bd=4, relief="ridge")
        inFrame.place(width=self.width / 3, height=self.height - 180, x=100, y=100)

    
        tk.Label(inFrame, text="Date (YYYY-MM-DD):", bg="light yellow", font=("Arial", 15)).grid(row=0, column=0, padx=20, pady=30)
        self.dateIn = tk.Entry(inFrame, bd=2, width=20, font=("Arial", 15, "bold"))
        self.dateIn.grid(row=0, column=1, padx=20, pady=30)
        self.dateIn.insert(0, datetime.now().strftime("%Y-%m-%d"))

    
        tk.Label(inFrame, text="Time (HH:MM):", bg="light yellow", font=("Arial", 15)).grid(row=1, column=0, padx=20, pady=30)
        self.timeIn = tk.Entry(inFrame, bd=2, width=20, font=("Arial", 15, "bold"))
        self.timeIn.grid(row=1, column=1, padx=20, pady=30)
        self.timeIn.insert(0, datetime.now().strftime("%H:%M"))

    
        tk.Label(inFrame, text="Subject:", bg="light yellow", font=("Arial", 15)).grid(row=2, column=0, padx=20, pady=30)
        self.subIn = tk.Entry(inFrame, bd=2, width=20, font=("Arial", 15, "bold"))
        self.subIn.grid(row=2, column=1, padx=20, pady=30)

        
        tk.Label(inFrame, text="Subject Teacher:", bg="light yellow", font=("Arial", 15)).grid(row=3, column=0, padx=20, pady=30)
        self.teachIn = tk.Entry(inFrame, bd=2, width=20, font=("Arial", 15, "bold"))
        self.teachIn.grid(row=3, column=1, padx=20, pady=30)


        tk.Label(inFrame, text="Absent Roll No(s):", bg="light yellow", font=("Arial", 15)).grid(row=4, column=0, padx=20, pady=30)
        self.absentIn = tk.Entry(inFrame, bd=2, width=20, font=("Arial", 15, "bold"))
        self.absentIn.grid(row=4, column=1, padx=20, pady=30)

    
        saveBtn = tk.Button(inFrame, text="SAVE ENTRY", command=self.saveAttendance,
                            font=("Arial", 20, "bold"), bg="green", fg="white",
                            width=20, bd=3, relief="raised", activebackground="dark green")
        saveBtn.grid(row=5, column=0, padx=40, pady=30, columnspan=2)

    
        self.outFrame = tk.Frame(self.root, bg="light cyan", bd=4, relief="ridge")
        self.outFrame.place(width=self.width / 2, height=self.height - 180,
                            x=self.width / 3 + 150, y=100)

        self.tabFun()
        self.loadData()

    def tabFun(self):
        
        tabFrame = tk.Frame(self.outFrame, bg="sky blue", bd=3, relief="sunken")
        tabFrame.place(x=40, y=40, width=self.width / 2 - 80, height=self.height - 260)

        x_scrol = tk.Scrollbar(tabFrame, orient="horizontal")
        x_scrol.pack(side="bottom", fill="x")

        y_scrol = tk.Scrollbar(tabFrame, orient="vertical")
        y_scrol.pack(side="right", fill="y")

        self.table = ttk.Treeview(tabFrame,
                                  columns=("date", "time", "subject", "teacher", "absent"),
                                  xscrollcommand=x_scrol.set,
                                  yscrollcommand=y_scrol.set)

        x_scrol.config(command=self.table.xview)
        y_scrol.config(command=self.table.yview)

        self.table.heading("date", text="Date")
        self.table.heading("time", text="Time")
        self.table.heading("subject", text="Subject")
        self.table.heading("teacher", text="Subject Teacher")
        self.table.heading("absent", text="Absent Roll No(s)")
        self.table["show"] = "headings"

        self.table.column("date", width=100)
        self.table.column("time", width=80)
        self.table.column("subject", width=150)
        self.table.column("teacher", width=150)
        self.table.column("absent", width=200)

        self.table.pack(fill="both", expand=1)

    def connect_db(self):
        
        return pymysql.connect(
            host="127.0.0.1",
            user="root",
            passwd="Password", 
            database="PY",
            port=3306
        )

    def loadData(self):
        
        try:
            con = self.connect_db()
            cur = con.cursor()
            cur.execute("SELECT * FROM attendance")
            data = cur.fetchall()
            self.table.delete(*self.table.get_children())
            for row in data:
                self.table.insert('', tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Unable to load data: {e}")
        finally:
            try:
                con.close()
            except:
                pass

    def saveAttendance(self):
        
        date = self.dateIn.get().strip()
        time = self.timeIn.get().strip()
        subject = self.subIn.get().strip()
        teacher = self.teachIn.get().strip()
        absent = self.absentIn.get().strip()

        if not (date and time and subject and teacher and absent):
            messagebox.showerror("Error", "Please fill all input fields")
            return

        try:
            con = self.connect_db()
            cur = con.cursor()
            cur.execute("""
                INSERT INTO attendance(date, time, subject, teacher, absent)
                VALUES (%s, %s, %s, %s, %s)
            """, (date, time, subject, teacher, absent))
            con.commit()

            messagebox.showinfo("Success", "Attendance entry saved successfully!")
            self.loadData()

        except Exception as e:
            messagebox.showerror("Error", f"Database Error: {e}")
        finally:
            try:
                con.close()
            except:
                pass



root = tk.Tk()
obj = AttendanceRegister(root)
root.mainloop()
                                                                    


                                                                    