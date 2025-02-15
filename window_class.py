import init
from init import general_settings, specifications_list, specifications_num, units_per_session
from unit_class import UnitGenerator
from methods import sex_to_str, format_few_worded_text

class Window:
    def __init__(self, window_size: tuple, title: str, icon_path: str):
        self.__root = init.Tk()
        self.__root.geometry(f"{window_size[0]}x{window_size[1]}")
        self.__root.resizable(False, False)
        self.__root.title(title)
        self.__root.iconbitmap(icon_path)

        self.__menu = self.new_menu()
        self.__root.config(menu=self.__menu)
        self._frame = self.new_frame()
        self._frame.pack(expand=True)

    def start(self):
        self.__root.mainloop()
    
    def set_title(self, new_title: str):
        self.__root.title(new_title)

    def new_menu(self):
        menu_main = init.Menu()

        menu_program = init.Menu(tearoff=0)
        menu_program.add_command(label="Restart", command=self.restart)
        menu_program.add_command(label="Clear DB", command=self.clear_db)
        menu_program.add_command(label="Settings", command=self.settings)
        menu_program.add_separator()
        menu_program.add_command(label="Exit", command=self.exit)

        menu_main.add_cascade(label="Program", menu=menu_program)
        menu_main.add_cascade(label="Help", command=self.help)
        
        return menu_main

    def new_frame(self):
        return init.Frame(
            self.__root,
            padx=8,
            pady=8
        )

    def new_label(self, text: str):
        return init.Label(
            self._frame,
            text=text,
            font=(general_settings['font_main'], 12)
        )
    
    def new_button(self, text: str, command: object):
        return init.Button(
            self._frame,
            text=text,
            font=(general_settings['font_main'], 12),
            command=command
        )
    
    def object_text_update(self, object: object, new_text: str):
        object.config(text=new_text)

    def exit(self):
        self.__root.destroy()

    def help(self):
        init.messagebox.showinfo("Help", "Help text")
    
    def settings(self):
        pass

    def restart(self):
        pass

    def clear_db(self):
        pass

class WindowUnit(Window):
    def __init__(self, window_size, title, icon_path, db_connection: object):
        super().__init__(window_size, title, icon_path)
        self.__db_connection = db_connection

        self.__specifications_names_label_list = []
        self.__specifications_values_label_list = []
        
        self.__unit = None
        self.__units_avaliable = units_per_session['avaliable']
        self.__units_selected = 0

    def template(self):
        self.__label_name = self.new_label(text="Name")
        self.__label_age = self.new_label(text="Age")
        self.__label_sex = self.new_label(text="Sex")
        self.__label_sum = self.new_label(text="Sum")

        self.__specifications_names_label_list.append(self.__label_name)
        self.__specifications_names_label_list.append(self.__label_age)
        self.__specifications_names_label_list.append(self.__label_sex)

        for i, label in enumerate(self.__specifications_names_label_list):
            label.grid(row=i, column=0)
        self.__label_sum.grid(row=specifications_num, column=1)

        # wip
        for i, key in enumerate(specifications_list):
            self.new_label(text=format_few_worded_text(key.capitalize())).grid(row=i, column=1)
            self.__specifications_values_label_list.append(self.new_label(text=0))
        self.new_label(text=0).grid(row=specifications_num, column=2)

        for i, label in enumerate(self.__specifications_values_label_list):
            label.grid(row=i, column=2)

        self.new_button(text="Next", command=self.next_unit).grid(row=specifications_num+1, column=2)
        self.new_button(text="Select", command=self.select_unit).grid(row=specifications_num+1, column=0)
        
    # wip
    def set_unit(self, unit: object):
        self.__unit = unit

        self.object_text_update(object=self.__label_name, new_text=self.__unit.get_name())
        self.object_text_update(object=self.__label_age, new_text=f"{self.__unit.get_age()} y.o.")
        self.object_text_update(object=self.__label_sex, new_text=sex_to_str(sex=self.__unit.get_sex()).capitalize())

        for i, key in enumerate(self.__unit.get_specifications()):
            self.new_label(text=str(self.__unit.get_specifications()[key])).grid(row=i, column=2)
        
        self.new_label(text=self.__unit.get_specifications_sum()).grid(row=specifications_num, column=2)

    def next_unit(self):
        if self.__units_avaliable > 0:
            self.__units_avaliable -= 1
            self.set_unit(unit=UnitGenerator().new_unit())
        else:
            print(f"units_avaliable: {self.__units_avaliable}")

    def select_unit(self):
        if self.__unit != None and self.__units_selected < units_per_session['may_be_selected']:
            self.__units_selected += 1
            self.set_unit_to_db(self.__unit)
            print(f"{self.__units_selected}. {self.__unit.get_name()} ({self.__unit.get_specifications_sum()}) was selected")
            self.next_unit()

    def set_unit_to_db(self, unit: object):
        self.__db_connection.write_unit(unit=unit)

    def clear_db(self):
        self.__db_connection.clear_tables()
        print("Database cleared successfully")
    
    # wip
    def restart(self):
        self.__units_selected = 0
        self.__units_avaliable = units_per_session['avaliable']
