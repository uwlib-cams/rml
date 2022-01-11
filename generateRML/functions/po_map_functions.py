"""Python Libraries/Modules/Packages"""
from rdflib import *

"""Lists"""
from functions.lists import classification_props
from functions.lists import no_language_tag_list
from functions.lists import nosplit_bnode_list

"""Imported Functions"""
from functions.formatting_functions import convert_string_to_IRI
from functions.formatting_functions import create_bnode_name
from functions.formatting_functions import generate_constant
from functions.logical_source_functions import generate_constant_logical_source
from functions.logical_source_functions import generate_dissertation_logical_source
from functions.logical_source_functions import generate_IRI_logical_source
from functions.logical_source_functions import generate_lang_logical_source
from functions.logical_source_functions import generate_lang_nosplit_logical_source
from functions.logical_source_functions import generate_neutral_literal_logical_source
from functions.logical_source_functions import generate_not_lang_logical_source
from functions.logical_source_functions import generate_not_lang_nosplit_logical_source
from functions.logical_source_functions import generate_title_logical_source
from functions.subject_map_functions import generate_bnode_subject_map

"""Namespaces"""
rml = Namespace('http://semweb.mmlab.be/ns/rml#')
rr = Namespace('http://www.w3.org/ns/r2rml#')

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

def generate_langnotlang_literal_po_map(RML_graph, map_name, predicate, property_number):
	map_name = URIRef(f"http://example.org/entity/{map_name}Map")
	predicate = convert_string_to_IRI(predicate)
	# lang
	po_map_lang = BNode()
	object_map_lang = BNode()
	language_map = BNode()
	property_number_lang = Literal(f'{property_number}[not(@rdf:resource)][@xml:lang]')
	language_map_reference = Literal(f'{property_number}/@xml:lang')

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
	property_number_not_lang = Literal(f'{property_number}[not(@rdf:resource) and not(@xml:lang)]')

	RML_graph.add((map_name, rr.predicateObjectMap, po_map_not_lang))
	RML_graph.add((po_map_not_lang, rr.predicate, predicate))
	RML_graph.add((po_map_not_lang, rr.objectMap, object_map_not_lang))
	RML_graph.add((object_map_not_lang, rml.reference, property_number_not_lang))
	RML_graph.add((object_map_not_lang, rr.termType, rr.Literal))

	return RML_graph

def generate_neutral_literal_po_map(RML_graph, map_name, predicate, property_number):
	map_name = URIRef(f"http://example.org/entity/{map_name}Map")
	predicate = convert_string_to_IRI(predicate)
	property_number = Literal(f'{property_number}[not(@rdf:resource)]')

	po_map = BNode()
	object_map = BNode()

	RML_graph.add((map_name, rr.predicateObjectMap, po_map))
	RML_graph.add((po_map, rr.predicate, predicate))
	RML_graph.add((po_map, rr.objectMap, object_map))
	RML_graph.add((object_map, rml.reference, property_number))
	RML_graph.add((object_map, rr.termType, rr.Literal))

	return RML_graph

def generate_IRI_po_map(RML_graph, map_name, predicate, property_number):
	map_name = URIRef(f"http://example.org/entity/{map_name}Map")
	if "*" not in predicate:
		print(f"{predicate} -- are you sure this takes an IRI?")
		quit()
	else:
		predicate = predicate.strip('*')
		predicate = convert_string_to_IRI(predicate)
	property_number = Literal(f'{property_number}/@rdf:resource')

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
		lang_map_value = Literal('@xml:lang')

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
	property_number = Literal(f'{property_number}[not(@rdf:resource)][@xml:lang]')

	po_map = BNode()
	object_map = BNode()
	language_map = BNode()
	language_map_reference = Literal(f'{property_number}/@xml:lang')

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
	property_number = Literal(f'{property_number}[not(@rdf:resource) and not(@xml:lang)]')

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
	property_number = Literal(f'{property_number}/@rdf:resource')

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
