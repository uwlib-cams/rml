import csv
from datetime import date
import os
from progress.bar import Bar
from rdflib import *
import time
from timeit import default_timer as timer
import uuid
import xml.etree.ElementTree as ET

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
skos = Namespace('http://www.w3.org/2004/02/skos/core#')

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
	g.bind('skos', skos)
	g.load(f'file:{file}', format='xml')
	g.serialize(destination=f'{file}', format='xml')

# XML Tree functions
def add_owlsameAs(rda_or_bf, entity, file, IRI):
	"""Add triple stating that old RDA resource owl:sameAs new BF resource, or vice versa"""
	file = file.split('.')[0] + '.xml'

	if rda_or_bf.lower() == 'rda':
		file_path = f'../input/{currentDate}/{entity}/{file}'
	elif rda_or_bf.lower() == 'bf':
		if entity == "work":
			entity = "work_1"
		elif entity == "expression":
			entity = "work_2"
		elif entity == "manifestation":
			entity = "instance"
		file_path = f'../output/{currentDate}/{entity}_xml/{file}'

	# open xml parser
	tree = ET.parse(file_path)
	root = tree.getroot()

	ns = {'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#', 'owl': 'http://www.w3.org/2002/07/owl#'}

	# insert owl:sameAs
	for desc in root.findall('rdf:Description', ns):
		# create dictionary of attributes for description
		attrib_dict = desc.attrib

		# if it contains rdf:about as an attribute...
		if '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about' in attrib_dict.keys():
			# write in owl:sameAs
			ET.SubElement(desc, '{http://www.w3.org/2002/07/owl#}sameAs')

	# add value for owl:sameAs
	for owl_new_triple in root.findall('rdf:Description/owl:sameAs', ns):
		owl_new_triple.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource', IRI)

	# write new XML to a temporary file
	tree.write(file_path)

	# reserialize
	reserialize(file_path)

def update_bf_IRI(entity, file, new_IRI):
	file_path = f'../output/{currentDate}/{entity}_xml/{file}'
	# open xml parser
	tree = ET.parse(file_path)
	root = tree.getroot()

	for child in root:
		if '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about' in child.attrib.keys():
			child.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about', new_IRI)

	tree.write(file_path)

	reserialize(file_path)

# RML functions
def transform_works(workList, currentDate):
	start = timer()

	# create output directory
	if not os.path.exists(f'../output/{currentDate}/work_1_xml'):
		print('>> Creating work_1_xml directory')
		os.makedirs(f'../output/{currentDate}/work_1_xml')

	bar = Bar(f'>> Transforming RDA Work to BIBFRAME Work', max=len(workList), suffix='%(percent)d%%') # progress bar
	for work in workList:
		# identify RDA ID and IRI
		RDA_ID = work.split('.')[0]
		RDA_IRI = f"https://api.sinopia.io/resource/{RDA_ID}"
		work_filepath = f"/home/mcm104/rml/input/{currentDate}/work/{RDA_ID}" # use RDA ID to make path # needs editing to be universal

		# generate new BF ID and IRI
		BF_ID = uuid.uuid4()
		BF_IRI = f"https://api.stage.sinopia.io/resource/{BF_ID}"

		# record equivalence in dictionary
		rda_bf_dict[RDA_ID] = BF_ID

		# prepare RML map for transforming this resource
		work_map_replace_to_ID(work_filepath) # use path as RML source in work monograph map

		# run RML Mapper with workRML map
		os.system(f"java -jar rmlmapper-4.9.1-r328.jar -m ../generateRML/rmlOutput/workRML.ttl -o {RDA_ID}.nq") # run RML, output as nquad file

		# create new empty graph
		Graph_localWork = Graph()

		# bind namespaces to graph
		Graph_localWork.bind('bf', bf)
		Graph_localWork.bind('bflc', bflc)
		Graph_localWork.bind('madsrdf', madsrdf)
		Graph_localWork.bind('skos', skos)

		# add nquad file to new graph
		Graph_localWork.load(f'file:{RDA_ID}.nq', format='nquads')

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
		Graph_localWork.serialize(destination=f'../output/{currentDate}/work_1_xml/{BF_ID}.xml', format="xml")

		# delete temporary nquad file
		os.system(f"rm {RDA_ID}.nq")

		# return work map to default
		work_map_replace_to_default(work_filepath)

		# add owl:sameAs triple to RDA
		add_owlsameAs("rda", "work", work, BF_IRI)

		# add owl:sameAs triple to BF
		add_owlsameAs("bf", "work", f"{BF_ID}.xml", RDA_IRI)

		# update IRI in BF resource
		update_bf_IRI("work_1", f"{BF_ID}.xml", BF_IRI)

		bar.next()
	end = timer()
	print(f"\nWorks transformed: {len(workList)}")
	print(f"Time elapsed: {round((end - start), 1)} s")
	bar.finish()

