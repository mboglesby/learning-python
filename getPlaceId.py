##########################################################################
## getPlaceId.py - v1.0 						##
## Created by Michael Oglesby for 'Using Python to Access Web Data'	##
##	class offered by University of Michigan on Coursera		##
## Usage: python3 getPlaceId.py 					##
## Description: Prompts user for a location name, calls API (using      ##
##      entered location name as address parameter), parses response    ##
##      for first Place ID, prints Place ID                             ##
##########################################################################

import sys
import urllib.request, urllib.parse, urllib.error
import ssl
import json

# API information
serviceUrl = "http://py4e-data.dr-chuck.net/json?"
apiKey = 42

# Prompt user for location
location = input("Enter location: ")

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Retrieve data from service url
parms = dict()
parms['address'] = location
parms['key'] = apiKey
requestUrl = serviceUrl + urllib.parse.urlencode(parms)
print("Retrieving", requestUrl)
try :
    urlHandle = urllib.request.urlopen(requestUrl)
except :
    print("Failed to open url...")
    sys.exit(0)

# Load raw json into python structure
responseRawData = urlHandle.read()
print("Retrieved", len(responseRawData), "characters")
try :
    response = json.loads(responseRawData)
except :
    print("Failed to retrieve...")
    sys.exit(0)

# Retrieve place_id for first result and print
firstPlaceId = response['results'][0]['place_id']
print("Place id", firstPlaceId)
