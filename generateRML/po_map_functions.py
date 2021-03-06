"""Python Libraries/Modules/Packages"""
from rdflib import *

"""Lists"""
from lists import classification_props

"""Imported Functions"""
from formatting_functions import convert_string_to_IRI
from formatting_functions import generate_constant

"""Namespaces"""
bf = Namespace('http://id.loc.gov/ontologies/bibframe/')
bflc = Namespace('http://id.loc.gov/ontologies/bflc/')
dbo = Namespace('http://dbpedia.org/ontology/')
ex = Namespace('http://example.org/entity/')
madsrdf = Namespace('http://www.loc.gov/mads/rdf/v1#')
ql = Namespace('http://semweb.mmlab.be/ns/ql#')
rdac = Namespace('http://rdaregistry.info/Elements/c/')
rdae = Namespace('http://rdaregistry.info/Elements/e/')
rdai = Namespace('http://rdaregistry.info/Elements/i/')
rdam = Namespace('http://rdaregistry.info/Elements/m/')
rdamdt = Namespace('http://rdaregistry.info/Elements/m/datatype/')
rdau = Namespace('http://rdaregistry.info/Elements/u/')
rdaw = Namespace('http://rdaregistry.info/Elements/w/')
rdax = Namespace('https://doi.org/10.6069/uwlib.55.d.4#')
rdf = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
rdfs = Namespace('http://www.w3.org/2000/01/rdf-schema#')
rml = Namespace('http://semweb.mmlab.be/ns/rml#')
rr = Namespace('http://www.w3.org/ns/r2rml#')
schema = Namespace('http://schema.org/')
sin = Namespace('http://sinopia.io/vocabulary/')
skos = Namespace('http://www.w3.org/2004/02/skos/core#')

"""Functions"""
def generate_bnode_po_map(RML_graph, map_name, bnode_map_name, predicate):
	bnode_po_map = BNode()
	object_map = BNode()
	map_name = URIRef(f"http://example.org/entity/{map_name}Map")
	bnode_map_name = URIRef(f"http://example.org/entity/{bnode_map_name}Map")
	predicate = convert_string_to_IRI(predicate)

	RML_graph.add((map_name, rr.predicateObjectMap, bnode_po_map))
	RML_graph.add((bnode_po_map, rr.predicate, predicate))
	RML_graph.add((bnode_po_map, rr.objectMap, object_map))
	RML_graph.add((object_map, rr.parentTriplesMap, bnode_map_name))

	return RML_graph

def generate_langnotlang_literal_po_main_map(RML_graph, map_name, predicate, property_number):
	map_name = URIRef(f"http://example.org/entity/{map_name}Map")
	predicate = convert_string_to_IRI(predicate)
	# lang
	po_map_lang = BNode()
	object_map_lang = BNode()
	language_map = BNode()
	property_number_lang = Literal(f'{property_number}[not(@resource)][@lang]')
	language_map_reference = Literal(f'{property_number}/@lang')

	RML_graph.add((map_name, rr.predicateObjectMap, po_map_lang))
	RML_graph.add((po_map_lang, rr.predicate, predicate))
	RML_graph.add((po_map_lang, rr.objectMap, object_map_lang))
	RML_graph.add((object_map_lang, rml.reference, property_number_lang))
	RML_graph.add((object_map_lang, rr.termType, rr.Literal))
	RML_graph.add((object_map_lang, rml.languageMap, language_map))
	RML_graph.add((language_map, rml.reference, language_map_reference))

	# not lang
	po_map_not_lang = BNode()
	object_map_not_lang = BNode()
	property_number_not_lang = Literal(f'{property_number}[not(@resource) and not(@lang)]')

	RML_graph.add((map_name, rr.predicateObjectMap, po_map_not_lang))
	RML_graph.add((po_map_not_lang, rr.predicate, predicate))
	RML_graph.add((po_map_not_lang, rr.objectMap, object_map_not_lang))
	RML_graph.add((object_map_not_lang, rml.reference, property_number_not_lang))
	RML_graph.add((object_map_not_lang, rr.termType, rr.Literal))

	return RML_graph

def generate_neutral_literal_po_main_map(RML_graph, map_name, predicate, property_number):
	map_name = URIRef(f"http://example.org/entity/{map_name}Map")
	predicate = convert_string_to_IRI(predicate)
	property_number = Literal(f'{property_number}[not(@resource)]')

	po_map = BNode()
	object_map = BNode()

	RML_graph.add((map_name, rr.predicateObjectMap, po_map))
	RML_graph.add((po_map, rr.predicate, predicate))
	RML_graph.add((po_map, rr.objectMap, object_map))
	RML_graph.add((object_map, rml.reference, property_number))
	RML_graph.add((object_map, rr.termType, rr.Literal))

	return RML_graph

