import mysql.connector
from mysql.connector import Error
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


class _mysql_(object):
    def connect_sql(self, name, psw):
        self.name = name
        self.psw = psw
        if name!='' and psw!='':
            try:
                global connection
                connection = mysql.connector.connect(host='127.0.0.1',
                                                    user=self.name,
                                                    password=self.psw)
                global cursor
                cursor = connection.cursor()

            except Error as e:
                messagebox.showerror("Error",e)
            finally:
                if connection.is_connected():
                    self.window_login.destroy()
                    main.update_home_tab(self, Frame)
                    main.update_main_frame(self, Frame)
        else:
            messagebox.showwarning("Warning","Input name and password!")
            return 0

    def close_connection_sql(self):
        cursor.close()
        connection.close()
        print("bay")
        main.update_home_tab(self, Frame)
        main.update_main_frame(self, Frame)

class _database_(object):    
    # CREATE DATABASE FUNCTION
    def create_db(self):
        
        def validate(str):
    
            if len(str) > 64 or ('/' in str) or ("\\" in str) or ('.' in str) or (str!='' and str[-1] == ' '):
                return 0
            else:
                return 1
    

        def create_db_query():
            db_name = input_db_name.get()
            char_set = self.menu_charsets.get()
            collation = self.menu_collation.get()

            if validate(db_name) and db_name != '':

                cursor.execute("SHOW DATABASES")
                db_list = cursor.fetchall()
                if (db_name,) in db_list:
                    question_response = messagebox.askyesno(" ", "Database already exists\nConnect to an existing database?")
                    
                    # if question_response == 1:
                        # connect_db_form()
                else:
                    try:
                        if connection.is_connected():
                            cursor.execute("CREATE DATABASE IF NOT EXISTS `" + db_name + "` CHARACTER SET " + char_set + " COLLATE " + collation) #IZPILDA VAICĀJUMU
                    except Error as e:
                        messagebox.showerror("Error",e)
                    else:
                        window_create_db.destroy()
                        cursor.execute("SHOW DATABASES")
                        db_list = cursor.fetchall()
                        if(db_name,) in db_list:
                            info_database_created = "The database has been created successfully\n\n" + "Database name: " + db_name + "\nCharacter set: " + char_set + "\nCollation: " + collation
                            messagebox.showinfo('Database info', info_database_created)
            elif validate(db_name)==False:
                messagebox.showinfo("Entry error", "Database name:\n"+"• Cannot be longer than 64 characters;\n"+"• Cannot contain '/' "+r"'\'"+" or '.' characters;\n"+"• Cannot end with space characters.")

            else:
                messagebox.showinfo("Entry error", "Please enter database name!")

        def show_btn():
            btn_create_db = Button(window_create_db, text="Create", command=create_db_query)
            btn_create_db.grid(row=3, column=0, columnspan=2, padx=10, pady=5)


        # SHOW ALL COLLATIONS FOR CHOOSEN CHARACTER SET
        def show_collations(event):
            self.collation_list = []
            self.selected_charset = self.menu_charsets.get()
        
            cursor.execute("SHOW COLLATION WHERE Charset = '"+ self.selected_charset+"';")
            for (collation) in cursor:
                self.collation_list.append(collation[0])


            label_collation = Label(window_create_db, text="Collation:")
            label_collation.grid(row=2, column=0, padx=10, pady=5)

            self.menu_collation = ttk.Combobox(window_create_db, value=self.collation_list)
            self.menu_collation.current(0)
            self.menu_collation.grid(row=2, column=1, padx=10, pady=5)
            
            show_btn()


        # 'CREATE A DATABASE' POPUP
        window_create_db = Toplevel()
        window_create_db.geometry("365x130")
        window_create_db.title("Create a database")
        

        label_db_name = Label(window_create_db, text="Enter database name:")
        label_db_name.grid(row=0, column=0, pady=5, padx=10)

        input_db_name = Entry(window_create_db, width=25)
        input_db_name.grid(row=0, column=1, padx=10)

        # SHOW ALL CHARSETS FROM CURRENT MYSQL VERSION
        self.charset_list = []
        cursor.execute("SHOW CHARACTER SET")

        for (charsets) in cursor:
            self.charset_list.append(charsets[0])

        label_charset = Label(window_create_db, text="Character set:")
        label_charset.grid(row=1, column=0, padx=5, pady=5)
        self.menu_charsets = ttk.Combobox(window_create_db, value=self.charset_list)
        # self.menu_charsets.current(0)
        self.menu_charsets.bind("<<ComboboxSelected>>", show_collations)
        self.menu_charsets.grid(row=1, column=1, padx=5, pady=5)

    def connect_db(self):
        def connect_db_query(selected_db, name, psw):
            self.name = name
            self.psw = psw

            if selected_db != '':
                try:
                    connection = mysql.connector.connect(host='127.0.0.1',
                                                        database=selected_db,
                                                        user=self.name,
                                                        password=self.psw)

                except Error as e:
                    messagebox.showerror("Error",e)
                finally:
                    if connection.is_connected():
                        print("Connected: ", selected_db)
                        window_connect_db.destroy()
                        main.update_database_tab(self, Frame, selected_db, 0)
                        # main.update_table_tab(self, Frame)
            else:
                messagebox.showwarning("Warning","Select database!")
                return 0

        def delete_db(selected_db):
            if selected_db != '':
                try:
                    cursor.execute('DROP DATABASE `' + str(selected_db) + "`")
                except Error as e:
                    messagebox.showerror("Error",e)
                else:
                    messagebox.showinfo("Success","Database deleted!")
                    # main.update_database_tab(self, Frame, selected_db, 0)

        # 'CONNECT TO AN DATABASE' POPUP
        window_connect_db = Toplevel()
        window_connect_db.geometry("365x365")
        window_connect_db.title("Connect to an database")


        Label(window_connect_db, text="Choose a databse:").grid(row=0, column=0, padx=10)
    
        self.db_listbox = Listbox(window_connect_db)

        self.db_list = []
        cursor.execute("SHOW DATABASES")

        for (database) in cursor:
            self.db_list.append(database[0])
            self.db_listbox.insert(END, database[0])

        self.db_listbox.grid(row=0, column=1, pady=10, padx=10)
            
        btn_connect_db = Button(window_connect_db, text="Connect", command=lambda:connect_db_query(self.db_listbox.get(ANCHOR), self.name, self.psw))
        btn_connect_db.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        btn_delete_db = Button(window_connect_db, text="Delete database", command=lambda:delete_db(self.db_listbox.get(ANCHOR)))
        btn_delete_db.grid(row=2, column=0, columnspan=2, padx=10, pady=10)