def transform_expressions(expressionList, currentDate):
	start = timer()

	# create output directory
	if not os.path.exists(f'../output/{currentDate}/work_2_xml'):
		print(f'>> Creating work_2_xml directory')
		os.makedirs(f'../output/{currentDate}/work_2_xml')

	bar = Bar(f'>> Transforming RDA Expression to BIBFRAME Work', max=len(expressionList), suffix='%(percent)d%%') # progress bar
	for expression in expressionList:
		# identify RDA ID and IRI
		RDA_ID = expression.split('.')[0]
		RDA_IRI = f"https://api.sinopia.io/resource/{RDA_ID}"
		expression_filepath = f"/home/mcm104/rml/input/{currentDate}/expression/{RDA_ID}" # use RDA ID to make path

		# generate new BF ID and IRI
		BF_ID = uuid.uuid4()
		BF_IRI = f"https://api.stage.sinopia.io/resource/{BF_ID}"

		# record equivalence in dictionary
		rda_bf_dict[RDA_ID] = BF_ID

		# prepare RML map for transforming this resource
		expression_map_replace_to_ID(expression_filepath) # use path as RML source in expression monograph map

		os.system(f"java -jar rmlmapper-4.9.1-r328.jar -m ../generateRML/rmlOutput/expressionRML.ttl -o {RDA_ID}.nq") # run RML, output as nquad file

		# create new empty graph
		Graph_localExpression = Graph()

		# bind namespaces to graph
		Graph_localExpression.bind('bf', bf)
		Graph_localExpression.bind('bflc', bflc)
		Graph_localExpression.bind('madsrdf', madsrdf)
		Graph_localExpression.bind('skos', skos)

		# add nquad file to new graph
		Graph_localExpression.load(f'file:{RDA_ID}.nq', format='nquads')

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
		Graph_localExpression.serialize(destination=f'../output/{currentDate}/work_2_xml/{BF_ID}.xml', format="xml")

		# delete temporary nquad file
		os.system(f"rm {RDA_ID}.nq")

		# return expression map to default
		expression_map_replace_to_default(expression_filepath)

		# add owl:sameAs triple to RDA
		add_owlsameAs("rda", "expression", expression, BF_IRI)

		# add owl:sameAs triple to BF
		add_owlsameAs("bf", "expression", f"{BF_ID}.xml", RDA_IRI)

		# update IRI in BF resource
		update_bf_IRI("work_2", f"{BF_ID}.xml", BF_IRI)

		bar.next()
	end = timer()
	print(f"\nExpressions transformed: {len(expressionList)}")
	print(f"Elapsed time: {round((end - start), 1)} s")
	bar.finish()

def transform_manifestations(manifestationList, currentDate):
	start = timer()

	# create output directory
	if not os.path.exists(f'../output/{currentDate}/instance_xml'):
		print(f'>> Creating instance_xml directory')
		os.makedirs(f'../output/{currentDate}/instance_xml')

	bar = Bar(f'>> Transforming RDA Manifestation to BIBFRAME Instance', max=len(manifestationList), suffix='%(percent)d%%') # progress bar

	for manifestation in manifestationList:
		# identify RDA ID and IRI
		RDA_ID = manifestation.split('.')[0]
		RDA_IRI = f"https://api.sinopia.io/resource/{RDA_ID}"
		manifestation_filepath = f"/home/mcm104/rml/input/{currentDate}/manifestation/{RDA_ID}" # use RDA ID to make path

		# generate new BF ID and IRI
		BF_ID = uuid.uuid4()
		BF_IRI = f"https://api.stage.sinopia.io/resource/{BF_ID}"

		# record equivalence in dictionary
		rda_bf_dict[RDA_ID] = BF_ID

		# prepare RML map for transforming this resource
		manifestation_map_replace_to_ID(manifestation_filepath) # use path as RML source in manifestation monograph map

		os.system(f"java -jar rmlmapper-4.9.1-r328.jar -m ../generateRML/rmlOutput/manifestationRML.ttl -o {RDA_ID}.nq") # run RML, output as nquad file

		# create new empty graph
		Graph_localManifestation = Graph()

		# bind namespaces to graph
		Graph_localManifestation.bind('bf', bf)
		Graph_localManifestation.bind('bflc', bflc)
		Graph_localManifestation.bind('madsrdf', madsrdf)
		Graph_localManifestation.bind('skos', skos)

		# add nquad file to new graph
		Graph_localManifestation.load(f'file:{RDA_ID}.nq', format='nquads')

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
		Graph_localManifestation.serialize(destination=f'../output/{currentDate}/instance_xml/{BF_ID}.xml', format="xml")

		# delete temporary nquad file
		os.system(f"rm {RDA_ID}.nq")

		# return manifestation map to default
		manifestation_map_replace_to_default(manifestation_filepath)

		# add owl:sameAs triple to RDA
		add_owlsameAs("rda", "manifestation", manifestation, BF_IRI)

		# add owl:sameAs triple to BF
		add_owlsameAs("bf", "manifestation", f"{BF_ID}.xml", RDA_IRI)

		# update IRI in BF resource
		update_bf_IRI("instance", f"{BF_ID}.xml", BF_IRI)

		bar.next()
	end = timer()
	print(f"\nManifestations transformed: {len(manifestationList)}")
	print(f"Elapsed time: {round((end - start), 1)} s")
	bar.finish()

