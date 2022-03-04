"""Python Libraries/Modules/Packages"""
from rdflib import *

"""Lists"""
from functions.lists import classificationLcc_props
from functions.lists import classificationNlm_props
from functions.lists import expression_title_props
from functions.lists import item_title_props
from functions.lists import manifestation_title_props
from functions.lists import provisionActivityDistributionList
from functions.lists import provisionActivityManufactureList
from functions.lists import provisionActivityProductionList
from functions.lists import provisionActivityPublicationList
from functions.lists import work_title_props

"""Namespaces"""
ex = Namespace('http://example.org/entity/')
ql = Namespace('http://semweb.mmlab.be/ns/ql#')
rdf = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
rml = Namespace('http://semweb.mmlab.be/ns/rml#')
rr = Namespace('http://www.w3.org/ns/r2rml#')

"""Functions"""
def generate_main_logical_source(RML_graph, entity):
	"""Set defaults based on entity"""
	if entity.lower() == "work":
		default_map = ex.WorkMap
		default_path = Literal("!!work_filepath!!.xml")
		default_iterator = Literal("/rdf:RDF/rdf:Description[rdf:type/@rdf:resource='http://rdaregistry.info/Elements/c/C10001']")
	elif entity.lower() == "expression":
		default_map = ex.ExpressionMap
		default_path = Literal("!!expression_filepath!!.xml")
		default_iterator = Literal("/rdf:RDF/rdf:Description[rdf:type/@rdf:resource='http://rdaregistry.info/Elements/c/C10006']")
	elif entity.lower() == "manifestation":
		default_map = ex.ManifestationMap
		default_path = Literal("!!manifestation_filepath!!.xml")
		default_iterator = Literal("/rdf:RDF/rdf:Description[rdf:type/@rdf:resource='http://rdaregistry.info/Elements/c/C10007']")
	elif entity.lower() == "item":
		default_map = ex.ItemMap
		default_path = Literal("!!item_filepath!!.xml")
		default_iterator = Literal("/rdf:RDF/rdf:Description[rdf:type/@rdf:resource='http://rdaregistry.info/Elements/c/C10003']")

	"""Set other variables"""
	main_logical_source = BNode()

	"""Add triples"""
	RML_graph.add((default_map, rdf.type, rr.TriplesMap))
	RML_graph.add((default_map, rml.logicalSource, main_logical_source))
	RML_graph.add((main_logical_source, rml.source, default_path))
	RML_graph.add((main_logical_source, rml.referenceFormulation, ql.XPath))
	RML_graph.add((main_logical_source, rml.iterator, default_iterator))

	return RML_graph

def generate_IRI_logical_source(RML_graph, entity, map_name, property_number):
	"""Logical sources for blank nodes where the property takes an IRI"""

	"""Set defaults based on entity"""
	if entity.lower() == "work":
		default_path = Literal("!!work_filepath!!.xml")
	elif entity.lower() == "expression":
		default_path = Literal("!!expression_filepath!!.xml")
	elif entity.lower() == "manifestation":
		default_path = Literal("!!manifestation_filepath!!.xml")
	elif entity.lower() == "item":
		default_path = Literal("!!item_filepath!!.xml")

	"""Set other variables"""
	map_name = URIRef(f"http://example.org/entity/{map_name}Map")
	IRI_logical_source = BNode()
	IRI_iterator = Literal(f"/rdf:RDF/rdf:Description/{property_number}/@rdf:resource")

	"""Add triples"""
	RML_graph.add((map_name, rdf.type, rr.TriplesMap))
	RML_graph.add((map_name, rml.logicalSource, IRI_logical_source))
	RML_graph.add((IRI_logical_source, rml.source, default_path))
	RML_graph.add((IRI_logical_source, rml.referenceFormulation, ql.XPath))
	RML_graph.add((IRI_logical_source, rml.iterator, IRI_iterator))

	return RML_graph

def generate_neutral_literal_logical_source(RML_graph, entity, map_name, property_number):
	"""Logical source for blank nodes where the property takes a literal"""
	"""This applies to literals regardless of whether or not they have a language tag (i.e. neutral)"""
	"""The language tags for these literals (if they exist) are *NOT* recorded"""

	"""Set defaults based on entity"""
	if entity.lower() == "work":
		default_path = Literal("!!work_filepath!!.xml")
	elif entity.lower() == "expression":
		default_path = Literal("!!expression_filepath!!.xml")
	elif entity.lower() == "manifestation":
		default_path = Literal("!!manifestation_filepath!!.xml")
	elif entity.lower() == "item":
		default_path = Literal("!!item_filepath!!.xml")

	"""Set other variables"""
	map_name = URIRef(f"http://example.org/entity/{map_name}Map")
	neutral_literal_logical_source = BNode()
	neutral_literal_iterator = Literal(f"/rdf:RDF/rdf:Description/{property_number}[not(@rdf:resource)]")

	"""Add triples"""
	RML_graph.add((map_name, rdf.type, rr.TriplesMap))
	RML_graph.add((map_name, rml.logicalSource, neutral_literal_logical_source))
	RML_graph.add((neutral_literal_logical_source, rml.source, default_path))
	RML_graph.add((neutral_literal_logical_source, rml.referenceFormulation, ql.XPath))
	RML_graph.add((neutral_literal_logical_source, rml.iterator, neutral_literal_iterator))

	return RML_graph

