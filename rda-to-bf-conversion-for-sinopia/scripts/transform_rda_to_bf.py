"""Python Libraries/Modules/Packages"""
import csv
from datetime import date
import os
from progress.bar import Bar
from rdflib import *
import time
from timeit import default_timer as timer
import uuid

"""Imported Functions"""
from scripts.arguments import define_arg

"""Namespaces"""
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

"""Variables"""
# format for naming folder according to date
currentDate_hyphen = date.today()
currentDate = str(currentDate_hyphen).replace('-', '_')

# arguments from command line
args = define_arg()
input_location = args.input
output_location = args.output

"""Lists and Dictionaries"""
workList = os.listdir(f'{input_location}/{currentDate}/work')
expressionList = os.listdir(f'{input_location}/{currentDate}/expression')
manifestationList = os.listdir(f'{input_location}/{currentDate}/manifestation')
itemList = os.listdir(f'{input_location}/{currentDate}/item')

resource_dict = {"work": workList, "expression": expressionList, "manifestation": manifestationList, "item": itemList}
rda_to_bf_entity_dict = {"work": "work_1", "expression": "work_2", "manifestation": "instance", "item": "item"}
rda_bf_dict = {}

"""Functions"""
def create_already_transformed_dict():
	IRI_dict = {}
	with open('other_files/set_IRIs.csv', mode='r') as IRI_file:
		csv_reader = csv.reader(IRI_file, delimiter=',')
		line_count = 0

		for line in csv_reader:
			if line_count != 0: # skip header
				IRI_dict[line[0]] = (line[1], line[2])

			line_count += 1

	return IRI_dict

def transform_rda_to_bf(entity, entityList, currentDate, output_location):
	start = timer()

	RDA_entity = entity
	BF_entity = rda_to_bf_entity_dict[entity]

	# create output directory
	if not os.path.exists(f'{output_location}/{currentDate}/{BF_entity}_xml'):
		print(f'>> Creating {BF_entity}_xml directory')
		os.makedirs(f'{output_location}/{currentDate}/{BF_entity}_xml')

	#start progress bar
	progress_bar_message_dict = {"work": ("Work", "Work"), "expression": ("Expression", "Work"), "manifestation": ("Manifestation", "Instance"), "item": ("Item", "Item")}
	bar = Bar(f'>> Transforming RDA {progress_bar_message_dict[RDA_entity][0]} to BIBFRAME {progress_bar_message_dict[RDA_entity][1]}', max=len(entityList), suffix='%(percent)d%%')
	for resource in entityList:
		# identify RDA ID and IRI
		RDA_ID = resource.split('.')[0]
		RDA_IRI = f"https://api.sinopia.io/resource/{RDA_ID}"
		rml_filepath = f"{input_location}/{currentDate}/{RDA_entity}/{RDA_ID}"

		if RDA_ID in IRI_dict.keys(): # BF has already been posted to Sinopia; treat as edit
			BF_ID = IRI_dict[RDA_ID][0]
			# record equivalence in dictionary
			rda_bf_dict[RDA_ID] = BF_ID
		else: # BF has not already been posted to Sinopia; treat as creation
			# generate new BF ID and IRI
			BF_ID = uuid.uuid4()
			# record equivalence in dictionary
			rda_bf_dict[RDA_ID] = BF_ID
		BF_IRI = f"https://api.sinopia.io/resource/{BF_ID}"

		# prepare RML map for transforming this resource
		replace_default_with_filepath(RDA_entity, rml_filepath)

		# run RML Mapper
		os.system(f"java -jar mapper.jar -m ../generateRML/rmlOutput/{RDA_entity}RML.ttl -o {RDA_ID}.nq")

		# create new empty graph
		g = Graph()

		# bind namespaces to graph
		g.bind('bf', bf)
		g.bind('bflc', bflc)
		g.bind('dbo', dbo)
		g.bind('madsrdf', madsrdf)
		g.bind('owl', owl)
		g.bind('skos', skos)

		# add nquad file to new graph
		g.load(f'file:{RDA_ID}.nq', format='nquads')

		# change subject from RDA_IRI to BF_IRI
		for s, p, o in g.triples((URIRef(RDA_IRI), None, None)):
			g.remove((s, p, o))
			g.add((URIRef(BF_IRI), p, o))

		# create variables for new triples
		snapshot_bnode = BNode()
		currentTime = time.strftime("%Y-%m-%dT%H:%M:%S")
		snapshot_literal = Literal(f"rda-to-bf-for-sinopia.py SNAPSHOT: {currentTime}")

		# create bf:generationProcess blank node with snapshot literal
		for s, p, o in g.triples((None, bf.adminMetadata, None)):
			g.add((o, bf.generationProcess, snapshot_bnode))
			g.add((snapshot_bnode, RDF.type, bf.GenerationProcess))
			g.add((snapshot_bnode, RDFS.label, snapshot_literal))

		# edit bf:creationDate; (opt.) add bf:changeDate
		if RDA_ID in IRI_dict.keys(): # BF has already been posted to Sinopia; treat as edit
			for s, p, o in g.triples((None, bf.adminMetadata, None)):
				g.remove((o, bf.creationDate, None))
				g.remove((o, bf.changeDate, None))
				g.add((o, bf.creationDate, Literal(IRI_dict[RDA_ID][1])))
				if currentDate_hyphen != IRI_dict[RDA_ID][1]: # current date is different from original post date
					g.add((o, bf.changeDate, Literal(currentDate_hyphen)))
		else: # BF has not already been posted to Sinopia; treat as creation
			for s, p, o in g.triples((None, bf.adminMetadata, None)):
				g.remove((o, bf.creationDate, None))
				g.remove((o, bf.changeDate, None))
				g.add((o, bf.creationDate, Literal(currentDate_hyphen)))

		# add triple in BF: <BF_IRI> owl:sameAs <RDA_IRI>
		g.add((URIRef(BF_IRI), owl.sameAs, URIRef(RDA_IRI)))

		# serialize BF graph as XML
		g.serialize(destination=f'{output_location}/{currentDate}/{BF_entity}_xml/{BF_ID}.xml', format="xml")

		# delete temporary nquad file
		os.system(f'rm {RDA_ID}.nq')

		# return RML map to default
		replace_filepath_with_default(RDA_entity, rml_filepath)

		# add triple in RDA: <RDA_IRI> owl:sameAs <BF_IRI>
			# create new empty graph for RDA file
		rda_g = Graph()

			# bind namespaces
		rda_g.bind('bf', bf)
		rda_g.bind('bflc', bflc)
		rda_g.bind('madsrdf', madsrdf)
		rda_g.bind('owl', owl)
		rda_g.bind('rdac', rdac)
		rda_g.bind('rdae', rdae)
		rda_g.bind('rdai', rdai)
		rda_g.bind('rdam', rdam)
		rda_g.bind('rdamdt', rdamdt)
		rda_g.bind('rdau', rdau)
		rda_g.bind('rdaw', rdaw)
		rda_g.bind('rdax', rdax)
		rda_g.bind('sin', sin)
		rda_g.bind('skos', skos)

			# load RDA file
		rda_g.load(f'file:{input_location}/{currentDate}/{RDA_entity}/{RDA_ID}.xml', format='xml')

			# add triple
		rda_g.add((URIRef(RDA_IRI), owl.sameAs, URIRef(BF_IRI)))

			# serialize RDA graph as XML
		rda_g.serialize(destination=f'{input_location}/{currentDate}/{RDA_entity}/{RDA_ID}.xml', format="xml")

		bar.next()
	end = timer()
	print(f'\n{progress_bar_message_dict[RDA_entity][0]}s transformed: {len(entityList)}')
	print(f'Time elapsed: {round((end - start), 1)} s')
	bar.finish()

