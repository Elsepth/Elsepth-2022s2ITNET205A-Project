# ui_pyqt.py

import sys
from PyQt6.QtWidgets import (
	QApplication, 
	QVBoxLayout,
	QFormLayout,
	QLineEdit,
	QWidget,
	QLabel,
	QRadioButton,
	QPushButton,
)

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

unit_system = "metric"




class MainWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("MapQuest QVBoxLayout")
		self.resize(270,110)
		self.layout=QVBoxLayout()

		self.layout.addWidget(QLabel("hello world",parent=self))


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

		self.layout.addWidget(QRadioButton("Metric",self))
		self.layout.addWidget(QRadioButton("Imperial",self))

		self.button_run = QPushButton("Run")
		self.button_run.clicked.connect(self.func_run)
		self.layout.addWidget(self.button_run)

		self.button_defaults = QPushButton("Defaults")
		self.button_defaults.clicked.connect(self.setDefaults)
		self.layout.addWidget(self.button_defaults)

		self.output = QLabel("[Output]",parent=self)
		self.layout.addWidget(self.output)

	#	self.button_quit = QPushButton("Quit")
	#	self.layout.addWidget(button_quit)
	
		self.setLayout(self.layout)

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
			#print("Miles: " + str(json_data["route"]["distance"]))
			#print("Fuel Used (Gal): " + str(json_data["route"]["fuelUsed"]))
			#print("Kilometers: " + str((json_data["route"]["distance"])*1.61))
			#print("Fuel Used (Ltr): " + str((json_data["route"]["fuelUsed"])*3.78))
			+ "\nKilometers: " + str("{:.2f}".format((self.d.json_data["route"]["distance"])*1.61))
			+ "\nFuel Used (Ltr): " + str("{:.2f}".format((self.d.json_data["route"]["fuelUsed"])*3.78))
			+ "\n=============================================")

			for each in self.d.json_data["route"]["legs"][0]["maneuvers"]:
				e = ("\n" 
				+ (each["narrative"]) 
				+ " (" 
				+ str("{:.2f}".format((each["distance"])*1.61))
				+ " km)"
				+ "\n=============================================")

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


def main():
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec())

if __name__ == "__main__":
	main()
#win.show()

#sys.exit(app.exec())