def generate_lang_logical_source(RML_graph, entity, map_name, property_number):
	"""Logical source for blank nodes where the property takes a literal"""
	"""This will only apply to literals that have a language tag (i.e. lang)"""
	"""The language tags for these literals *ARE* recorded"""

	"""Set defaults based on entity"""
	if entity.lower() == "work":
		default_path = Literal("!!work_filepath!!.xml")
	elif entity.lower() == "expression":
		default_path = Literal("!!expression_filepath!!.xml")
	elif entity.lower() == "manifestation":
		default_path = Literal("!!manifestation_filepath!!.xml")
	elif entity.lower() == "item":
		default_path = Literal("!!item_filepath!!.xml")

	"""Set other variables"""
	map_name = URIRef(f"http://example.org/entity/{map_name}Map")
	lang_logical_source = BNode()
	lang_iterator = Literal(f"/rdf:RDF/rdf:Description/{property_number}[not(@rdf:resource)][@xml:lang]")

	"""Add triples"""
	RML_graph.add((map_name, rdf.type, rr.TriplesMap))
	RML_graph.add((map_name, rml.logicalSource, lang_logical_source))
	RML_graph.add((lang_logical_source, rml.source, default_path))
	RML_graph.add((lang_logical_source, rml.referenceFormulation, ql.XPath))
	RML_graph.add((lang_logical_source, rml.iterator, lang_iterator))

	return RML_graph

def generate_not_lang_logical_source(RML_graph, entity, map_name, property_number):
	"""Logical source for blank nodes where the property takes a literal"""
	"""This will only apply to literals that do *NOT* have a language tag (i.e. not_lang)"""
	"""The language tags for these literals are *NOT* recorded (because they don't exist)"""

	"""Set defaults based on entity"""
	if entity.lower() == "work":
		default_path = Literal("!!work_filepath!!.xml")
	elif entity.lower() == "expression":
		default_path = Literal("!!expression_filepath!!.xml")
	elif entity.lower() == "manifestation":
		default_path = Literal("!!manifestation_filepath!!.xml")
	elif entity.lower() == "item":
		default_path = Literal("!!item_filepath!!.xml")

	"""Set other variables"""
	map_name = URIRef(f"http://example.org/entity/{map_name}Map")
	not_lang_logical_source = BNode()
	not_lang_iterator = Literal(f"/rdf:RDF/rdf:Description/{property_number}[not(@rdf:resource) and not(@xml:lang)]")

	"""Add triples"""
	RML_graph.add((map_name, rdf.type, rr.TriplesMap))
	RML_graph.add((map_name, rml.logicalSource, not_lang_logical_source))
	RML_graph.add((not_lang_logical_source, rml.source, default_path))
	RML_graph.add((not_lang_logical_source, rml.referenceFormulation, ql.XPath))
	RML_graph.add((not_lang_logical_source, rml.iterator, not_lang_iterator))

	return RML_graph

def generate_constant_logical_source(RML_graph, entity, map_name, property_number):
	"""Logical source for blank nodes that only contain a constant IRI or literal"""

	"""Set defaults based on entity"""
	if entity.lower() == "work":
		default_path = Literal("!!work_filepath!!.xml")
	elif entity.lower() == "expression":
		default_path = Literal("!!expression_filepath!!.xml")
	elif entity.lower() == "manifestation":
		default_path = Literal("!!manifestation_filepath!!.xml")
	elif entity.lower() == "item":
		default_path = Literal("!!item_filepath!!.xml")

	"""Set defaults based on value type"""
	if "Literal" in map_name:
		if "Not_" in map_name and "Lang_" in map_name:
			constant_iterator = Literal(f"/rdf:RDF/rdf:Description[{property_number}[not(@rdf:resource) and not(@xml:lang)]]")
		elif "Lang_" in map_name:
			constant_iterator = Literal(f"/rdf:RDF/rdf:Description[{property_number}[not(@rdf:resource)][@xml:lang]]")
		else:
			constant_iterator = Literal(f"/rdf:RDF/rdf:Description[{property_number}[not(@rdf:resource)]]")
	elif "IRI" in map_name:
		constant_iterator = Literal(f"/rdf:RDF/rdf:Description[{property_number}[@rdf:resource]]")

	"""Set other variables"""
	map_name = URIRef(f"http://example.org/entity/{map_name}Map")
	constant_logical_source = BNode()

	"""Add triples"""
	RML_graph.add((map_name, rdf.type, rr.TriplesMap))
	RML_graph.add((map_name, rml.logicalSource, constant_logical_source))
	RML_graph.add((constant_logical_source, rml.source, default_path))
	RML_graph.add((constant_logical_source, rml.referenceFormulation, ql.XPath))
	RML_graph.add((constant_logical_source, rml.iterator, constant_iterator))

	return RML_graph

