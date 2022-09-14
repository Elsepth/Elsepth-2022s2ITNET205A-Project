# fetch.py

# 0.1
# function that gets the information and keeps it for access by other functions

import urllib.parse
import requests
#API authentication key file
import keys
# proxy authentication file for use on TAFE network
try:
	import proxy
except ImportError:
	print ("Unable to import proxy definition file.")
	print ("Check that proxy.py exists in the directory.")
	quit()
# proxy file should be named proxy.py and have the following contents:
	# USE_PROXY = False # set True if running on TAFE Network, else set False
	# proxies = {'http': 'http://username:password@proxy.tafensw.edu.au:8080'}

class Directions():
	def __init__(self, orig, dest):
		print("initiating fetch_directions")
		API_LINK = "http://www.mapquestapi.com/directions/v2/route?"
		
		url = API_LINK + urllib.parse.urlencode({"key":keys.mapquest, "from":orig, "to":dest})

		print("fetching: " + url)

		if proxy.USE_PROXY == True:
			self.json_data = requests.get(url, proxies=proxy.proxies).json()
		else:
			self.json_data = requests.get(url).json()

		self.json_status = self.json_data["info"]["statuscode"]
	#	if self.json_status == 0:
	#		print ("OK")
	#	else:
	#		print("Error " + str(json_status) )

	def parse():
		pass