class _table_(object):

    def create_tbl(self, selected_db):
        # self.tab_menu.select(2)
        # CREATE TABLE POPUP
        self.window_create_table = Toplevel()
        self.window_create_table.geometry("300x300")
        self.window_create_table.title("Create table")

        Label(self.window_create_table, text="Name: ").pack(pady=5)
        input_tbl_name = Entry(self.window_create_table, width=25)
        input_tbl_name.pack()

        Label(self.window_create_table, text="Number of columns:").pack(pady=5)

        number_of_columns = Spinbox(self.window_create_table, from_=1, to=999, font=16, width=3)
        number_of_columns.pack()

        btn_generate_cols = Button(self.window_create_table, text="Next", command=lambda:_table_.generate_columns(self, int(number_of_columns.get()), input_tbl_name.get(), selected_db))
        btn_generate_cols.pack()

    def generate_columns(self, rows, tbl_name, selected_db):

        self.window_create_table.destroy()

        # DATA TYPE LISTF
        self.datatypes = ["INT", "TINYINT", "SMALLINT", "MEDIUMINT", "BIGINT",
                        "DECIMAL", "FLOAT", "BOOLEAN", "SERAIL",
                        "DATE", "DATETIME", "TIMESTAMP", "TIME", "YEAR",
                        "STRING", "CHAR", "VARCHAR", "TINYTEXT", "TEXT",
                        "MEDIUMTEXT", "LONGTEXT","BINARY", "VARBINARY",
                        "TINYBLOB", "MEDIUMBLOB", "BLOB", "LONGBLOB"
                        ]

        # DATA TYPES WITH FIXED SIZE
        self.datatyps_w_fixed_len = ["TEXT","DATE","SERIAL","SERIAL", "TINYINT",
                                    "MEDIUMINT", "TINYBLOB", "MEDIUMBLOB", "BLOB",
                                    "LONGBLOB"
                                    ]
                                
    
        # COL LISTS
        self.list_col_name = []
        self.list_col_type = []
        self.list_col_length = []
        self.list_col_default = []
        self.list_col_attribute = []
        self.list_col_null = []
        self.list_col_index = []
        self.list_col_auto_incr = []

        def create_tbl_query(selected_db):

            # upadte table list


            query = StringVar()
            query.set("CREATE TABLE `" + str(tbl_name) +"` (")

            for n in range(rows):
                query.set(query.get() + "`" + str(self.list_col_name[n].get()) + "` ")
                query.set(query.get() + str(self.list_col_type[n].get()))

                if self.list_col_type[n].get()  not in self.datatyps_w_fixed_len:
                    query.set(query.get() + "(" + str(self.list_col_length[n].get())+ ")")

                if self.list_col_attribute[n].get() != "":
                    query.set(query.get() + " " + str(self.list_col_attribute[n].get()))

                query.set(query.get() + " " + str(self.list_col_null[n].get()))
                
                if self.list_col_default[n].get() != "":
                    query.set(query.get() + " DEFAULT '" +str(self.list_col_default[n].get()) + "'")

                if self.list_col_auto_incr[n].get() != "":
                    query.set(query.get() + " " + str(self.list_col_auto_incr[n].get()))
                

                if rows != 1:
                    if n+1 < rows:
                        query.set(query.get() + ", ")


                    if n+1 == rows:
                        for x in range(rows):
                            if self.list_col_index[x].get() != "":
                                query.set(query.get() + ", " +str(self.list_col_index[x].get()) + " (`" + self.list_col_name[x].get() + "`)")



                if self.list_col_index[n].get() != "" and rows == 1:
                    query.set(query.get() + "," + str(self.list_col_index[n].get()) + " (`" + self.list_col_name[n].get() + "`)")
            
                # if rows == 1:
                #     query.set(query.get() + ")")
                print(" n= ", n)
                print("rows= ", rows)

            query.set(query.get()+") ENGINE = InnoDB;")

            print(query.get())
            try:
                cursor.execute("USE " + selected_db)
                cursor.execute(query.get())
            except Error as e:
                messagebox.showerror("Error",e)
            else:
                messagebox.showinfo(title='Success', message='Table has been created')
                self.window_table_columns.destroy()
                main.update_database_tab(self, Frame, selected_db, 1)


        self.window_table_columns = Toplevel()
        self.window_table_columns.geometry("1350x200")
        self.window_table_columns.title("Create a table")

        # CANVAS
        main_canvas = Canvas(self.window_table_columns)
        main_canvas.pack(side=LEFT, fill=BOTH, expand=1)
        # CREATE SCROLLBAR
        canvas_scrollbar = ttk.Scrollbar(self.window_table_columns, orient=VERTICAL, command=main_canvas.yview)
        if rows > 5 :
            canvas_scrollbar.pack(side=RIGHT, fill=Y)
        # ADD SCROLLBAR TO CANVAS
        main_canvas.configure(yscrollcommand=canvas_scrollbar.set)
        main_canvas.bind('<Configure>', lambda e: main_canvas.configure(scrollregion = main_canvas.bbox("all")))
        # SUB FRAME
        sub_frame = Frame(main_canvas)
        # ADD SUB FRAME TO CANVAS
        main_canvas.create_window((0,0), window=sub_frame, anchor=NW)


        # HEADERS
        Label(sub_frame, text="Name").grid(row=0, column=0)
        Label(sub_frame, text="Datatype").grid(row=0, column=1)
        Label(sub_frame, text="Length").grid(row=0, column=2)
        Label(sub_frame, text="Default").grid(row=0, column=3)
        Label(sub_frame, text="Attributes").grid(row=0, column=4)
        Label(sub_frame, text="Null").grid(row=0, column=5)
        Label(sub_frame, text="Index").grid(row=0, column=6)
        Label(sub_frame, text="Auto Increment").grid(row=0, column=7)


        for y in range(rows):

            var_null = StringVar()
            var_auto_incr = StringVar()

            col_name = Entry(sub_frame, width=25)
            col_type = ttk.Combobox(sub_frame, value=["INT", "VARCHAR", "TEXT", "DATE"])
            col_length = Spinbox(sub_frame, from_=1, to=9999, width=6)
            col_default = Entry(sub_frame, width=25)
            col_attribute = ttk.Combobox(sub_frame, value=["BINARY", "UNSIGNED", "UNSIGNED ZEROFILL"])
            col_null = Checkbutton(sub_frame, variable=var_null, onvalue="NULL", offvalue="NOT NULL")
            col_index = ttk.Combobox(sub_frame, value=["PRIMARY KEY","UNIQUE", "INDEX", "FULLTEXT", "SPATIL"])
            col_auto_incr = Checkbutton(sub_frame, variable=var_auto_incr, onvalue="AUTO_INCREMENT", offvalue="")

            col_null.deselect()
            col_auto_incr.deselect()

            col_name.grid(row=y+1, column=0, pady=5, padx=10)
            col_type.grid(row=y+1, column=1, pady=5, padx=10)
            col_length.grid(row=y+1, column=2, pady=5, padx=10)
            col_default.grid(row=y+1, column=3, pady=5, padx=10)
            col_attribute.grid(row=y+1, column=4, pady=5, padx=10)
            col_null.grid(row=y+1, column=5, pady=5, padx=10)
            col_index.grid(row=y+1, column=6, pady=5, padx=10)
            col_auto_incr.grid(row=y+1, column=7, pady=5, padx=10)

            self.list_col_name.append(col_name)
            self.list_col_type.append(col_type)
            self.list_col_length.append(col_length)
            self.list_col_default.append(col_default)
            self.list_col_attribute.append(col_attribute)
            self.list_col_null.append(var_null)
            self.list_col_index.append(col_index)
            self.list_col_auto_incr.append(var_auto_incr)


        Button(sub_frame, text="Create table", command=lambda:create_tbl_query(selected_db)).grid(row=rows+1, column=8, columnspan=2, ipadx=30, pady=10)

    def insert_data(self, selected_db ,selected_tbl, field_list, entry_dir):

        cursor.execute("USE " + selected_db)
        query = StringVar()
        fields = StringVar()
        values = StringVar()


        query.set("INSERT INTO `" + selected_tbl + "` (")

        # IZIET CAURI VISIEM IEVADES LOGIEM UN PIE VALUES PIEVIENO TIKAI TOS LAUKU NOSAKUMUS, KURI NAV TUKŠI
        for n in range(len(field_list)):
            # JA ENTRYS NAV TUKŠS
            if entry_dir[field_list[n] + "_entry"].get(): 
                fields.set(fields.get() + field_list[n] + ", ")
                values.set(values.get() +  "'" + entry_dir[field_list[n] + "_entry"].get() + "', ")


        # NOŅEM PĒDĒJO KOMATU UN ATSTARPI
        fields.set(fields.get()[:-2])
        values.set(values.get()[:-2])

        query.set(query.get() + fields.get() + ") VALUES(" + values.get() + ")")

        try:
            cursor.execute(str(query.get()))
            connection.commit()
            print(query.get())

        except Error as e:
            messagebox.showerror("Error",e)
        else:

            main.update_table_tab(self, Frame, selected_db, selected_tbl)
            print("DATA INSERTED")

    def delete_record(self, selected_record):
        if not selected_record:
            messagebox.showinfo('', 'SELECT RECORD')
        else:
            print(selected_record)



