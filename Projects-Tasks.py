from tkinter import *
import sqlite3
import tkinter.scrolledtext as tkst


t_name_editor = NONE
t_start_date_editor = NONE
t_type_editor = NONE
editor = NONE
var = NONE


conn = sqlite3.connect('db1.py')
c = conn.cursor()

c.execute("""CREATE TABLE projects (

        name text,
        start_date real,
       type text
         )""")


c.execute("""CREATE TABLE tasks (
           instruction text,
           due_date real,
           to_project integer
               )""")


class Page(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


class Page1(Page):

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        # create Text boxes
        self.t_name = Entry(self, width=30)
        self.t_name.grid(row=0, column=1, padx=20, pady=(35, 0))

        self.t_start_date = Entry(self, width=30)
        self.t_start_date.grid(row=1, column=1, padx=20)

        self.t_type = Entry(self, width=30)
        self.t_type.grid(row=2, column=1, padx=20)

        self.delete_box = Entry(self, width=30)
        self.delete_box.grid(row=9, column=1, pady=5)

        # create Lables for text boxes
        self.t_name_lable = Label(self, text="Name of the Project").grid(
            row=0, column=0, pady=(35, 0))

        self.t_start_date_lable = Label(
            self, text="Start date").grid(row=1, column=0)

        self.t_type_lable = Label(self, text="Type").grid(row=2, column=0)

        self.delete_box_lable = Label(self, text=" Choose Project ID").grid(
            row=9, column=0, pady=5)

        # create Buttons
        self.add_btn = Button(self, text="Add Project",
                              command=self.create_project)
        self.add_btn.grid(row=6, column=0, columnspan=2,
                          pady=10, padx=10, ipadx=139)

        self.show_db_btn = Button(
            self, text="Show Project Database", command=self.query)
        self.show_db_btn.grid(row=13, column=0, columnspan=2,
                              pady=10, padx=10, ipadx=112)

        self.delete_btn = Button(self, text="Delete Project",
                                 command=self.remove_project)
        self.delete_btn.grid(row=10, column=0, columnspan=2,
                             pady=10, padx=10, ipadx=135)

        self.edit_btn = Button(self, text="Update Project",
                               command=self.update_project)
        self.edit_btn.grid(row=11, column=0, columnspan=2,
                           pady=10, padx=10, ipadx=133)

    def create_project(self):
        conn = sqlite3.connect('db1.py')
        c = conn.cursor()

        c.execute("INSERT INTO projects VALUES (:name, :start_date,:type)",
                  {

                      'name': self.t_name.get(),
                      'start_date': self.t_start_date.get(),
                      'type': self.t_type.get()

                  })

        conn.commit()
        conn.close()

        self.t_name.delete(0, END)
        self.t_start_date.delete(0, END)
        self.t_type.delete(0, END)

    def query(self):

        query = Tk()
        query.geometry("375x180")

        conn = sqlite3.connect('db1.py')
        c = conn.cursor()
        c.execute("SELECT *,oid  FROM projects")
        records = c.fetchall()

        print_records = ''
        for record in records:
            print_records += str(record) + "\n"

        query_lable = Label(query, text=print_records)
        query_lable.grid(row=0, column=0, padx=95, pady=10)

        conn.commit()
        conn.close()

    def remove_project(self):
        conn = sqlite3.connect('db1.py')
        c = conn.cursor()

        c.execute("DELETE from projects WHERE oid = " + self.delete_box.get())
        self.delete_box.delete(0, END)

        conn.commit()
        conn.close()

    def update_project(self):
        global t_name_editor
        global t_start_date_editor
        global t_type_editor
        global editor
        editor = Tk()
        editor.geometry("375x180")

        conn = sqlite3.connect('db1.py')

        c = conn.cursor()

        project_id = self.delete_box.get()
        c.execute("SELECT *  FROM projects WHERE oid = " + project_id)
        records = c.fetchall()

        # create Text boxes
        t_name_editor = Entry(editor, width=30)
        t_name_editor.grid(row=0, column=1, padx=20, pady=(10, 0))

        t_start_date_editor = Entry(editor, width=30)
        t_start_date_editor.grid(row=1, column=1, padx=20)

        t_type_editor = Entry(editor, width=30)
        t_type_editor.grid(row=2, column=1, padx=20)

        # create Lables for text boxes

        t_name_lable_editor = Label(editor, text="Name of the Project").grid(
            row=0, column=0, pady=(10, 0))

        t_start_date_lable_editor = Label(
            editor, text="Start date").grid(row=1, column=0)

        t_type_lable_editor = Label(editor, text="Type").grid(row=2, column=0)

        for record in records:
            t_name_editor.insert(0, record[0])
            t_start_date_editor.insert(0, record[1])
            t_type_editor.insert(0, record[2])

        save_btn = Button(editor, text="Save Record",
                          command=self.edit_project)
        save_btn.grid(row=4, column=0, columnspan=2,
                      pady=10, padx=10, ipadx=133)

    def edit_project(self):
        conn = sqlite3.connect('db1.py')
        c = conn.cursor()

        project_id = self.delete_box.get()

        c.execute("""UPDATE projects SET
                name = :name,
                start_date = :start_date,
                type = :type
                WHERE oid = :oid""",
                  {
                      'name': t_name_editor.get(),
                      'start_date': t_start_date_editor.get(),
                      'type': t_type_editor.get(),
                      'oid': project_id
                  })

        conn.commit()
        conn.close()
        editor.destroy()


class Page2(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        conn = sqlite3.connect('db1.py')
        c = conn.cursor()
        c.execute("SELECT name  FROM projects")
        list1 = c.fetchall()
        if not list1:
            list1.append("No Projects yet")

        global var

        # create Text boxes
        self.t_instruction = tkst.ScrolledText(self, height=5, width=22)
        self.t_instruction.grid(row=0, column=1, padx=0, pady=(15, 0))

        self.t_due_date = Entry(self, width=32)
        self.t_due_date.grid(row=1, column=1, padx=20)

        self.delete_box = Entry(self, width=32)
        self.delete_box.grid(row=4, column=1, pady=5)

        var = StringVar()
        var.set("Project Name")
        self.which_project = OptionMenu(self,  var, *list1)
        self.which_project.grid(row=2, column=1, padx=20,)

        # create Lables for text boxes
        self.t_instruction_lable = Label(self, text="Task Instructions").grid(
            row=0, column=0, padx=20, pady=(15, 0))

        self.t_due_date_lable = Label(
            self, text="Due date").grid(row=1, column=0, pady=10)

        self.t_which_project_lable = Label(
            self, text="Chose Project").grid(row=2, column=0, pady=10)

        self.delete_box_lable = Label(self, text=" Choose Task ID").grid(
            row=4, column=0, pady=5)

        # create Buttons

        self.add_btn = Button(self, text="Add Task",
                              command=self.add_task)
        self.add_btn.grid(row=3, column=0, columnspan=2,
                          pady=10, padx=10, ipadx=136)

        self.show_db_btn = Button(
            self, text="Show Task Database", command=self.query2)
        self.show_db_btn.grid(row=6, column=0, columnspan=2,
                              pady=10, padx=10, ipadx=112)

        self.delete_btn = Button(self, text="Delete Task",
                                 command=self.remove_task)
        self.delete_btn.grid(row=5, column=0, columnspan=2,
                             pady=10, padx=10, ipadx=135)

        conn.commit()
        conn.close()

    def add_task(self):
        conn = sqlite3.connect('db1.py')
        c = conn.cursor()

        c.execute("INSERT INTO tasks VALUES (:instruction, :due_date,:to_project)",
                  {
                      'instruction': self.t_instruction.get(1.0, END),
                      'due_date': self.t_due_date.get(),
                      'to_project': var.get()
                  })

        conn.commit()
        conn.close()

        self.t_instruction.delete(1.0, END)
        self.t_due_date.delete(0, END)

    def query2(self):

        query2 = Tk()
        query2.geometry("375x180")

        conn = sqlite3.connect('db1.py')
        c = conn.cursor()
        c.execute("SELECT *,oid  FROM tasks")
        records = c.fetchall()

        print_records = ''
        for record in records:
            print_records += str(record) + "\n"

        query_lable = Label(query2, text=print_records)
        query_lable.grid(row=0, column=0, padx=60, pady=10)

        conn.commit()
        conn.close()

    def remove_task(self):
        conn = sqlite3.connect('db1.py')
        c = conn.cursor()

        c.execute("DELETE from tasks WHERE oid = " + self.delete_box.get())
        self.delete_box.delete(0, END)

        conn.commit()
        conn.close()


class MainView(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        p1 = Page1(self)
        p2 = Page2(self)

        buttonframe = Frame(self)
        container = Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = Button(buttonframe, text="Projects", command=p1.lift)
        b2 = Button(buttonframe, text="Tasks", command=p2.lift)

        b1.pack(side="left")
        b2.pack(side="left")

        p1.show()


if __name__ == "__main__":
    root = Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("375x500")
    root.mainloop()

# commit changes
conn.commit()
# close connection
conn.close()
