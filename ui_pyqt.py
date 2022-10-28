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

import weatherforecast as W


# app = QApplication ([])

# win = QWidget()
# win.setWindowTitle("Mapquest GUI App")

# setGeometry(x,y,width,height)
# win.setGeometry(100,100,280,80)


# helloMsg = QLabel("<h1>Hello, World!</h1>", parent=win)
# move(relative x, y)
# helloMsg.move(60, 15)


# https://www.pythonguis.com/tutorials/pyqt6-signals-slots-events/

# this class extends QMainWindow, so it includes all methods of QMainWindow by default
class MainWindow2(QMainWindow):
    def __init__(self):
        # call __init__ from QMainWindow
        super().__init__()

        # set the window title
        self.setWindowTitle("MapQuest PyQt6 GUI")

        # a text field
        self.label_instruction = QLabel("Enter locations to find directions between:")
#        self.label_output = QLabel("[Waiting for input.]")
        self.label_output = QLabel("[Waiting for input.]")
        self.label_output.setWordWrap(True)
        self.label_output.setIndent(4)

	
        # two input fields
        self.formOrig = QLineEdit()
        self.formOrig.setPlaceholderText("From")
        self.formOrig.textChanged.connect(self.slot_update)
        self.formOrig.setStatusTip("<TODO>")

        self.formDest = QLineEdit()
        self.formDest.setPlaceholderText("To")
        self.formDest.textChanged.connect(self.slot_update)
        self.formDest.setStatusTip("<TODO>")

        # Radio Button
        self.radiobutton_metric = QRadioButton("Metric", self)
        self.radiobutton_metric.toggled.connect(self.slot_unit_selection)
        self.radiobutton_imperial = QRadioButton("Imperial", self)
        self.radiobutton_imperial.toggled.connect(self.slot_unit_selection)

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

        #this button toggles display of weather data
        self.button_weather = QPushButton("Show Weather")
        self.button_weather.clicked.connect(self.slot_button_weather)
        self.button_run.setStatusTip("toggle weather display")


        # label for weather data
        weather_text_default = "City : \nTemperature :\nWind Speed :\nDescription :\nLatitude :\nLongitude :"
        self.label_weather = QLabel(weather_text_default)
        self.label_weather.hide()

        # the layout definition
        # layout for user input
        layout_input = QVBoxLayout()
        layout_input.addWidget(self.label_instruction)
        layout_input.addWidget(self.formOrig)
        layout_input.addWidget(self.formDest)

        # buttons are combined in a horizontal row
        layout_buttons = QHBoxLayout()
        layout_buttons.addWidget(button_defaults)
        layout_buttons.addWidget(self.button_run)
        layout_buttons.addWidget(self.button_weather)

        layout_radiobuttons = QHBoxLayout()
        layout_radiobuttons.addWidget(self.radiobutton_imperial)
        layout_radiobuttons.addWidget(self.radiobutton_metric)

        layout_input.addLayout(layout_radiobuttons)
        layout_input.addLayout(layout_buttons)

        # layout for program output
        layout_output = QVBoxLayout()
        layout_output.addWidget(self.label_output)

        layout_left = QVBoxLayout()
        layout_left.addLayout(layout_input)
        layout_left.addLayout(layout_output)
        layout_left.addStretch()

        layout_right = QVBoxLayout()
        layout_right.addWidget(self.label_weather)
    #    layout_right.addLayout()
        layout_right.addStretch()

        layout = QHBoxLayout()
        layout.addLayout(layout_left)
        layout.addLayout(layout_right)

        container = QWidget()
        container.setLayout(layout)

        self.setMinimumSize(QSize(600, 800))
        self.setMaximumSize(QSize(1000, 1000))

        #	self.setCentralWidget(self.button_run)
        self.setCentralWidget(container)

        statusBar = QStatusBar(self)
        self.setStatusBar(statusBar)

        #default
        self.unit_system = "imperial"
        statusBar.showMessage("Ready")

    # slots, these accept signals
    def slot_unit_selection(self):
        if True == self.radiobutton_metric.isChecked():
            self.unit_system = "metric"
        elif True == self.radiobutton_imperial.isChecked():
            self.unit_system = "imperial"

    # Slots, these accept signals
    def slot_button_defaults(self):
        print("DEFAULT")
        self.formOrig.setText("Washington, D.C.")
        self.formDest.setText("Baltimore, Md")

    def slot_button_weather(self):
    	if self.label_weather.isHidden():
    		self.button_weather.setText("Hide Weather")
    		self.label_weather.show()
    	else:
    		self.button_weather.setText("Show Weather")
    		self.label_weather.hide()


    def slot_button_run(self):
        print("RUN")

        orig = self.formOrig.text()
        dest = self.formDest.text()

        #	self.d = fetch.Directions(orig,dest)

        data_d = fetch.Directions(orig, dest)

        self.label_output.setText(
            func_output(
                orig,
                dest,
                data_d,
                self.unit_system
            )
        )
    #    self.label_output.adjustSize()
        city0 = data_d.json_data["route"]["locations"][0]["adminArea5"]
        city1 = data_d.json_data["route"]["locations"][1]["adminArea5"]
        print(f"Getting weather for {city0} in {self.unit_system}")
        print(f"Getting weather for {city1} in {self.unit_system}")
        self.label_weather.setText(
        	W.Weather.fetch(city0,self.unit_system)+
        	"\n---\n"+
        	W.Weather.fetch(city1,self.unit_system)
		)
    #    self.label_weather.adjustSize()

    #	self.setOutput("FOO BAR")

    def slot_update(self):
        # if both fields are filled then enable run
        if "" == self.formOrig.text():
            self.button_run.setEnabled(False)
        elif "" == self.formDest.text():
            self.button_run.setEnabled(False)
        else:
            self.button_run.setEnabled(True)


