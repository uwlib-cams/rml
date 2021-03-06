# 1. convert RDA to BF, output turtle locally
# 2. convert RDA to BF, output json-ld locally
# 3. convert RDA to BF, output json-ld for upload into sinopia
# 4. upload to sinopia

# should these all happen at once? or should they be optional arguments?

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
LDP = Namespace('http://www.w3.org/ns/ldp#')
bf = Namespace('http://id.loc.gov/ontologies/bibframe/')
bflc = Namespace('http://id.loc.gov/ontologies/bflc/')
dbo = Namespace('http://dbpedia.org/ontology/')
madsrdf = Namespace('http://www.loc.gov/mads/rdf/v1#')
owl = Namespace('http://www.w3.org/2002/07/owl')
rdac = Namespace('http://rdaregistry.info/Elements/c/')
rdae = Namespace('http://rdaregistry.info/Elements/e/')
rdai = Namespace('http://rdaregistry.info/Elements/i/')
rdam = Namespace('http://rdaregistry.info/Elements/m/')
rdamdt = Namespace('http://rdaregistry.info/Elements/m/datatype/')
rdau = Namespace('http://rdaregistry.info/Elements/u/')
rdaw = Namespace('http://rdaregistry.info/Elements/w/')
rdax = Namespace('https://doi.org/10.6069/uwlib.55.d.4#')
sin = Namespace('http://sinopia.io/vocabulary/')

"""Functions"""

## RDFLIB functions

def create_URI_list():
	"""Creates a list of all URIs for all records in UW mongoDB"""
	# pull from mongo + http to get all URIs
	response = requests.get('https://api.sinopia.io/resource?limit=575&group=washington')
	with open('uw_list.json', 'w') as output_file:
		output_file.write(response.text)

	# get URIs from JSON-LD into python list
	os.system('java -jar rmlmapper-4.9.1-r328.jar -m json_rml.ttl -o uw_uri_list.nq')
	URI_list = []
	uriGraph = Graph()
	uriGraph.load('file:uw_uri_list.nq', format='nquads')
	for uri in uriGraph.objects(None, None):
		URI_list.append(uri)
	return URI_list

def save_works(URI_list, currentDate):
	"""Look for works from trellis according to RDA class"""
	# create directory for works
	if not os.path.exists(f'input/{currentDate}/work'):
		print("...\nCreating work directory")
		os.system(f'mkdir input/{currentDate}/work')
	workURIList = []
	bar = Bar('Locating works', max=len(URI_list), suffix='%(percent)d%%')
	for URI in URI_list:
		label = URI.split('/')[-1]
		g = rdflib.Graph()
		g.bind('bf', bf)
		g.bind('bflc', bflc)
		g.bind('rdac', rdac)
		g.bind('rdaw', rdaw)
		g.bind('rdax', rdax)
		g.bind('sin', sin)
		g.bind('madsrdf', madsrdf)
		g.parse(URI, format="json-ld")
		for work in g.subjects(RDF.type, rdac.C10001):
			g.serialize(destination=f'input/{currentDate}/work/' + label + '.xml', format="xml") # serializes in xml
		bar.next()
	bar.finish()
	return workURIList

def save_expressions(URI_list, currentDate, workURIList=[]):
	"""Look for expressions from trellis according to RDA class"""
	# remove works from URI list to save time
	for work in workURIList:
		URI_list.remove(work)
	# create directory for expressions
	if not os.path.exists(f'input/{currentDate}/expression'):
		print("...\nCreating expression directory")
		os.system(f'mkdir input/{currentDate}/expression')
	expressionURIList = []
	bar = Bar('Locating expressions', max=len(URI_list), suffix='%(percent)d%%')
	for URI in URI_list:
		label = URI.split('/')[-1]
		g = rdflib.Graph()
		g.bind('bf', bf)
		g.bind('bflc', bflc)
		g.bind('rdac', rdac)
		g.bind('rdae', rdae)
		g.bind('rdax', rdax)
		g.bind('sin', sin)
		g.bind('madsrdf', madsrdf)
		g.parse(URI, format="json-ld")
		for work in g.subjects(RDF.type, rdac.C10006):
			g.serialize(destination=f'input/{currentDate}/expression/' + label + '.xml', format="xml") # serialize in xml
		bar.next()
	bar.finish()
	return expressionURIList

