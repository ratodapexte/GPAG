import tkinter as tk
import cliente

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Conectar ao servidor\n(click me)"
        self.hi_there["command"] = cliente.connect_to_server
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

        self.disconect = tk.Button(self)
        self.disconect["text"] = "Desconectar do servidor" 
        self.hi_there["command"] = cliente.close



    def say_hi(self):
        print("hi there, everyone!")

        


root = tk.Tk()
app = Application(master=root)
app.mainloop()