def generate_IRI_po_main_map(RML_graph, map_name, predicate, property_number):
	map_name = URIRef(f"http://example.org/entity/{map_name}Map")
	if "*" not in predicate:
		print(f"{predicate} -- are you sure this takes an IRI?")
		quit()
	else:
		predicate = predicate.strip('*')
		predicate = convert_string_to_IRI(predicate)
	property_number = Literal(f'{property_number}/@resource')

	po_map = BNode()
	object_map = BNode()

	RML_graph.add((map_name, rr.predicateObjectMap, po_map))
	RML_graph.add((po_map, rr.predicate, predicate))
	RML_graph.add((po_map, rr.objectMap, object_map))
	RML_graph.add((object_map, rml.reference, property_number))
	RML_graph.add((object_map, rr.termType, rr.IRI))

	return RML_graph

def generate_lang_literal_split_po_map(RML_graph, map_name, predicate, RDA_prop):
	if RDA_prop in classification_props:
		generate_not_lang_literal_split_po_map(RML_graph, map_name, predicate, RDA_prop)
	else:
		RDA_prop = RDA_prop[0].split(":")[-1]
		map_name = URIRef(f"http://example.org/entity/{map_name}Map")
		predicate = convert_string_to_IRI(predicate)

		po_map = BNode()
		object_map = BNode()
		language_map = BNode()

		reference_value = Literal('.')
		lang_map_value = Literal('@lang')

		RML_graph.add((map_name, rr.predicateObjectMap, po_map))
		RML_graph.add((po_map, rr.predicate, predicate))
		RML_graph.add((po_map, rr.objectMap, object_map))
		RML_graph.add((object_map, rml.reference, reference_value))
		RML_graph.add((object_map, rr.termType, rr.Literal))
		RML_graph.add((object_map, rml.languageMap, language_map))
		RML_graph.add((language_map, rml.reference, lang_map_value))

		return RML_graph

def generate_not_lang_literal_split_po_map(RML_graph, map_name, predicate, RDA_prop):
	RDA_prop = RDA_prop.split(":")[-1]
	map_name = URIRef(f"http://example.org/entity/{map_name}Map")
	predicate = convert_string_to_IRI(predicate)

	po_map = BNode()
	object_map = BNode()

	if RDA_prop in classification_props:
		reference_value = Literal(RDA_prop)
	else:
		reference_value = Literal('.')

	RML_graph.add((map_name, rr.predicateObjectMap, po_map))
	RML_graph.add((po_map, rr.predicate, predicate))
	RML_graph.add((po_map, rr.objectMap, object_map))
	RML_graph.add((object_map, rml.reference, reference_value))
	RML_graph.add((object_map, rr.termType, rr.Literal))

	return RML_graph

def generate_neutral_literal_split_po_map(RML_graph, map_name, predicate):
	map_name = URIRef(f"http://example.org/entity/{map_name}Map")
	predicate = convert_string_to_IRI(predicate)

	po_map = BNode()
	object_map = BNode()

	RML_graph.add((map_name, rr.predicateObjectMap, po_map))
	RML_graph.add((po_map, rr.predicate, predicate))
	RML_graph.add((po_map, rr.objectMap, object_map))
	RML_graph.add((object_map, rml.reference, Literal('.')))
	RML_graph.add((object_map, rr.termType, rr.Literal))

	return RML_graph

def generate_IRI_split_po_map(RML_graph, map_name, predicate):
	map_name = URIRef(f"http://example.org/entity/{map_name}Map")
	if "*" not in predicate:
		print(f"{predicate} -- are you sure this takes an IRI?")
		quit()
	else:
		predicate = predicate.strip('*')
		predicate = convert_string_to_IRI(predicate)

	po_map = BNode()
	object_map = BNode()

	RML_graph.add((map_name, rr.predicateObjectMap, po_map))
	RML_graph.add((po_map, rr.predicate, predicate))
	RML_graph.add((po_map, rr.objectMap, object_map))
	RML_graph.add((object_map, rml.reference, Literal('self::node()')))
	RML_graph.add((object_map, rr.termType, rr.IRI))

	return RML_graph

