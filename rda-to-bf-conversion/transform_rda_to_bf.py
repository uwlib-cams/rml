from datetime import date
import os
from progress.bar import Bar
from rdflib import *
import time

"""Namespaces"""
LDP = Namespace('http://www.w3.org/ns/ldp#')
bf = Namespace('http://id.loc.gov/ontologies/bibframe/')
bflc = Namespace('http://id.loc.gov/ontologies/bflc/')
dbo = Namespace('http://dbpedia.org/ontology/')
madsrdf = Namespace('http://www.loc.gov/mads/rdf/v1#')
owl = Namespace('http://www.w3.org/2002/07/owl#')
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
# RDFLIB functions
def reserialize(file):
	"""Reserialize with rdflib to fix namespaces and UTf-8"""
	g = Graph()
	g.bind('bf', bf)
	g.bind('bflc', bflc)
	g.bind('dbo', dbo)
	g.bind('madsrdf', madsrdf)
	g.bind('owl', owl)
	g.bind('rdac', rdac)
	g.bind('rdae', rdae)
	g.bind('rdai', rdai)
	g.bind('rdam', rdam)
	g.bind('rdamdt', rdamdt)
	g.bind('rdau', rdau)
	g.bind('rdaw', rdaw)
	g.bind('rdax', rdax)
	g.bind('sin', sin)
	g.load(f'file:{file}', format='xml')
	g.serialize(destination=f'{file}', format='xml')

# RML functions
def transform_works(workList, currentDate):
	# create output directory
	if not os.path.exists(f'../output/{currentDate}/work_1'):
		print('...\nCreating work_1 directory')
		os.makedirs(f'../output/{currentDate}/work_1')

	print('...')

	bar = Bar(f'Transforming {len(workList)} files from RDA Work to BIBFRAME Work', max=len(workList), suffix='%(percent)d%%') # progress bar
	for work in workList:
		# identify RDA ID and IRI
		work_identifier = work.split('.')[0]
		work_filepath = f"{currentDate}/work/{work_identifier}" # use RDA ID to make path

		# prepare RML map for transforming this resource
		work_map_replace_to_ID(work_filepath) # use path as RML source in work monograph map

		# run RML Mapper with workRML map
		os.system(f"java -jar rmlmapper-4.9.1-r328.jar -m ../generateRML/rmlOutput/workRML.ttl -o {work_identifier}.nq") # run RML, output as nquad file

		# create new empty graph
		Graph_localWork = Graph()

		# bind namespaces to graph
		Graph_localWork.bind('bf', bf)
		Graph_localWork.bind('bflc', bflc)
		Graph_localWork.bind('madsrdf', madsrdf)

		# add nquad file to new graph
		Graph_localWork.load(f'file:{work_identifier}.nq', format='nquads')

		# create variables for new triples
		snapshot_bnode = BNode()
		currentTime = time.strftime("%Y-%m-%dT%H:%M:%S+00:00")
		snapshot_literal = Literal(f"rml.py SNAPSHOT: {currentTime}")

		# create new triples
		for s, p, o in Graph_localWork.triples((None, bf.adminMetadata, None)):
			Graph_localWork.add((o, bf.generationProcess, snapshot_bnode))
			Graph_localWork.add((snapshot_bnode, RDF.type, bf.GenerationProcess))
			Graph_localWork.add((snapshot_bnode, RDFS.label, snapshot_literal))

		# serialize graph as XML
		Graph_localWork.serialize(destination=f'../output/{currentDate}/work_1/{work_identifier}.xml', format="xml")

		# delete temporary nquad file
		os.system(f"rm {work_identifier}.nq")

		# return work map to default
		work_map_replace_to_default(work_filepath)

		bar.next()
	bar.finish()

def transform_expressions(expressionList, currentDate):
	# create output directory
	if not os.path.exists(f'../output/{currentDate}/work_2'):
		print(f'...\nCreating work_2 directory')
		os.makedirs(f'../output/{currentDate}/work_2')

	print("...")

	bar = Bar(f'Transforming {len(expressionList)} from RDA Expression to BIBFRAME Work', max=len(expressionList), suffix='%(percent)d%%') # progress bar
	for expression in expressionList:
		# identify RDA ID and IRI
		expression_identifier = expression.split('.')[0]
		expression_filepath = f"{currentDate}/expression/{expression_identifier}" # use RDA ID to make path

		# prepare RML map for transforming this resource
		expression_map_replace_to_ID(expression_filepath) # use path as RML source in expression monograph map

		# run RML Mapper with expressionRML map
		os.system(f"java -jar rmlmapper-4.9.1-r328.jar -m ../generateRML/rmlOutput/expressionRML.ttl -o {expression_identifier}.nq") # run RML, output as nquad file

		# create new empty graph
		Graph_localExpression = Graph()

		# bind namespaces to graph
		Graph_localExpression.bind('bf', bf)
		Graph_localExpression.bind('bflc', bflc)
		Graph_localExpression.bind('madsrdf', madsrdf)

		# add nquad file to new graph
		Graph_localExpression.load(f'file:{expression_identifier}.nq', format='nquads')

		# create variables for new triples
		snapshot_bnode = BNode()
		currentTime = time.strftime("%Y-%m-%dT%H:%M:%S+00:00")
		snapshot_literal = Literal(f"rml.py SNAPSHOT: {currentTime}")

		# create new triples
		for s, p, o in Graph_localExpression.triples((None, bf.adminMetadata, None)):
			Graph_localExpression.add((o, bf.generationProcess, snapshot_bnode))
			Graph_localExpression.add((snapshot_bnode, RDF.type, bf.GenerationProcess))
			Graph_localExpression.add((snapshot_bnode, RDFS.label, snapshot_literal))

		# serialize graph as XML
		Graph_localExpression.serialize(destination=f'../output/{currentDate}/work_2/{expression_identifier}.xml', format="xml")

		# delete temporary nquad file
		os.system(f"rm {expression_identifier}.nq")

		# return expression map to default
		expression_map_replace_to_default(expression_filepath)

		bar.next()
	bar.finish()

