##########################################################################
## sumCountsFromXML.py - v1.0						##
## Created by Michael Oglesby for 'Using Python to Access Web Data'	##
##	class offered by University of Michigan on Coursera		##
## Usage: python3 sumCountsFromXML.py					##
## Description: Prompts the user for a url, opens the web file represe-	##
##	nted by the url, parses the XML for comment counts, and then	##
##	sums the counts.						##
## Test with url: http://py4e-data.dr-chuck.net/comments_42.xml		##
##########################################################################

##########################################################################
## Import needed libraries						##
##########################################################################
import sys
import urllib.request
import xml.etree.ElementTree as ET

##########################################################################
## Program execution begins here					##
##########################################################################

# If the user entered "help" or "-help" or "-h" as a parameter, print help test and quit execution
if ("help" in sys.argv) or ("-help" in sys.argv) or ("-h" in sys.argv) :
	print("sumCountsFromXML.py - v1.0")
	print("Created by Michael Oglesby for 'Using Python to Access Web Data'")
	print("	class offered by University of Michigan on Coursera")
	print("Usage: python3 sumCountsFromXML.py")
	print("Description: Prompts the user for a url, opens the web file represe-")
	print("	nted by the url, parses the XML for comment counts, and then")
	print("	sums the counts.")
	print("Test with url: http://py4e-data.dr-chuck.net/comments_42.xml")
	sys.exit(0)

# Get url from user and open web file
url = input("Enter URL: ")
print("Opening URL:", url)
try :
	webFile = urllib.request.urlopen(url)
except :
	print("Error opening URL:", url)
	sys.exit(0)

# Create XML tree from web file
xmlTree = ET.parse(webFile)
treeRoot = xmlTree.getroot()

# Load all comment counts into a list
counts = treeRoot.findall('./comments/comment/count')

# Loop through all comment counts and sum the counts
totalCount = 0
for count in counts :
	totalCount += int(count.text)

# Print the total sum of comment counts
print("Total Count =", totalCount)
