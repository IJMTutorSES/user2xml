import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class UpdateFrame:
    def __init__(self, master):
        self.master = master

        self.lbls = {}
        self.lbls["login"] = ttk.Label(master, text="Benutzername:", anchor="w")
        self.lbls["login"].grid(column=0, row=0, sticky="w")
        self.lbls["courses"] = ttk.Label(master, text="Kursauswahl:", anchor="w")
        self.lbls["courses"].grid(column=0, row=1, sticky="w")
        self.lbls["edate"] = ttk.Label(master, text="Enddatum:", anchor="w")
        self.lbls["edate"].grid(column=0, row=2, sticky="w")

        self.etrs = {}
        self.etrs["login"] = ttk.Entry(master, width=20)

        self.etrs["courses"] = ttk.Combobox(
            master,
            width=17,
            values=["Mathematik", "Sprachen", "Beide", "Andere", "Propädeutikum"],
        )
        self.etrs["courses"].bind("<<ComboboxSelected>>", self.list_select)
        self.etrs["courses"].insert(tk.END, "Mathematik")
        self.etrs["math"] = tk.Listbox(
            master, selectmode="multiple", exportselectio=0, width=20, height=6
        )
        self.etrs["math"].insert(
            tk.END,
            "Klasse 4+5",
            "Klasse 6+7",
            "Klasse 8+9",
            "Klasse 10+11",
            "Analysis (Abitur)",
            "Algebra (Abitur)",
        )
        self.etrs["lang"] = tk.Listbox(
            master, selectmode="multiple", exportselection=0, width=20, height=6
        )
        self.etrs["lang"].insert(
            tk.END,
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
        self.etrs["stip"] = tk.Listbox(
            master, selectmode="multiple", exportselection=0, height=6, width=20
        )
        self.etrs["stip"].insert(
            tk.END,
            "Robotik Smarttech",
            "Robotik und Coding",
            "Technik und Statik",
        )
        self.etrs["prop"] = tk.Listbox(
            master, selectmode="multiple", exportselection=0, height=6, width=20
        )
        self.etrs["prop"].insert(
            tk.END,
            "Physik",
            "Chemie",
            "Biologie",
            "Human-Medizin",
            "Finanzwesen",
            "BWL",
            "Volkswirtschaft",
        )

        self.etrs["edate"] = ttk.Entry(
            master,
            width=20,
        )

        i = 0
        for _, val in self.etrs.items():
            val.grid(row=i, column=1, sticky="w")
            i += 1

        self.list_select()

    def clear_selection(self):
        for i in self.etrs["math"].curselection():
            self.etrs["math"].selection_clear(i)
        for i in self.etrs["lang"].curselection():
            self.etrs["lang"].selection_clear(i)
        for i in self.etrs["stip"].curselection():
            self.etrs["stip"].selection_clear(i)
        for i in self.etrs["prop"].curselection():
            self.etrs["prop"].selection_clear(i)

    def list_select(self, *args, **kwargs):
        value = self.etrs["courses"].get()
        width = 230
        height = 280
        self.hide_all()
        if value == "Sprachen":
            self.etrs["lang"].grid(row=5, column=1, sticky="w")
        elif value == "Mathematik":
            self.etrs["math"].grid(row=5, column=1, sticky="w")
        elif value == "Beide":
            self.etrs["edate"].grid_forget()
            self.lbls["edate"].grid_forget()
            self.etrs["math"].grid(row=5, column=1, sticky="w")
            self.etrs["lang"].grid(row=6, column=1, sticky="w")
            self.etrs["edate"].grid(row=8, column=1, sticky="w")
            self.lbls["edate"].grid(row=8, column=0, sticky="w")
            height = 380
        elif value == "Andere":
            self.etrs["stip"].grid(row=5, column=1, sticky="w")
        elif value == "Propädeutikum":
            self.etrs["prop"].grid(row=5, column=1, sticky="w")
        self.clear_selection()
        self.master.geometry(f"{width}x{height}")

    def hide_all(self):
        self.etrs["math"].grid_forget()
        self.etrs["lang"].grid_forget()
        self.etrs["stip"].grid_forget()
        self.etrs["prop"].grid_forget()
        self.etrs["edate"].grid_forget()
        self.lbls["edate"].grid_forget()
        self.etrs["edate"].grid(row=7, column=1, sticky="w")
        self.lbls["edate"].grid(row=7, column=0, sticky="w")

    def listbox_select(self, *args, **kwargs):
        if len(sel := self.etrs["lang"].curselection()) > 2:
            for i in set(sel) ^ set(self.lang_selection):
                self.etrs["lang"].selection_clear(i)
            messagebox.showwarning(
                "Sprachenauswahl",
                message="Es dürfen nur zwei Sprachen ausgewählt werden.",
            )
        self.lang_selection = self.etrs["lang"].curselection()


class window2:
    def __init__(self, master1):
        self.panel2 = tk.Frame(master1)
        self.panel2.grid()
        self.button2 = tk.Button(self.panel2, text="Quit", command=self.panel2.quit)
        self.button2.grid()
        vcmd = (master1.register(self.validate), "%d", "%i", "%P", "%S", "%W")
        self.text1 = tk.Entry(self.panel2, validate="key", validatecommand=vcmd)
        self.text1.grid()
        self.text1.focus()
        self.text2 = tk.Entry(self.panel2, validate="key", validatecommand=vcmd)
        self.text2.grid()
        self.text2.focus()

    def validate(self, action, index, new_text, change, widget):
        print(action, index, new_text, change, widget)
        if action == "1":
            if change in "0123456789":
                if index == "4" or index == "7":
                    self.text1.insert(tk.END, "-" + change)
                    self.panel2.after_idle(lambda: self.text1.config(validate="key"))
                    return None
                elif index == "10":
                    return False
            else:
                return False
        elif action == "0":
            if index == "8" or index == "5":
                self.text1.delete(str(int(index) - 1), tk.END)
                self.panel2.after_idle(lambda: self.text1.config(validate="key"))
                return None
        return True


root1 = tk.Tk()
UpdateFrame(root1)
root1.mainloop()
