from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from googleAnalyticsTools.GAExplorer import GAExplorer

class FinalPage(Frame):

	def __init__(self, parent, controller):
		Frame.__init__(self, parent, padx=0, pady=0)

		self.controller = controller

		self.container = Frame(self, bg='white', relief=RAISED, borderwidth=1)
		self.container.pack(expand=1, fill=BOTH)

		# footer
		self.footer = Frame(self)
		self.footer.pack(expand=True)

		self.closeButton = Button(self, text="Close", command=parent.quit)
		self.closeButton.pack(side=RIGHT, padx=5, pady=5)
		self.nextButton = Button(self, text="Back", command=lambda:controller.show_frame(0))
		self.nextButton.pack(side=RIGHT)

	def reloadFooter(self):
		self.footer.pack_forget()
		self.footer.pack(expand=True)
		self.closeButton.pack_forget()
		self.closeButton.pack(side=RIGHT, padx=5, pady=5)
		self.nextButton.pack_forget()
		self.nextButton.pack(side=RIGHT)

	def matplotCanvasDays(self, data):

		dataToPlot = []
		xAxis = []
		legend = []

		for x in data:
			xAxis.append(x.date().strftime("%d/%m/%y\n(%A)"))
			tmpList = []
			for y in data[x]:
				tmpList.append(int(data[x][y]))
				if y not in legend:
					legend.append(y)
			dataToPlot.append(tuple(tmpList))

		frame = Frame(self.container)
		frame.grid(row=1, columnspan=2, rowspan=2, pady=10, padx=10)

		f = Figure(dpi=100)
		a = f.add_subplot(111)
		for temp in zip(*dataToPlot):
			a.plot(xAxis, list(temp))
		a.legend(list(legend), loc='lower right', fontsize='xx-small', bbox_to_anchor=(0.5, 0., 0.5, 0.5))
		f.subplots_adjust(bottom=0.19)

		for tick in a.get_xticklabels():
			tick.set_rotation(20)

		canvas = FigureCanvasTkAgg(f, frame)
		canvas.get_tk_widget().pack(pady=10)

		# toolbar = NavigationToolbar2Tk(canvas, frame)
		# canvas._tkcanvas.pack()
		return

	def matplotCanvasHours(self, data):

		dataToPlot = []
		xAxis = []
		legend = []

		for x in data:
			xAxis.append("{}h".format(x))
			tmpList = []
			for y in data[x]:
				tmpList.append(int(data[x][y]))
				if y not in legend:
					legend.append(y)
			dataToPlot.append(tuple(tmpList))

		frame = Frame(self.container)
		frame.grid(row=1, column=3, columnspan=2, rowspan=2, pady=10, padx=10)

		f = Figure(dpi=100)
		a = f.add_subplot(111)
		for temp in zip(*dataToPlot):
			a.plot(xAxis, list(temp))
		a.legend(list(legend), loc='lower right', fontsize='xx-small', bbox_to_anchor=(0.5, 0., 0.5, 0.5))
		for tick in a.get_xticklabels():
			tick.set_rotation(45)

		canvas = FigureCanvasTkAgg(f, frame)
		canvas.get_tk_widget().pack(pady=10)

		# toolbar = NavigationToolbar2Tk(canvas, frame)
		# canvas._tkcanvas.pack()
		return

	def updateView(self, filePath, viewID):
		googleAnalytics = GAExplorer(filePath, viewID)

		self.container.pack_forget()
		self.container = Frame(self, bg='blue', relief=RAISED, borderwidth=1)
		self.container.pack(expand=1, fill=BOTH)

		try:
			data_one = googleAnalytics.week_report_by_days()
			data_two = googleAnalytics.week_report_by_hours()
			self.matplotCanvasDays(data_one)
			self.matplotCanvasHours(data_two)

		except Exception as err:
			print("{}".format(err))

		self.reloadFooter()