def generate_provact_logical_source(RML_graph, class_name, map_name):
	"""Logical source for blank nodes that are the value of bf:provisionActivity"""

	"""Set defaults based on blank node class"""
	if class_name == "Distribution":
		property_numbers = " or ".join(provisionActivityDistributionList)
	elif class_name == "Manufacture":
		property_numbers = " or ".join(provisionActivityManufactureList)
	elif class_name == "Production":
		property_numbers = " or ".join(provisionActivityProductionList)
	elif class_name == "Publication":
		property_numbers = " or ".join(provisionActivityPublicationList)

	"""Set other variables"""
	map_name = URIRef(f"http://example.org/entity/{map_name}Map")
	provact_logical_source = BNode()
	provact_iterator = Literal(f"/rdf:RDF/rdf:Description[{property_numbers}]")
	manifestation_path = Literal("!!manifestation_filepath!!.xml")

	"""Add triples"""
	RML_graph.add((map_name, rdf.type, rr.TriplesMap))
	RML_graph.add((map_name, rml.logicalSource, provact_logical_source))
	RML_graph.add((provact_logical_source, rml.source, manifestation_path))
	RML_graph.add((provact_logical_source, rml.referenceFormulation, ql.XPath))
	RML_graph.add((provact_logical_source, rml.iterator, provact_iterator))

	return RML_graph

def generate_title_logical_source(RML_graph, entity, map_name):
	"""Logical source for blank nodes that are the value of bf:title"""

	"""Set defaults based on entity"""
	if entity.lower() == "work":
		default_path = Literal("!!work_filepath!!.xml")
		property_numbers = " or ".join(work_title_props)
	elif entity.lower() == "expression":
		default_path = Literal("!!expression_filepath!!.xml")
		property_numbers = " or ".join(expression_title_props)
	elif entity.lower() == "manifestation":
		default_path = Literal("!!manifestation_filepath!!.xml")
		property_numbers = " or ".join(manifestation_title_props)
	elif entity.lower() == "item":
		default_path = Literal("!!item_filepath!!.xml")
		property_numbers = " or ".join(item_title_props)

	"""Set other variables"""
	map_name = URIRef(f"http://example.org/entity/{map_name}Map")
	title_logical_source = BNode()
	title_iterator = Literal(f"/rdf:RDF/rdf:Description[{property_numbers}]")

	"""Add triples"""
	RML_graph.add((map_name, rdf.type, rr.TriplesMap))
	RML_graph.add((map_name, rml.logicalSource, title_logical_source))
	RML_graph.add((title_logical_source, rml.source, default_path))
	RML_graph.add((title_logical_source, rml.referenceFormulation, ql.XPath))
	RML_graph.add((title_logical_source, rml.iterator, title_iterator))

	return RML_graph

def generate_classification_logical_source(RML_graph, entity, map_name):
	"""Logical source for blank nodes classed as bf:ClassificationLcc or bf:ClassificationNlm"""

	"""Set defaults based on entity"""
	if entity.lower() == "manifestation":
		default_path = Literal("!!manifestation_filepath!!.xml")
	elif entity.lower() == "item":
		default_path = Literal("!!item_filepath!!.xml")

	"""Set defaults based on blank node class"""
	if "Lcc" in map_name:
		property_numbers = " or ".join(classificationLcc_props)
	elif "Nlm" in map_name:
		property_numbers = " or ".join(classificationNlm_props)

	"""Set other variables"""
	map_name = URIRef(f"http://example.org/entity/{map_name}Map")
	classification_logical_source = BNode()
	classification_iterator = Literal(f"/rdf:RDF/rdf:Description[{property_numbers}]")

	"""Add triples"""
	RML_graph.add((map_name, rdf.type, rr.TriplesMap))
	RML_graph.add((map_name, rml.logicalSource, classification_logical_source))
	RML_graph.add((classification_logical_source, rml.source, default_path))
	RML_graph.add((classification_logical_source, rml.referenceFormulation, ql.XPath))
	RML_graph.add((classification_logical_source, rml.iterator, classification_iterator))

	return RML_graph

