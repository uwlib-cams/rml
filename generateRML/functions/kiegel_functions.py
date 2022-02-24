"""Python Libraries/Modules/Packages"""
import csv
import os

"""Imported Functions"""
from functions.formatting_functions import edit_kiegel

"""Functions"""
def get_file_list(csv_dir, entity):
	"""Get list of CSV files for a given entity"""
	csv_file_list = os.listdir(csv_dir)
	file_list = []
	for file in csv_file_list:
		if entity in file:
			file_list.append(file)
	return file_list

def get_property_kiegel_list(csv_dir, entity):
	"""Get list of tuples (property number, kiegel) from CSV files for a given entity"""
	file_list = get_file_list(csv_dir, entity)

	if entity == "work":
		rda_iri = 'http://rdaregistry.info/Elements/w/'
		from functions.lists import skip_work_props as skip_prop_list
	elif entity == "expression":
		rda_iri = 'http://rdaregistry.info/Elements/e/'
		from functions.lists import skip_expression_props as skip_prop_list
	elif entity == "manifestation":
		rda_iri = 'http://rdaregistry.info/Elements/m/'
		from functions.lists import skip_manifestation_props as skip_prop_list
	elif entity == "item":
		rda_iri = 'http://rdaregistry.info/Elements/i/'
		from functions.lists import skip_item_props as skip_prop_list
	else:
		print("Entity not recognized.")
		quit()

	property_kiegel_list = []
	for csv_file in file_list:
		with open(f"{csv_dir}/{csv_file}") as file:
			csv_reader = csv.reader(file, delimiter=',')
			line_count = 0
			for line in csv_reader:
				if line_count == 0: # ignore header row
					pass
				elif "rdf-syntax" in line[1]:
					pass
				elif line[1].strip(rda_iri) in skip_prop_list:
					pass
				elif "P10002" in line[1] or "P20002" in line[1] or "P30004" in line[1] or "P40001" in line[1]:
					pass
				else:
					"""Find property number"""
					prop_IRI = line[1]
					if "rdaregistry" in prop_IRI:
						prop_num = prop_IRI.lstrip(rda_iri)
					else:
						prop_num = prop_IRI.lstrip('https://doi.org/10.6069/uwlib.55.d.4')
						prop_num = prop_num.strip('#')

					"""Find kiegel"""
					kiegel = line[3]
					# remove subclass variables, if they exist
					if ".subclass" in kiegel:
						split_kiegel = kiegel.split("\nor\n")
						for line in split_kiegel:
							if ".subclass" in line:
								split_kiegel.remove(line)
						kiegel = "\nor\n".join(split_kiegel)

					"""Create tuple and add to list"""
					property_kiegel_tuple = (prop_num, kiegel)
					property_kiegel_list.append(property_kiegel_tuple)
				line_count += 1

	return property_kiegel_list

def create_kiegel_dict(csv_dir, entity):
	"""Create dictionary ["property number": [kiegel split into list]"""
	kiegel_dict = {}

	property_kiegel_list = get_property_kiegel_list(csv_dir, entity)
	for tuple in property_kiegel_list:
		property_number = tuple[0]
		kiegel_dict[property_number] = []

		"""Turn kiegel into list"""
		kiegel = tuple[1]
		mapping_dict = edit_kiegel(kiegel)
		kiegel_dict[property_number] = mapping_dict

	return kiegel_dict
