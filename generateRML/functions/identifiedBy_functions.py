"""Python Libraries/Modules/Packages"""
from rdflib import *

"""Namespaces"""
bf = Namespace('http://id.loc.gov/ontologies/bibframe/')
ex = Namespace('http://example.org/entity/')
ql = Namespace('http://semweb.mmlab.be/ns/ql#')
rdf = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
rml = Namespace('http://semweb.mmlab.be/ns/rml#')
rr = Namespace('http://www.w3.org/ns/r2rml#')

"""Functions"""
def P10002_mapping(RML_graph):
	work_po_map_identifiedBy_bnode = BNode()
	work_object_map_identifiedBy_bnode = BNode()
	work_logical_source_identifiedBy_bnode = BNode()

	work_po_map_identifiedBy_IRI = BNode()
	work_object_map_identifiedBy_IRI = BNode()
	work_logical_source_identifiedBy_IRI = BNode()

	identifiedBy_logical_source = BNode()

	identifiedBy_subject_map = BNode()
	class_property = URIRef('http://www.w3.org/ns/r2rml#class')

	identifiedBy_po_map = BNode()
	identifiedBy_object_map = BNode()

	RML_graph.add((ex.WorkMap, rr.predicateObjectMap, work_po_map_identifiedBy_bnode))
	RML_graph.add((work_po_map_identifiedBy_bnode, rr.predicate, bf.identifiedBy))
	RML_graph.add((work_po_map_identifiedBy_bnode, rr.objectMap, work_object_map_identifiedBy_bnode))
	RML_graph.add((work_object_map_identifiedBy_bnode, rr.parentTriplesMap, ex.IdentifierMap))

	RML_graph.add((ex.WorkMap, rr.predicateObjectMap, work_po_map_identifiedBy_IRI))
	RML_graph.add((work_po_map_identifiedBy_IRI, rr.predicate, bf.identifiedBy))
	RML_graph.add((work_po_map_identifiedBy_IRI, rr.objectMap, work_object_map_identifiedBy_IRI))
	RML_graph.add((work_object_map_identifiedBy_IRI, rml.reference, Literal("rdaw:P10002/@rdf:resource")))
	RML_graph.add((work_object_map_identifiedBy_IRI, rr.termType, rr.IRI))

	RML_graph.add((ex.IdentifierMap, rdf.type, rr.TriplesMap))
	RML_graph.add((ex.IdentifierMap, rml.logicalSource, identifiedBy_logical_source))
	RML_graph.add((identifiedBy_logical_source, rml.source, Literal("!!work_filepath!!.xml")))
	RML_graph.add((identifiedBy_logical_source, rml.referenceFormulation, ql.XPath))
	RML_graph.add((identifiedBy_logical_source, rml.iterator, Literal("/rdf:RDF/rdf:Description/rdaw:P10002[not(@rdf:resource)]")))

	RML_graph.add((ex.IdentifierMap, rr.subjectMap, identifiedBy_subject_map))
	RML_graph.add((identifiedBy_subject_map, rr.termType, rr.BlankNode))
	RML_graph.add((identifiedBy_subject_map, class_property, bf.Identifier))

	RML_graph.add((ex.IdentifierMap, rr.predicateObjectMap, identifiedBy_po_map))
	RML_graph.add((identifiedBy_po_map, rr.predicate, rdf.value))
	RML_graph.add((identifiedBy_po_map, rr.objectMap, identifiedBy_object_map))
	RML_graph.add((identifiedBy_object_map, rml.reference, Literal('.')))
	RML_graph.add((identifiedBy_object_map, rr.termType, rr.Literal))

	return RML_graph

