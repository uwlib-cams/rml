"""Python Libraries/Modules/Packages"""
from rdflib import *

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
def start_RML_map():
	# start graph
	RML_graph = Graph()

	# bind to graph all prefixes used in RML, UW's RDA data, and desired BIBFRAME output
	RML_graph.bind('bf', bf)
	RML_graph.bind('bflc', bflc)
	RML_graph.bind('dbo', dbo)
	RML_graph.bind('ex', ex)
	RML_graph.bind('madsrdf', madsrdf)
	RML_graph.bind('ql', ql)
	RML_graph.bind('rdac', rdac)
	RML_graph.bind('rdae', rdae)
	RML_graph.bind('rdai', rdai)
	RML_graph.bind('rdam', rdam)
	RML_graph.bind('rdamdt', rdamdt)
	RML_graph.bind('rdau', rdau)
	RML_graph.bind('rdaw', rdaw)
	RML_graph.bind('rdax', rdax)
	RML_graph.bind('rdf', rdf)
	RML_graph.bind('rdfs', rdfs)
	RML_graph.bind('rml', rml)
	RML_graph.bind('rr', rr)
	RML_graph.bind('schema', schema)
	RML_graph.bind('sin', sin)
	RML_graph.bind('skos', skos)

	return RML_graph
