from datetime import date
import os
from progress.bar import Bar
from rdflib import *
from timeit import default_timer as timer
import xml.etree.ElementTree as ET

"""Namespaces"""
LDP = Namespace('http://www.w3.org/ns/ldp#')
bf = Namespace('http://id.loc.gov/ontologies/bibframe/')
bflc = Namespace('http://id.loc.gov/ontologies/bflc/')
dbo = Namespace('http://dbpedia.org/ontology/')
madsrdf = Namespace('http://www.loc.gov/mads/rdf/v1#')
owl = Namespace('http://www.w3.org/2002/07/owl#')
rdac = Namespace('http://rdaregistry.info/Elements/c/')
rdae = Namespace('http://rdaregistry.info/Elements/e/')
rdai = Namespace('http://rdaregistry.info/Elements/i/')
rdam = Namespace('http://rdaregistry.info/Elements/m/')
rdamdt = Namespace('http://rdaregistry.info/Elements/m/datatype/')
rdau = Namespace('http://rdaregistry.info/Elements/u/')
rdaw = Namespace('http://rdaregistry.info/Elements/w/')
rdax = Namespace('https://doi.org/10.6069/uwlib.55.d.4#')
sin = Namespace('http://sinopia.io/vocabulary/')
skos = Namespace('http://www.w3.org/2004/02/skos/core#')

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
def reserialize(file):
	"""Reserialize with rdflib to fix namespaces and UTf-8"""
	g = Graph()
	g.bind('bf', bf)
	g.bind('bflc', bflc)
	g.bind('dbo', dbo)
	g.bind('madsrdf', madsrdf)
	g.bind('owl', owl)
	g.bind('rdac', rdac)
	g.bind('rdae', rdae)
	g.bind('rdai', rdai)
	g.bind('rdam', rdam)
	g.bind('rdamdt', rdamdt)
	g.bind('rdau', rdau)
	g.bind('rdaw', rdaw)
	g.bind('rdax', rdax)
	g.bind('sin', sin)
	g.bind('skos', skos)
	g.load(f'file:{file}', format='xml')
	g.serialize(destination=file, format='xml')

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

def add_dates_in_xml(currentDate, entity, file):
	edit_made = False

	# open xml parser
	tree = ET.parse(f'../output/{currentDate}/{entity}_xml/{file}')
	root = tree.getroot()

	for child in root:
		for prop in child:
			if prop.tag.split('}')[-1] in bf_date_prop_list:
				date_type = determine_date_type(prop.text)
				if date_type == "date":
					prop.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}datatype', f"http://www.w3.org/2001/XMLSchema#{date_type}")
					edit_made = True

					tree.write(f'../output/{currentDate}/{entity}_xml/{file}')

					reserialize(f'../output/{currentDate}/{entity}_xml/{file}')

	return edit_made

###
num_of_resources = len(work_1_list) + len(work_2_list) + len(instance_list) + len(item_list)
num_of_edits = 0

start = timer()
bar = Bar(">> Adding datatypes to dates", max=num_of_resources, suffix='%(percent)d%%') # progress bar
for entity in resource_dict.keys():
	for resource in resource_dict[entity]:
		edit_made = add_dates_in_xml(currentDate, entity, resource)
		if edit_made == True:
			num_of_edits += 1
		bar.next()
end = timer()
bar.finish()

print(f"Edits made: {num_of_edits}")
print(f"Elapsed time: {round((end - start), 1)} s")