def P20002_mapping(RML_graph):
	expression_po_map_identifiedBy_bnode = BNode()
	expression_object_map_identifiedBy_bnode = BNode()
	expression_logical_source_identifiedBy_bnode = BNode()

	expression_po_map_identifiedBy_IRI = BNode()
	expression_object_map_identifiedBy_IRI = BNode()
	expression_logical_source_identifiedBy_IRI = BNode()

	identifiedBy_logical_source = BNode()

	identifiedBy_subject_map = BNode()
	class_property = URIRef('http://www.w3.org/ns/r2rml#class')

	identifiedBy_po_map = BNode()
	identifiedBy_object_map = BNode()

	RML_graph.add((ex.ExpressionMap, rr.predicateObjectMap, expression_po_map_identifiedBy_bnode))
	RML_graph.add((expression_po_map_identifiedBy_bnode, rr.predicate, bf.identifiedBy))
	RML_graph.add((expression_po_map_identifiedBy_bnode, rr.objectMap, expression_object_map_identifiedBy_bnode))
	RML_graph.add((expression_object_map_identifiedBy_bnode, rr.parentTriplesMap, ex.IdentifierMap))

	RML_graph.add((ex.ExpressionMap, rr.predicateObjectMap, expression_po_map_identifiedBy_IRI))
	RML_graph.add((expression_po_map_identifiedBy_IRI, rr.predicate, bf.identifiedBy))
	RML_graph.add((expression_po_map_identifiedBy_IRI, rr.objectMap, expression_object_map_identifiedBy_IRI))
	RML_graph.add((expression_object_map_identifiedBy_IRI, rml.reference, Literal("rdae:P20002/@rdf:resource")))
	RML_graph.add((expression_object_map_identifiedBy_IRI, rr.termType, rr.IRI))

	RML_graph.add((ex.IdentifierMap, rdf.type, rr.TriplesMap))
	RML_graph.add((ex.IdentifierMap, rml.logicalSource, identifiedBy_logical_source))
	RML_graph.add((identifiedBy_logical_source, rml.source, Literal("!!expression_filepath!!.xml")))
	RML_graph.add((identifiedBy_logical_source, rml.referenceFormulation, ql.XPath))
	RML_graph.add((identifiedBy_logical_source, rml.iterator, Literal("/rdf:RDF/rdf:Description/rdae:P20002[not(@rdf:resource)]")))

	RML_graph.add((ex.IdentifierMap, rr.subjectMap, identifiedBy_subject_map))
	RML_graph.add((identifiedBy_subject_map, rr.termType, rr.BlankNode))
	RML_graph.add((identifiedBy_subject_map, class_property, bf.Identifier))

	RML_graph.add((ex.IdentifierMap, rr.predicateObjectMap, identifiedBy_po_map))
	RML_graph.add((identifiedBy_po_map, rr.predicate, rdf.value))
	RML_graph.add((identifiedBy_po_map, rr.objectMap, identifiedBy_object_map))
	RML_graph.add((identifiedBy_object_map, rml.reference, Literal('.')))
	RML_graph.add((identifiedBy_object_map, rr.termType, rr.Literal))

	return RML_graph