class _relations_(object):

    def relation_view(self, tbl_list, selected_db):

        self.window_select_tbl.destroy()

        self.window_relation_view = Toplevel()
        self.window_relation_view.geometry("1200x800")
        self.window_relation_view.title("Relations")

        cursor.execute("USE `" + selected_db + "`")

        print(tbl_list)
        # DEIFINE DICTIONARYS
        self.temp_treeview = {}
        self.temp_combobox = {}

        for n in range(2):
            # DEFINE COLUMN LIST
            tbl_column_list = []
            # DEFINE TREEVIEW
            self.temp_treeview['table_' + str(n)] = ttk.Treeview(self.window_relation_view)
            #  DEFINE TREEVIEW COLUMNS
            self.temp_treeview['table_' + str(n)]['columns'] = ('column_name', 'data_type')
            
            self.temp_treeview['table_' + str(n)].column('#0', anchor=CENTER, width=60)
            self.temp_treeview['table_' + str(n)].column('column_name', anchor=CENTER, width=200)
            self.temp_treeview['table_' + str(n)].column('data_type', anchor=CENTER, width=100)
            #  DEFINE TREEVIEW HEADINGS
            self.temp_treeview['table_' + str(n)].heading('#0', text="KEY", anchor=CENTER) 
            self.temp_treeview['table_' + str(n)].heading('column_name', text=tbl_list[n], anchor=CENTER) 
            self.temp_treeview['table_' + str(n)].heading('data_type', text="type", anchor=CENTER)

            #  ADD DATA
            cursor.execute("DESCRIBE `"+ tbl_list[n] + "`")
            for cols in cursor:
                self.temp_treeview['table_' + str(n)].insert(parent='', index='end', text=cols[3], values=(cols[0], cols[1]))
                tbl_column_list.append(cols[0])

            # CREATE A DROPDOWN LIST    
            self.temp_combobox['combobox_' + str(n)] = ttk.Combobox(self.window_relation_view, value=tbl_column_list)

            # PLACE TREEVIEWS AND COMBOBOXES ON SCREEN
            self.temp_treeview['table_' + str(n)].grid(row=1, column=n, padx=10, pady=10)
            self.temp_combobox['combobox_' + str(n)].grid(row=2, column=n, padx=10, pady=10)

        # RELATION TABLE
        self.relation_table_name = StringVar()

        Label(self.window_relation_view, textvariable=self.relation_table_name, font = 16).grid(row=0, column=3, pady=20, padx=10)
        self.relation_table_name.set("Relations from '" + tbl_list[0] + "' TO '" + tbl_list[1] + "'")
        # DEFINE TREEVIEW
        self.relation_treeview = ttk.Treeview(self.window_relation_view)
        #  DEFINE TREEVIEW COLUMNS
        self.relation_treeview['columns'] = ('TO')
        self.relation_treeview.column('#0', anchor=CENTER, width=80)
        self.relation_treeview.column('TO', anchor=CENTER, width=80)
        
        #  DEFINE TREEVIEW HEADINGS
        self.relation_treeview.heading('#0', text=tbl_list[0], anchor=CENTER)
        self.relation_treeview.heading('TO', text=tbl_list[1], anchor=CENTER)

        # GET INFORMATION ABOUT RELATIONS
        # print("SELECT COLUMN_NAME, REFERENCED_COLUMN_NAME FROM information_schema.key_column_usage WHERE REFERENCED_TABLE_SCHEMA = '"+ selected_db +"' AND REFERENCED_TABLE_NAME = '" + tbl_list[1] +"' AND TABLE_NAME = '" + tbl_list[0] + "';")
        cursor.execute("SELECT COLUMN_NAME, REFERENCED_COLUMN_NAME FROM information_schema.key_column_usage WHERE REFERENCED_TABLE_SCHEMA = '"+ str(selected_db) +"' AND REFERENCED_TABLE_NAME = '" + str(tbl_list[1]) +"' AND TABLE_NAME = '" + str(tbl_list[0]) + "';")
        for col in cursor:
            print(col)
            self.relation_treeview.insert(parent='', index='end', text=col[0], values=col[1])

        self.relation_treeview.grid(row=1, column=3)

        def create_relation_query(col_0, col_1, tbl_list):
            print("quer-def: ",tbl_list)
            key_name = StringVar()
            key_name.set("fk_" + str(tbl_list[0]) + "_" + str(col_0) + "_to_" + str(col_1))
            print(key_name.get())
            query = StringVar()
            query.set("ALTER TABLE `" + str(tbl_list[0]) + "` ADD CONSTRAINT " + str(key_name.get()) + " FOREIGN KEY (" + str(col_0) + ") REFERENCES " + str(tbl_list[1]) + "(" + str(col_1) + ")")
            try:
                cursor.execute(str(query.get()))
                # print(query.get())

            except Error as e:
                messagebox.showerror("Error",e)
            else:
                self.window_relation_view.destroy()
                connection.commit()
                messagebox.showinfo('','Relation created')
                print('Relation created')


        self.col_swap = [0,1]
        self.swap = False
        def swap_tables(tbl_list):
            tbl_list[0], tbl_list[1] = tbl_list[1], tbl_list[0]
        
            self.temp_treeview['table_0'].grid_forget()
            self.temp_combobox['combobox_0'].grid_forget()

            self.temp_treeview['table_1'].grid_forget()
            self.temp_combobox['combobox_1'].grid_forget()


            if self.swap == True:
                self.temp_combobox['combobox_0'], self.temp_combobox['combobox_1'] = self.temp_combobox['combobox_1'], self.temp_combobox['combobox_0']

                Button(self.window_relation_view, text = "Go", command = lambda:create_relation_query(self.temp_combobox['combobox_1'].get(), self.temp_combobox['combobox_0'].get(), tbl_list)).grid(row=3, column=0, columnspan=2)

            self.temp_treeview['table_0'].grid(row=1, column=self.col_swap[1], padx=10, pady=10)
            self.temp_combobox['combobox_0'].grid(row=2, column=self.col_swap[1], padx=10, pady=10)

            self.temp_treeview['table_1'].grid(row=1, column=self.col_swap[0], padx=10, pady=10)
            self.temp_combobox['combobox_1'].grid(row=2, column=self.col_swap[0], padx=10, pady=10)

            self.col_swap[0], self.col_swap[1] = self.col_swap[1], self.col_swap[0]

            self.temp_combobox['combobox_0'], self.temp_combobox['combobox_1'] = self.temp_combobox['combobox_1'], self.temp_combobox['combobox_0']
            Button(self.window_relation_view, text = "Go", command = lambda:create_relation_query(self.temp_combobox['combobox_0'].get(), self.temp_combobox['combobox_1'].get(), tbl_list)).grid(row=3, column=0, columnspan=2)

            for record in self.relation_treeview.get_children():
                self.relation_treeview.delete(record)
            
            self.relation_table_name.set("Relations from '" + tbl_list[0] + "' TO '" + tbl_list[1] + "'")

            #  REDEFINE TREEVIEW HEADINGS
            self.relation_treeview.heading('#0', text=tbl_list[0], anchor=CENTER)
            self.relation_treeview.heading('TO', text=tbl_list[1], anchor=CENTER)

            # GET INFORMATION ABOUT RELATIONS
            cursor.execute("SELECT COLUMN_NAME, REFERENCED_COLUMN_NAME FROM information_schema.key_column_usage WHERE REFERENCED_TABLE_SCHEMA = '"+ str(selected_db) +"' AND REFERENCED_TABLE_NAME = '" + str(tbl_list[1]) +"' AND TABLE_NAME = '" + str(tbl_list[0]) + "';")
            for col_name in cursor:
                self.relation_treeview.insert(parent='', index='end', text=col_name[0], values=col_name[1])
            self.relation_treeview.grid(row=1, column=3)
            
            self.swap = True



        Button(self.window_relation_view, text="<-\n->", command = lambda:swap_tables(tbl_list)).grid(row=0, column=0, columnspan=2)
        Button(self.window_relation_view, text = "Go", command = lambda:create_relation_query(self.temp_combobox['combobox_0'].get(), self.temp_combobox['combobox_1'].get(), tbl_list)).grid(row=3, column=0, columnspan=2)
        
        info_relation = StringVar()

        lbl_info_relation = Label(self.window_relation_view, textvariable=info_relation)
        lbl_info_relation.grid(row=3, column=3)

        def del_relation_info(e):
            info_relation.set("")
        def selectItem(e):
            temp_key_list = []
            curItem = self.relation_treeview.focus()
            
            cursor.execute("SHOW COLUMNS FROM " + tbl_list[0] + " WHERE Field='"+str(self.relation_treeview.item(curItem)["text"])+"';")
            for col in cursor:
                temp_key_list.append(col[3])

            # SHOW COLUMNS FROM post WHERE Field='post_id';
            cursor.execute("SHOW COLUMNS FROM " + tbl_list[1] + " WHERE Field='"+str(self.relation_treeview.item(curItem)["values"][0])+"';")
            for col in cursor:
                temp_key_list.append(col[3])
            print(temp_key_list)
            if (temp_key_list[0] == 'MUL' and temp_key_list[1] == 'PRI'):
                info_relation.set('many to one')
            elif (temp_key_list[0] == 'PRI' and temp_key_list[1] == 'MUL'):
                info_relation.set('one to many')
            elif (temp_key_list[0] == 'PRI' and temp_key_list[1] == 'PRI'):
                info_relation.set('one to one') 
            elif (temp_key_list[0] == 'MUL' and temp_key_list[1] == 'MUL'):
                info_relation.set('many to many') 
        self.relation_treeview.bind('<ButtonRelease-1>', selectItem)
        self.relation_treeview.bind('<Leave>', del_relation_info)





    def add_to_list_b(self, tbl):
        if tbl != "":
            self.tbl_listbox_a.delete(ANCHOR)
            self.list_selected_tbl.append(tbl)
            self.tbl_listbox_b.insert(END, tbl)
            print("Selected tables: ", self.list_selected_tbl)
        else:
            print('Nothing is selected!')
        if len(self.list_selected_tbl) == 2:
            self.btn_relation_go.grid(row=2, column=1, pady=10, padx=10)
        else:
            self.btn_relation_go.grid_forget()


    def remove_from_list_b(self, tbl):
        if tbl != "":
            self.tbl_listbox_b.delete(ANCHOR)
            self.list_selected_tbl.remove(tbl)
            self.tbl_listbox_a.insert(END, tbl)    
            print("Selected tables: ", self.list_selected_tbl)
        else:
            print('Nothing is selected!')
        if len(self.list_selected_tbl) == 2:
            self.btn_relation_go.grid(row=2, column=1, pady=10, padx=10)
        else:
            self.btn_relation_go.grid_forget()



    def select_tbl_relation_view(self, selected_db):
        self.window_select_tbl = Toplevel()
        self.window_select_tbl.geometry("565x365")
        self.window_select_tbl.title("Select tables")
        
        self.tbl_listbox_a = Listbox(self.window_select_tbl)
        self.list_selected_tbl = []
        tbl_list = []
        cursor.execute("SHOW TABLES FROM "+ selected_db)



        for (table) in cursor:
            tbl_list.append(table[0])
            self.tbl_listbox_a.insert(END, table[0])

        self.tbl_listbox_b = Listbox(self.window_select_tbl)


        Label(self.window_select_tbl, text="Select tables:").grid(row=0, column=0, pady=10, padx=10)
        self.tbl_listbox_a.grid(row=1, column=0, pady=10, padx=10)
        self.tbl_listbox_b.grid(row=1, column=2, pady=10, padx=10)
        Button(self.window_select_tbl, text="Add", command=lambda:_relations_.add_to_list_b(self, self.tbl_listbox_a.get(ANCHOR))).grid(row=2, column=0, pady=10, padx=10)
        Button(self.window_select_tbl, text="Remove", command=lambda:_relations_.remove_from_list_b(self, self.tbl_listbox_b.get(ANCHOR))).grid(row=2, column=2, pady=10, padx=10)
        self.btn_relation_go = Button(self.window_select_tbl, text="Next", command=lambda:_relations_.relation_view(self, self.list_selected_tbl, selected_db))