def save_manifestations(URI_list, currentDate, expressionURIList=[]):
	"""Look for manifestations from trellis according to RDA class"""
	# remove works + expressions from URI list to save time
	for expression in expressionURIList:
		URI_list.remove(expression)
	# create directory for manifestations
	if not os.path.exists(f'input/{currentDate}/manifestation'):
		print("...\nCreating manifestation directory")
		os.system(f'mkdir input/{currentDate}/manifestation')
	manifestationURIList = []
	bar = Bar('Locating manifestations', max=len(URI_list), suffix='%(percent)d%%')
	for URI in URI_list:
		label = URI.split('/')[-1]
		g = rdflib.Graph()
		g.bind('bf', bf)
		g.bind('bflc', bflc)
		g.bind('rdac', rdac)
		g.bind('rdam', rdam)
		g.bind('rdamdt', rdamdt)
		g.bind('rdax', rdax)
		g.bind('sin', sin)
		g.bind('madsrdf', madsrdf)
		g.parse(URI, format="json-ld")
		for work in g.subjects(RDF.type, rdac.C10007):
			g.serialize(destination=f'input/{currentDate}/manifestation/' + label + '.xml', format="xml")
		bar.next()
	bar.finish()
	return manifestationURIList

def save_items(URI_list, currentDate, manifestationURIList=[]):
	"""Look for items from trellis according to RDA class"""
	# remove works, expressions + manifestations from URI list to save time
	for manifestation in manifestationURIList:
		URI_list.remove(manifestation)
	# create directory for items
	if not os.path.exists(f'input/{currentDate}/item'):
		print("...\nCreating item directory")
		os.system(f'mkdir input/{currentDate}/item')
	bar = Bar('Locating items', max=len(URI_list), suffix='%(percent)d%%')
	for URI in URI_list:
		label = URI.split('/')[-1]
		g = rdflib.Graph()
		g.bind('bf', bf)
		g.bind('bflc', bflc)
		g.bind('rdac', rdac)
		g.bind('rdai', rdai)
		g.bind('rdax', rdax)
		g.bind('sin', sin)
		g.bind('madsrdf', madsrdf)
		g.parse(URI, format="json-ld")
		for work in g.subjects(RDF.type, rdac.C10003):
			g.serialize(destination=f'input/{currentDate}/item/' + label + '.xml', format="xml")
		bar.next()
	bar.finish()

def work_1_ttl_to_json(currentDate):
	# create list of work 1s in turtle
	work_1_ttl_list = os.listdir(f'output/{currentDate}/work_1_ttl')

	# create work 1 json directory
	if not os.path.exists(f'output/{currentDate}/work_1_json'):
		print(f'...\nCreating work_1 directory')
		os.makedirs(f'output/{currentDate}/work_1_json')
	print("...")
	bar = Bar(f'Transforming {len(work_1_ttl_list)} work 1 files from Turtle to JSON-LD', max=len(work_1_ttl_list), suffix='%(percent)d%%')
	for work in work_1_ttl_list:
		os.system(f"chmod u+rwx output/{currentDate}/work_1_ttl/{work}") # adjust file permissions for data
		# create new empty graph
		Graph_localWork = Graph()
		# bind namespaces to graph
		Graph_localWork.bind('bf', bf)
		Graph_localWork.bind('bflc', bflc)
		Graph_localWork.bind('madsrdf', madsrdf)
		# add turtle file to new graph
		Graph_localWork.load(f'file:output/{currentDate}/work_1_ttl/{work}', format='turtle')
		# serialize graph as JSON-LD
		Graph_localWork.serialize(destination=f'output/{currentDate}/work_1_json/' + work.split('.')[0] + ".json", format="json-ld")
		bar.next()
	bar.finish()

