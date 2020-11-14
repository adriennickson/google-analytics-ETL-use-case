from tkinter import *
from StartPage import StartPage
from FinalPage import FinalPage
from PageTwo import PageTwo
from MainMenu import MainMenu


class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.minsize(1320, 600)
        self.title("website - GoogleAnalysis")

        self.viewID = None
        self.filePath = None

        # Setup Menu
        MainMenu(self)

        # Setup Frame
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = []

        for F in (StartPage, FinalPage, PageTwo):
            frame = F(container, self)
            self.frames.append(frame)
            frame.grid(row=0, column=0, sticky="nsew")

        # Center the window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x_cordinate = int((screen_width / 2) - (1320 / 2))
        y_cordinate = int((screen_height / 2) - (600 / 2))

        self.geometry("{}x{}+{}+{}".format(1320, 600, x_cordinate, y_cordinate))

        self.show_frame(0)

    def show_frame(self, context):
        frame = self.frames[context]
        frame.tkraise()

    def updateGoogleAnalyticsValues(self, filePath, viewID):
        self.filePath = filePath
        self.viewID = viewID
        self.frames[1].updateView(filePath, viewID)

app = App()
app.mainloop()
