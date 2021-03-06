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

"""Namespaces"""

bf = Namespace('http://id.loc.gov/ontologies/bibframe/')
bflc = Namespace('http://id.loc.gov/ontologies/bflc/')
madsrdf = Namespace('http://www.loc.gov/mads/rdf/v1#')
owl = Namespace('http://www.w3.org/2002/07/owl#')
rdac = Namespace('http://rdaregistry.info/Elements/c/')
rdae = Namespace('http://rdaregistry.info/Elements/e/')
rdai = Namespace('http://rdaregistry.info/Elements/i/')
rdam = Namespace('http://rdaregistry.info/Elements/m/')
rdamdt = Namespace('http://rdaregistry.info/Elements/m/datatype/')
rdaw = Namespace('http://rdaregistry.info/Elements/w/')
rdax = Namespace('https://doi.org/10.6069/uwlib.55.d.4#')
sin = Namespace('http://sinopia.io/vocabulary/')

"""Functions"""

def add_triple_to_xml(entity, file, new_IRI):
	"""Add triple stating that new BF resource owl:sameAs old RDA resource"""
	file = file.split('.')[0] + '.xml'

	# open xml parser
	tree = ET.parse(f'../input/{currentDate}/{entity}/{file}')
	root = tree.getroot()

	ns = {'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#', 'owl': 'http://www.w3.org/2002/07/owl#'}

	# append owl:sameAs
	for desc in root.findall('rdf:Description', ns):
		# create dictionary of attributes for description
		attrib_dict = desc.attrib

		# if it contains rdf:about as an attribute...
		if '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about' in attrib_dict.keys():
			# write in owl:sameAs
			ET.SubElement(desc, '{http://www.w3.org/2002/07/owl#}sameAs')

	# add value for owl:sameAs
	for owl_new_triple in root.findall('rdf:Description/owl:sameAs', ns):
		owl_new_triple.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource', new_IRI)

	# write new XML to a temporary file
	tree.write('temp.xml')

	# reserialize with rdflib to fix namespaces and UTF-8
	g = Graph()
	g.bind('bf', bf)
	g.bind('bflc', bflc)
	g.bind('madsrdf', madsrdf)
	g.bind('owl', owl)
	g.bind('rdac', rdac)
	g.bind('rdae', rdae)
	g.bind('rdai', rdai)
	g.bind('rdam', rdam)
	g.bind('rdamdt', rdamdt)
	g.bind('rdaw', rdaw)
	g.bind('rdax', rdax)
	g.bind('sin', sin)
	g.load(f'file:temp.xml', format='xml')
	g.serialize(destination=f'../input/{currentDate}/{entity}/{file}', format='xml')

def replace_IRIs(entity, resource, old_IRI, new_IRI):
	"""Replace old IRI from original RDA/RDF with new IRI for new BIBFRAME"""
	original = open(f"../output/{currentDate}/{entity}_json/{resource}", "rt")
	edit = original.read()
	edit = edit.replace(old_IRI, new_IRI)
	original.close()
	new = open(f"../output/{currentDate}/{entity}_json/{resource}", "wt")
	new.write(edit)
	new.close()

"""Variables"""

# format for naming folder according to date
today = date.today()
currentDate = str(today).replace('-', '_')

"""Lists and Dictionaries"""

work_1_json_list = os.listdir(f"../output/{currentDate}/work_1_json/")
work_2_json_list = os.listdir(f"../output/{currentDate}/work_2_json/")
instance_json_list = os.listdir(f"../output/{currentDate}/instance_json/")
item_json_list = os.listdir(f"../output/{currentDate}/item_json/")

resource_dict = {"work_1": work_1_json_list, "work_2": work_2_json_list, "instance": instance_json_list, "item": item_json_list}
bf_rda_entities_dict = {'work_1': 'work', 'work_2': 'expression', 'instance': 'manifestation', 'item': 'item'}

###

if not os.path.exists(f'RDA_BF_URI_list_{currentDate}.csv'):
	print("...\nCreating RDA IRI to BF IRI key")
	os.system(f'touch RDA_BF_URI_list_{currentDate}.csv')

print("...\nGenerating new IRIs for BF resources")

print("...")

# record old and new IRIs in central CSV file for easy reference
with open(f"RDA_BF_URI_list_{currentDate}.csv", mode="w") as csv_output:
	csv_writer = csv.writer(csv_output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

	# write header row
	csv_writer.writerow(['original_RDA_identifier','rda_entity','equivalent_BF_identifier','bf_entity'])

	for entity in resource_dict.keys():
		bar = Bar(f'Adding new IRIs to BIBFRAME {entity} resources', max=len(resource_dict[entity]), suffix='%(percent)d%%')
		for resource in resource_dict[entity]:
			# find identifier for RDA
			old_identifier = resource.split('.')[0]
			old_IRI = f"https://api.sinopia.io/resource/{old_identifier}"

			# generate new identifier for BF
			new_identifier = uuid.uuid4()
			new_IRI = f"https://api.sinopia.io/resource/{new_identifier}"

			# record in CSV file
			csv_writer.writerow([f'{old_identifier}',f'{bf_rda_entities_dict[entity]}',f'{new_identifier}',f'{entity.split("_")[0]}'])

			# record in original RDA/RDF
			add_triple_to_xml(bf_rda_entities_dict[entity], resource, new_IRI)

			# replace identifier in BF
			replace_IRIs(entity, resource, old_IRI, new_IRI)

			# rename BF file to new identifier
			os.system(f'mv ../output/{currentDate}/{entity}_json/{old_identifier}.json ../output/{currentDate}/{entity}_json/{new_identifier}.json')

			bar.next()
		bar.finish()
