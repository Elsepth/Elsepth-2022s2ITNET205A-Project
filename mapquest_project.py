#!/usr/bin/env python3
# Han Lin
# mapquest_project.py

import urllib.parse
import requests

# proxy definition for use on TAFE network
try:
	import proxy
except ImportError:
	print ("Unable to import proxy definition file.")
	print ("Check that proxy.py exists in the directory.")
	quit()
# proxy file should be named proxy.py and have the following contents:
	# USE_PROXY = False # set True if running on TAFE Network, else set False
	# proxies = {'http': 'http://username:password@proxy.tafensw.edu.au:8080'}

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

		url = main_api + urllib.parse.urlencode({"key":key, "from":orig, "to":dest})
		#url = "http://www.mapquestapi.com/directions/v2/route?key=kY8ADmvJPCmj9QyGob07gTBJODvFz62X&from=Washington, D.C.&to=Baltimore, Md"
		# curl -X GET "http://www.mapquestapi.com/directions/v2/route?key=kY8ADmvJPCmj9QyGob07gTBJODvFz62X&from=Washington, D.C.&to=Baltimore, Md"
		
		print('URL: ' + url)
		# print("GETTING")
		if proxy.USE_PROXY == True:
			json_data = requests.get(url, proxies=proxy.proxies).json()
		else:
			json_data = requests.get(url).json()
		# print("GOT")

		# print(json_data)
		json_status = json_data["info"]["statuscode"]

		if json_status == 0:
			print("API Status: " + str(json_status) + " = A successful route call.\n")

			print("=============================================")
			print("Directions from " + (orig) + " to " + (dest))
			print("Trip Duration: " + (json_data["route"]["formattedTime"]))
			#print("Miles: " + str(json_data["route"]["distance"]))
			#print("Fuel Used (Gal): " + str(json_data["route"]["fuelUsed"]))
			#print("Kilometers: " + str((json_data["route"]["distance"])*1.61))
			#print("Fuel Used (Ltr): " + str((json_data["route"]["fuelUsed"])*3.78))
			print("Kilometers: " + str("{:.2f}".format((json_data["route"]["distance"])*1.61)))
			print("Fuel Used (Ltr): " + str("{:.2f}".format((json_data["route"]["fuelUsed"])*3.78)))

			print("=============================================")
			for each in json_data["route"]["legs"][0]["maneuvers"]:
				print((each["narrative"]) + " (" + str("{:.2f}".format((each["distance"])*1.61) + " km)"))
			print("=============================================\n")

		elif json_status == 402:
			print("**********************************************")
			print("Status Code: " + str(json_status) + "; Invalid user inputs for one or both locations.")
			print("**********************************************\n")
		elif json_status == 611:
			print("**********************************************")
			print("Status Code: " + str(json_status) + "; Missing an entry for one or both locations.")
			print("**********************************************\n")
		else:
			print("************************************************************************")
			print("For Status Code: " + str(json_status) + "; Refer to:")
			print("https://developer.mapquest.com/documentation/directions-api/status-codes")
			print("************************************************************************\n")


	return 0

main()