def work_2_ttl_to_json(currentDate):
	# create list of work 2s in turtle
	work_2_ttl_list = os.listdir(f'output/{currentDate}/work_2_ttl')

	# create work 2 json directory
	if not os.path.exists(f'output/{currentDate}/work_2_json'):
		print(f'...\nCreating work_2 directory')
		os.makedirs(f'output/{currentDate}/work_2_json')
	print("...")
	bar = Bar(f'Transforming {len(work_2_ttl_list)} work 2 files from Turtle to JSON-LD', max=len(work_2_ttl_list), suffix='%(percent)d%%')
	for work in work_2_ttl_list:
		os.system(f"chmod u+rwx output/{currentDate}/work_2_ttl/{work}") # adjust file permissions for data
		# create new empty graph
		Graph_localWork = Graph()
		# bind namespaces to graph
		Graph_localWork.bind('bf', bf)
		Graph_localWork.bind('bflc', bflc)
		Graph_localWork.bind('madsrdf', madsrdf)
		# add turtle file to new graph
		Graph_localWork.load(f'file:output/{currentDate}/work_2_ttl/{work}', format='turtle')
		# serialize graph as JSON-LD
		Graph_localWork.serialize(destination=f'output/{currentDate}/work_2_json/' + work.split('.')[0] + ".json", format="json-ld")
		bar.next()
	bar.finish()

def instance_ttl_to_json(currentDate):
	# create list of instances in turtle
	instance_ttl_list = os.listdir(f'output/{currentDate}/instance_ttl')

	# create instance json directory
	if not os.path.exists(f'output/{currentDate}/instance_json'):
		print(f'...\nCreating instance directory')
		os.makedirs(f'output/{currentDate}/instance_json')
	print("...")
	bar = Bar(f'Transforming {len(instance_ttl_list)} instance files from Turtle to JSON-LD', max=len(instance_ttl_list), suffix='%(percent)d%%')
	for instance in instance_ttl_list:
		os.system(f"chmod u+rwx output/{currentDate}/instance_ttl/{instance}") # adjust file permissions for data
		# create new empty graph
		Graph_localInstance = Graph()
		# bind namespaces to graph
		Graph_localInstance.bind('bf', bf)
		Graph_localInstance.bind('bflc', bflc)
		Graph_localInstance.bind('madsrdf', madsrdf)
		# add turtle file to new graph
		Graph_localInstance.load(f'file:output/{currentDate}/instance_ttl/{instance}', format='turtle')
		# serialize graph as JSON-LD
		Graph_localInstance.serialize(destination=f'output/{currentDate}/instance_json/' + instance.split('.')[0] + ".json", format="json-ld")
		bar.next()
	bar.finish()

def item_ttl_to_json(currentDate):
	# create list of items in turtle
	item_ttl_list = os.listdir(f'output/{currentDate}/item_ttl')

	# create item json directory
	if not os.path.exists(f'output/{currentDate}/item_json'):
		print(f'...\nCreating item directory')
		os.makedirs(f'output/{currentDate}/item_json')
	print("...")
	bar = Bar(f'Transforming {len(item_ttl_list)} item files from Turtle to JSON-LD', max=len(item_ttl_list), suffix='%(percent)d%%')
	for item in item_ttl_list:
		os.system(f"chmod u+rwx output/{currentDate}/item_ttl/{item}") # adjust file permissions for data
		# create new empty graph
		Graph_localItem = Graph()
		# bind namespaces to graph
		Graph_localItem.bind('bf', bf)
		Graph_localItem.bind('bflc', bflc)
		Graph_localItem.bind('madsrdf', madsrdf)
		# add turtle file to new graph
		Graph_localItem.load(f'file:output/{currentDate}/item_ttl/{item}', format='turtle')
		# serialize graph as JSON-LD
		Graph_localItem.serialize(destination=f'output/{currentDate}/item_json/' + item.split('.')[0] + ".json", format="json-ld")
		bar.next()
	bar.finish()

## RML functions

