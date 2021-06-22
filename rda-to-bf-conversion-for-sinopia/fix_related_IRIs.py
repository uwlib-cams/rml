from arguments import define_arg
import csv
from datetime import date
import os
from progress.bar import Bar
from rdflib import *
from reserialize import reserialize
from timeit import default_timer as timer
import xml.etree.ElementTree as ET

"""Variables"""

# format for naming folder according to date
today = date.today()
currentDate = str(today).replace('-', '_')

# arguments from command line
args = define_arg()
output_location = args.output

"""Lists and Dictionaries"""

work_1List = os.listdir(f'{output_location}/{currentDate}/work_1_xml')
work_2List = os.listdir(f'{output_location}/{currentDate}/work_2_xml')
instanceList = os.listdir(f'{output_location}/{currentDate}/instance_xml')
itemList = os.listdir(f'{output_location}/{currentDate}/item_xml')
resource_dict = {"work_1": work_1List, "work_2": work_2List, "instance": instanceList, "item": itemList}

"""Functions"""

def fix_related_IRIs(RDA_ID, BF_ID, entity, file, output_location):
	num_of_edits = 0
	edit = False

	# open xml parser
	tree = ET.parse(f'{output_location}/{currentDate}/{entity}_xml/{file}')
	root = tree.getroot()

	for child in root: # for each node...
		for prop in child: # for each property in node...
			if '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource' in prop.attrib.keys(): # if the value is an IRI...
				RDA_IRI = f'https://api.sinopia.io/resource/{RDA_ID}'
				if prop.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource'] == RDA_IRI: # if that IRI is the RDA IRI in question
					if prop.tag != '{http://www.w3.org/2002/07/owl#}sameAs': # and it is NOT our owl:sameAs triple, which should be left alone
						BF_IRI = f'https://api.sinopia.io/resource/{BF_ID}'
						prop.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource', BF_IRI) # replace it with its equivalent BF IRI
						num_of_edits += 1
						edit = True

	if edit == True: # only rewrite / reserialize if an edit was made
		tree.write(f'{output_location}/{currentDate}/{entity}_xml/{file}')

		reserialize(f'{output_location}/{currentDate}/{entity}_xml/{file}', f'{output_location}/{currentDate}/{entity}_xml/{file}', 'xml')

	return num_of_edits

###

start = timer()
with open(f"RDA_BF_IRI_list_{currentDate}.csv", mode="r") as key_file:
	"""Get number of IRI pairs to iterate through"""
	csv_reader = csv.reader(key_file, delimiter=',')
	total_line_count = 0

	for line in csv_reader:
		total_line_count += 1

num_of_edits = 0

with open(f"RDA_BF_IRI_list_{currentDate}.csv", mode="r") as key_file:
	"""For each resource, look for IRI pairs and make appropriate changes"""
	csv_reader = csv.reader(key_file, delimiter=',')
	line_count = 0
	num_of_edits = 0

	bar = Bar(">> Replacing RDA IRIs with BIBFRAME IRIs", max=total_line_count, suffix='%(percent)d%%') # progress bar
	for line in csv_reader:
		if line_count == 0: # skip header row
			pass
		else:
			RDA_ID = line[0]
			BF_ID = line[1]

			for entity in resource_dict.keys():
				for resource in resource_dict[entity]:
					edits_made = fix_related_IRIs(RDA_ID, BF_ID, entity, resource, output_location)
					num_of_edits += edits_made
		line_count += 1
		bar.next()
	end = timer()
	bar.finish()

print(f"IRIs fixed: {num_of_edits}")
print(f"Elapsed time: {round((end - start), 1)} s")
