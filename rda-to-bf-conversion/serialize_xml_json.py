from datetime import date
import os
from progress.bar import Bar
from rdflib import *
import rdflib
import time

"""Namespaces"""

bf = Namespace('http://id.loc.gov/ontologies/bibframe/')
bflc = Namespace('http://id.loc.gov/ontologies/bflc/')
madsrdf = Namespace('http://www.loc.gov/mads/rdf/v1#')

"""Functions"""

def work_1_xml_to_json(currentDate):
	# create list of work_1s in XML
	work_1_xml_list = os.listdir(f'../output/{currentDate}/work_1_xml')

	# create work_1 json directory
	if not os.path.exists(f'../output/{currentDate}/work_1_json'):
		print(f'...\nCreating work_1 directory')
		os.makedirs(f'../output/{currentDate}/work_1_json')

	print("...")

	bar = Bar(f'Transforming {len(work_1_xml_list)} work_1 files from XML to JSON-LD', max=len(work_1_xml_list), suffix='%(percent)d%%')
	for work in work_1_xml_list:
		# create new empty graph
		Graph_localWork_1 = Graph()
		# bind namespaces to graph
		Graph_localWork_1.bind('bf', bf)
		Graph_localWork_1.bind('bflc', bflc)
		Graph_localWork_1.bind('madsrdf', madsrdf)
		# add XML file to new graph
		Graph_localWork_1.load(f'file:../output/{currentDate}/work_1_xml/{work}', format='xml')
		# serialize graph as JSON-LD
		Graph_localWork_1.serialize(destination=f'../output/{currentDate}/work_1_json/' + work.split('.')[0] + ".json", format="json-ld")
		bar.next()
	bar.finish()

def work_2_xml_to_json(currentDate):
	# create list of work 2s in XML
	work_2_xml_list = os.listdir(f'../output/{currentDate}/work_2_xml')

	# create work 2 json directory
	if not os.path.exists(f'../output/{currentDate}/work_2_json'):
		print(f'...\nCreating work_2 directory')
		os.makedirs(f'../output/{currentDate}/work_2_json')

	print("...")

	bar = Bar(f'Transforming {len(work_2_xml_list)} work 2 files from XML to JSON-LD', max=len(work_2_xml_list), suffix='%(percent)d%%')
	for work in work_2_xml_list:
		# create new empty graph
		Graph_localWork_2 = Graph()
		# bind namespaces to graph
		Graph_localWork_2.bind('bf', bf)
		Graph_localWork_2.bind('bflc', bflc)
		Graph_localWork_2.bind('madsrdf', madsrdf)
		# add XML file to new graph
		Graph_localWork_2.load(f'file:../output/{currentDate}/work_2_xml/{work}', format='xml')
		# serialize graph as JSON-LD
		Graph_localWork_2.serialize(destination=f'../output/{currentDate}/work_2_json/' + work.split('.')[0] + ".json", format="json-ld")
		bar.next()
	bar.finish()

def instance_xml_to_json(currentDate):
	# create list of instances in XML
	instance_xml_list = os.listdir(f'../output/{currentDate}/instance_xml')

	# create instance json directory
	if not os.path.exists(f'../output/{currentDate}/instance_json'):
		print(f'...\nCreating instance directory')
		os.makedirs(f'../output/{currentDate}/instance_json')

	print("...")

	bar = Bar(f'Transforming {len(instance_xml_list)} instance files from XML to JSON-LD', max=len(instance_xml_list), suffix='%(percent)d%%')
	for instance in instance_xml_list:
		# create new empty graph
		Graph_localInstance = Graph()
		# bind namespaces to graph
		Graph_localInstance.bind('bf', bf)
		Graph_localInstance.bind('bflc', bflc)
		Graph_localInstance.bind('madsrdf', madsrdf)
		# add XML file to new graph
		Graph_localInstance.load(f'file:../output/{currentDate}/instance_xml/{instance}', format='xml')
		# serialize graph as JSON-LD
		Graph_localInstance.serialize(destination=f'../output/{currentDate}/instance_json/' + instance.split('.')[0] + ".json", format="json-ld")
		bar.next()
	bar.finish()

def item_xml_to_json(currentDate):
	# create list of items in XML
	item_xml_list = os.listdir(f'../output/{currentDate}/item_xml')

	# create item json directory
	if not os.path.exists(f'../output/{currentDate}/item_json'):
		print(f'...\nCreating item directory')
		os.makedirs(f'../output/{currentDate}/item_json')

	print("...")

	bar = Bar(f'Transforming {len(item_xml_list)} item files from XML to JSON-LD', max=len(item_xml_list), suffix='%(percent)d%%')
	for item in item_xml_list:
		# create new empty graph
		Graph_localItem = Graph()
		# bind namespaces to graph
		Graph_localItem.bind('bf', bf)
		Graph_localItem.bind('bflc', bflc)
		Graph_localItem.bind('madsrdf', madsrdf)
		# add XML file to new graph
		Graph_localItem.load(f'file:../output/{currentDate}/item_xml/{item}', format='xml')
		# serialize graph as JSON-LD
		Graph_localItem.serialize(destination=f'../output/{currentDate}/item_json/' + item.split('.')[0] + ".json", format="json-ld")
		bar.next()
	bar.finish()

"""Variables"""

# format for naming folder according to date
today = date.today()
currentDate = str(today).replace('-', '_')

###

print("...\nReserializing XML output as JSON-LD")
work_1_xml_to_json(currentDate)
work_2_xml_to_json(currentDate)
instance_xml_to_json(currentDate)
item_xml_to_json(currentDate)
