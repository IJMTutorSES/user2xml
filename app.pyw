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
)
from tkinter.ttk import Combobox
from datetime import date
from export import export, validate, end_file


class MyDialog(simpledialog.Dialog):
    def __init__(self, master, rlist):
        self.rlist = rlist
        super().__init__(master)

    def body(self, master):

        l1 = Label(master, text="Benutzername:", anchor="w")
        l2 = Label(master, text="Passwort:", anchor="w")

        l1.grid(row=0)
        l2.grid(row=1)

        self.e1 = Entry(master)
        self.e2 = Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)

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
        self.etrs["lname"] = Entry(root, width=20)
        self.etrs["email"] = Entry(root, width=20)
        self.etrs["gender"] = Combobox(
            root, width=17, values=["Herr", "Frau", "Keine Angabe"]
        )
        self.etrs["gender"].insert(END, "Herr")
        self.etrs["courses"] = Combobox(
            root,
            width=17,
            values=["Mathematik", "Sprachen", "Beide", "Andere", "Propädeutikum"],
        )
        self.etrs["courses"].bind("<<ComboboxSelected>>", self.list_select)
        self.etrs["courses"].insert(END, "Mathematik")
        self.etrs["math"] = Listbox(
            root, selectmode="multiple", exportselectio=0, width=20, height=6
        )
        self.etrs["math"].insert(
            END,
            "Klasse 4+5",
            "Klasse 6+7",
            "Klasse 8+9",
            "Klasse 10+11",
            "Analysis (Abitur)",
            "Algebra (Abitur)",
        )
        self.etrs["lang"] = Listbox(
            root, selectmode="multiple", exportselection=0, width=20, height=6
        )
        self.etrs["lang"].insert(
            END,
            "Japanisch",
            "Arabisch",
            "Chinesisch",
            "Deutsch",
            "Englisch (AE)",
            "Englisch (BE)",
            "Französisch",
            "Griechisch",
            "Hebräisch",
            "Hindi",
            "Irisch",
            "Italiensich",
            "Koreanisch",
            "Latein",
            "Niederländisch",
            "Persisch",
            "Philippinisch",
            "Polnisch",
            "Portugiesisch",
            "Russisch",
            "Schwedisch",
            "Spanisch (Lateinamerika)",
            "Spanisch (Spanien)",
            "Türkisch",
            "Vietnamesisch",
        )
        self.etrs["lang"].bind("<<ListboxSelect>>", self.listbox_select)
        self.lang_selection = self.etrs["lang"].curselection()
        self.etrs["stip"] = Listbox(
            root, selectmode="multiple", exportselection=0, height=6, width=20
        )
        self.etrs["stip"].insert(
            END,
            "Robotik Smarttech",
            "Robotik und Coding",
            "Technik und Statik",
        )
        self.etrs["prop"] = Listbox(
            root, selectmode="multiple", exportselection=0, height=6, width=20
        )
        self.etrs["prop"].insert(
            END,
            "Physik",
            "Chemie",
            "Biologie",
            "Human-Medizin",
            "Finanzwesen",
            "BWL",
            "Volkswirtschaft",
        )
        self.etrs["sdate"] = Entry(root, width=20)
        self.etrs["sdate"].insert(END, str(date.today()))
        self.etrs["edate"] = Entry(root, width=20)

        i = 0
        for _, val in self.etrs.items():
            val.grid(row=i, column=1, sticky="w")
            i += 1

        self.btn = Button(
            root,
            text="XML-Datei erstellen",
            command=self.export,
        )

        self.list_select(None)

        self.root.mainloop()

    def listbox_select(self, a):
        if len(sel := self.etrs["lang"].curselection()) > 2:
            for i in set(sel) ^ set(self.lang_selection):
                self.etrs["lang"].selection_clear(i)
            messagebox.showwarning(
                "Sprachenauswahl",
                message="Es dürfen nur zwei Sprachen ausgewählt werden.",
            )
        self.lang_selection = self.etrs["lang"].curselection()

    def list_select(self, a):
        value = self.etrs["courses"].get()
        width = 205
        height = 280
        self.hide_all()
        if value == "Sprachen":
            self.etrs["lang"].grid(row=5, column=1, sticky="w")
        elif value == "Mathematik":
            self.etrs["math"].grid(row=5, column=1, sticky="w")
        elif value == "Beide":
            self.etrs["sdate"].grid_forget()
            self.etrs["edate"].grid_forget()
            self.lbls["sdate"].grid_forget()
            self.lbls["edate"].grid_forget()
            self.etrs["math"].grid(row=5, column=1, sticky="w")
            self.etrs["lang"].grid(row=6, column=1, sticky="w")
            self.etrs["sdate"].grid(row=7, column=1, sticky="w")
            self.etrs["edate"].grid(row=8, column=1, sticky="w")
            self.lbls["sdate"].grid(row=7, column=0, sticky="w")
            self.lbls["edate"].grid(row=8, column=0, sticky="w")
            height = 380
        elif value == "Andere":
            self.etrs["stip"].grid(row=5, column=1, sticky="w")
        elif value == "Propädeutikum":
            self.etrs["prop"].grid(row=5, column=1, sticky="w")
        self.clear_selection()
        self.root.geometry(f"{width}x{height}")
        self.btn.place(relx=0.5, y=height - 15, anchor=CENTER)

    def hide_all(self):
        self.etrs["math"].grid_forget()
        self.etrs["lang"].grid_forget()
        self.etrs["stip"].grid_forget()
        self.etrs["prop"].grid_forget()
        self.etrs["sdate"].grid_forget()
        self.etrs["edate"].grid_forget()
        self.lbls["sdate"].grid_forget()
        self.lbls["edate"].grid_forget()
        self.etrs["sdate"].grid(row=6, column=1, sticky="w")
        self.etrs["edate"].grid(row=7, column=1, sticky="w")
        self.lbls["sdate"].grid(row=6, column=0, sticky="w")
        self.lbls["edate"].grid(row=7, column=0, sticky="w")

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
            MyDialog(self.root, login)
            if len(login[0]) > 3 and len(login[1]) > 3:
                export(vals, prop, login, self.session)
                messagebox.showinfo(
                    "Info", message=f"XML-Datei wurde erstellt. ({self.session})"
                )
                for etr in [
                    self.etrs["fname"],
                    self.etrs["lname"],
                    self.etrs["email"],
                    self.etrs["courses"],
                    self.etrs["sdate"],
                    self.etrs["edate"],
                ]:
                    etr.delete(0, END)
                self.clear_selection()
                self.etrs["courses"].insert(END, "Mathematik")
                self.etrs["sdate"].insert(END, str(date.today()))
                self.list_select(None)
        else:
            messagebox.showerror(
                f"Fehler - {prop}",
                message="XML-Dateien konnten nicht erstellt werden. Bitte überprüfen Sie Ihre Eingaben.\n\n"
                + "Daten: im Format YYYY-MM-DD\n\n"
                + "Bitte überprüfen Sie auch, ob sie in einem Feld ungewollte Leerzeichen eingegeben haben.",
            )

    def clear_selection(self):
        for i in self.etrs["math"].curselection():
            self.etrs["math"].selection_clear(i)
        for i in self.etrs["lang"].curselection():
            self.etrs["lang"].selection_clear(i)
        for i in self.etrs["stip"].curselection():
            self.etrs["stip"].selection_clear(i)
        for i in self.etrs["prop"].curselection():
            self.etrs["prop"].selection_clear(i)

    def end_session(self):
        end_file(self.session)
        self.root.destroy()


root = Tk()
a = App(root)
