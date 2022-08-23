import random
from tkinter import (
    Tk,
    Entry,
    Label,
    Listbox,
    END,
    messagebox,
    Button,
    CENTER,
    simpledialog,
    filedialog
)
from tkinter.ttk import Combobox
from datetime import date
import os.path
from export import export, validate, end_file
from data_reader import Data, last_file
import sys

class DataDialog(simpledialog.Dialog):
    def __init__(self, master, rlist, file):
        self.rlist = rlist
        self.file = file
        self.data_file = ""
        super().__init__(master)
    
    def body(self, master):
        l1 = Label(master, text="Kurse konnten nicht gefunden werden. Bitte wähle eine gültige Kurs-Datei.")
        l1.grid(row=0)
        self.l2 = Label(master, text="Datei: ")
        b = Button(master, text="Öffnen", command=self.get_file)
        self.l2.grid(row=1)
        b.grid(row=2)
        return b

    def apply(self):
        self.rlist.append(self.data_file)
    
    def get_file(self):
        self.data_file = filedialog.askopenfilename(title="Öffne Kurs-Datei", initialdir=os.path.dirname(self.file), filetypes=(("Kurs-Datei", ".courses"),),)
        self.l2["text"] = "Datei: " + self.data_file

class ExportDialog(simpledialog.Dialog):
    def __init__(self, master, rlist, courses):
        self.rlist = rlist
        self.courses = courses
        super().__init__(master)

    def body(self, master):

        l1 = Label(master, text="Benutzername:", anchor="w")
        l2 = Label(master, text="Passwort:", anchor="w")
        l3 = Label(master, text="Kursauswahl:")
        l4 = Label(master, text=self.courses)

        l1.grid(row=0)
        l2.grid(row=1)

        self.e1 = Entry(master)
        self.e2 = Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)

        l3.grid(row=3)
        l4.grid(row=3, column=1)
        return self.e1

    def apply(self):
        first = self.e1.get()
        second = self.e2.get()
        self.rlist.extend([first, second])