def transform_works(workList, currentDate):
	os.system("chmod u+rwx generateRML/rmlOutput/workRML.ttl") # adjust file permissions for map (RML sometimes trips on file permissions)
	# create work output directory
	if not os.path.exists(f'output/{currentDate}/work_1_ttl'):
		print(f'...\nCreating work_1 directory')
		os.makedirs(f'output/{currentDate}/work_1_ttl')
	print("...")
	bar = Bar(f'Transforming {len(workList)} files from RDA Work to BIBFRAME Work', max=len(workList), suffix='%(percent)d%%')
	for work in workList:
		os.system(f"chmod u+rwx input/{currentDate}/work/{work}") # adjust file permissions for data
		label = work.split('.')[0] # save trellis identifier as label
		workID = f"{currentDate}/work/{label}" # use label to make path
		work_map_replace_to_ID(workID) # use path as RML source in work monograph map
		os.system(f"java -jar rmlmapper-4.9.1-r328.jar -m generateRML/rmlOutput/workRML.ttl -o {label}.nq") # run RML, output as nquad file
		# create new empty graph
		Graph_localWork = Graph()
		# bind namespaces to graph
		Graph_localWork.bind('bf', bf)
		Graph_localWork.bind('bflc', bflc)
		Graph_localWork.bind('madsrdf', madsrdf)
		# add nquad file to new graph
		Graph_localWork.load(f'file:{label}.nq', format='nquads')
		# create variables for new triples
		snapshot_bnode = BNode()
		currentTime = time.strftime("%Y-%m-%dT%H:%M:%S+00:00")
		snapshot_literal = Literal(f"rml.py SNAPSHOT: {currentTime}")
		# create new triples
		for s, p, o in Graph_localWork.triples((None, bf.adminMetadata, None)):
			Graph_localWork.add((o, bf.generationProcess, snapshot_bnode))
			Graph_localWork.add((snapshot_bnode, RDF.type, bf.GenerationProcess))
			Graph_localWork.add((snapshot_bnode, RDFS.label, snapshot_literal))
		# serialize graph as turtle
		Graph_localWork.serialize(destination=f'output/{currentDate}/work_1_ttl/' + label + ".ttl", format="turtle")
		# delete nquad file
		os.system(f"rm {label}.nq")
		# return work map to default
		work_map_replace_to_default(workID)
		bar.next()
	bar.finish()

def transform_expressions(expressionList, currentDate):
	os.system("chmod u+rwx generateRML/rmlOutput/expressionRML.ttl") # adjust file permissions for map (RML sometimes trips on file permissions)
	# create expression directory
	if not os.path.exists(f'output/{currentDate}/work_2_ttl'):
		print(f'...\nCreating work_2 directory')
		os.makedirs(f'output/{currentDate}/work_2_ttl')
	print("...")
	bar = Bar(f'Transforming {len(expressionList)} from RDA Expression to BIBFRAME Work', max=len(expressionList), suffix='%(percent)d%%')
	for expression in expressionList:
		os.system(f"chmod u+rwx input/{currentDate}/expression/{expression}") # adjust file permissions for data
		label = expression.split('.')[0] # save trellis identifier as label
		expressionID = f"{currentDate}/expression/{label}" # use label to make path
		expression_map_replace_to_ID(expressionID) # use trellis identifier as RML source in expression monograph map
		os.system(f"java -jar rmlmapper-4.9.1-r328.jar -m generateRML/rmlOutput/expressionRML.ttl -o {label}.nq") # run RML, output as nquad file
		# create new empty graph
		Graph_localExpression = Graph()
		# bind namespaces to graph
		Graph_localExpression.bind('bf', bf)
		Graph_localExpression.bind('bflc', bflc)
		Graph_localExpression.bind('madsrdf', madsrdf)
		# add nquad file to new graph
		Graph_localExpression.load(f'file:{label}.nq', format='nquads')
		# create variables for new triples
		snapshot_bnode = BNode()
		currentTime = time.strftime("%Y-%m-%dT%H:%M:%S+00:00")
		snapshot_literal = Literal(f"rml.py SNAPSHOT: {currentTime}")
		# create new triples
		for s, p, o in Graph_localExpression.triples((None, bf.adminMetadata, None)):
			Graph_localExpression.add((o, bf.generationProcess, snapshot_bnode))
			Graph_localExpression.add((snapshot_bnode, RDF.type, bf.GenerationProcess))
			Graph_localExpression.add((snapshot_bnode, RDFS.label, snapshot_literal))
		# serialize graph as turtle
		Graph_localExpression.serialize(destination=f'output/{currentDate}/work_2_ttl/' + label + ".ttl", format="turtle")
		# delete nquad file
		os.system(f"rm {label}.nq")
		# return expression map to default
		expression_map_replace_to_default(expressionID)
		bar.next()
	bar.finish()