def func_output(orig, dest, fetched, unit_system):
    print("OUTPUTTING")
    status = fetched.json_status
    data = fetched.json_data

    if status == 0:
        print("JSON STATUS 0")

        o = ("API Status: " + str(status) + " = A successful route call."
             + "\n============================================="
             + "\nDirections from " + data["route"]["locations"][0]["adminArea5"] + " to " + data["route"]["locations"][1]["adminArea5"]
             + "\nTrip Duration: " + (data["route"]["formattedTime"])
             )
	#HOTFIX: Fuel disabled because it seems that MAPQUEST API is no longer returning this data
        if "metric" == unit_system:
            o = o + ("\nKilometers: " + str("{:.2f}".format((data["route"]["distance"]) * 1.61))
    #                 + "\nFuel Used (Ltr): " + str("{:.2f}".format((data["route"]["fuelUsed"]) * 3.78))
                     )
        elif "imperial" == unit_system:
            o = o + ("\nMiles: " + str("{:.2f}".format((data["route"]["distance"])))
     #                + "\nFuel Used (Gal): " + str("{:.2f}".format((data["route"]["fuelUsed"])))
                     )
        o += "\n================== DIRECTIONS =================="

        for each in data["route"]["legs"][0]["maneuvers"]:
            if "metric" == unit_system:
                dist = " (" + str("{:.2f}".format((each["distance"]) * 1.61)) + " km)"
            elif "imperial" == unit_system:
                dist = " (" + str("{:.2f}".format((each["distance"]))) + " mi)"
            e = ("\n⤷ "
                 + (each["narrative"])
                 + dist
				 # + "\n============================================="
				 )

            o = o + e

    elif status == 402:
        o = ("\n**********************************************"
             + "\nStatus Code: " + str(status) + "; Invalid user inputs for one or both locations."
             + "\n**********************************************")
    elif status == 611:
        o = ("\n**********************************************"
             + "\nStatus Code: " + str(status) + "; Missing an entry for one or both locations."
             + "\n**********************************************")
    else:
        o = ("\n************************************************************************"
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
# win.show()

# sys.exit(app.exec())