def replace_default_with_filepath(entity, filepath):
	original = open(f"../generateRML/rmlOutput/{entity}RML.ttl", "rt")
	find_and_replace = original.read()
	find_and_replace = find_and_replace.replace(f"!!{entity}_filepath!!", filepath)
	original.close()
	new = open(f"../generateRML/rmlOutput/{entity}RML.ttl", "wt")
	new.write(find_and_replace)
	new.close()

def replace_filepath_with_default(entity, filepath):
	original = open(f"../generateRML/rmlOutput/{entity}RML.ttl", "rt")
	find_and_replace = original.read()
	find_and_replace = find_and_replace.replace(filepath, f"!!{entity}_filepath!!")
	original.close()
	new = open(f"../generateRML/rmlOutput/{entity}RML.ttl", "wt")
	new.write(find_and_replace)
	new.close()

###

IRI_dict = create_already_transformed_dict()

# create directory with today's date for BF-in-XML data
if not os.path.exists(f'{output_location}/{currentDate}'):
	print('>> Creating output directory')
	os.makedirs(f'{output_location}/{currentDate}')

for entity in resource_dict.keys():
	transform_rda_to_bf(entity, resource_dict[entity], currentDate, output_location)

print(">> Creating record of new IRIs")
start = timer()
with open(f"other_files/set_IRIs.csv", mode="a") as csv_output:
	csv_writer = csv.writer(csv_output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

	for RDA_ID in rda_bf_dict.keys():
		if RDA_ID not in IRI_dict.keys():
			csv_writer.writerow([RDA_ID, rda_bf_dict[RDA_ID], currentDate_hyphen])
end = timer()
print(f"Elapsed time: {round((end - start), 1)} s")
