from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os, sys


class operateData():
	def __init__(self):
		pass
	def getFile(self,fileName):
		f = open("goprograms/" + str(fileName) + ".go", "r")
		returned = f.read()
		return returned

class seleniumGoSiteParser():
	def __init__(self, fileData):
		self.programText = fileData
		self.WebDriver = webdriver.Chrome()
		self.WebDriver.get("https://golang.org/")
	def __del__(self):
		self.unlinkDriver()
	def unlinkDriver(self):
		self.WebDriver.quit()
	def goParse(self):
		try:
			#Get Playground link object
			playgroundButton = self.WebDriver.find_element_by_xpath("/html/body/header/nav/ul/li[6]/a")
			playgroundButton.click()
			#Get input Area and Output object
			codeArea = self.WebDriver.find_element_by_id("code")
			runButton = self.WebDriver.find_element_by_id("run")
			outputArea = self.WebDriver.find_element_by_id("output")
			#Send the code from file
			codeArea.clear() # clear the old code
			codeArea.send_keys(self.programText)
			#Click debug button
			runButton.click()
			#Wait for GoLang playground to respond
			systemOutput = WebDriverWait(self.WebDriver, 250).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#output > pre > span.system")))
			returned = ""
			if ("Program exited." in systemOutput.get_attribute("innerHTML")):
				stdOutput = WebDriverWait(self.WebDriver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#output > pre > span.stdout")))
				returned = stdOutput.get_attribute("innerHTML")
			else:
				errorOutput = WebDriverWait(self.WebDriver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#output > pre > span.stderr")))
				returned = errorOutput.get_attribute("innerHTML")
			return returned
		except Exception as e:
			#formatted string literal(f-string) output for Python 3.6+: https://docs.python.org/3/reference/lexical_analysis.html#formatted-string-literals
			print(f"Selenium Web Driver Instance Error: {str(e)}") 

def main():
	if (len(sys.argv) >= 2):
		operateDataInstance = operateData()
		fileData = operateDataInstance.getFile(sys.argv[1])
		seleniumGoSiteParserInstance = seleniumGoSiteParser(fileData)
		programResult = seleniumGoSiteParserInstance.goParse()
		if (programResult != None):
			print(f"Program:\n{fileData}")
			print(f"Result:\n{programResult}")
		del seleniumGoSiteParserInstance
	else:
		print("Please create a Go program using the information from the site https://golang.org/ and store it into goprograms folder located nearby")
		print("Text files with Go programs should have .go extension, however, when you execute Python script please ommit the extension as per example")
		print("Example:python3 PythonToGo.py test ")
	exit()
if __name__=='__main__': main()


