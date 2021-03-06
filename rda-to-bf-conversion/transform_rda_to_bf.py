from datetime import date
import os
from progress.bar import Bar
from rdflib import *
import rdflib
import time

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
# RML functions
def transform_works(workList, currentDate):
	# create output directory
	if not os.path.exists(f'../output/{currentDate}/work_1_ttl'):
		print('...\nCreating work_1 directory')
		os.makedirs(f'../output/{currentDate}/work_1_ttl')

	print('...')

	bar = Bar(f'Transforming {len(workList)} files from RDA Work to BIBFRAME Work', max=len(workList), suffix='%(percent)d%%') # progress bar
	for work in workList[0:3]:
		label = work.split('.')[0] # save trellis identifier as label
		work_filepath = f"{currentDate}/work/{label}" # use label to make path

		work_map_replace_to_ID(work_filepath) # use path as RML source in work monograph map

		os.system(f"java -jar rmlmapper-4.9.1-r328.jar -m ../generateRML/rmlOutput/workRML.ttl -o {label}.nq") # run RML, output as nquad file

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
		Graph_localWork.serialize(destination=f'../output/{currentDate}/work_1_ttl/' + label + ".xml", format="xml")

		# delete temporary nquad file
		os.system(f"rm {label}.nq")

		# return work map to default
		work_map_replace_to_default(work_filepath)
		bar.next()
	bar.finish()

def transform_expressions(expressionList, currentDate):
	# create expression directory
	if not os.path.exists(f'../output/{currentDate}/work_2_ttl'):
		print(f'...\nCreating work_2 directory')
		os.makedirs(f'../output/{currentDate}/work_2_ttl')

	print("...")

	bar = Bar(f'Transforming {len(expressionList)} from RDA Expression to BIBFRAME Work', max=len(expressionList), suffix='%(percent)d%%') # progress bar
	for expression in expressionList[0:3]:
		label = expression.split('.')[0] # save trellis identifier as label
		expression_filepath = f"{currentDate}/expression/{label}" # use label to make path

		expression_map_replace_to_ID(expression_filepath) # use trellis identifier as RML source in expression monograph map

		os.system(f"java -jar rmlmapper-4.9.1-r328.jar -m ../generateRML/rmlOutput/expressionRML.ttl -o {label}.nq") # run RML, output as nquad file

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
		Graph_localExpression.serialize(destination=f'../output/{currentDate}/work_2_ttl/' + label + ".xml", format="xml")

		# delete temporary nquad file
		os.system(f"rm {label}.nq")
		# return expression map to default

		# return expression map to default
		expression_map_replace_to_default(expression_filepath)
		bar.next()
	bar.finish()

def transform_manifestations(manifestationList, currentDate):
	# create manifestation directory
	if not os.path.exists(f'../output/{currentDate}/instance_ttl'):
		print(f'...\nCreating instance directory')
		os.makedirs(f'../output/{currentDate}/instance_ttl')

	print("...")

	bar = Bar(f'Transforming {len(manifestationList)} files from RDA Manifestation to BIBFRAME Instance', max=len(manifestationList), suffix='%(percent)d%%') # progress bar

	for manifestation in manifestationList[0:3]:
		label = manifestation.split('.')[0] # save trellis identifier as label
		manifestation_filepath = f"{currentDate}/manifestation/{label}" # use label to make path

		manifestation_map_replace_to_ID(manifestation_filepath) # use trellis identifier as RML source in manifestation monograph map

		os.system(f"java -jar rmlmapper-4.9.1-r328.jar -m ../generateRML/rmlOutput/manifestationRML.ttl -o {label}.nq") # run RML, output as nquad file

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
		Graph_localManifestation.serialize(destination=f'../output/{currentDate}/instance_ttl/' + label + ".xml", format="xml")

		# delete temporary nquad file
		os.system(f"rm {label}.nq")
		# return manifestation map to default
		manifestation_map_replace_to_default(manifestation_filepath)
		bar.next()
	bar.finish()

def transform_items(itemList, currentDate):
	# create item directory
	if not os.path.exists(f'../output/{currentDate}/item_ttl'):
		print(f'...\nCreating item directory')
		os.makedirs(f'../output/{currentDate}/item_ttl')

	print("...")

	bar = Bar(f'Transforming {len(itemList)} files from RDA Item to BIBFRAME Item', max=len(itemList), suffix='%(percent)d%%') # progress bar

	for item in itemList[0:3]:
		label = item.split('.')[0] # save trellis identifier as label
		item_filepath = f"{currentDate}/item/{label}" # use label to make path

		item_map_replace_to_ID(item_filepath) # use trellis identifier as RML source in item monograph map

		os.system(f"java -jar rmlmapper-4.9.1-r328.jar -m ../generateRML/rmlOutput/itemRML.ttl -o {label}.nq") # run RML, output as nquad file

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
		Graph_localItem.serialize(destination=f'../output/{currentDate}/item_ttl/' + label + ".xml", format="xml")

		# delete temporary nquad file
		os.system(f"rm {label}.nq")

		# return item map to default
		item_map_replace_to_default(item_filepath)
		bar.next()
	bar.finish()

