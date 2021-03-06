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

def work_1_ttl_to_json(currentDate):
	# create list of work_1s in turtle
	work_1_ttl_list = os.listdir(f'../output/{currentDate}/work_1_ttl')

	# create work_1 json directory
	if not os.path.exists(f'../output/{currentDate}/work_1_json'):
		print(f'...\nCreating work_1 directory')
		os.makedirs(f'../output/{currentDate}/work_1_json')

	print("...")

	bar = Bar(f'Transforming {len(work_1_ttl_list)} work_1 files from Turtle to JSON-LD', max=len(work_1_ttl_list), suffix='%(percent)d%%')
	for work in work_1_ttl_list:
		# create new empty graph
		Graph_localWork_1 = Graph()
		# bind namespaces to graph
		Graph_localWork_1.bind('bf', bf)
		Graph_localWork_1.bind('bflc', bflc)
		Graph_localWork_1.bind('madsrdf', madsrdf)
		# add turtle file to new graph
		Graph_localWork_1.load(f'file:../output/{currentDate}/work_1_ttl/{work}', format='turtle')
		# serialize graph as JSON-LD
		Graph_localWork_1.serialize(destination=f'../output/{currentDate}/work_1_json/' + work.split('.')[0] + ".json", format="json-ld")
		bar.next()
	bar.finish()

def work_2_ttl_to_json(currentDate):
	# create list of work 2s in turtle
	work_2_ttl_list = os.listdir(f'../output/{currentDate}/work_2_ttl')

	# create work 2 json directory
	if not os.path.exists(f'../output/{currentDate}/work_2_json'):
		print(f'...\nCreating work_2 directory')
		os.makedirs(f'../output/{currentDate}/work_2_json')

	print("...")

	bar = Bar(f'Transforming {len(work_2_ttl_list)} work 2 files from Turtle to JSON-LD', max=len(work_2_ttl_list), suffix='%(percent)d%%')
	for work in work_2_ttl_list:
		# create new empty graph
		Graph_localWork_2 = Graph()
		# bind namespaces to graph
		Graph_localWork_2.bind('bf', bf)
		Graph_localWork_2.bind('bflc', bflc)
		Graph_localWork_2.bind('madsrdf', madsrdf)
		# add turtle file to new graph
		Graph_localWork_2.load(f'file:../output/{currentDate}/work_2_ttl/{work}', format='turtle')
		# serialize graph as JSON-LD
		Graph_localWork_2.serialize(destination=f'../output/{currentDate}/work_2_json/' + work.split('.')[0] + ".json", format="json-ld")
		bar.next()
	bar.finish()

def instance_ttl_to_json(currentDate):
	# create list of instances in turtle
	instance_ttl_list = os.listdir(f'../output/{currentDate}/instance_ttl')

	# create instance json directory
	if not os.path.exists(f'../output/{currentDate}/instance_json'):
		print(f'...\nCreating instance directory')
		os.makedirs(f'../output/{currentDate}/instance_json')

	print("...")

	bar = Bar(f'Transforming {len(instance_ttl_list)} instance files from Turtle to JSON-LD', max=len(instance_ttl_list), suffix='%(percent)d%%')
	for instance in instance_ttl_list:
		# create new empty graph
		Graph_localInstance = Graph()
		# bind namespaces to graph
		Graph_localInstance.bind('bf', bf)
		Graph_localInstance.bind('bflc', bflc)
		Graph_localInstance.bind('madsrdf', madsrdf)
		# add turtle file to new graph
		Graph_localInstance.load(f'file:../output/{currentDate}/instance_ttl/{instance}', format='turtle')
		# serialize graph as JSON-LD
		Graph_localInstance.serialize(destination=f'../output/{currentDate}/instance_json/' + instance.split('.')[0] + ".json", format="json-ld")
		bar.next()
	bar.finish()

def item_ttl_to_json(currentDate):
	# create list of items in turtle
	item_ttl_list = os.listdir(f'../output/{currentDate}/item_ttl')

	# create item json directory
	if not os.path.exists(f'../output/{currentDate}/item_json'):
		print(f'...\nCreating item directory')
		os.makedirs(f'../output/{currentDate}/item_json')

	print("...")

	bar = Bar(f'Transforming {len(item_ttl_list)} item files from Turtle to JSON-LD', max=len(item_ttl_list), suffix='%(percent)d%%')
	for item in item_ttl_list:
		# create new empty graph
		Graph_localItem = Graph()
		# bind namespaces to graph
		Graph_localItem.bind('bf', bf)
		Graph_localItem.bind('bflc', bflc)
		Graph_localItem.bind('madsrdf', madsrdf)
		# add turtle file to new graph
		Graph_localItem.load(f'file:../output/{currentDate}/item_ttl/{item}', format='turtle')
		# serialize graph as JSON-LD
		Graph_localItem.serialize(destination=f'../output/{currentDate}/item_json/' + item.split('.')[0] + ".json", format="json-ld")
		bar.next()
	bar.finish()

"""Variables"""

# format for naming folder according to date
today = date.today()
currentDate = str(today).replace('-', '_')

###

print("...\nReserializing Turtle output as JSON-LD")
work_1_ttl_to_json(currentDate)
work_2_ttl_to_json(currentDate)
instance_ttl_to_json(currentDate)
item_ttl_to_json(currentDate)