def transform_items(itemList, currentDate):
	start = timer()

	# create output directory
	if not os.path.exists(f'../output/{currentDate}/item_xml'):
		print(f'>> Creating item directory')
		os.makedirs(f'../output/{currentDate}/item_xml')

	bar = Bar(f'>> Transforming RDA Item to BIBFRAME Item', max=len(itemList), suffix='%(percent)d%%') # progress bar

	for item in itemList:
		# identify RDA ID and IRI
		RDA_ID = item.split('.')[0]
		RDA_IRI = f"https://api.sinopia.io/resource/{RDA_ID}"
		item_filepath = f"/home/mcm104/rml/input/{currentDate}/item/{RDA_ID}" # use RDA ID to make path

		# generate new BF ID and IRI
		BF_ID = uuid.uuid4()
		BF_IRI = f"https://api.stage.sinopia.io/resource/{BF_ID}"

		# record equivalence in dictionary
		rda_bf_dict[RDA_ID] = BF_ID

		# prepare RML map for transforming this resource
		item_map_replace_to_ID(item_filepath) # use path as RML source in item monograph map

		os.system(f"java -jar rmlmapper-4.9.1-r328.jar -m ../generateRML/rmlOutput/itemRML.ttl -o {RDA_ID}.nq") # run RML, output as nquad file

		# create new empty graph
		Graph_localItem = Graph()

		# bind namespaces to graph
		Graph_localItem.bind('bf', bf)
		Graph_localItem.bind('bflc', bflc)
		Graph_localItem.bind('madsrdf', madsrdf)
		Graph_localItem.bind('skos', skos)

		# add nquad file to new graph
		Graph_localItem.load(f'file:{RDA_ID}.nq', format='nquads')

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
		Graph_localItem.serialize(destination=f'../output/{currentDate}/item_xml/{BF_ID}.xml', format="xml")

		# delete temporary nquad file
		os.system(f"rm {RDA_ID}.nq")

		# return item map to default
		item_map_replace_to_default(item_filepath)

		# add owl:sameAs triple to RDA
		add_owlsameAs("rda", "item", item, BF_IRI)

		# add owl:sameAs triple to BF
		add_owlsameAs("bf", "item", f"{BF_ID}.xml", RDA_IRI)

		# update IRI in BF resource
		update_bf_IRI("item", f"{BF_ID}.xml", BF_IRI)

		bar.next()
	end = timer()
	print(f"\nItems transformed: {len(itemList)}")
	print(f"Elapsed time: {round((end - start), 1)} s")
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

# format for naming directory according to date
today = date.today()
currentDate = str(today).replace('-', '_')

"""Lists and Dictionaries"""

workList = os.listdir(f'../input/{currentDate}/work')
expressionList = os.listdir(f'../input/{currentDate}/expression')
manifestationList = os.listdir(f'../input/{currentDate}/manifestation')
itemList = os.listdir(f'../input/{currentDate}/item')

rda_bf_dict = {}

###

# create directory with today's date for BF-in-XML data
if not os.path.exists(f'../output/{currentDate}'):
	print('>> Creating output directory')
	os.makedirs(f'../output/{currentDate}')

transform_works(workList, currentDate)
transform_expressions(expressionList, currentDate)
transform_manifestations(manifestationList, currentDate)
transform_items(itemList, currentDate)

print(">> Creating record of new IRIs")
start = timer()
with open(f"RDA_BF_IRI_list_{currentDate}.csv", mode="w") as csv_output:
	csv_writer = csv.writer(csv_output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

	# write header row
	csv_writer.writerow(['original_RDA_identifier','equivalent_BF_identifier'])

	for RDA_ID in rda_bf_dict.keys():
		csv_writer.writerow([f'{RDA_ID}', f'{rda_bf_dict[RDA_ID]}'])
end = timer()
print(f"Elapsed time: {round((end - start), 1)} s")
