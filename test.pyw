import tkinter as tk


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
window2(root1)
root1.mainloop()
