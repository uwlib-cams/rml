"""Python Libraries/Modules/Packages"""
from datetime import date
import os
from progress.bar import Bar
from rdflib import *
from timeit import default_timer as timer
import xml.etree.ElementTree as ET

"""Imported Functions"""
from scripts.arguments import define_arg
from scripts.reserialize import reserialize

"""Variables"""
today = date.today()
currentDate = str(today).replace('-','_')

# arguments from command line
args = define_arg()
output_location = args.output

"""Lists and Dictionaries"""
bf_date_prop_list = ["date", "originDate", "legalDate", "copyrightDate", "changeDate", "creationDate", "generationDate"]

work_1_list = os.listdir(f"{output_location}/{currentDate}/work_1_xml/")
work_2_list = os.listdir(f"{output_location}/{currentDate}/work_2_xml/")
instance_list = os.listdir(f"{output_location}/{currentDate}/instance_xml/")
item_list = os.listdir(f"{output_location}/{currentDate}/item_xml/")

resource_dict = {"work_1": work_1_list, "work_2": work_2_list, "instance": instance_list, "item": item_list}

"""Functions"""
def determine_date_type(value):
	date_type = ""

	if len(value) == 4:
		date_type = "gYear"
		for character in value:
			if character.isnumeric() != True:
				date_type = ""
	elif len(value) == 7:
		date_type = "gYearMonth"
		for character in value[0:4]:
			if character.isnumeric() != True:
				date_type = ""
		if value[4] != "-":
			date_type = ""
		for character in value[5:]:
			if character.isnumeric() != True:
				date_type = ""
	elif len(value) == 10:
		date_type = "date"
		for character in value[0:4]:
			if character.isnumeric() != True:
				date_type = ""
		if value[4] != "-":
			date_type = ""
		for character in value[5:7]:
			if character.isnumeric() != True:
				date_type = ""
		if value[7] != "-":
			date_type = ""
		for character in value[8:]:
			if character.isnumeric() != True:
				date_type == ""
	elif len(value) == 25:
		date_type = "dateTime"
		value_numbers = value.replace('-','***')
		value_numbers = value_numbers.replace(':', '***')
		value_numbers = value_numbers.replace('T', '***')
		value_numbers = value_numbers.split('***')

		if len(value_numbers) != 6:
			date_type = ""
		else:
			year = value_numbers[0]
			month = value_numbers[1]
			day = value_numbers[2]
			hour = value_numbers[3]
			minute = value_numbers[4]
			seconds_additional_info = value_numbers[5]

			if len(year) != 4:
				date_type = ""
			for character in year:
				if character.isnumeric() != True:
					date_type = ""
			if len(month) != 2:
				date_type = ""
			for character in month:
				if character.isnumeric() != True:
					date_type = ""
			if len(day) != 2:
				date_type = ""
			for character in day:
				if character.isnumeric() != True:
					date_type = ""
			if len(hour) != 2:
				date_type = ""
			for character in hour:
				if charhacter.isnumeric() != True:
					date_type = ""
			if len(minute) != 2:
				date_type = ""
			for character in minute:
				if character.isnumeric() != True:
					date_type = ""

	return date_type

def add_dates_in_xml(currentDate, entity, file, output_location):
	num_of_edits = 0

	# open xml parser
	tree = ET.parse(f'{output_location}/{currentDate}/{entity}_xml/{file}')
	root = tree.getroot()

	for child in root:
		for prop in child:
			if prop.tag.split('}')[-1] in bf_date_prop_list:
				date_type = determine_date_type(prop.text)
				if date_type == "date":
					prop.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}datatype', f"http://www.w3.org/2001/XMLSchema#{date_type}")
					num_of_edits += 1

					tree.write(f'{output_location}/{currentDate}/{entity}_xml/{file}')

					reserialize(f'{output_location}/{currentDate}/{entity}_xml/{file}', f'{output_location}/{currentDate}/{entity}_xml/{file}', 'xml')

	return num_of_edits

###

num_of_resources = len(work_1_list) + len(work_2_list) + len(instance_list) + len(item_list)
num_of_edits = 0

start = timer()
bar = Bar(">> Adding datatypes to dates", max=num_of_resources, suffix='%(percent)d%%') # progress bar
for entity in resource_dict.keys():
	for resource in resource_dict[entity]:
		edits_made = add_dates_in_xml(currentDate, entity, resource, output_location)
		num_of_edits += edits_made
		bar.next()
end = timer()
bar.finish()

print(f"Datatypes added: {num_of_edits}")
print(f"Elapsed time: {round((end - start), 1)} s")
