import os
from datetime import date
import xml.etree.ElementTree as ET

"""Variables"""

today = date.today()
currentDate = str(today).replace('-','_')

"""Lists and Dictionaries"""

bf_date_prop_list = ["date", "originDate", "legalDate", "copyrightDate", "changeDate", "creationDate", "generationDate"]

work_1_list = os.listdir(f"../output/{currentDate}/work_1_xml/")
work_2_list = os.listdir(f"../output/{currentDate}/work_2_xml/")
instance_list = os.listdir(f"../output/{currentDate}/instance_xml/")
item_list = os.listdir(f"../output/{currentDate}/item_xml/")

resource_dict = {"work_1": work_1_list, "work_2": work_2_list, "instance": instance_list, "item": item_list}

"""Functions"""
def determine_date_type(value):
	num_of_dashes = 0
	time_included = False
	for character in value:
		if character == '-':
			num_of_dashes += 1
		elif character == ':':
			time_included = True


	if num_of_dashes == 0: # e.g. "1886"
		date_type = "gYear"
	elif num_of_dashes == 1: # e.g. "1886-02"
		date_type = 'gYearMonth'
	elif num_of_dashes == 2: # e.g. "1886-02-14" or "2021-03-17T12:00:00+00:00"
		if time_included == True:
			date_type = 'dateTime'
		else:
			date_type = 'date'

	return date_type

def add_dates_in_xml(currentDate, entity, file):
	# open xml parser
	tree = ET.parse(f'../output/{currentDate}/{entity}_xml/{file}')
	root = tree.getroot()

	for child in root:
		for prop in child:
			if prop.tag.split('}')[-1] in bf_date_prop_list:
				date_type = determine_date_type(prop.text)
				prop.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}datatype', f"http://www.w3.org/2001/XMLSchema#{date_type}")

	tree.write(f'../output/{currentDate}/{entity}_xml/{file}')

###

for entity in resource_dict.keys():
	for resource in resource_dict[entity]:
		add_dates_in_xml(currentDate, entity, resource)
