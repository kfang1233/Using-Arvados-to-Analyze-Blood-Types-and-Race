#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This script reads all the blood types from the 173-HarvardPGP folder and all the ethnicities from CSVFiles/phenotypes-race.csv and prints a formatted table to the standard output.
# This also collects blood types from phenotypes-race.csv and only use BOOGIE's guess as a failsafe.
import os
import csv

class BloodStorage:
	#bloodTypes: [A, B, O, AB]
	def __init__(self):
		self.bloodTypes = [0, 0, 0, 0]
	def __str__(self):
		return "A: " + str(self.bloodTypes[0]) + "\t B: " + str(self.bloodTypes[1]) + "\t AB: " + str(self.bloodTypes[2]) + "\t O: " + str(self.bloodTypes[3])
	def incrementA(self):
		self.bloodTypes[0] += 1;
	def incrementB(self):
		self.bloodTypes[1] += 1;
	def incrementAB(self):
		self.bloodTypes[2] += 1;
	def incrementO(self):
		self.bloodTypes[3] += 1;

# search CSV file for name and return blood type for respective name
def searchCSVForRace(name):
	with open("./CSVFiles/phenotypes-race.csv") as csvFile:
		reader = csv.DictReader(csvFile)
		for row in reader:
			if row["Participant"] == name:
				race = row["Race/ethnicity"]
				if race != "No response" and race != "":
					csvFile.close()
					return race
	csvFile.close()
	return "None"

def searchCSVForBlood(name):
	with open("./CSVFiles/phenotypes-basic2015.csv") as csvFile:
		reader = csv.DictReader(csvFile)
		for row in reader:
			#print row
			#print row["Participant"] + " " + row["1.1 \xe2\x80\x94 Blood Type"]
			if row["Participant"] == name:
				try:
					bloodType = row["Blood Type"]
					if bloodType == "Don't know":
						return None
					else:
						bloodType = bloodType[0:2].replace(" ", "")
						csvFile.close()
						return bloodType
				except:
					break;
	csvFile.close()
	return None

# dictionary containing the race and associated blood type data
raceDict = {}
#for every person found, search in PGP and compare

pgpDirectory = "./173-HarvardPGP/"

for filename in os.listdir(pgpDirectory):
	if filename.startswith("hu"):
		person = open(pgpDirectory + filename)
		race = searchCSVForRace(filename) # this is the race of the person
		blood = searchCSVForBlood(filename) # this is the blood of the person
		if blood == None:
			# failsafe - will use data generated by BOOGIE only if the data is not available in the CSV file.
			blood = person.read()

		blood = blood.rstrip()
		if blood != None and race != None and race != "None":
			#print repr(blood)
			try:
				if blood == "A":
					raceDict[race].incrementA()
				elif blood == "B":
					raceDict[race].incrementB()
				elif blood == "O":
					raceDict[race].incrementO()
				elif blood == "AB":
					raceDict[race].incrementAB()
			except:
				raceDict[race] = BloodStorage()
				if blood == "A":
					raceDict[race].incrementA()
				elif blood == "B":
					raceDict[race].incrementB()
				elif blood == "O":
					raceDict[race].incrementO()
				elif blood == "AB":
					raceDict[race].incrementAB()
for race in raceDict:
	print race + ":\n" + str(raceDict[race])