class _query_(object):

    def query_view(self, selected_db):
        self.window_query_view = Toplevel()
        self.window_query_view.geometry("700x400")
        self.window_query_view.title("Querys")
        
        self.window_query_view.grid_columnconfigure(0, weight=1) #centers content horizontally

        btn_create_query_view = Button(self.window_query_view, text="New", command=lambda:_query_.create_query_view(self, selected_db))
        btn_create_query_view.grid(row=0, column=1, sticky=NE)

        list_query_name = []

        query_table = selected_db + "_querys"
        cursor.execute("SHOW TABLES FROM `" + selected_db + "`")
        tables = cursor.fetchall()
        if (query_table,) in tables:
            listbox_querys = Listbox(self.window_query_view)
            cursor.execute("USE `" + selected_db + "`")
            cursor.execute("SELECT query_name FROM `" + query_table + "`")

            for query_name in cursor:
                list_query_name.append(query_name[0])
                listbox_querys.insert(END, query_name[0])

            listbox_querys.grid(row = 0, column=0)
            Button(self.window_query_view, text='Select', command=lambda:_query_.execute_query(self, selected_db, query_table, listbox_querys.get(ANCHOR))).grid(row=1, column=0, pady=10)

        else:
            messagebox.showinfo(title='', message='There is no querys\nClick "New query" to create a new query')


    def create_query_view(self, selected_db):
        self.window_query_view.destroy()
        self.window_create_query_view = Toplevel()
        self.window_create_query_view.geometry("1200x800")
        self.window_create_query_view.title("New query")
        
        # window_create_query_view.grid_columnconfigure(0, weight=1) #centers content horizontally

        # CREATE FRAMES
        frame_top_create_query_view = Frame(self.window_create_query_view)
        frame_bottom_create_query_view = Frame(self.window_create_query_view)
        frame_top_create_query_view.pack(side=TOP)
        frame_bottom_create_query_view.pack(side=BOTTOM, expand=1, fill=BOTH)

        # CREATE CANVAS
        canvas_create_query_view_bottom = Canvas(frame_bottom_create_query_view)
        canvas_create_query_view_bottom.pack(fill=BOTH, expand=1)

        # CREATE SUBFRAME
        self.sub_frame_bottom_create_query_view = Frame(canvas_create_query_view_bottom)

        # ADD SUBFRAME TO CANVAS
        canvas_create_query_view_bottom.create_window((0,0), window=self.sub_frame_bottom_create_query_view, anchor=NW)

        # CREATE SCROLLBAR
        self.scrollbar_bottom_frame = ttk.Scrollbar(frame_bottom_create_query_view, orient=HORIZONTAL, command=canvas_create_query_view_bottom.xview)
        
        canvas_create_query_view_bottom.configure(xscrollcommand=self.scrollbar_bottom_frame.set)
        # scrollbar_bottom_frame.configure(command=canvas_create_query_view_bottom.xview)
        canvas_create_query_view_bottom.bind('<Configure>', lambda e: canvas_create_query_view_bottom.configure(scrollregion = canvas_create_query_view_bottom.bbox("all")))

        self.tbl_listbox_a = Listbox(frame_top_create_query_view)
        self.list_selected_tbl = []
        tbl_list = []
        
        
        cursor.execute("USE `"+ selected_db + "`")
        cursor.execute("SHOW TABLES")
        for (table) in cursor:
            tbl_list.append(table[0])
            self.tbl_listbox_a.insert(END, table[0])

        self.tbl_listbox_b = Listbox(frame_top_create_query_view)

        # DICTIONARYS FOR GENERATED WIDGETS
        self.temp_tbl_labels = {}
        self.temp_listbox_a = {}
        self.temp_listbox_b = {}
        self.temp_add_btn = {}
        self.temp_remove_btn = {}

        # DICTIONARYS FOR GENERATED LISTS
        self.temp_col_list = {}

        Label(frame_top_create_query_view, text="Select tables:").grid(row=0, column=0, pady=10, padx=10)
        self.tbl_listbox_a.grid(row=1, column=0, pady=10, padx=10)
        self.tbl_listbox_b.grid(row=1, column=2, pady=10, padx=10)
        Button(frame_top_create_query_view, text="Add", command=lambda:_query_.add_to_list_b(self, self.tbl_listbox_a.get(ANCHOR))).grid(row=2, column=0, pady=10, padx=10)
        Button(frame_top_create_query_view, text="Remove", command=lambda:_query_.remove_from_list_b(self, self.tbl_listbox_b.get(ANCHOR))).grid(row=2, column=2, pady=10, padx=10)
        Button(frame_top_create_query_view, text="Next", command=lambda:_query_.generate_query_entrys(self, selected_db, self.temp_col_list)).grid(row=3, column=4)


    # Add table names to listbox
    def add_to_list_b(self, tbl):
        if tbl != "":
            self.tbl_listbox_a.delete(ANCHOR)
            self.list_selected_tbl.append(tbl)
            self.tbl_listbox_b.insert(END, tbl)
            print("Selected tables: ", self.list_selected_tbl)
            _query_.generate_listboxes(self, self.list_selected_tbl, tbl)

            if len(self.list_selected_tbl) > 6:
                        self.scrollbar_bottom_frame.pack(side=BOTTOM, fill=X)

        else:
            print('Nothing is selected!')

    # Remove table names from listbox
    def remove_from_list_b(self, tbl):
        if tbl != "":
            self.tbl_listbox_b.delete(ANCHOR)
            _query_.remove_listboxes(self, tbl)
            self.list_selected_tbl.remove(tbl)
            self.tbl_listbox_a.insert(END, tbl)    
            print("Selected tables: ", self.list_selected_tbl)
            if len(self.list_selected_tbl) < 6:
                self.scrollbar_bottom_frame.pack_forget()

        else:
            print('Nothing is selected!')

    # Add column names to listbox
    def add_col_to_list_b(self, tbl_name, col_name):
        if col_name != "":
            self.temp_listbox_a['listbox_' + tbl_name].delete(ANCHOR)
            self.temp_col_list['col_list_' + tbl_name].append(col_name)
            self.temp_listbox_b['listbox_' + tbl_name].insert(END, col_name)
        else:
            print('Nothing is selected!')

    # Remove column names from listbox
    def remove_col_from_list_b(self, tbl_name, col_name):
        if col_name != "":
            self.temp_listbox_b['listbox_' + tbl_name].delete(ANCHOR)
            self.temp_col_list['col_list_' + tbl_name].remove(col_name)
            self.temp_listbox_a['listbox_' + tbl_name].insert(END, col_name)
        else:
            print('Nothing is selected!')            
        
        
    def generate_listboxes(self, tbl_list, tbl_name):

        # GENERATE LISTS
        self.temp_col_list['col_list_' + tbl_name] = []

        # GENERATE WIDGETS(Listboxes, labels, buttons)
        self.temp_listbox_a['listbox_' + tbl_name] = Listbox(self.sub_frame_bottom_create_query_view)
        self.temp_listbox_b['listbox_' + tbl_name] = Listbox(self.sub_frame_bottom_create_query_view)
        self.temp_tbl_labels['label_' + tbl_name] = Label(self.sub_frame_bottom_create_query_view, text=tbl_name)
        self.temp_add_btn['add_' + tbl_name] = Button(self.sub_frame_bottom_create_query_view, text=' ↓ ', command=lambda:_query_.add_col_to_list_b(self, tbl_name, self.temp_listbox_a['listbox_' + tbl_name].get(ANCHOR)))
        self.temp_remove_btn['remove_' + tbl_name] = Button(self.sub_frame_bottom_create_query_view, text=' ↑ ', command=lambda:_query_.remove_col_from_list_b(self, tbl_name, self.temp_listbox_b['listbox_' + tbl_name].get(ANCHOR)))

        #  ADD DATA
        cursor.execute("DESCRIBE `"+ tbl_name + "`")
        for cols in cursor:
            # Add table name
            self.temp_tbl_labels['label_' + tbl_name].grid(row=0, column=tbl_list.index(tbl_name), pady=10)

            # Add listboxes A
            self.temp_listbox_a['listbox_' + tbl_name].insert(END, cols[0])
            self.temp_listbox_a['listbox_' + tbl_name].grid(row=1, column=tbl_list.index(tbl_name), padx=10)

            # Add buttons
            self.temp_add_btn['add_' + tbl_name].grid(row=2, column=tbl_list.index(tbl_name), pady=5, padx=10, sticky=W)
            self.temp_remove_btn['remove_' + tbl_name].grid(row=2, column=tbl_list.index(tbl_name), pady=5, padx=10, sticky=E)

            # Add listboxes B
            self.temp_listbox_b['listbox_' + tbl_name].grid(row=3, column=tbl_list.index(tbl_name), padx=10)



    def remove_listboxes(self, tbl_name):  

        # Remove table names
        self.temp_tbl_labels['label_' + tbl_name].grid_forget()
        del self.temp_tbl_labels['label_' + tbl_name]

        # Remove lisboxes
        self.temp_listbox_a['listbox_' + tbl_name].grid_forget()
        del self.temp_listbox_a['listbox_' + tbl_name]

        self.temp_listbox_b['listbox_' + tbl_name].grid_forget()

        # Remove buttons
        self.temp_add_btn['add_' + tbl_name].grid_forget()
        self.temp_remove_btn['remove_' + tbl_name].grid_forget()


    def generate_query_entrys(self, selected_db, cols):

        self.window_create_query_view.destroy()

        def create_query(query_name, col_count, cols):

            def save_query(selected_db ,query_name, query, cols):
                table_name = StringVar()
                table_name.set(selected_db + "_querys")
                sql_create_query = StringVar()
                sql_insert_query = StringVar()

                col_string = ', '.join(cols)
                # CREATE QUERY TO CREATE A TABLE
                sql_create_query.set("CREATE TABLE IF NOT EXISTS `" + str(table_name.get()) + "` ( query_name VARCHAR(100) NOT NULL, sql_query VARCHAR(1000) NOT NULL, cols VARCHAR(100) NOT NULL)")
                # CREATE QUERY TO INSERT DATA
                sql_insert_query.set('INSERT INTO `' + str(table_name.get()) + '` VALUES("' +str(query_name) + '", "' + str(query) + '", "' + col_string +'")')
                
                try:
                    # EXECUTE CREATE QUERY
                    cursor.execute(str(sql_create_query.get()))
                    connection.commit()
                    # INSERT QUERY AND QUERYS NAME IN TABLE
                    print(str(sql_insert_query.get()))
                    cursor.execute(str(sql_insert_query.get()))
                    connection.commit()

                except Error as e:
                    messagebox.showerror("Error", e)

                else:
                    # self.window_query_view.destroy()
                    self.window_query_entrys.destroy()
                    self.window_create_query_view.destroy()
                    message = "Query: " + query_name + " has been created successfully"
                    messagebox.showinfo(title='Success', message=message)



            if not query_name:
                print("Enter query name!")
            else:
                query = StringVar()
                str_tbl_col = StringVar()
                str_tbl = StringVar()
                str_sort = StringVar()
                str_criteria = StringVar()
                str_criteria_or = StringVar()

                query.set("SELECT ")
                # IEGŪST SARAKSTU AR TABULĀM UN KOLONNĀM (tbl1.col1, tbl3.col5) 
                for tbl in range(len(self.list_selected_tbl)):
                    for col in range(len(self.temp_col_list['col_list_' + self.list_selected_tbl[tbl]])):
                        str_tbl_col.set(str_tbl_col.get() + self.list_selected_tbl[tbl] + "." + self.temp_col_list['col_list_' + self.list_selected_tbl[tbl]][col] + ", ")
                
                list_tbl_col = str_tbl_col.get()[:-2].split(', ')

                str_tbl_col.set(str_tbl_col.get()[:-2]) #DELETE LAST TWO CHARACTERS
                query.set(query.get()+str_tbl_col.get())

                # IEGŪST SARAKSTU AR TABULĀM
                for tbl in range(len(self.list_selected_tbl)):
                    str_tbl.set(str_tbl.get() + self.list_selected_tbl[tbl] + ", ")

                str_tbl.set(str_tbl.get()[:-2]) #DELETE LAST TWO CHARACTERS
                query.set(query.get() + " FROM " + str_tbl.get())

                # IEGŪST KRITĒRIJUS
                for n in range(col_count):
                    if self.list_query_criteria[n].get():
                        str_criteria.set(str_criteria.get() + "((" + str(list_tbl_col[n]) + ") ='" + self.list_query_criteria[n].get() + "') AND ")

                # IEGŪST SEKUNDĀROS KRITĒRIJUS
                for n in range(col_count):
                    if self.list_query_criteria_or[n].get():
                        str_criteria_or.set(str_criteria_or.get() + "((" + str(list_tbl_col[n]) + ") ='" + self.list_query_criteria_or[n].get() + "') AND ")


                str_criteria.set(str_criteria.get()[:-5])
                str_criteria_or.set(str_criteria_or.get()[:-5])
                # IEVADĪTI ABI KRITĒRIJI
                if str_criteria.get() and str_criteria_or.get():
                    query.set(query.get() + " WHERE " + "(" + str_criteria.get())
                    query.set(query.get() + " OR " + str_criteria_or.get() + ")")

                # IEVADĪTS TIKAI GALVENAIS KRITĒRIJS
                elif str_criteria.get():
                    query.set(query.get() + " WHERE " + "(" + str_criteria.get() + ")")
                
                # IEVADĪTS TIKAI SEKUNDĀRAIS KRITĒRIJS
                elif str_criteria_or.get():
                    query.set(query.get() + " WHERE " + "(" + str_criteria_or.get() + ")")

                # NAV IEVADĪTS NEVIENS KRITĒRIJS
                else:
                    pass

                # IEGŪST KĀRTOŠANAS SECĪBAS
                for n in range(col_count):
                    if self.list_query_sort[n].get():
                        str_sort.set(str_sort.get() + str(list_tbl_col[n]) + " " + self.list_query_sort[n].get() + ", ")


                if not str_sort.get():
                    pass # NAV IZVĒLĒTA NEVIENA KĀRTOŠANAS SECĪBA
                else:
                    str_sort.set(str_sort.get()[:-2])
                    query.set(query.get() + " ORDER BY " + str_sort.get())


                print(query.get())

                save_query(selected_db, query_name, query.get(), cols)


        self.window_query_entrys = Toplevel()
        self.window_query_entrys.geometry("1000x500")
        self.window_query_entrys.title("New query")

        # CREATE FRAME ON TOP OF TOPLEVEL
        frame_query_entrys_top = Frame(self.window_query_entrys)
        frame_query_entrys_top.pack(side=TOP, fill=X)

        # CREATE FRAME ON BOTTOM OF TOPLEVEL
        frame_query_entrys_bottom = Frame(self.window_query_entrys)
        frame_query_entrys_bottom.pack(side=BOTTOM, fill=BOTH, expand=1)

        # CREATE FRAME INSIDE BOTTOM FRAME (LEFT SIDE)
        frame_query_entrys_bottom_left = Frame(frame_query_entrys_bottom)
        frame_query_entrys_bottom_left.pack(side=LEFT, fill=Y)

        # CREATE CANVAS INSIDE BOTTOM FRAME (RIGHT SIDE)
        canvas_query_entrys_bottom_right = Canvas(frame_query_entrys_bottom)
        canvas_query_entrys_bottom_right.pack(side=LEFT, fill=BOTH, expand=1)

        # CREATE FRAME INSIDE CANVAS
        subframe_query_entrys = Frame(canvas_query_entrys_bottom_right)

        # ADD FRAME TO CANVAS
        canvas_query_entrys_bottom_right.create_window((0,0), window=subframe_query_entrys, anchor=NW)


        Label(frame_query_entrys_top, text="Query name:").grid(row=0, column=0, pady=10, padx=10)
        entry_query_name = Entry(frame_query_entrys_top, width=30)
        entry_query_name.grid(row=0, column=1, pady=10, padx=10) 

        Label(frame_query_entrys_bottom_left, text="Table:").grid(row=1, column=0, pady=10, padx=10)
        Label(frame_query_entrys_bottom_left, text="Field:").grid(row=2, column=0, pady=10, padx=10)
        Label(frame_query_entrys_bottom_left, text="Sort:").grid(row=3, column=0, pady=10, padx=10)
        Label(frame_query_entrys_bottom_left, text="Criteria:").grid(row=4, column=0, pady=10, padx=10)
        Label(frame_query_entrys_bottom_left, text="Or:").grid(row=5, column=0, pady=10, padx=10)

        col_count = 0

        self.list_query_sort = []
        self.list_query_criteria = []
        self.list_query_criteria_or = []
        cols = []

        for tbl in range(len(self.list_selected_tbl)):
            for col in range(len(self.temp_col_list['col_list_' + self.list_selected_tbl[tbl]])):
                col_count += 1

                lbl_tbl_name = Label(subframe_query_entrys, text=self.list_selected_tbl[tbl])
                lbl_col_name = Label(subframe_query_entrys, text=self.temp_col_list['col_list_' + self.list_selected_tbl[tbl]][col])
                combobox_sort = ttk.Combobox(subframe_query_entrys, value=["ASC","DESC"])
                entry_criteria = Entry(subframe_query_entrys, width=20)
                entry_criteria_or = Entry(subframe_query_entrys, width=20)
                        
                # Add widgets to screen
                lbl_tbl_name.grid(row=1, column=col_count, pady=10, padx=10)
                lbl_col_name.grid(row=2, column=col_count, pady=10, padx=10)
                combobox_sort.grid(row=3, column=col_count, pady=10, padx=10)
                entry_criteria.grid(row=4, column=col_count, pady=10, padx=10)
                entry_criteria_or.grid(row=5, column=col_count, pady=10, padx=10)


                self.list_query_sort.append(combobox_sort)
                self.list_query_criteria.append(entry_criteria)
                self.list_query_criteria_or.append(entry_criteria_or)

    
                cols.append(self.temp_col_list['col_list_' + self.list_selected_tbl[tbl]][col])

        # CREATE QUERY BUTTON
        btn_create_query = Button(canvas_query_entrys_bottom_right, text="Create", command=lambda:create_query(entry_query_name.get(), col_count, cols))
        btn_create_query.pack(side=BOTTOM, anchor=SE)


    def execute_query(self, db, table, query_name):
        self.window_query_view.destroy()

        print("DB:" + db)
        print("table:" + table)
        print("query name:" + query_name)
        cursor.execute('USE ' + db)
        cursor.execute("SELECT sql_query, cols FROM `" + str(table) + "` WHERE query_name = '" + str(query_name) + "'")
        sql_query = cursor.fetchone()
        print(sql_query[0])

        main.update_query_tab(self, query_name, sql_query[0], sql_query[1])


