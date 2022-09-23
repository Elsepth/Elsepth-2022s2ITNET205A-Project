# ui_pyqt.py

import sys

from PyQt6.QtCore import (
	Qt,
	QSize,
)
from PyQt6.QtWidgets import (
	QMainWindow,
	QApplication, 
	QVBoxLayout,
	QHBoxLayout,
	QFormLayout,
	QLineEdit,
	QStatusBar,
	QWidget,
	QLabel,
	QRadioButton,
	QPushButton,
)
from PyQt6.QtGui import QAction, QIcon

import keys
import proxy
import fetch

#app = QApplication ([])

#win = QWidget()
#win.setWindowTitle("Mapquest GUI App")

# setGeometry(x,y,width,height)
#win.setGeometry(100,100,280,80)


#helloMsg = QLabel("<h1>Hello, World!</h1>", parent=win)
# move(relative x, y)
#helloMsg.move(60, 15)



# https://www.pythonguis.com/tutorials/pyqt6-signals-slots-events/

#this class extends QMainWindow, so it includes all methods of QMainWindow by default
class MainWindow2(QMainWindow):
	def __init__(self):
		#call __init__ from QMainWindow
		super().__init__() 
		
		#set the window title
		self.setWindowTitle("MapQuest Again")
	
		#a text field
		self.label_instruction = QLabel("Enter locations to find directions between:")
		self.label_output = QLabel("OUTPUT")

		#two input fields
		self.formOrig = QLineEdit()
		self.formOrig.setPlaceholderText("From")
		self.formOrig.textChanged.connect(self.slot_update)
		self.formOrig.setStatusTip("<TODO>")


		self.formDest = QLineEdit()
		self.formDest.setPlaceholderText("To")
		self.formDest.textChanged.connect(self.slot_update)
		self.formDest.setStatusTip("<TODO>")



		# this button does not need to store a value
		button_defaults = QPushButton("Defaults")
		button_defaults.clicked.connect(self.slot_button_defaults)
		button_defaults.setStatusTip("<TODO>")


		# this button stores a value, so it must be self.button
		self.button_run = QPushButton("Run")
		# disable button by default
		self.button_run.setEnabled(False)
		# sends a SIGNAL on click, which connects to a slot
		self.button_run.clicked.connect(self.slot_button_run)
		# displays status on hover
		self.button_run.setStatusTip("Get directions")


	#the layout definition
		# layout for user input
		layout_input = QVBoxLayout()
		layout_input.addWidget(self.label_instruction)
		layout_input.addWidget(self.formOrig)
		layout_input.addWidget(self.formDest)

		# buttons are combined in a horizontal row
		layout_buttons = QHBoxLayout()
		layout_buttons.addWidget(button_defaults)
		layout_buttons.addWidget(self.button_run)

		layout_input.addLayout(layout_buttons)


		# layout for program output
		layout_output = QVBoxLayout()
		layout_output.addWidget(self.label_output)

		layout = QVBoxLayout()
		layout.addLayout(layout_input)
		layout.addLayout(layout_output)

		container = QWidget()
		container.setLayout(layout)

		self.setMinimumSize(QSize(400,300))
		self.setMaximumSize(QSize(1000,1000))

	#	self.setCentralWidget(self.button_run)
		self.setCentralWidget(container)

		statusBar = QStatusBar(self)
		self.setStatusBar(statusBar)

		statusBar.showMessage("Ready")


	#Slots, these accept signals
	def slot_button_defaults(self):
		print("DEFAULT")
		self.formOrig.setText("Washington, D.C.")
		self.formDest.setText("Baltimore, Md")

	def slot_button_run(self):
		print("RUN")
		
		orig = self.formOrig.text()
		dest = self.formDest.text()

	#	self.d = fetch.Directions(orig,dest)

		self.label_output.setText (
			func_output	(
				orig,
				dest,
				fetch.Directions(orig,dest),
				"metric"
			)
		)

	#	self.setOutput("FOO BAR")


	def slot_update(self):
		#if both fields are filled then enable run
		if "" == self.formOrig.text(): 
			self.button_run.setEnabled(False)
		elif "" == self.formDest.text(): 
			self.button_run.setEnabled(False)
		else: 
			self.button_run.setEnabled(True)


class MainWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.unit_system = "metric"
		self.setWindowTitle("MapQuest QVBoxLayout")
		self.resize(270,110)
		self.layout=QVBoxLayout()

		self.layout.addWidget(QLabel("Enter locations to find directions between",parent=self))


		self.formOrig = QLineEdit()
		self.formOrig.setPlaceholderText("From")
		self.formDest = QLineEdit()
		self.formDest.setPlaceholderText("To")

		self.layout.addWidget(self.formOrig)
		self.layout.addWidget(self.formDest)

		#formLayout = QFormLayout()
		#formLayout.addRow("From", QLineEdit())
		#formLayout.addRow("To", QLineEdit())

		#layout.addLayout(formLayout)

		self.unitsBox = QHBoxLayout()
		self.button_metric = QRadioButton("Metric",self)
		self.button_metric.value = "metric"
		self.button_metric.toggled.connect(self.unitClicked)
		self.button_metric.setChecked(True)
		
		self.button_imperial = QRadioButton("Imperial",self)
		self.button_imperial.value = "imperial"
		self.button_imperial.toggled.connect(self.unitClicked)
		
		self.unitsBox.addWidget(self.button_metric)
		self.unitsBox.addWidget(self.button_imperial)
		self.layout.addLayout(self.unitsBox)

		self.button_defaults = QPushButton("Defaults")
		self.button_defaults.clicked.connect(self.setDefaults)
		self.layout.addWidget(self.button_defaults)

		self.button_run = QPushButton("Run")
		self.button_run.clicked.connect(self.func_run)
		self.layout.addWidget(self.button_run)

		self.output = QLabel("[Output]",parent=self)
		self.output.setWordWrap(True)
		self.layout.addWidget(self.output)

	#	self.button_quit = QPushButton("Quit")
	#	self.layout.addWidget(button_quit)
	
		self.setLayout(self.layout)


		self.setStatusBar(QStatusBar(self))
	#	self.statusBar = QStatusBar(self)
	#	self.setStatusBar(self.statusBar)
	#	self.statusBar.showMessage("READY")

	def unitClicked(self):
		rb = self.sender()
		if rb.isChecked():
			print("Set unit system to " + rb.value)
			self.unit_system = rb.value

	def setDefaults(self):
		self.formOrig.setText("Washington, D.C.")
		self.formDest.setText("Baltimore, Md")

	def getLocationOrig(self):
		return self.formOrig.text()
		
	def getLocationDest(self):
		return self.formDest.text()
	
	def setOutput(self,foo):
		self.output.setText(foo)



	def func_run(self):
		print("START")
		main_api = "http://www.mapquestapi.com/directions/v2/route?"
		key = keys.mapquest
		
		#orig = "Washington, D.C."
		#dest = "Baltimore, Md"
		orig = self.getLocationOrig()
		dest = self.getLocationDest()

		self.d = fetch.Directions(orig,dest)

	#	self.setOutput("FOO BAR")

		print("OUTPUTTING")

		if self.d.json_status == 0:
			print("JSON STATUS 0")

			o = ("API Status: " + str(self.d.json_status) + " = A successful route call."
			+ "\n============================================="
			+ "\nDirections from " + (orig) + " to " + (dest)
			+ "\nTrip Duration: " + (self.d.json_data["route"]["formattedTime"])
			)
			#print("Miles: " + str(json_data["route"]["distance"]))
			#print("Fuel Used (Gal): " + str(json_data["route"]["fuelUsed"]))
			#print("Kilometers: " + str((json_data["route"]["distance"])*1.61))
			#print("Fuel Used (Ltr): " + str((json_data["route"]["fuelUsed"])*3.78))
			
			if "metric" == self.unit_system:
				o = o + ("\nKilometers: " + str("{:.2f}".format((self.d.json_data["route"]["distance"])*1.61))
				+ "\nFuel Used (Ltr): " + str("{:.2f}".format((self.d.json_data["route"]["fuelUsed"])*3.78))
				)
			elif "imperial" == self.unit_system:
				o = o + ("\nMiles: " + str("{:.2f}".format((self.d.json_data["route"]["distance"])))
				+ "\nFuel Used (Gal): " + str("{:.2f}".format((self.d.json_data["route"]["fuelUsed"])))
				)
			o += "\n================== DIRECTIONS =================="

			for each in self.d.json_data["route"]["legs"][0]["maneuvers"]:
				if "metric" == self.unit_system:
					dist = " (" + str("{:.2f}".format((each["distance"])*1.61)) + " km)"
				elif "imperial" == self.unit_system:
					dist = " (" + str("{:.2f}".format((each["distance"]))) + " mi)"
				e = ("\n⤷ " 
				+ (each["narrative"]) 
				+ dist
				#+ "\n============================================="
				)

				o = o + e

		elif self.d.json_status == 402:
			o=("\n**********************************************"
			+ "\nStatus Code: " + str(self.d.json_status) + "; Invalid user inputs for one or both locations."
			+ "\n**********************************************")
		elif self.d.json_status == 611:
			o=("\n**********************************************"
			+ "\nStatus Code: " + str(self.d.json_status) + "; Missing an entry for one or both locations."
			+ "\n**********************************************")
		else:
			o=("\n************************************************************************"
			+ "\nFor Status Code: " + str(self.d.json_status) + "; Refer to:"
			+ "\nhttps://developer.mapquest.com/documentation/directions-api/status-codes"
			+ "\n************************************************************************")

		self.setOutput(o)

		return 0


