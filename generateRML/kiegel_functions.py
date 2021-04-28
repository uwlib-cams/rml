"""Python Libraries/Modules/Packages"""
import csv
import os

"""Lists"""
from lists import skip_expression_props
from lists import skip_item_props
from lists import skip_manifestation_props
from lists import skip_work_props

"""Functions"""
def get_work_property_list(csv_dir):
	csv_file_list = os.listdir(csv_dir)
	work_files = []
	for file in csv_file_list:
		if "work" in file:
			work_files.append(file)

	work_property_list = []
	for csv_file in work_files:
		with open(f"{csv_dir}/{csv_file}") as file:
			csv_reader = csv.reader(file, delimiter=',')
			line_count = 0
			for line in csv_reader:
				if line_count == 0: # ignore header row
					pass
				elif line[1].strip('http://rdaregistry.info/Elements/w/') in skip_work_props:
					pass
				elif "rdf-syntax" in line[1]:
					pass
				else:
					prop_IRI = line[1]
					if "rdaregistry" in prop_IRI:
						prop_num = prop_IRI.lstrip('http://rdaregistry.info/Elements/w/')
					else:
						prop_num = prop_IRI.lstrip('https://doi.org/10.6069/uwlib.55.d.4')
						prop_num = prop_num.strip('#')

					work_property_list.append(prop_num)
				line_count += 1

	return work_property_list

def get_work_kiegel_list(csv_dir):
	csv_file_list = os.listdir(csv_dir)
	work_files = []
	for file in csv_file_list:
		if "work" in file:
			work_files.append(file)

	work_kiegel_list = []
	for csv_file in work_files:
		with open(f"{csv_dir}/{csv_file}") as file:
			csv_reader = csv.reader(file, delimiter=',')
			line_count = 0
			for line in csv_reader:
				if line_count == 0: # ignore header row
					pass
				elif line[1].strip('http://rdaregistry.info/Elements/w/') in skip_work_props:
					pass
				elif "rdf-syntax" in line[1]:
					pass
				else:
					kiegel = line[3]

					if ".subclass" in kiegel:
						kiegel_split = kiegel.split("\nor\n")
						for line in kiegel_split:
							if ".subclass" in line:
								kiegel_split.remove(line)
						kiegel = "\nor\n".join(kiegel_split)

					work_kiegel_list.append(kiegel)
				line_count += 1

	return work_kiegel_list

def get_expression_property_list(csv_dir):
	csv_file_list = os.listdir(csv_dir)
	expression_files = []
	for file in csv_file_list:
		if "expression" in file:
			expression_files.append(file)

	expression_property_list = []
	for csv_file in expression_files:
		with open(f"{csv_dir}/{csv_file}") as file:
			csv_reader = csv.reader(file, delimiter=',')
			line_count = 0
			for line in csv_reader:
				if line_count == 0: # ignore header row
					pass
				elif line[1].strip('http://rdaregistry.info/Elements/e/') in skip_expression_props:
					pass
				elif "rdf-syntax" in line[1]:
					pass
				else:
					prop_IRI = line[1]
					if "rdaregistry" in prop_IRI:
						prop_num = prop_IRI.lstrip('http://rdaregistry.info/Elements/e/')
					else:
						prop_num = prop_IRI.lstrip('https://doi.org/10.6069/uwlib.55.d.4')
						prop_num = prop_num.strip('#')

					expression_property_list.append(prop_num)
				line_count += 1

	return expression_property_list

def get_expression_kiegel_list(csv_dir):
	csv_file_list = os.listdir(csv_dir)
	expression_files = []
	for file in csv_file_list:
		if "expression" in file:
			expression_files.append(file)

	expression_kiegel_list = []
	for csv_file in expression_files:
		with open(f"{csv_dir}/{csv_file}") as file:
			csv_reader = csv.reader(file, delimiter=',')
			line_count = 0
			for line in csv_reader:
				if line_count == 0: # ignore header row
					pass
				elif line[1].strip('http://rdaregistry.info/Elements/e/') in skip_expression_props:
					pass
				elif "rdf-syntax" in line[1]:
					pass
				else:
					kiegel = line[3]

					if ".subclass" in kiegel:
						kiegel_split = kiegel.split("\nor\n")
						for line in kiegel_split:
							if ".subclass" in line:
								kiegel_split.remove(line)
						kiegel = "\nor\n".join(kiegel_split)

					expression_kiegel_list.append(kiegel)
				line_count += 1

	return expression_kiegel_list

