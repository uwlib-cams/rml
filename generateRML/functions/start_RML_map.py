"""Python Libraries/Modules/Packages"""
from rdflib import *

"""Namespaces"""
# rml namespaces
ex = Namespace('http://example.org/entity/')
ql = Namespace('http://semweb.mmlab.be/ns/ql#')
rml = Namespace('http://semweb.mmlab.be/ns/rml#')
rr = Namespace('http://www.w3.org/ns/r2rml#')

# output namespaces
bf = Namespace('http://id.loc.gov/ontologies/bibframe/')
bflc = Namespace('http://id.loc.gov/ontologies/bflc/')
madsrdf = Namespace('http://www.loc.gov/mads/rdf/v1#')
rdf = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
rdfs = Namespace('http://www.w3.org/2000/01/rdf-schema#')
skos = Namespace('http://www.w3.org/2004/02/skos/core#')

"""Functions"""
def start_RML_map():
	# start graph
	RML_graph = Graph()

	# bind rml namespaces
	RML_graph.bind('ex', ex)
	RML_graph.bind('ql', ql)
	RML_graph.bind('rml', rml)
	RML_graph.bind('rr', rr)

	# bind output namespaces
	RML_graph.bind('bf', bf)
	RML_graph.bind('bflc', bflc)
	RML_graph.bind('madsrdf', madsrdf)
	RML_graph.bind('rdf', rdf)
	RML_graph.bind('rdfs', rdfs)
	RML_graph.bind('skos', skos)

	return RML_graph