# Find-and-replace functions
def work_map_replace_to_ID(work_filepath):
	"""Replace all RML sources in the work monograph map from a random string (!!work_filepath!!) to the work's identifier"""
	w = open("../generateRML/rmlOutput/workRML.ttl", "rt")
	w_ = w.read()
	w_ = w_.replace("!!work_filepath!!", work_filepath)
	w.close()
	w = open("../generateRML/rmlOutput/workRML.ttl", "wt")
	w.write(w_)

	w.close()

def work_map_replace_to_default(work_filepath):
	"""Replace all RML sources in the work monograph map from the work's identifier back to a random string (!!work_filepath!!)"""
	w = open("../generateRML/rmlOutput/workRML.ttl", "rt")
	w_ = w.read()
	w_ = w_.replace(work_filepath, "!!work_filepath!!")
	w.close()
	w = open("../generateRML/rmlOutput/workRML.ttl", "wt")
	w.write(w_)
	w.close()

def expression_map_replace_to_ID(expression_filepath):
	"""Replace all RML sources in the expression monograph map from a random string (!!expression_filepath!!) to the expression's identifier"""
	e = open("../generateRML/rmlOutput/expressionRML.ttl", "rt")
	e_ = e.read()
	e_ = e_.replace("!!expression_filepath!!", expression_filepath)
	e.close()
	e = open("../generateRML/rmlOutput/expressionRML.ttl", "wt")
	e.write(e_)
	e.close()

def expression_map_replace_to_default(expression_filepath):
	"""Replace all RML sources in the expression monograph map from the expression's identifier back to a random string (!!expression_filepath!!)"""
	e = open("../generateRML/rmlOutput/expressionRML.ttl", "rt")
	e_ = e.read()
	e_ = e_.replace(expression_filepath, "!!expression_filepath!!")
	e.close()
	e = open("../generateRML/rmlOutput/expressionRML.ttl", "wt")
	e.write(e_)
	e.close()

def manifestation_map_replace_to_ID(manifestation_filepath):
	"""Replace all RML sources in the manifestation monograph map from a random string (!!manifestation_filepath!!) to the manifestation's identifier"""
	m = open("../generateRML/rmlOutput/manifestationRML.ttl", "rt")
	m_ = m.read()
	m_ = m_.replace("!!manifestation_filepath!!", manifestation_filepath)
	m.close()
	m = open("../generateRML/rmlOutput/manifestationRML.ttl", "wt")
	m.write(m_)
	m.close()

def manifestation_map_replace_to_default(manifestation_filepath):
	"""Replace all RML sources in the manifestation monograph map from the manifestation's identifier back to a random string (!!manifestation_filepath!!)"""
	m = open("../generateRML/rmlOutput/manifestationRML.ttl", "rt")
	m_ = m.read()
	m_ = m_.replace(manifestation_filepath, "!!manifestation_filepath!!")
	m.close()
	m = open("../generateRML/rmlOutput/manifestationRML.ttl", "wt")
	m.write(m_)
	m.close()

def item_map_replace_to_ID(item_filepath):
	"""Replace all RML sources in the item monograph map from a random string (!!item_filepath!!) to the item's identifier"""
	i = open("../generateRML/rmlOutput/itemRML.ttl", "rt")
	i_ = i.read()
	i_ = i_.replace("!!item_filepath!!", item_filepath)
	i.close()
	i = open("../generateRML/rmlOutput/itemRML.ttl", "wt")
	i.write(i_)
	i.close()

def item_map_replace_to_default(item_filepath):
	"""Replace all RML sources in the item monograph map from the item's identifier back to a random string (!!item_filepath!!)"""
	i = open("../generateRML/rmlOutput/itemRML.ttl", "rt")
	i_ = i.read()
	i_ = i_.replace(item_filepath, "!!item_filepath!!")
	i.close()
	i = open("../generateRML/rmlOutput/itemRML.ttl", "wt")
	i.write(i_)
	i.close()

"""Variables"""

# format for naming folder according to date
today = date.today()
currentDate = str(today).replace('-', '_')

"""Lists"""

workList = os.listdir(f'../input/{currentDate}/work')
expressionList = os.listdir(f'../input/{currentDate}/expression')
manifestationList = os.listdir(f'../input/{currentDate}/manifestation')
itemList = os.listdir(f'../input/{currentDate}/item')

###

# create directory with today's date for BF-in-turtle data
if not os.path.exists(f'../output/{currentDate}'):
	print('...\nCreating output folder')
	os.makedirs(f'../output/{currentDate}')

transform_works(workList, currentDate)
transform_expressions(expressionList, currentDate)
transform_manifestations(manifestationList, currentDate)
transform_items(itemList, currentDate)