def transform_manifestations(manifestationList, currentDate):
	os.system("chmod u+rwx generateRML/rmlOutput/manifestationRML.ttl") # adjust file permissions for map (RML sometimes trips on file permissions)
	# create manifestation directory
	if not os.path.exists(f'output/{currentDate}/instance_ttl'):
		print(f'...\nCreating instance directory')
		os.makedirs(f'output/{currentDate}/instance_ttl')
	print("...")
	bar = Bar(f'Transforming {len(manifestationList)} files from RDA Manifestation to BIBFRAME Instance', max=len(manifestationList), suffix='%(percent)d%%')
	for manifestation in manifestationList:
		os.system(f"chmod u+rwx input/{currentDate}/manifestation/{manifestation}") # adjust file permissions for data
		label = manifestation.split('.')[0] # save trellis identifier as label
		manifestationID = f"{currentDate}/manifestation/{label}" # use label to make path
		manifestation_map_replace_to_ID(manifestationID) # use trellis identifier as RML source in manifestation monograph map
		os.system(f"java -jar rmlmapper-4.9.1-r328.jar -m generateRML/rmlOutput/manifestationRML.ttl -o {label}.nq") # run RML, output as nquad file
		# create new empty graph
		Graph_localManifestation = Graph()
		# bind namespaces to graph
		Graph_localManifestation.bind('bf', bf)
		Graph_localManifestation.bind('bflc', bflc)
		Graph_localManifestation.bind('madsrdf', madsrdf)
		# add nquad file to new graph
		Graph_localManifestation.load(f'file:{label}.nq', format='nquads')
		# create variables for new triples
		snapshot_bnode = BNode()
		currentTime = time.strftime("%Y-%m-%dT%H:%M:%S+00:00")
		snapshot_literal = Literal(f"rml.py SNAPSHOT: {currentTime}")
		# create new triples
		for s, p, o in Graph_localManifestation.triples((None, bf.adminMetadata, None)):
			Graph_localManifestation.add((o, bf.generationProcess, snapshot_bnode))
			Graph_localManifestation.add((snapshot_bnode, RDF.type, bf.GenerationProcess))
			Graph_localManifestation.add((snapshot_bnode, RDFS.label, snapshot_literal))
		# serialize graph as turtle
		Graph_localManifestation.serialize(destination=f'output/{currentDate}/instance_ttl/' + label + ".ttl", format="turtle")
		# delete nquad file
		os.system(f"rm {label}.nq")
		# return manifestation map to default
		manifestation_map_replace_to_default(manifestationID)
		bar.next()
	bar.finish()

def transform_items(itemList, currentDate):
	os.system("chmod u+rwx generateRML/rmlOutput/itemRML.ttl") # adjust file permissions for map (RML sometimes trips on file permissions)
	# create item directory
	if not os.path.exists(f'output/{currentDate}/item_ttl'):
		print(f'...\nCreating item directory')
		os.makedirs(f'output/{currentDate}/item_ttl')
	print("...")
	bar = Bar(f'Transforming {len(itemList)} files from RDA Item to BIBFRAME Item', max=len(itemList), suffix='%(percent)d%%')
	for item in itemList:
		os.system(f"chmod u+rwx input/{currentDate}/item/{item}") # adjust file permissions for data
		label = item.split('.')[0] # save trellis identifier as label
		itemID = f"{currentDate}/item/{label}" # use label to make path
		item_map_replace_to_ID(itemID) # use trellis identifier as RML source in item monograph map
		os.system(f"java -jar rmlmapper-4.9.1-r328.jar -m generateRML/rmlOutput/itemRML.ttl -o {label}.nq") # run RML, output as nquad file
		# create new empty graph
		Graph_localItem = Graph()
		# bind namespaces to graph
		Graph_localItem.bind('bf', bf)
		Graph_localItem.bind('bflc', bflc)
		Graph_localItem.bind('madsrdf', madsrdf)
		# add nquad file to new graph
		Graph_localItem.load(f'file:{label}.nq', format='nquads')
		# create variables for new triples
		snapshot_bnode = BNode()
		currentTime = time.strftime("%Y-%m-%dT%H:%M:%S+00:00")
		snapshot_literal = Literal(f"rml.py SNAPSHOT: {currentTime}")
		# create new triples
		for s, p, o in Graph_localItem.triples((None, bf.adminMetadata, None)):
			Graph_localItem.add((o, bf.generationProcess, snapshot_bnode))
			Graph_localItem.add((snapshot_bnode, RDF.type, bf.GenerationProcess))
			Graph_localItem.add((snapshot_bnode, RDFS.label, snapshot_literal))
		# serialize file in turtle
		Graph_localItem.serialize(destination=f'output/{currentDate}/item_ttl/' + label + ".ttl", format="turtle")
		# delete nquad file
		os.system(f"rm {label}.nq")
		# return item map to default
		item_map_replace_to_default(itemID)
		bar.next()
	bar.finish()

