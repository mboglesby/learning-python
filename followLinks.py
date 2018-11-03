##########################################################################
## followLinks.py - v1.0						##
## Created by Michael Oglesby for 'Using Python to Access Web Data'	##
##	class offered by University of Michigan on Coursera		##
## Usage: python3 followLinks.py					##
## Description: Prompts the user for a url, opens the web file represe-	##
##	nted by the url in BeautifulSoup, then prompts the user for an	##
##	integer represenging the position of an anchor tag within the	##
##	file, then opens the web file represented by the url in the	##
##	href attribute of the anchor tag in BeautifulSoup. Repeats the	##
##	process of prompting the user for the position of an anchor tag	##
##	until the user quits.						##
## Test with url: http://py4e-data.dr-chuck.net/known_by_Fikret.html	##
##########################################################################

##########################################################################
## Import needed libraries						##
##########################################################################
import sys
import urllib.request
import ssl
from bs4 import BeautifulSoup

##########################################################################
## openHtmlInSoup(url) --> Returns BeautifulSoup instance		##
## Description: Function to open a web file via BeautifulSoup. Accepts	##
##	 a url as a parameter and returns a BeautifulSoup instance	##
##########################################################################
def openHtmlInSoup(url) :
	try :
		print("Opening URL:", url)
		html = urllib.request.urlopen(url)
		soup = BeautifulSoup(html, 'html.parser')
		return soup
	except :
		print("Error opening URL:", url)
		sys.exit(0)

##########################################################################
## Program execution begins here					##
##########################################################################

# If the user entered "help" or "-help" or "-h" as a parameter, print help test and quit execution
if ("help" in sys.argv) or ("-help" in sys.argv) or ("-h" in sys.argv) :
	print("followLinks.py - v1.0")
	print("Created by Michael Oglesby for 'Using Python to Access Web Data'")
	print("	class offered by University of Michigan on Coursera")
	print("Usage: python3 followLinks.py")
	print("Description: Prompts the user for a url, opens the web file represe-")
	print("	nted by the url in BeautifulSoup, then prompts the user for an")
	print("	integer represenging the position of an anchor tag within the")
	print("	file, then opens the web file represented by the url in the")
	print("	href attribute of the anchor tag in BeautifulSoup. Repeats the")
	print("	process of prompting the user for the position of an anchor tag")
	print("	until the user quits.")
	print("Test with url: http://py4e-data.dr-chuck.net/known_by_Fikret.html")
	sys.exit(0)

# Get url from user and open web file via BeautifulSoup
url = input("Enter URL: ")
soup = openHtmlInSoup(url)
urlsOpened = 1

# Continue opening urls until the user quits
while True :
	# Ask the user which link in the file they want to open
	while True :
		userInput = input("Open link at position (Enter 'quit' to quit): ")
		
		# If the user enters "quit", quit execution 
		if userInput.strip().lower() == "quit" :
			print("URLs opened:", urlsOpened)
			print("Quitting...")
			sys.exit(0)

		# Ensure that the link position entered by the user is a positive integer
		# If not, prompt the user again
		try :
			linkPos = int(userInput)
			if linkPos < 1 :
				raise Exception('Position < 1')
		except :
			print("Error: Enter a valid position or \"quit\"")
			continue
		else :
			break

	# Find all anchor tags in file
	anchors = soup.find_all('a')

	# Attempt to retrieve anchor tag at position entered by user
	# If no anchor tag at position, prompt the user again
	try :
		anchorAtPos = anchors[linkPos-1]
	except :
		print("Error: No link at position")
		continue

	# Retrieve link text from anchor tag
	linkText = anchorAtPos.contents[0]
	print("Link text:", linkText)

	# Retrieve url from href attribute in achor tag and open web file via BeautifulSoup
	url = anchorAtPos['href']
	soup = openHtmlInSoup(url)
	urlsOpened += 1
	print("URLs opened:", urlsOpened)