class main(object):
    def __init__(self, Frame):
        self.Frame = Frame
        self.tab_list = ['','']
        self.main_page()

    def main_page(self):
        self.Frame.geometry("800x528")
        self.Frame.title("Python3-CONNECT")
        # CONNECTION INDICATOR
        self.img_disconnected = PhotoImage(file = "img/neutral.png") 
        self.disconnected_indicaton = Label(self.Frame, image = self.img_disconnected)
        self.disconnected_indicaton.pack(anchor=NE)
        # HEADER TEXT
        self.header = Label(self.Frame, text="Python3-CONNECT", font="Bold 32")
        self.header.pack()
        # CREATE TAB MENU
        self.tab_menu = ttk.Notebook(self.Frame)
        self.tab_menu.pack()
        # CREATE TABS
        self.tab_home = Frame(self.tab_menu, width=800, height=450)
        self.tab_home.grid(row=0, column=0)
        self.tab_home.grid_propagate(0) #frames size stays fixed
        # tab_home.grid_rowconfigure(0,weight=1) #centers vertically
        self.tab_home.grid_columnconfigure(0,weight=1) #centers content horizontally
        # ADD TAB TO A TAB MENU
        self.tab_menu.add(self.tab_home, text="Home")
        # APP DESCRIPTION
        Label(self.tab_home, text='''Easy to use relational database management system.
        
        Designed to make it easy to learn relational databases.
        
        Only the most necessary functions for database management.''', font="16").grid(row=0,column=0, pady=40)
        # LOGIN BUTTON
        self.btn_home_login = Button(self.tab_home, text="Login", command=lambda:self.login())
        self.btn_home_login.grid(row=1, column=0, pady=40)
        
    
    # LOGIN POPUP
    def login(self):
        self.window_login = Toplevel()
        self.window_login.geometry("300x120")
        self.window_login.title("Login")

        # ADD INPUTS FIELDS AND LABELS
        # username entry
        Label(self.window_login,text="Username: ").grid(row=0, column=0, pady=5, padx=5)
        self.input_user_name = Entry(self.window_login, width=25)
        self.input_user_name.grid(row=0,column=1, padx=20)
        # password entry
        Label(self.window_login,text="Password: ").grid(row=1, column=0, pady=5, padx=5)
        self.input_user_psw = Entry(self.window_login, width=25, show="•")
        self.input_user_psw.grid(row=1,column=1, padx=20)
        btn_login = Button(self.window_login, text="Log in", command=lambda:_mysql_.connect_sql(self, str(self.input_user_name.get()), str(self.input_user_psw.get())))
        btn_login.grid(row=2, column=0, columnspan=2, pady=15, padx=10, ipadx=60)        


    def update_home_tab(self, Frame):
        # ADDS BUTTONS, LABELS AND INFORMATION BAR TO A HOME TAB IF CONNECTION IS CREATED
        if connection.is_connected():
            self.btn_home_login.grid_remove() #hides login button
            # ADD BUTTONS AND LABELS
            # add 'connect to a database' button
            self.btn_connect_to_db = Button(self.tab_home, text="Open database", comman=lambda:_database_.connect_db((self)))
            self.btn_connect_to_db.grid(row=1, column=0)
            # add 'OR' label
            self.lbl_or = Label(self.tab_home, text="OR")
            self.lbl_or.grid(row=2, column=0, pady=30)
            # add 'create a database' button
            self.btn_create_db = Button(self.tab_home, text="Create database", command=lambda:_database_.create_db(self))
            self.btn_create_db.grid(row=3, column=0)
            # add 'close connection/logout' button
            self.exit_photo = PhotoImage(file = "img/exit.png") 
            self.btn_disconnect = Button(self.tab_home, image=self.exit_photo, command=lambda:_mysql_.close_connection_sql(self))
            self.btn_disconnect.grid(row=0, column=0, sticky=NE)
            # INFORMATION BAR
            self.info_bar_text = StringVar()
            cursor.execute("SELECT VERSION();")
            self.sql_version = str(cursor.fetchone()).replace("('"," ").replace("',)", " ")
            cursor.execute("SELECT USER();")
            self.current_user = str(cursor.fetchone()).replace("('"," ").replace("',)", " ")

            self.info_bar_text = self.current_user + " | Server version:"+ self.sql_version

            self.info_bar = Label(self.tab_home, text=self.info_bar_text, relief=SUNKEN, anchor=E)
            self.info_bar.grid(row=4, column=0, sticky=EW, pady=80)
        # RESETS HOME TAB IF CONNECTION IS CLOSED
        else:
            self.lbl_or.grid_remove()
            self.btn_create_db.grid_remove()
            self.btn_connect_to_db.grid_remove()
            self.btn_disconnect.grid_remove()
            self.info_bar.grid_remove()
            self.btn_home_login.grid()

    def update_main_frame(self, Frame):
        # REPACKS MAIN FRAME AND ADDS GREEN CIRCLE IF CONNECTION IS CREATED
        if connection.is_connected():
            self.disconnected_indicaton.pack_forget()
            self.tab_menu.pack_forget()
            self.header.pack_forget()
            self.img_connected = PhotoImage(file = "img/green.png") 
            self.connected_indicaton = Label(self.Frame, image = self.img_connected)
            self.connected_indicaton.pack(anchor=NE)
            self.header.pack()
            self.tab_menu.pack()
        # REPACKS MAIN FRAME AND ADDS NEUTRAL CIRCLE IF CONNECTION IS CLOSED
        else:
            self.connected_indicaton.pack_forget()
            self.tab_menu.pack_forget()
            self.header.pack_forget()
            self.img_connected = PhotoImage(file = "img/neutral.png") 
            self.disconnected_indicaton = Label(self.Frame, image = self.img_connected)
            self.disconnected_indicaton.pack(anchor=NE)
            self.header.pack()
            self.tab_menu.pack()
    
    def update_database_tab(self, Frame, selected_db, refresh):
        
        def close_tab(tab_name):
            # self.tab_menu.hide(self.tab_list.index(tab_name))
            # self.tab_list.remove(tab_name)
            self.tab_menu.forget(self.tab_menu.select())

        def update_listbox():
            # self.tbl_listbox.grid_forget()
            self.tbl_listbox.delete(0,'end')
            self.tbl_list = []
            cursor.execute("SHOW TABLES FROM "+ selected_db)

            for (table) in cursor:
                self.tbl_list.append(table[0])
                self.tbl_listbox.insert(END, table[0])



        if refresh == 0:
        
            self.tab_db = Frame(self.tab_menu, width=800, height=450)
            self.tab_db.grid(row=0, column=0)
            self.tab_db.grid_propagate(0) #frames size stays fixed
            # tab_home.grid_rowconfigure(0,weight=1) #centers vertically
            self.tab_db.grid_columnconfigure(0,weight=1) #centers content horizontally
            
            self.tab_menu.add(self.tab_db, text=selected_db)

            self.tbl_listbox = Listbox(self.tab_db)
            self.tbl_list = []
            cursor.execute("SHOW TABLES FROM "+ selected_db)

            self.tab_menu.select(1)

            for (table) in cursor:
                self.tbl_list.append(table[0])
                self.tbl_listbox.insert(END, table[0])



            # BUTTON UPADATE TABLE TAB
            btn_select_tbl = Button(self.tab_db, text="Select table", command=lambda:self.update_table_tab(Frame, selected_db, self.tbl_listbox.get(ANCHOR)))

            # BUTTON RELATION VIEW
            btn_open_realation_view = Button(self.tab_db, text="Relations", command=lambda:_relations_.select_tbl_relation_view(self, selected_db))

            # BUTTON OPEN QUERY VIEW
            btn_open_query_view = Button(self.tab_db, text="Querys", command=lambda:_query_.query_view(self, selected_db))


            # IF DATABASE NOT EMTPY
            if self.tbl_list:
                self.tbl_listbox.grid(row=0, column=0, pady=10, padx=10)
                btn_select_tbl.grid(row=1, column=0, pady=10, padx=10)
                btn_open_realation_view.grid(row=3, column=0, pady=10, padx=10)
                btn_open_query_view.grid(row=4, column=0, pady=10, padx=10)

            else:
                self.tbl_listbox.grid_forget()
                btn_select_tbl.grid_forget()
                btn_open_realation_view.grid_forget()
                btn_open_query_view.grid_forget()
                question_response = messagebox.askyesno(" ", "Database "+ str(selected_db) + " is emty\nCreate new table?")

                if question_response == 1:
                    _table_.create_tbl(self, selected_db)
                else:
                    close_tab(selected_db)
        else:
            update_listbox()
            


        btn_create_tbl = Button(self.tab_db, text="Create table", command=lambda:_table_.create_tbl(self, selected_db))
        btn_create_tbl.grid(row=2, column=0, pady=10, padx=10)

        # CLOSE BUTTON
        Button(self.tab_db, text = "✖", command=lambda:close_tab(selected_db)).grid(row=0, column=2, sticky=N)
    
    def update_table_tab(self, Frame, selected_db, selected_tbl):

        def close_tab(tab_name):
            self.tab_list.remove(tab_name)
            self.tab_menu.forget(self.tab_menu.select())


        def refresh(Frame, fields):
            for widget in Frame.winfo_children():
                widget.delete(*widget.get_children())
           
            cursor.execute("USE `" + selected_db + "`")
            cursor.execute("SELECT * FROM `" + selected_tbl + "`")
            
            table_data = cursor.fetchall()
        

            
            for n in range(len(table_data)):
                for x in range(len(fields)):
                    if isinstance(table_data[n][x], (bytes, bytearray)):
                        # print("bytearray detected: ", table_data[n][x])
                        temp = table_data[n][x].decode('utf8')
                        table_data[n] = list(table_data[n])
                        table_data[n].remove(table_data[n][x])
                        table_data[n].insert(x,temp)    
                        table_data[n] = tuple(table_data[n])
                        # print("bytearray changed: ", table_data[n][x])

                for widget in Frame.winfo_children():
                    widget.insert('', 'end', values=(table_data[n]))
            

        if selected_tbl not in self.tab_list:

            # TAB FRAME
            self.tab_tbl = Frame(self.tab_menu, width=800, height=450)

            # CREATE CANVAS
            canvas_tbl_tab = Canvas(self.tab_tbl)
            # CREATE SUB FRAMES
            sub_frame_bottom = Frame(canvas_tbl_tab)
            self.sub_frame_top = Frame(canvas_tbl_tab)

            # DEFINE TREEVIEW
            table_tree_view = ttk.Treeview(self.sub_frame_top)


            self.tab_tbl.grid(row=0, column=0)
            self.tab_tbl.grid_propagate(0) #frames size stays fixed
            self.tab_tbl.grid_columnconfigure(0,weight=1) #centers content horizontally
            self.tab_menu.add(self.tab_tbl, text=selected_tbl)

            self.tab_list.append(selected_tbl)
            # self.tab_menu.select(2)

            # CLOSE BUTTON
            Button(self.tab_tbl, text = "✖", command=lambda:close_tab(selected_tbl)).pack(side=TOP, anchor=NE)

            # EDIT TABLE NAME BUTTON
            edit_tbl_name_btn = Button(self.tab_tbl, text="Edit table name")
            edit_tbl_name_btn.pack(side=TOP, anchor=NW)


            # ADD CANVAS TO TAB
            canvas_tbl_tab.pack(side=TOP, fill=BOTH, expand=1)

        
            # ADD SUB FRAMES TO CANVAS
            canvas_tbl_tab.create_window((0,0), window=sub_frame_bottom, anchor=N)
            canvas_tbl_tab.create_window((0,0), window=self.sub_frame_top, anchor=S)
            # canvas_tbl_tab.itemconfig(sub_frame_bottom, anchor='N')
            # canvas_tbl_tab.itemconfig(sub_frame_top, anchor='S')
            
        

            # DEFINE SCROLLBAR
            tree_scrollbar_x = ttk.Scrollbar(self.tab_tbl, orient=HORIZONTAL, command=canvas_tbl_tab.xview)

            canvas_tbl_tab.configure(xscrollcommand=tree_scrollbar_x.set)
            canvas_tbl_tab.bind('<Configure>', lambda e: canvas_tbl_tab.configure(scrollregion = canvas_tbl_tab.bbox("all")))


        
            self.field_name_list = []
            cursor.execute("USE `" + selected_db + "`")
            cursor.execute("DESCRIBE `" + selected_tbl + "`")
            for (field_name) in cursor:
                self.field_name_list.append(field_name[0])
                      
            # DEFINE TREEVIEW COLUMNS
            table_tree_view['columns']  = (self.field_name_list)

            table_tree_view.column("#0", width=0)        
            for (field_name) in self.field_name_list:
                table_tree_view.column(field_name, anchor=CENTER, width=150)
                table_tree_view.heading(field_name, text=field_name, anchor=CENTER)

            cursor.execute("SELECT * FROM `" + selected_tbl + "`")
            table_data = cursor.fetchall()
        

            for n in range(len(table_data)):
                for x in range(len(self.field_name_list)):
                    if isinstance(table_data[n][x], (bytes, bytearray)):
                        # print("bytearray detected: ", table_data[n][x])
                        temp = table_data[n][x].decode('utf8')
                        table_data[n] = list(table_data[n])
                        table_data[n].remove(table_data[n][x])
                        table_data[n].insert(x,temp)    
                        table_data[n] = tuple(table_data[n])
                        # print("bytearray changed: ", table_data[n][x])
                table_tree_view.insert(parent='', index='end', values=(table_data[n]))    

            table_tree_view.pack(side=BOTTOM, fill=X)



            # DATA ENTRY DICTIONARY
            data_entry_dir = {}

            # GENERATES ENTRYS FOR INSERT QUERY

            for n in range(len(self.field_name_list)):
                Label(sub_frame_bottom, text = self.field_name_list[n]).grid(row=0, column=n, pady=10, padx=5)
                data_entry_dir[self.field_name_list[n] + "_entry"] =  Entry(sub_frame_bottom, width=19)
                data_entry_dir[self.field_name_list[n] + "_entry"].grid(row=1, column=n, padx=6)
                if n>5:
                    tree_scrollbar_x.pack(side=BOTTOM, fill=X)
            

            # ADD DATA BUTTON
            insert_button = Button(self.tab_tbl, text="Add data")
            insert_button.pack(side=RIGHT)
            

            # INSERT BUTTON
            insert_button = Button(self.tab_tbl, text="INSERT", command=lambda:_table_.insert_data(self, selected_db , selected_tbl, self.field_name_list, data_entry_dir))
            insert_button.pack(side=RIGHT)

            # selected_record =  
            # DELETE BUTTON
            insert_button = Button(self.tab_tbl, text="DELETE", command=lambda:_table_.delete_record(self,table_tree_view.item(table_tree_view.focus())))
            insert_button.pack(side=RIGHT)

            # VIEW TABLE STRUCTURE BUTTON
            tbl_structure_btn = Button(self.tab_tbl, text="Structure")
            tbl_structure_btn.pack(side=RIGHT)


            print("Selected db: ", selected_db)
            print("Selected table: ", selected_tbl)

        else:
            refresh(self.sub_frame_top, self.field_name_list)

    def update_query_tab(self, query_name, sql_query, cols):

        def close_tab(tab_name):
            self.tab_list.remove(tab_name)
            self.tab_menu.forget(self.tab_menu.select())


        self.tab_query = Frame(self.tab_menu, width=800, height=450)
        self.tab_query.grid(row=0, column=0)
        self.tab_query.grid_propagate(0) #frames size stays fixed
        # tab_home.grid_rowconfigure(0,weight=1) #centers vertically
        self.tab_query.grid_columnconfigure(0,weight=1) #centers content horizontally
        
        self.tab_menu.add(self.tab_query, text=query_name)

        self.tab_list.append(query_name)

        # CLOSE BUTTON
        Button(self.tab_query, text = "✖", command=lambda:close_tab(query_name)).pack(side=TOP, anchor=NE)



        list_cols = cols.split(', ')


        # DEFINE TREEVIEW
        query_tree_view = ttk.Treeview(self.tab_query)

        # DEFINE TREEVIEW COLUMNS
        query_tree_view['columns']  = (list_cols)

        query_tree_view.column("#0", width=0)

        for (col) in list_cols:
            query_tree_view.column(col, anchor=CENTER, width=150)
            query_tree_view.heading(col, text=col, anchor=CENTER)


        cursor.execute(str(sql_query))
        table_data = cursor.fetchall()

        for n in range(len(table_data)):
            for x in range(len(list_cols)):
                if isinstance(table_data[n][x], (bytes, bytearray)):
                    # print("bytearray detected: ", table_data[n][x])
                    temp = table_data[n][x].decode('utf8')
                    table_data[n] = list(table_data[n])
                    table_data[n].remove(table_data[n][x])
                    table_data[n].insert(x,temp)    
                    table_data[n] = tuple(table_data[n])
                    # print("bytearray changed: ", table_data[n][x])
            query_tree_view.insert(parent='', index='end', values=(table_data[n]))    

        query_tree_view.pack()
        


# SELECT * FROM `user` WHERE `Grant_priv` = 'N' AND `User` = 'mysql.sys'
# CHECK if privileges granted.

# mysql -u `testuser`@`ļocalhost` -p test123

after_id = None

def session_end():
    messagebox.showinfo("" ,"Session expired")

def reset_timer(event=None):
    global after_id
    if after_id is not None:
        root.after_cancel(after_id)
    after_id = root.after(180000, session_end)

root = Tk()
reset_timer()
root.bind_all("<Any-KeyPress>", reset_timer)
root.bind_all("<Any-ButtonPress>", reset_timer)
screen = main(root) 
root.mainloop()