def P30004_mapping(RML_graph):
	manifestation_po_map_identifiedBy_bnode = BNode()
	manifestation_object_map_identifiedBy_bnode = BNode()
	manifestation_logical_source_identifiedBy_bnode = BNode()

	manifestation_po_map_identifiedBy_IRI = BNode()
	manifestation_object_map_identifiedBy_IRI = BNode()
	manifestation_logical_source_identifiedBy_IRI = BNode()

	identifiedBy_logical_source = BNode()

	identifiedBy_subject_map = BNode()
	class_property = URIRef('http://www.w3.org/ns/r2rml#class')

	identifiedBy_po_map = BNode()
	identifiedBy_object_map = BNode()

	# IRIs
	RML_graph.add((ex.ManifestationMap, rr.predicateObjectMap, manifestation_po_map_identifiedBy_IRI))
	RML_graph.add((manifestation_po_map_identifiedBy_IRI, rr.predicate, bf.identifiedBy))
	RML_graph.add((manifestation_po_map_identifiedBy_IRI, rr.objectMap, manifestation_object_map_identifiedBy_IRI))
	RML_graph.add((manifestation_object_map_identifiedBy_IRI, rml.reference, Literal("rdam:P30004/@rdf:resource")))
	RML_graph.add((manifestation_object_map_identifiedBy_IRI, rr.termType, rr.IRI))

	# literals
	RML_graph.add((ex.ManifestationMap, rr.predicateObjectMap, manifestation_po_map_identifiedBy_bnode))
	RML_graph.add((manifestation_po_map_identifiedBy_bnode, rr.predicate, bf.identifiedBy))
	RML_graph.add((manifestation_po_map_identifiedBy_bnode, rr.objectMap, manifestation_object_map_identifiedBy_bnode))
	RML_graph.add((manifestation_object_map_identifiedBy_bnode, rr.parentTriplesMap, ex.IdentifierMap))

	# blank node for literal value
	RML_graph.add((ex.IdentifierMap, rdf.type, rr.TriplesMap))
	RML_graph.add((ex.IdentifierMap, rml.logicalSource, identifiedBy_logical_source))
	RML_graph.add((identifiedBy_logical_source, rml.source, Literal("!!manifestation_filepath!!.xml")))
	RML_graph.add((identifiedBy_logical_source, rml.referenceFormulation, ql.XPath))
	RML_graph.add((identifiedBy_logical_source, rml.iterator, Literal("/rdf:RDF/rdf:Description/rdam:P30004[not(@rdf:resource)]")))

	RML_graph.add((ex.IdentifierMap, rr.subjectMap, identifiedBy_subject_map))
	RML_graph.add((identifiedBy_subject_map, rr.termType, rr.BlankNode))
	RML_graph.add((identifiedBy_subject_map, class_property, bf.Identifier))

	RML_graph.add((ex.IdentifierMap, rr.predicateObjectMap, identifiedBy_po_map))
	RML_graph.add((identifiedBy_po_map, rr.predicate, rdf.value))
	RML_graph.add((identifiedBy_po_map, rr.objectMap, identifiedBy_object_map))
	RML_graph.add((identifiedBy_object_map, rml.reference, Literal('.')))
	RML_graph.add((identifiedBy_object_map, rr.termType, rr.Literal))

	# for rdam:30004 values with wrong namespace in original Sinopia data <http://rdaregistry.info/Elements/m/datatype/>
	manifestation_po_map_identifiedBy_bnode_rdamdt = BNode()
	manifestation_object_map_identifiedBy_bnode_rdamdt = BNode()
	manifestation_logical_source_identifiedBy_bnode_rdamdt = BNode()

	manifestation_po_map_identifiedBy_IRI_rdamdt = BNode()
	manifestation_object_map_identifiedBy_IRI_rdamdt = BNode()
	manifestation_logical_source_identifiedBy_IRI_rdamdt = BNode()

	identifiedBy_logical_source_rdamdt = BNode()

	identifiedBy_subject_map_rdamdt = BNode()

	identifiedBy_po_map_rdamdt = BNode()
	identifiedBy_object_map_rdamdt = BNode()

	# IRIs
	RML_graph.add((ex.ManifestationMap, rr.predicateObjectMap, manifestation_po_map_identifiedBy_IRI_rdamdt))
	RML_graph.add((manifestation_po_map_identifiedBy_IRI_rdamdt, rr.predicate, bf.identifiedBy))
	RML_graph.add((manifestation_po_map_identifiedBy_IRI_rdamdt, rr.objectMap, manifestation_object_map_identifiedBy_IRI_rdamdt))
	RML_graph.add((manifestation_object_map_identifiedBy_IRI_rdamdt, rml.reference, Literal("rdamdt:P30004/@rdf:resource")))
	RML_graph.add((manifestation_object_map_identifiedBy_IRI_rdamdt, rr.termType, rr.IRI))

	# literals
	RML_graph.add((ex.ManifestationMap, rr.predicateObjectMap, manifestation_po_map_identifiedBy_bnode_rdamdt))
	RML_graph.add((manifestation_po_map_identifiedBy_bnode_rdamdt, rr.predicate, bf.identifiedBy))
	RML_graph.add((manifestation_po_map_identifiedBy_bnode_rdamdt, rr.objectMap, manifestation_object_map_identifiedBy_bnode_rdamdt))
	RML_graph.add((manifestation_object_map_identifiedBy_bnode_rdamdt, rr.parentTriplesMap, ex.RdamdtIdentifierMap))

	# blank node for literal value
	RML_graph.add((ex.RdamdtIdentifierMap, rdf.type, rr.TriplesMap))
	RML_graph.add((ex.RdamdtIdentifierMap, rml.logicalSource, identifiedBy_logical_source_rdamdt))
	RML_graph.add((identifiedBy_logical_source_rdamdt, rml.source, Literal("!!manifestation_filepath!!.xml")))
	RML_graph.add((identifiedBy_logical_source_rdamdt, rml.referenceFormulation, ql.XPath))
	RML_graph.add((identifiedBy_logical_source_rdamdt, rml.iterator, Literal("/rdf:RDF/rdf:Description/rdamdt:P30004[not(@rdf:resource)]")))

	RML_graph.add((ex.RdamdtIdentifierMap, rr.subjectMap, identifiedBy_subject_map_rdamdt))
	RML_graph.add((identifiedBy_subject_map_rdamdt, rr.termType, rr.BlankNode))
	RML_graph.add((identifiedBy_subject_map_rdamdt, class_property, bf.Identifier))

	RML_graph.add((ex.RdamdtIdentifierMap, rr.predicateObjectMap, identifiedBy_po_map_rdamdt))
	RML_graph.add((identifiedBy_po_map_rdamdt, rr.predicate, rdf.value))
	RML_graph.add((identifiedBy_po_map_rdamdt, rr.objectMap, identifiedBy_object_map_rdamdt))
	RML_graph.add((identifiedBy_object_map_rdamdt, rml.reference, Literal('.')))
	RML_graph.add((identifiedBy_object_map_rdamdt, rr.termType, rr.Literal))

	return RML_graph

