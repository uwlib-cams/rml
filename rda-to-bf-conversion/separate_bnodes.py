from sys import argv
import os
import time
from rdflib import *
import rdflib
from datetime import date
import uuid
from progress.bar import Bar
import requests
import csv
import xml.etree.ElementTree as ET

def replace_bnodes_w_IRIs(currentDate, entity, file):
	# open xml parser
	tree = ET.parse(f'../output/{currentDate}/{entity}_xml/{file}')
	root = tree.getroot()

	ns = {'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'}

	bnode_IRI_dict = {}

	for child in root: # resource and blank nodes
		if "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}nodeID" in child.attrib.keys(): # just blank nodes
			bnode_ID = child.attrib["{http://www.w3.org/1999/02/22-rdf-syntax-ns#}nodeID"]

			# generate new IRI
			new_identifier = uuid.uuid4()
			new_IRI = f"https://api.sinopia.io/resource/{new_identifier}"

			bnode_IRI_dict[bnode_ID] = new_IRI

	for bnode_ID in bnode_IRI_dict.keys(): # for each blank node ID...
		new_IRI = bnode_IRI_dict[bnode_ID]
		# find the blank node
		for child in root: # resource and blank nodes
			if "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}nodeID" in child.attrib.keys(): # just blank nodes
				if child.attrib["{http://www.w3.org/1999/02/22-rdf-syntax-ns#}nodeID"] == bnode_ID:
					child.attrib.pop("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}nodeID")
					child.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about', new_IRI)
		# find the triple where it's referenced
			else:
				for prop in child: # look for properties within node
					if "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}nodeID" in prop.attrib.keys():
						if prop.attrib["{http://www.w3.org/1999/02/22-rdf-syntax-ns#}nodeID"] == bnode_ID:
							prop.clear()
							prop.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource', new_IRI)

	tree.write(f'../output/{currentDate}/{entity}_xml/{file}')

def gen_bnode_list(currentDate, entity, file):
	bnode_list = []
	# open xml parser
	tree = ET.parse(f'../output/{currentDate}/{entity}_xml/{file}')
	root = tree.getroot()

	for child in root:
		if child.attrib["{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about"] != f"https://api.sinopia.io/resource/{file.split('.')[0]}":
			bnode_IRI = child.attrib["{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about"]
			bnode_list.append(bnode_IRI)

	bnode_list.append(f"https://api.sinopia.io/resource/{file.split('.')[0]}") # original resource has to be done last

	return bnode_list

def create_new_bnode_file(currentDate, entity, file, bnode):
	# write data to new XML file
	bnode_ID = bnode.split('/')[-1]
	os.system(f'touch ../output/{currentDate}/{entity}_xml/{bnode_ID}.xml')

	tree = ET.parse(f'../output/{currentDate}/{entity}_xml/{file}')
	root = tree.getroot()

	tree.write(f'../output/{currentDate}/{entity}_xml/{bnode_ID}.xml')

	# erase unnecessary data from new XML file
	tree = ET.parse(f'../output/{currentDate}/{entity}_xml/{bnode_ID}.xml')
	root = tree.getroot()

	remove_list = []

	for child in root:
		if child.attrib["{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about"] != bnode:
			remove_list.append(child)

	for child in remove_list:
		root.remove(child)

	tree.write(f'../output/{currentDate}/{entity}_xml/{bnode_ID}.xml')

"""Variables"""

# format for naming folder according to date
today = date.today()
currentDate = str(today).replace('-', '_')

"""Lists and Dictionaries"""

work_1List = os.listdir(f'../output/{currentDate}/work_1_xml')
work_2List = os.listdir(f'../output/{currentDate}/work_2_xml')
instanceList = os.listdir(f'../output/{currentDate}/instance_xml')
itemList = os.listdir(f'../output/{currentDate}/item_xml')
entity_dict = {"work_1": work_1List, "work_2": work_2List, "instance": instanceList, "item": itemList}

###

for entity in entity_dict.keys():
	for resource in entity_dict[entity]:
		replace_bnodes_w_IRIs(currentDate, entity, resource)

		bnode_list = gen_bnode_list(currentDate, entity, resource)
		print(bnode_list)

		for bnode in bnode_list:
			create_new_bnode_file(currentDate, entity, file, resource)