def func_output(orig,dest,fetched,unit_system):
	print("OUTPUTTING")
	status = fetched.json_status
	data = fetched.json_data

	if status == 0:
		print("JSON STATUS 0")

		o = ("API Status: " + str(status) + " = A successful route call."
		+ "\n============================================="
		+ "\nDirections from " + (orig) + " to " + (dest)
		+ "\nTrip Duration: " + (data["route"]["formattedTime"])
		)
		
		if "metric" == unit_system:
			o = o + ("\nKilometers: " + str("{:.2f}".format((data["route"]["distance"])*1.61))
			+ "\nFuel Used (Ltr): " + str("{:.2f}".format((data["route"]["fuelUsed"])*3.78))
			)
		elif "imperial" == unit_system:
			o = o + ("\nMiles: " + str("{:.2f}".format((data["route"]["distance"])))
			+ "\nFuel Used (Gal): " + str("{:.2f}".format((data["route"]["fuelUsed"])))
			)
		o += "\n================== DIRECTIONS =================="

		for each in data["route"]["legs"][0]["maneuvers"]:
			if "metric" == unit_system:
				dist = " (" + str("{:.2f}".format((each["distance"])*1.61)) + " km)"
			elif "imperial" == unit_system:
				dist = " (" + str("{:.2f}".format((each["distance"]))) + " mi)"
			e = ("\n⤷ " 
			+ (each["narrative"]) 
			+ dist
			#+ "\n============================================="
			)

			o = o + e

	elif status == 402:
		o=("\n**********************************************"
		+ "\nStatus Code: " + str(status) + "; Invalid user inputs for one or both locations."
		+ "\n**********************************************")
	elif status == 611:
		o=("\n**********************************************"
		+ "\nStatus Code: " + str(status) + "; Missing an entry for one or both locations."
		+ "\n**********************************************")
	else:
		o=("\n************************************************************************"
		+ "\nFor Status Code: " + str(status) + "; Refer to:"
		+ "\nhttps://developer.mapquest.com/documentation/directions-api/status-codes"
		+ "\n************************************************************************")

	return o

def main():
	app = QApplication(sys.argv)
#	window = MainWindow()
	window = MainWindow2()
	window.show()
	sys.exit(app.exec())

if __name__ == "__main__":
	main()
#win.show()

#sys.exit(app.exec())

