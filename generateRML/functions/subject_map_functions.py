"""Python Libraries/Modules/Packages"""
from rdflib import *

"""Imported Functions"""
from functions.formatting_functions import convert_string_to_IRI

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
def generate_main_subject_map(RML_graph, entity):
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

	main_subject_map = BNode()
	class_property = URIRef('http://www.w3.org/ns/r2rml#class') # throws an error when you just enter rr.class

	RML_graph.add((default_map, rr.subjectMap, main_subject_map))
	RML_graph.add((main_subject_map, rml.reference, Literal("@rdf:about")))
	RML_graph.add((main_subject_map, class_property, class_name))

	return RML_graph

def generate_bnode_subject_map(RML_graph, map_name, class_name):
	bnode_subject_map = BNode()
	map_name = URIRef(f"http://example.org/entity/{map_name}Map")
	class_property = URIRef('http://www.w3.org/ns/r2rml#class') # throws an error when you just enter rr.class
	class_name = convert_string_to_IRI(class_name)

	RML_graph.add((map_name, rr.subjectMap, bnode_subject_map))
	RML_graph.add((bnode_subject_map, rr.termType, rr.BlankNode))
	RML_graph.add((bnode_subject_map, class_property, class_name))

	return RML_graph