## XML Element Tree functions

def remove_extra_descriptions(entity, file):
	"""Remove triples from original RDA/RDF that do not describe the resource in question"""
	# fix file permissions # remove this before pushing
	os.system(f'chmod u+rwx input/{currentDate}/{entity}/{file}')

	# open xml parser
	tree = ET.parse(f'input/{currentDate}/{entity}/{file}')
	root = tree.getroot()

	resource_identifier = file.split('.')[0]
	IRI = f'https://api.sinopia.io/resource/{resource_identifier}'

	ns = {'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'}

	for desc in root.findall('rdf:Description', ns):
		# create dictionary of attributes for description
		attrib_dict = desc.attrib

		# if it contains rdf:about as an attribute...
		if '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about' in attrib_dict.keys():
			# and if the value of rdf:about is not the resource in question...
			if attrib_dict['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about'] != IRI:
				# remove the description
				root.remove(desc)

		# fix file permissions # remove this before pushing
		os.system('chmod u+rwx temp.xml')
		# write new XML to a temporary file
		tree.write('temp.xml')

		# reserialize with rdflib to fix namespaces and UTf-8
		g = Graph()
		g.bind('bf', bf)
		g.bind('bflc', bflc)
		g.bind('rdac', rdac)
		g.bind('rdae', rdae)
		g.bind('rdai', rdai)
		g.bind('rdam', rdam)
		g.bind('rdamdt', rdamdt)
		g.bind('rdaw', rdaw)
		g.bind('rdax', rdax)
		g.bind('sin', sin)
		g.bind('madsrdf', madsrdf)
		g.load(f'file:temp.xml', format='xml')
		g.serialize(destination=f'input/{currentDate}/{entity}/{file}', format='xml')

def add_triple_to_xml(entity, file, new_IRI):
	"""Add triple stating that new BF resource owl:sameAs old RDA resource"""
	file = file.split('.')[0] + '.xml'

	# fix file permissions # remove this before pushing
	os.system(f'chmod u+rwx input/{currentDate}/{entity}/{file}')

	# open xml parser
	tree = ET.parse(f'input/{currentDate}/{entity}/{file}')
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
	for owl in root.findall('rdf:Description/owl:sameAs', ns):
		owl.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource', new_IRI)

	# fix file permissions # remove this before pushing
	os.system('chmod u+rwx temp.xml')
	# write new XML to a temporary file
	tree.write('temp.xml')

	# reserialize with rdflib to fix namespaces and UTf-8
	g = Graph()
	g.bind('bf', bf)
	g.bind('bflc', bflc)
	g.bind('owl', owl)
	g.bind('rdac', rdac)
	g.bind('rdae', rdae)
	g.bind('rdai', rdai)
	g.bind('rdam', rdam)
	g.bind('rdamdt', rdamdt)
	g.bind('rdaw', rdaw)
	g.bind('rdax', rdax)
	g.bind('sin', sin)
	g.bind('madsrdf', madsrdf)
	g.load(f'file:temp.xml', format='xml')
	g.serialize(destination=f'input/{currentDate}/{entity}/{file}', format='xml')

## Find-and-replace functions