def generate_lang_literal_nosplit_po_map(RML_graph, map_name, property_number):
	map_name = URIRef(f"http://example.org/entity/{map_name}Map")
	predicate = convert_string_to_IRI(predicate)
	property_number = Literal(f'{property_number}[not(@resource)][@lang]')

	po_map = BNode()
	object_map = BNode()
	language_map = BNode()
	language_map_reference = Literal(f'{property_number}/@lang')

	RML_graph.add((map_name, rr.predicateObjectMap, po_map))
	RML_graph.add((po_map, rr.predicate, predicate))
	RML_graph.add((po_map, rr.objectMap, object_map))
	RML_graph.add((object_map, rml.reference, property_number))
	RML_graph.add((object_map, rr.termType, rr.Literal))
	RML_graph.add((object_map, rml.languageMap, language_map))
	RML_graph.add((language_map, rml.reference, language_map_reference))

	return RML_graph

def generate_not_lang_literal_nosplit_po_map(RML_graph, map_name, property_number):
	map_name = URIRef(f"http://example.org/entity/{map_name}Map")
	predicate = convert_string_to_IRI(predicate)
	property_number = Literal(f'{property_number}[not(@resource) and not(@lang)]')

	po_map = BNode()
	object_map = BNode()

	RML_graph.add((map_name, rr.predicateObjectMap, po_map))
	RML_graph.add((po_map, rr.predicate, predicate))
	RML_graph.add((po_map, rr.objectMap, object_map))
	RML_graph.add((object_map, rml.reference, property_number))
	RML_graph.add((object_map, rr.termType, rr.Literal))

	return RML_graph

def generate_neutral_literal_nosplit_po_map(RML_graph, map_name, predicate, property_number):
	map_name = URIRef(f"http://example.org/entity/{map_name}Map")
	predicate = convert_string_to_IRI(predicate)
	property_number = Literal(f'{property_number}')

	po_map = BNode()
	object_map = BNode()

	RML_graph.add((map_name, rr.predicateObjectMap, po_map))
	RML_graph.add((po_map, rr.predicate, predicate))
	RML_graph.add((po_map, rr.objectMap, object_map))
	RML_graph.add((object_map, rml.reference, property_number))
	RML_graph.add((object_map, rr.termType, rr.Literal))

	return RML_graph

def generate_IRI_nosplit_po_map(RML_graph, map_name, predicate, property_number):
	map_name = URIRef(f"http://example.org/entity/{map_name}Map")
	if "*" not in predicate:
		print(f"{predicate} -- are you sure this takes an IRI?")
		quit()
	else:
		predicate = predicate.strip('*')
		predicate = convert_string_to_IRI(predicate)
	property_number = Literal(f'{property_number}/@resource')

	po_map = BNode()
	object_map = BNode()

	RML_graph.add((map_name, rr.predicateObjectMap, po_map))
	RML_graph.add((po_map, rr.predicate, predicate))
	RML_graph.add((po_map, rr.objectMap, object_map))
	RML_graph.add((object_map, rml.reference, property_number))
	RML_graph.add((object_map, rr.termType, rr.IRI))

	return RML_graph

def generate_constant_IRI(RML_graph, map_name, constant):
	map_name = URIRef(f"http://example.org/entity/{map_name}Map")
	constant_pair = generate_constant(constant)
	predicate = constant_pair[0]
	constant = constant_pair[1]

	po_map = BNode()
	object_map = BNode()

	RML_graph.add((map_name, rr.predicateObjectMap, po_map))
	RML_graph.add((po_map, rr.predicate, predicate))
	RML_graph.add((po_map, rr.objectMap, object_map))
	RML_graph.add((object_map, rr.constant, constant))
	RML_graph.add((object_map, rr.termType, rr.IRI))

	return RML_graph

def generate_constant_literal(RML_graph, map_name, constant, language="en"):
	map_name = URIRef(f"http://example.org/entity/{map_name}Map")
	constant_pair = generate_constant(constant)
	predicate = constant_pair[0]
	constant = constant_pair[1]

	po_map = BNode()
	object_map = BNode()

	RML_graph.add((map_name, rr.predicateObjectMap, po_map))
	RML_graph.add((po_map, rr.predicate, predicate))
	RML_graph.add((po_map, rr.objectMap, object_map))
	RML_graph.add((object_map, rr.constant, constant))
	RML_graph.add((object_map, rr.termType, rr.Literal))
	RML_graph.add((object_map, rr.language, Literal(language)))

	return RML_graph