def generate_dissertation_logical_source(RML_graph, map_name):
	"""Logical source for blank nodes classed as bf:Dissertation"""

	"""Set variables"""
	work_path = Literal("!!work_filepath!!.xml")
	property_numbers = " or ".join(dissertationList)
	dissertation_iterator = Literal(f"/rdf:RDF/rdf:Description[{property_numbers}]")
	map_name = URIRef(f"http://example.org/entity/{map_name}Map")
	dissertation_logical_source = BNode()

	RML_graph.add((map_name, rdf.type, rr.TriplesMap))
	RML_graph.add((map_name, rml.logicalSource, dissertation_logical_source))
	RML_graph.add((dissertation_logical_source, rml.source, work_path))
	RML_graph.add((dissertation_logical_source, rml.referenceFormulation, ql.XPath))
	RML_graph.add((dissertation_logical_source, rml.iterator, dissertation_iterator))

	return RML_graph

def generate_lang_nosplit_logical_source(RML_graph, entity, map_name, property_number):
	"""Logical source for "no-split" blank nodes"""
	# See: https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#nosplit_bnode_list
	"""If generated for a literal, this will only apply to literals that have a language tag (i.e. lang)"""
	"""The language tags for these literals *ARE* recorded"""

	"""Set defaults based on entity"""
	if entity.lower() == "work":
		default_path = Literal("!!work_filepath!!.xml")
	elif entity.lower() == "expression":
		default_path = Literal("!!expression_filepath!!.xml")
	elif entity.lower() == "manifestation":
		default_path = Literal("!!manifestation_filepath!!.xml")
	elif entity.lower() == "item":
		default_path = Literal("!!item_filepath!!.xml")

	"""Set defaults based on value type"""
	if "IRI" in map_name:
		lang_nosplit_iterator = Literal(f"/rdf:RDF/rdf:Description[{property_number}[@rdf:resource]]")
	else:
		lang_nosplit_iterator = Literal(f"/rdf:RDF/rdf:Description[{property_number}[not(@rdf:resource)][@xml:lang]]")

	"""Set other variables"""
	map_name = URIRef(f"http://example.org/entity/{map_name}Map")
	lang_nosplit_logical_source = BNode()

	"""Add triples"""
	RML_graph.add((map_name, rdf.type, rr.TriplesMap))
	RML_graph.add((map_name, rml.logicalSource, lang_nosplit_logical_source))
	RML_graph.add((lang_nosplit_logical_source, rml.source, default_path))
	RML_graph.add((lang_nosplit_logical_source, rml.referenceFormulation, ql.XPath))
	RML_graph.add((lang_nosplit_logical_source, rml.iterator, lang_nosplit_iterator))

	return RML_graph

def generate_not_lang_nosplit_logical_source(RML_graph, entity, map_name, property_number):
	"""Logical source for "no-split" blank nodes"""
	# See: https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#nosplit_bnode_list
	"""If generated for a literal, this will only apply to literals that do *NOT* have a language tag (i.e. not_lang)"""
	"""The language tags for these literals are *NOT* recorded (because they don't exist)"""

	"""Set defaults based on entity"""
	if entity.lower() == "work":
		default_path = Literal("!!work_filepath!!.xml")
	elif entity.lower() == "expression":
		default_path = Literal("!!expression_filepath!!.xml")
	elif entity.lower() == "manifestation":
		default_path = Literal("!!manifestation_filepath!!.xml")
	elif entity.lower() == "item":
		default_path = Literal("!!item_filepath!!.xml")

	"""Set defaults based on value type"""
	if "IRI" in map_name:
		not_lang_nosplit_iterator = Literal(f"/rdf:RDF/rdf:Description[{property_numbers}[@rdf:resource]]")
	else:
		not_lang_nosplit_iterator = Literal(f"/rdf:RDF/rdf:Description[{property_number}[not(@rdf:resource) and not(@xml:lang)]]")

	"""Set other variables"""
	map_name = URIRef(f"http://example.org/entity/{map_name}Map")
	not_lang_nosplit_logical_source = BNode()

	"""Add triples"""
	RML_graph.add((map_name, rdf.type, rr.TriplesMap))
	RML_graph.add((map_name, rml.logicalSource, not_lang_nosplit_logical_source))
	RML_graph.add((not_lang_nosplit_logical_source, rml.source, default_path))
	RML_graph.add((not_lang_nosplit_logical_source, rml.referenceFormulation, ql.XPath))
	RML_graph.add((not_lang_nosplit_logical_source, rml.iterator, not_lang_nosplit_iterator))

	return RML_graph