def work_map_replace_to_ID(workID):
	"""Replace all RML sources in the work monograph map from a random string (!!workID!!) to the work's identifier"""
	w = open("generateRML/rmlOutput/workRML.ttl", "rt")
	w_ = w.read()
	w_ = w_.replace("!!workID!!", workID)
	w.close()
	w = open("generateRML/rmlOutput/workRML.ttl", "wt")
	w.write(w_)

	w.close()

def work_map_replace_to_default(workID):
	"""Replace all RML sources in the work monograph map from the work's identifier back to a random string (!!workID!!)"""
	w = open("generateRML/rmlOutput/workRML.ttl", "rt")
	w_ = w.read()
	w_ = w_.replace(workID, "!!workID!!")
	w.close()
	w = open("generateRML/rmlOutput/workRML.ttl", "wt")
	w.write(w_)
	w.close()

def expression_map_replace_to_ID(expressionID):
	"""Replace all RML sources in the expression monograph map from a random string (!!expressionID!!) to the expression's identifier"""
	e = open("generateRML/rmlOutput/expressionRML.ttl", "rt")
	e_ = e.read()
	e_ = e_.replace("!!expressionID!!", expressionID)
	e.close()
	e = open("generateRML/rmlOutput/expressionRML.ttl", "wt")
	e.write(e_)
	e.close()

def expression_map_replace_to_default(expressionID):
	"""Replace all RML sources in the expression monograph map from the expression's identifier back to a random string (!!expressionID!!)"""
	e = open("generateRML/rmlOutput/expressionRML.ttl", "rt")
	e_ = e.read()
	e_ = e_.replace(expressionID, "!!expressionID!!")
	e.close()
	e = open("generateRML/rmlOutput/expressionRML.ttl", "wt")
	e.write(e_)
	e.close()

def manifestation_map_replace_to_ID(manifestationID):
	"""Replace all RML sources in the manifestation monograph map from a random string (!!manifestationID!!) to the manifestation's identifier"""
	m = open("generateRML/rmlOutput/manifestationRML.ttl", "rt")
	m_ = m.read()
	m_ = m_.replace("!!manifestationID!!", manifestationID)
	m.close()
	m = open("generateRML/rmlOutput/manifestationRML.ttl", "wt")
	m.write(m_)
	m.close()

def manifestation_map_replace_to_default(manifestationID):
	"""Replace all RML sources in the manifestation monograph map from the manifestation's identifier back to a random string (!!manifestationID!!)"""
	m = open("generateRML/rmlOutput/manifestationRML.ttl", "rt")
	m_ = m.read()
	m_ = m_.replace(manifestationID, "!!manifestationID!!")
	m.close()
	m = open("generateRML/rmlOutput/manifestationRML.ttl", "wt")
	m.write(m_)
	m.close()

def item_map_replace_to_ID(itemID):
	"""Replace all RML sources in the item monograph map from a random string (!!itemID!!) to the item's identifier"""
	i = open("generateRML/rmlOutput/itemRML.ttl", "rt")
	i_ = i.read()
	i_ = i_.replace("!!itemID!!", itemID)
	i.close()
	i = open("generateRML/rmlOutput/itemRML.ttl", "wt")
	i.write(i_)
	i.close()

def item_map_replace_to_default(itemID):
	"""Replace all RML sources in the item monograph map from the item's identifier back to a random string (!!itemID!!)"""
	i = open("generateRML/rmlOutput/itemRML.ttl", "rt")
	i_ = i.read()
	i_ = i_.replace(itemID, "!!itemID!!")
	i.close()
	i = open("generateRML/rmlOutput/itemRML.ttl", "wt")
	i.write(i_)
	i.close()

def replace_IRIs(entity, resource, old_IRI, new_IRI):
	"""Replace old IRI from original RDA/RDF with new IRI for new BIBFRAME"""
	original = open(f"output/{currentDate}/{entity}_json/{resource}", "rt")
	edit = original.read()
	edit = edit.replace(old_IRI, new_IRI)
	original.close()
	new = open(f"output/{currentDate}/{entity}_json/{resource}", "wt")
	new.write(edit)
	new.close()

"""Variables"""