class App:
    def __init__(self, root):
        self.session = (
            str(date.today()).replace("-", "") + "_" + str(random.randint(100, 999))
        )
        file = last_file()
        if not Data.load_data(file):
            datafile = []
            DataDialog(root, datafile, file)
            if not datafile or not Data.load_data(datafile[0]):
                messagebox.showerror(title="Fehler - Kurs-Datei", message=f"Es wurde keine oder eine falsche Kurs-Datei geladen. {datafile}")
                root.quit()
                sys.exit()
        self.root = root
        self.root.title("user2xml")
        self.root.geometry("300x500")
        self.root.protocol("WM_DELETE_WINDOW", self.end_session)

        self.lbls = {}
        self.lbls["fname"] = Label(root, text="Vorname:", anchor="w")
        self.lbls["fname"].grid(row=0, column=0, sticky="w")
        self.lbls["lname"] = Label(root, text="Nachname:", anchor="w")
        self.lbls["lname"].grid(row=1, column=0, sticky="w")
        self.lbls["email"] = Label(root, text="E-Mail:", anchor="w")
        self.lbls["email"].grid(row=2, column=0, sticky="w")
        self.lbls["gender"] = Label(root, text="Anrede:", anchor="w")
        self.lbls["gender"].grid(row=3, column=0, sticky="w")
        self.lbls["courses"] = Label(root, text="Kursauswahl:", anchor="w")
        self.lbls["courses"].grid(row=4, column=0, sticky="w")
        self.lbls["sdate"] = Label(root, text="Startdatum:", anchor="w")
        self.lbls["sdate"].grid(row=6, column=0, sticky="w")
        self.lbls["edate"] = Label(root, text="Enddatum:", anchor="w")
        self.lbls["edate"].grid(row=7, column=0, sticky="w")

        self.etrs = {}
        self.etrs["fname"] = Entry(root, width=20)
        self.etrs["fname"].grid(row=0, column=1)
        self.etrs["lname"] = Entry(root, width=20)
        self.etrs["lname"].grid(row=1, column=1)
        self.etrs["email"] = Entry(root, width=20)
        self.etrs["email"].grid(row=2, column=1)
        self.etrs["gender"] = Combobox(
            root, width=17, values=["Herr", "Frau", "Keine Angabe"]
        )
        self.etrs["gender"].insert(END, "Herr")
        self.etrs["gender"].grid(row=3, column=1)
        self.etrs["courses"] = Combobox(
            root,
            width=17,
            values=Data.CATEGORIES,
        )
        self.etrs["courses"].bind("<<ComboboxSelected>>", self.list_select)
        self.etrs["courses"].insert(END, Data.CATEGORIES[0])
        self.etrs["courses"].grid(row=4, column=1)
        for cat in Data.CATEGORIES:
            self.etrs[cat] = Listbox(
                root, selectmode="multiple", exportselection=0, height=6, width=20
            )
            self.etrs[cat].insert(
                END,
                *Data.COURSES[cat]
            )
        vcmd = (root.register(self.validate), "%d", "%i", "%P", "%S", "%W")
        self.etrs["sdate"] = Entry(root, width=20, validate="key", validatecommand=vcmd)
        self.etrs["sdate"].insert(END, "-".join(str(date.today()).split("-")[::-1]))
        self.etrs["sdate"].grid(row=6, column=1)
        self.etrs["edate"] = Entry(root, width=20, validate="key", validatecommand=vcmd)
        self.etrs["edate"].grid(row=7, column=1)
            

        self.btn = Button(
            root,
            text="XML-Datei erstellen",
            command=self.export,
        )

        self.list_select(None)

        self.root.mainloop()

    def list_select(self, a):
        value = self.etrs["courses"].get()
        self.hide_all()
        self.etrs[value].grid(row=5, column=1, sticky="w")
        self.root.geometry(f"205x280")
        self.btn.place(relx=0.5, y=265, anchor=CENTER)

    def hide_all(self):
        for cat in Data.CATEGORIES:
            self.etrs[cat].grid_forget()

    def export(self):
        vals = {}
        for k, val in self.etrs.items():
            try:
                vals[k] = val.get()
            except TypeError:
                vals[k] = [val.get(i) for i in val.curselection()]
            except AttributeError:
                continue
        if isinstance(prop := validate(vals), tuple):
            login = []
            ExportDialog(self.root, login, "\n".join(("\n".join(self.etrs[cat].get(i) for i in self.etrs[cat].curselection()) for cat in Data.CATEGORIES if self.etrs[cat].curselection())))
            if login and len(login[0]) > 3 and len(login[1]) > 3:
                export(vals, prop, login, self.session)
                messagebox.showinfo(
                    "Info", message=f"XML-Datei wurde erstellt. ({self.session})"
                )
                for etr in [
                    self.etrs["fname"],
                    self.etrs["lname"],
                    self.etrs["email"],
                    self.etrs["gender"],
                    self.etrs["courses"],
                    self.etrs["sdate"],
                    self.etrs["edate"],
                ]:
                    etr.delete(0, END)
                self.clear_selection()
                self.etrs["courses"].insert(END, "Mathematik")
                self.etrs["sdate"].insert(END, str(date.today()))
                self.etrs["gender"].insert(END, "Herr")
                self.btn = Button(
                    self.root,
                    text="Zu XML-Datei hinzufügen",
                    command=self.export,
                )
                self.list_select(None)
        else:
            messagebox.showerror(
                f"Fehler - {prop}",
                message="XML-Dateien konnten nicht erstellt werden. Bitte überprüfen Sie Ihre Eingaben.\n\n"
                + "Bitte überprüfen Sie auch, ob sie in einem Feld ungewollte Leerzeichen eingegeben haben.",
            )

    def clear_selection(self):
        for cat in Data.CATEGORIES:
            for i in self.etrs[cat].curselection():
                self.etrs[cat].selection_clear(i)

    def validate(self, action, index, new_text, change, widget):
        WIDGET = {".!entry4": "sdate", ".!entry5": "edate"}
        if len(change) == 1:
            if action == "1":
                if change in "0123456789":
                    if index == "2" or index == "5":
                        self.etrs[WIDGET[widget]].insert(END, "-" + change)
                        self.root.after_idle(
                            lambda: self.etrs[WIDGET[widget]].config(validate="key")
                        )
                        return None
                    elif index == "10":
                        return False
                else:
                    return False
            elif action == "0":
                if index == "3" or index == "6":
                    self.etrs[WIDGET[widget]].delete(str(int(index) - 1), END)
                    self.root.after_idle(
                        lambda: self.etrs[WIDGET[widget]].config(validate="key")
                    )
                    return None
        return True

    def end_session(self):
        end_file(self.session)
        self.root.destroy()


root = Tk()
a = App(root)