def get_manifestation_kiegel_list(csv_dir):
	csv_file_list = os.listdir(csv_dir)
	manifestation_files = []
	for file in csv_file_list:
		if "manifestation" in file:
			manifestation_files.append(file)

	manifestation_kiegel_list = []
	for csv_file in manifestation_files:
		with open(f"{csv_dir}/{csv_file}") as file:
			csv_reader = csv.reader(file, delimiter=',')
			line_count = 0
			for line in csv_reader:
				if line_count == 0: # ignore header row
					pass
				elif line[1].strip('http://rdaregistry.info/Elements/m/') in skip_manifestation_props:
					pass
				elif "rdf-syntax" in line[1]:
					pass
				else:
					kiegel = line[3]

					if ".subclass" in kiegel:
						kiegel_split = kiegel.split("\nor\n")
						for line in kiegel_split:
							if ".subclass" in line:
								kiegel_split.remove(line)
						kiegel = "\nor\n".join(kiegel_split)

					manifestation_kiegel_list.append(kiegel)
				line_count += 1

	return manifestation_kiegel_list

def get_manifestation_property_list(csv_dir):
	csv_file_list = os.listdir(csv_dir)
	manifestation_files = []
	for file in csv_file_list:
		if "manifestation" in file:
			manifestation_files.append(file)

	manifestation_property_list = []
	for csv_file in manifestation_files:
		with open(f"{csv_dir}/{csv_file}") as file:
			csv_reader = csv.reader(file, delimiter=',')
			line_count = 0
			for line in csv_reader:
				if line_count == 0: # ignore header row
					pass
				elif line[1].strip('http://rdaregistry.info/Elements/m/') in skip_manifestation_props:
					pass
				elif "rdf-syntax" in line[1]:
					pass
				else:
					prop_IRI = line[1]
					if "rdaregistry" in prop_IRI:
						prop_num = prop_IRI.lstrip('http://rdaregistry.info/Elements/m/')
					else:
						prop_num = prop_IRI.lstrip('https://doi.org/10.6069/uwlib.55.d.4')
						prop_num = prop_num.strip('#')

					manifestation_property_list.append(prop_num)
				line_count += 1

	return manifestation_property_list

def get_item_property_list(csv_dir):
	csv_file_list = os.listdir(csv_dir)
	item_files = []
	for file in csv_file_list:
		if "item" in file:
			item_files.append(file)

	item_property_list = []
	for csv_file in item_files:
		with open(f"{csv_dir}/{csv_file}") as file:
			csv_reader = csv.reader(file, delimiter=',')
			line_count = 0
			for line in csv_reader:
				if line_count == 0: # ignore header row
					pass
				elif line[1].strip('http://rdaregistry.info/Elements/i/') in skip_item_props:
					pass
				elif "rdf-syntax" in line[1]:
					pass
				else:
					prop_IRI = line[1]
					if "rdaregistry" in prop_IRI:
						prop_num = prop_IRI.lstrip('http://rdaregistry.info/Elements/i/')
					else:
						prop_num = prop_IRI.lstrip('https://doi.org/10.6069/uwlib.55.d.4')
						prop_num = prop_num.strip('#')

					item_property_list.append(prop_num)
				line_count += 1

	return item_property_list

def get_item_kiegel_list(csv_dir):
	csv_file_list = os.listdir(csv_dir)
	item_files = []
	for file in csv_file_list:
		if "item" in file:
			item_files.append(file)

	item_kiegel_list = []
	for csv_file in item_files:
		with open(f"{csv_dir}/{csv_file}") as file:
			csv_reader = csv.reader(file, delimiter=',')
			line_count = 0
			for line in csv_reader:
				if line_count == 0: # ignore header row
					pass
				elif line[1].strip('http://rdaregistry.info/Elements/i/') in skip_item_props:
					pass
				elif "rdf-syntax" in line[1]:
					pass
				else:
					kiegel = line[3]

					if ".subclass" in kiegel:
						kiegel_split = kiegel.split("\nor\n")
						for line in kiegel_split:
							if ".subclass" in line:
								kiegel_split.remove(line)
						kiegel = "\nor\n".join(kiegel_split)

					item_kiegel_list.append(kiegel)
				line_count += 1

	return item_kiegel_list