# format for naming folder according to date
today = date.today()
currentDate = str(today).replace('-', '_')

###

"""Retrieve RDA Data"""
URI_list = create_URI_list()

# create directory with today's date for RDA-in-RDF/XML data
if not os.path.exists(f'input/{currentDate}'):
	print('...\nCreating input folder')
	os.system(f'mkdir input/{currentDate}')

#workURIList = save_works(URI_list, currentDate)
workList = os.listdir(f'input/{currentDate}/work') # add RDA-in-RDF/XML works to new list

#expressionURIList = save_expressions(URI_list, currentDate, workURIList)
expressionList = os.listdir(f'input/{currentDate}/expression') # add RDA-in-RDF/XML expressions to new list

#manifestationURIList = save_manifestations(URI_list, currentDate, expressionURIList)
manifestationList = os.listdir(f'input/{currentDate}/manifestation') # add RDA-in-RDF/XML manifestations to new list

#save_items(URI_list, currentDate, manifestationURIList)
itemList = os.listdir(f'input/{currentDate}/item') # add RDA-in-RDF/XML items to new list

#print("...\nCleaning input data")

#print(">> Removing extra descriptions")
#for work in workList:
	#remove_extra_descriptions('work', work)
#for exp in expressionList:
	#remove_extra_descriptions('expression', exp)
#for man in manifestationList:
	#remove_extra_descriptions("manifestation", man)
#for item in itemList:
	#remove_extra_descriptions("item", item)
if os.path.exists('temp.xml'): # remove temp file
	os.system('rm temp.xml')

#print(">> Fixing IRIs typed as literals")
#os.system('chmod u+rwx fix_URIs.py')
#import fix_URIs

#print(">> Removing blank copyright dates")
#os.system('chmod u+rwx fix_copyright_dates.py')
#import fix_copyright_dates

"""Transform RDA to BIBFRAME in Turtle"""

# create directory with today's date for BF-in-turtle data
if not os.path.exists(f'output/{currentDate}'):
	print('...\nCreating output folder')
	os.makedirs(f'output/{currentDate}')

#transform_works(workList, currentDate)
#transform_expressions(expressionList, currentDate)
#transform_manifestations(manifestationList, currentDate)
#transform_items(itemList, currentDate)

#print("...\nCleaning output data")

#print(">> Fixing language tags")
#os.system('chmod u+rwx langtags.py')
#import langtags

#print(">> Adding datatypes to dates") # this script needs fixing
#os.system('chmod u+rwx type_dates_2.py')
#import type_dates_2

"""Reserialize Turtle as JSON-LD"""

print("...\nReserializing Turtle output as JSON-LD")
#work_1_ttl_to_json(currentDate)
#work_2_ttl_to_json(currentDate)
#instance_ttl_to_json(currentDate)
#item_ttl_to_json(currentDate)

"""Generate new IRIs for JSON-LD resources"""

work_1_json_list = os.listdir(f"output/{currentDate}/work_1_json/")
work_2_json_list = os.listdir(f"output/{currentDate}/work_2_json/")
instance_json_list = os.listdir(f"output/{currentDate}/instance_json/")
item_json_list = os.listdir(f"output/{currentDate}/item_json/")
resource_dict = {"work_1": work_1_json_list, "work_2": work_2_json_list, "instance": instance_json_list, "item": item_json_list}

bf_rda_entities_dict = {'work_1': 'work', 'work_2': 'expression', 'instance': 'manifestation', 'item': 'item'}

if not os.path.exists(f'RDA_BF_URI_list_{currentDate}.csv'):
	print("...\nCreating RDA IRI to BF IRI key")
	os.system(f'touch RDA_BF_URI_list_{currentDate}.csv')

print("...\nGenerating new IRIs for BF resources")
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
			os.system(f'mv output/{currentDate}/{entity}_json/{old_identifier}.json output/{currentDate}/{entity}_json/{new_identifier}.json')

			bar.next()
		bar.finish()

"""Prepare JSON-LD for upload into Sinopia"""

# make the current file contents the value of property "data"

# wrap it all in brackets {} to make it a json object

# inside that object, insert Sinopia admin metadata

# post each file to Sinopia

print("...\nDone!")
