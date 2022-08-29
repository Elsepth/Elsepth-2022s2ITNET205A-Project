# proxy definition for use on TAFE network

USE_PROXY = False # set this to True if running on TAFE Network, else set False

# set username to your TAFE username (the part before the @)
# set password to your TAFE password

# WARNING! storing passwords in plaintext format in this manner is generally insecure. 
# Do not allow unauthorised users to access this file!
proxies = {'http': 'http://username:password@proxy.tafensw.edu.au:8080'}
