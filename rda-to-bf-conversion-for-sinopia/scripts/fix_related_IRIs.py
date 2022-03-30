"""Python Libraries/Modules/Packages"""
import csv
from datetime import date
import os
from progress.bar import Bar
import rdflib
from rdflib import *
from timeit import default_timer as timer

"""Imported Functions"""
from scripts.arguments import define_arg

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
def find_IRIs_to_fix(output_location, resource_dict, rda_bf_dict):
	fix_dict = {}

	for entity in resource_dict.keys():
		for resource in resource_dict[entity]:
			g = Graph()

			g.load(f'{output_location}/{currentDate}/{entity}_xml/{resource}', format="xml")

			for s, p, o in g:
				if isinstance(o, rdflib.term.URIRef) == True:
					if p != URIRef("http://www.w3.org/2002/07/owl#sameAs"):
						if o[0:32] == "https://api.sinopia.io/resource/":
							# add to dict
							if resource not in fix_dict.keys():
								fix_dict[resource] = []

							RDA_ID = o.split("/")[-1]
							if RDA_ID in rda_bf_dict.keys():
								BF_ID = rda_bf_dict[RDA_ID]
							else: # the IRI found in this triple is not for a resource we know
								print(f"Error: RDA IRI https://api.sinopia.io/resource/{RDA_ID} found in {output_location}/{currentDate}/{entity}_xml/{resource}, but no equivalent BIBFRAME IRI is found in other_files/set_IRIs.csv. Is this IRI correct?")
								continue
							new_object = URIRef(f"https://api.sinopia.io/resource/{BF_ID}")
							tuple = (entity, s, p, o, new_object)

							fix_dict[resource].append(tuple)

	return fix_dict

def fix_related_IRIs(file, tuple, output_location):
	entity = tuple[0]
	s = tuple[1]
	p = tuple[2]
	o = tuple[3]
	new_object = tuple[4]

	g = Graph()

	g.load(f'{output_location}/{currentDate}/{entity}_xml/{file}', format="xml")

	g.remove((s, p, o))
	g.add((s, p, new_object))

	g.serialize(destination=f'{output_location}/{currentDate}/{entity}_xml/{file}', format="xml")

###

start = timer()

num_of_edits = 0
rda_bf_dict = {}

with open(f"other_files/set_IRIs.csv", mode="r") as key_file:
	"""For each resource, look for IRI pairs and make appropriate changes"""
	csv_reader = csv.reader(key_file, delimiter=',')
	line_count = 0
	for line in csv_reader:
		if line_count == 0: # skip header row
			pass
		else:
			RDA_ID = line[0]
			BF_ID = line[1]

			rda_bf_dict[RDA_ID] = BF_ID

		line_count += 1

fix_dict = find_IRIs_to_fix(output_location, resource_dict, rda_bf_dict)

max_len = 0
for key in fix_dict.keys():
	list = fix_dict[key]
	max_len += len(list)

bar = Bar(">> Replacing RDA IRIs with BIBFRAME IRIs", max=max_len, suffix='%(percent)d%%') # progress bar
for resource in fix_dict.keys():
	for tuple in fix_dict[resource]:
		edits_made = fix_related_IRIs(resource, tuple, output_location)
		bar.next()
end = timer()
bar.finish()

print(f"IRIs fixed: {max_len}")
print(f"Elapsed time: {round((end - start), 1)} s")
