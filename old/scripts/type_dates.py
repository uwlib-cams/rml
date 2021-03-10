import os
from datetime import date

"""Variables"""

today = date.today()
currentDate = str(today).replace('-','_')

"""Functions"""

def type_snapshot(line):
	spacing = line.split('rdfs:')[0]
	edited_line = line.strip()

	punctuation = edited_line.split('"')[-1]

	edited_line = edited_line.strip(punctuation)
	edited_line = spacing + edited_line + "^^xsd:dateTime" + punctuation + "\n"

	return edited_line

def determine_date_type(line):
	value = line.split('"')[1]

	dash_count = 0
	for character in value:
		if character == '-':
			dash_count += 1

	if dash_count == 0: # e.g. "1886"
		date_type = "gYear"
	elif dash_count == 1: # e.g. "1886-02"
		date_type = "gYearMonth"
	elif dash_count == 2: # e.g. "1886-02-14"
		date_type = "date"

	return date_type

def type_date(line, date_type):
	spacing = line.split('bf:')[0]
	edited_line = line.strip()

	punctuation = edited_line.split('"')[-1]

	edited_line = edited_line.strip(punctuation)
	edited_line = spacing + edited_line + f"^^xsd:{date_type}" + punctuation + "\n"

	return edited_line

"""Lists and Dictionaries"""

bf_date_prop_list = ["date", "originDate", "legalDate", "copyrightDate", "changeDate", "creationDate", "generationDate"]

work_1_list = os.listdir(f"../output/{currentDate}/work_1_ttl/")
work_2_list = os.listdir(f"../output/{currentDate}/work_2_ttl/")
instance_list = os.listdir(f"../output/{currentDate}/instance_ttl/")
item_list = os.listdir(f"../output/{currentDate}/item_ttl/")

resource_dict = {"work_1": work_1_list, "work_2": work_2_list, "instance": instance_list, "item": item_list}

###

for entity in resource_dict.keys():
	resource_list = resource_dict[entity]
	for resource in resource_list:
		with open(f"../output/{currentDate}/{entity}_ttl/{resource}", "r") as input_file:
			output_file_lines = []

			row_count = 0

			for line in input_file:
				# preserve prefixes
				if "@prefix" in line:
					output_file_lines.append(line)
					row_count += 1

				elif "rml.py SNAPSHOT:" in line:
					edited_line = type_snapshot(line)
					output_file_lines.append(edited_line)

				else:
					prop = line.split('bf:')[-1]
					prop = line.split(' ')[0]

					if prop in bf_date_prop_list:
						date_type = determine_date_type(line)
						edited_line = type_date(line, date_type)
						output_file_lines.append(edited_line)
					else:
						output_file_lines.append(line)
			output_file_lines[row_count] = output_file_lines[row_count].strip() + "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\n" # add prefix for datatypes after last prefix
		with open(f"../output/{currentDate}/{entity}_ttl/{resource}", "w") as output_file:
			for line in output_file_lines:
				output_file.write(line)
