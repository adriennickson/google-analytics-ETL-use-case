from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from FinalPage import FinalPage
from PageTwo import PageTwo

from tkinter import Tk, RIGHT, BOTH, RAISED
from tkinter.ttk import Frame, Button, Style
from googleAnalyticsTools.GAExplorer import GAExplorer

class StartPage(Frame):

	def __init__(self, parent, controller):
		Frame.__init__(self, parent)

		self.controller = controller
		self.fileName = None


		self.style = Style()
		self.style.theme_use("default")

		# Browse json file
		self.frameFileBrowser = Frame(self)
		self.frameFileBrowser.pack(fill=X)

		lblFileBrowser = Label(self.frameFileBrowser, text="Please upload the credential json file", width=35, anchor="w")
		lblFileBrowser.pack(side=LEFT, padx=5, pady=5)

		self.buttonFileBrowser = ttk.Button(self.frameFileBrowser, text = "Browse A File", command = self.fileDialog )
		self.buttonFileBrowser.pack(fill=X, padx=5, pady=5, side=LEFT)

		self.fileNameLabel = Label(self.frameFileBrowser, text=self.fileName, width=35, anchor="w")
		self.fileNameLabel.pack(fill=X, padx=5, pady=5)

		# google analytics view ID
		frameViewID = Frame(self)
		frameViewID.pack(fill=X)

		lblViewID = Label(frameViewID, text="Please enter the google analytics view ID", width=35, anchor="w")
		lblViewID.pack(side=LEFT, padx=5, pady=5)

		self.entryViewID = Entry(frameViewID)
		self.entryViewID.pack(fill=X, padx=5, expand=True)

		# Test access
		self.frameTestAccess = Frame(self)
		self.frameTestAccess.pack(fill=X)

		self.buttonTestAccess = ttk.Button(self.frameTestAccess, text = "Test API", command = self.testApiAcess )
		self.buttonTestAccess.pack(fill=X, padx=(300, 5), pady=5, side=LEFT)

		# Show test result
		self.frameTestResult = Frame(self)
		self.frameTestResult.pack(fill=X)

		self.lblTestResult = Label(self.frameTestResult, text="", width=35, anchor="w")
		self.lblTestResult.pack(side=LEFT, padx=(300, 5), pady=5)

		# footer
		frame = Frame(self, relief=RAISED, borderwidth=1)
		frame.pack(expand=True)

		self.pack(fill=BOTH)

		closeButton = Button(self, text="Close", command=parent.quit)
		closeButton.pack(side=RIGHT, padx=5, pady=5)
		self.nextButton = Button(self, text="Next", command=lambda:controller.show_frame(1), state=DISABLED)
		self.nextButton.pack(side=RIGHT)




	def fileDialog(self):
		self.fileName = filedialog.askopenfilename(title = "Select A File", filetypes = [("json", "*.json"), ("All Files", "*.*")] )
		self.fileNameLabel.pack_forget()
		self.fileNameLabel = Label(self.frameFileBrowser, text=self.fileName, width=35, anchor="w")
		self.fileNameLabel.pack(fill=X, padx=5, pady=5)

	def testApiAcess(self):
		if self.fileName is None:
			self.lblTestResult.pack_forget()
			self.lblTestResult = Label(self.frameTestResult, text="No file Selected.\n Please selet the json file", width=35, anchor="w")
			self.lblTestResult.pack(side=LEFT, fill=X, padx=(300, 5), pady=5)
			self.nextButton['state'] = DISABLED

		elif not self.entryViewID.get():
			self.lblTestResult.pack_forget()
			self.lblTestResult = Label(self.frameTestResult, text="View ID is not set.\n Please set je view ID", width=35, anchor="w")
			self.lblTestResult.pack(side=LEFT, fill=X, padx=(300, 5), pady=5)
			self.nextButton['state'] = DISABLED

		else:
			googleAnalytics = GAExplorer(self.fileName, self.entryViewID.get())

			try:
				texte = googleAnalytics.test_connection()
				self.lblTestResult.pack_forget()
				self.lblTestResult = Label(self.frameTestResult, text='Everything is okay! You Can continnue!', anchor="w", fg='green', relief='groove', wraplength=300)
				self.lblTestResult.pack(side=LEFT, fill=X, padx=(300, 5), pady=5, expand=True)
				self.nextButton['state'] = NORMAL
				self.controller.updateGoogleAnalyticsValues(self.fileName, self.entryViewID.get())

			except Exception as err:
				self.lblTestResult.pack_forget()
				self.lblTestResult = Label(self.frameTestResult, text="Error: {0}".format(err), anchor="w", fg='red', relief='groove', wraplength=300)
				self.lblTestResult.pack(side=LEFT, fill=X, padx=(300, 5), pady=5, expand=True)
				self.nextButton['state'] = DISABLED

			