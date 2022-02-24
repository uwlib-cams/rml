"""Python Libraries/Modules/Packages"""
from rdflib import *

"""Imported Functions"""
from functions.formatting_functions import convert_string_to_IRI

"""Namespaces"""
bf = Namespace('http://id.loc.gov/ontologies/bibframe/')
ex = Namespace('http://example.org/entity/')
rml = Namespace('http://semweb.mmlab.be/ns/rml#')
rr = Namespace('http://www.w3.org/ns/r2rml#')

"""Functions"""
def generate_main_subject_map(RML_graph, entity):
	"""Set defaults based on entity"""
	if entity.lower() == "work":
		default_map = ex.WorkMap
		class_name = bf.Work
	elif entity.lower() == "expression":
		default_map = ex.ExpressionMap
		class_name = bf.Work
	elif entity.lower() == "manifestation":
		default_map = ex.ManifestationMap
		class_name = bf.Instance
	elif entity.lower() == "item":
		default_map = ex.ItemMap
		class_name = bf.Item

	"""Set other variables"""
	main_subject_map = BNode()
	class_property = URIRef('http://www.w3.org/ns/r2rml#class') # MCM: using full URI because it throws an error when you just enter rr.class

	"""Add triples"""
	RML_graph.add((default_map, rr.subjectMap, main_subject_map))
	RML_graph.add((main_subject_map, rml.reference, Literal("@rdf:about")))
	RML_graph.add((main_subject_map, class_property, class_name))

	return RML_graph

def generate_bnode_subject_map(RML_graph, map_name, class_name):
	"""Set variables"""
	bnode_subject_map = BNode()
	map_name = URIRef(f"http://example.org/entity/{map_name}Map")
	class_property = URIRef('http://www.w3.org/ns/r2rml#class') # throws an error when you just enter rr.class
	class_name = convert_string_to_IRI(class_name)

	"""Add triples"""
	RML_graph.add((map_name, rr.subjectMap, bnode_subject_map))
	RML_graph.add((bnode_subject_map, rr.termType, rr.BlankNode))
	RML_graph.add((bnode_subject_map, class_property, class_name))

	return RML_graph