def P40001_mapping(RML_graph):
	item_po_map_identifiedBy_bnode = BNode()
	item_object_map_identifiedBy_bnode = BNode()
	item_logical_source_identifiedBy_bnode = BNode()

	item_po_map_identifiedBy_IRI = BNode()
	item_object_map_identifiedBy_IRI = BNode()
	item_logical_source_identifiedBy_IRI = BNode()

	identifiedBy_logical_source = BNode()

	identifiedBy_subject_map = BNode()
	class_property = URIRef('http://www.w3.org/ns/r2rml#class')

	identifiedBy_po_map = BNode()
	identifiedBy_object_map = BNode()

	RML_graph.add((ex.ItemMap, rr.predicateObjectMap, item_po_map_identifiedBy_bnode))
	RML_graph.add((item_po_map_identifiedBy_bnode, rr.predicate, bf.identifiedBy))
	RML_graph.add((item_po_map_identifiedBy_bnode, rr.objectMap, item_object_map_identifiedBy_bnode))
	RML_graph.add((item_object_map_identifiedBy_bnode, rr.parentTriplesMap, ex.IdentifierMap))

	RML_graph.add((ex.ItemMap, rr.predicateObjectMap, item_po_map_identifiedBy_IRI))
	RML_graph.add((item_po_map_identifiedBy_IRI, rr.predicate, bf.identifiedBy))
	RML_graph.add((item_po_map_identifiedBy_IRI, rr.objectMap, item_object_map_identifiedBy_IRI))
	RML_graph.add((item_object_map_identifiedBy_IRI, rml.reference, Literal("rdai:P40001/@rdf:resource")))
	RML_graph.add((item_object_map_identifiedBy_IRI, rr.termType, rr.IRI))

	RML_graph.add((ex.IdentifierMap, rdf.type, rr.TriplesMap))
	RML_graph.add((ex.IdentifierMap, rml.logicalSource, identifiedBy_logical_source))
	RML_graph.add((identifiedBy_logical_source, rml.source, Literal("!!item_filepath!!.xml")))
	RML_graph.add((identifiedBy_logical_source, rml.referenceFormulation, ql.XPath))
	RML_graph.add((identifiedBy_logical_source, rml.iterator, Literal("/rdf:RDF/rdf:Description/rdai:P40001[not(@rdf:resource)]")))

	RML_graph.add((ex.IdentifierMap, rr.subjectMap, identifiedBy_subject_map))
	RML_graph.add((identifiedBy_subject_map, rr.termType, rr.BlankNode))
	RML_graph.add((identifiedBy_subject_map, class_property, bf.Identifier))

	RML_graph.add((ex.IdentifierMap, rr.predicateObjectMap, identifiedBy_po_map))
	RML_graph.add((identifiedBy_po_map, rr.predicate, rdf.value))
	RML_graph.add((identifiedBy_po_map, rr.objectMap, identifiedBy_object_map))
	RML_graph.add((identifiedBy_object_map, rml.reference, Literal('.')))
	RML_graph.add((identifiedBy_object_map, rr.termType, rr.Literal))

	return RML_graph