def transform_manifestations(manifestationList, currentDate):
	# create output directory
	if not os.path.exists(f'../output/{currentDate}/instance'):
		print(f'...\nCreating instance directory')
		os.makedirs(f'../output/{currentDate}/instance')

	print("...")

	bar = Bar(f'Transforming {len(manifestationList)} files from RDA Manifestation to BIBFRAME Instance', max=len(manifestationList), suffix='%(percent)d%%') # progress bar

	for manifestation in manifestationList:
		# identify RDA ID and IRI
		manifestation_identifier = manifestation.split('.')[0]
		manifestation_filepath = f"{currentDate}/manifestation/{manifestation_identifier}" # use RDA ID to make path

		# prepare RML map for transforming this resource
		manifestation_map_replace_to_ID(manifestation_filepath) # use path as RML source in manifestation monograph map

		# run RML Mapper with manifestationRML map
		os.system(f"java -jar rmlmapper-4.9.1-r328.jar -m ../generateRML/rmlOutput/manifestationRML.ttl -o {manifestation_identifier}.nq") # run RML, output as nquad file

		# create new empty graph
		Graph_localManifestation = Graph()

		# bind namespaces to graph
		Graph_localManifestation.bind('bf', bf)
		Graph_localManifestation.bind('bflc', bflc)
		Graph_localManifestation.bind('madsrdf', madsrdf)

		# add nquad file to new graph
		Graph_localManifestation.load(f'file:{manifestation_identifier}.nq', format='nquads')

		# create variables for new triples
		snapshot_bnode = BNode()
		currentTime = time.strftime("%Y-%m-%dT%H:%M:%S+00:00")
		snapshot_literal = Literal(f"rml.py SNAPSHOT: {currentTime}")

		# create new triples
		for s, p, o in Graph_localManifestation.triples((None, bf.adminMetadata, None)):
			Graph_localManifestation.add((o, bf.generationProcess, snapshot_bnode))
			Graph_localManifestation.add((snapshot_bnode, RDF.type, bf.GenerationProcess))
			Graph_localManifestation.add((snapshot_bnode, RDFS.label, snapshot_literal))

		# serialize graph as XML
		Graph_localManifestation.serialize(destination=f'../output/{currentDate}/instance/{expression_identifier}.xml', format="xml")

		# delete temporary nquad file
		os.system(f"rm {manifestation_identifier}.nq")

		# return manifestation map to default
		manifestation_map_replace_to_default(manifestation_filepath)

		bar.next()
	bar.finish()

def transform_items(itemList, currentDate):
	# create output directory
	if not os.path.exists(f'../output/{currentDate}/item'):
		print(f'...\nCreating item directory')
		os.makedirs(f'../output/{currentDate}/item')

	print("...")

	bar = Bar(f'Transforming {len(itemList)} files from RDA Item to BIBFRAME Item', max=len(itemList), suffix='%(percent)d%%') # progress bar

	for item in itemList:
		# identify RDA ID and IRI
		item_identifier = item.split('.')[0]
		item_filepath = f"{currentDate}/item/{item_identifier}" # use RDA ID to make path

		# prepare RML map for transforming this resource
		item_map_replace_to_ID(item_filepath) # use path as RML source in item monograph map

		# run RML Mapper with itemRML map
		os.system(f"java -jar rmlmapper-4.9.1-r328.jar -m ../generateRML/rmlOutput/itemRML.ttl -o {item_identifier}.nq") # run RML, output as nquad file

		# create new empty graph
		Graph_localItem = Graph()

		# bind namespaces to graph
		Graph_localItem.bind('bf', bf)
		Graph_localItem.bind('bflc', bflc)
		Graph_localItem.bind('madsrdf', madsrdf)

		# add nquad file to new graph
		Graph_localItem.load(f'file:{item_identifier}.nq', format='nquads')

		# create variables for new triples
		snapshot_bnode = BNode()
		currentTime = time.strftime("%Y-%m-%dT%H:%M:%S+00:00")
		snapshot_literal = Literal(f"rml.py SNAPSHOT: {currentTime}")

		# create new triples
		for s, p, o in Graph_localItem.triples((None, bf.adminMetadata, None)):
			Graph_localItem.add((o, bf.generationProcess, snapshot_bnode))
			Graph_localItem.add((snapshot_bnode, RDF.type, bf.GenerationProcess))
			Graph_localItem.add((snapshot_bnode, RDFS.label, snapshot_literal))

		# serialize file in XML
		Graph_localItem.serialize(destination=f'../output/{currentDate}/item_xml/{expression_identifier}.xml', format="xml")

		# delete temporary nquad file
		os.system(f"rm {item_identifier}.nq")

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

"""Lists and Dictionaries"""

workList = os.listdir(f'../input/{currentDate}/work')
expressionList = os.listdir(f'../input/{currentDate}/expression')
manifestationList = os.listdir(f'../input/{currentDate}/manifestation')
itemList = os.listdir(f'../input/{currentDate}/item')

###

# create directory with today's date for BF-in-XML data
if not os.path.exists(f'../output/{currentDate}'):
	print('...\nCreating output folder')
	os.makedirs(f'../output/{currentDate}')

transform_works(workList, currentDate)
transform_expressions(expressionList, currentDate)
transform_manifestations(manifestationList, currentDate)
transform_items(itemList, currentDate)
