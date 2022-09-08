#!/usr/bin/env python3
# Han (Lily) Lin, Catherine Hocking, Dean Ervin Sebial, Ahmad Mohiuddin
# ui_basic.py

import fetch


def main():
	# print("START")
	main_api = "http://www.mapquestapi.com/directions/v2/route?"
	key = "kY8ADmvJPCmj9QyGob07gTBJODvFz62X" # This is my key, but it doesn't really matter whose key it is for this project. If it did, I would split it off into a separate file to import as well. -Lily
	
	#orig = "Washington, D.C."
	#dest = "Baltimore, Md"
	while True:
		orig = input("Starting Location: ")
		if orig == "quit" or orig == "q":
			break
		if orig == 'd':
			orig = "Washington, D.C."
		dest = input("Destination: ")
		if dest == "quit" or dest == "q":
			break
		if dest =='d':
			dest = "Baltimore, Md"


		d = fetch.Directions(orig,dest)


		if d.json_status == 0:
			print("API Status: " + str(d.json_status) + " = A successful route call.\n")

			print("=============================================")
			print("Directions from " + (orig) + " to " + (dest))
			print("Trip Duration: " + (d.json_data["route"]["formattedTime"]))
			#print("Miles: " + str(json_data["route"]["distance"]))
			#print("Fuel Used (Gal): " + str(json_data["route"]["fuelUsed"]))
			#print("Kilometers: " + str((json_data["route"]["distance"])*1.61))
			#print("Fuel Used (Ltr): " + str((json_data["route"]["fuelUsed"])*3.78))
			print("Kilometers: " + str("{:.2f}".format((d.json_data["route"]["distance"])*1.61)))
			print("Fuel Used (Ltr): " + str("{:.2f}".format((d.json_data["route"]["fuelUsed"])*3.78)))

			print("=============================================")
			for each in d.json_data["route"]["legs"][0]["maneuvers"]:
				print((each["narrative"]) + " (" + str("{:.2f}".format((each["distance"])*1.61) + " km)"))
			print("=============================================\n")

		elif d.json_status == 402:
			print("**********************************************")
			print("Status Code: " + str(d.json_status) + "; Invalid user inputs for one or both locations.")
			print("**********************************************\n")
		elif d.json_status == 611:
			print("**********************************************")
			print("Status Code: " + str(d.json_status) + "; Missing an entry for one or both locations.")
			print("**********************************************\n")
		else:
			print("************************************************************************")
			print("For Status Code: " + str(d.json_status) + "; Refer to:")
			print("https://developer.mapquest.com/documentation/directions-api/status-codes")
			print("************************************************************************\n")


	return 0

main()