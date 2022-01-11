"""Python Libraries/Modules/Packages"""
from rdflib import *

"""Namespaces"""
bf = Namespace('http://id.loc.gov/ontologies/bibframe/')
bflc = Namespace('http://id.loc.gov/ontologies/bflc/')
ex = Namespace('http://example.org/entity/')
ql = Namespace('http://semweb.mmlab.be/ns/ql#')
rdf = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
rml = Namespace('http://semweb.mmlab.be/ns/rml#')
rr = Namespace('http://www.w3.org/ns/r2rml#')

"""Functions"""
def admin_metadata_mapping(RML_graph, entity):
	# Establish defaults based on RDA entity
	if entity.lower() == "work":
		default_map = ex.WorkMap
		default_path = Literal("!!work_filepath!!.xml")
	elif entity.lower() == "expression":
		default_map = ex.ExpressionMap
		default_path = Literal("!!expression_filepath!!.xml")
	elif entity.lower() == "manifestation":
		default_map = ex.ManifestationMap
		default_path = Literal("!!manifestation_filepath!!.xml")
	elif entity.lower() == "item":
		default_map = ex.ItemMap
		default_path = Literal("!!item_filepath!!.xml")

	"""Predicate-object map to open admin metadata blank node"""
	# Set variables
	entity_po = BNode()
	entity_object_map = BNode()

	# Add triples to graph
	RML_graph.add((default_map, rr.predicateObjectMap, entity_po))
	RML_graph.add((entity_po, rr.predicate, bf.adminMetadata))
	RML_graph.add((entity_po, rr.objectMap, entity_object_map))
	RML_graph.add((entity_object_map, rr.parentTriplesMap, ex.AdminMetadataMap))

	"""Logical source map for admin metadata blank node"""
	# Set variables
	admin_metadata_logical_source = BNode()
	admin_metadata_iterator = Literal("/rdf:RDF/rdf:Description[bflc:catalogerID]")

	# Add triples to graph
	RML_graph.add((ex.AdminMetadataMap, rdf.type, rr.TriplesMap))
	RML_graph.add((ex.AdminMetadataMap, rml.logicalSource, admin_metadata_logical_source))
	RML_graph.add((admin_metadata_logical_source, rml.source, default_path))
	RML_graph.add((admin_metadata_logical_source, rml.referenceFormulation, ql.XPath))
	RML_graph.add((admin_metadata_logical_source, rml.iterator, admin_metadata_iterator))

	"""Subject map for admin metadata blank node"""
	# Set variables
	admin_metadata_subject_map = BNode()
	class_property = URIRef('http://www.w3.org/ns/r2rml#class') # throwing me an error when you just enter rr.class

	# Add triples to graph
	RML_graph.add((ex.AdminMetadataMap, rr.subjectMap, admin_metadata_subject_map))
	RML_graph.add((admin_metadata_subject_map, rr.termType, rr.BlankNode))
	RML_graph.add((admin_metadata_subject_map, class_property, bf.AdminMetadata))

	"""Predicate-object map for cataloger ID"""
	# Set variables
	catalogerID_po_map = BNode()
	catalogerID_object_map = BNode()

	# Add triples to graph
	RML_graph.add((ex.AdminMetadataMap, rr.predicateObjectMap, catalogerID_po_map))
	RML_graph.add((catalogerID_po_map, rr.predicate, bflc.catalogerId))
	RML_graph.add((catalogerID_po_map, rr.objectMap, catalogerID_object_map))
	RML_graph.add((catalogerID_object_map, rml.reference, Literal("bflc:catalogerID")))
	RML_graph.add((catalogerID_object_map, rr.termType, rr.Literal))

	"""Predicate-object map for encoding level"""
	# Set variables
	encodingLevel_po_map = BNode()
	encodingLevel_object_map = BNode()

	# Add triples to graph
	RML_graph.add((ex.AdminMetadataMap, rr.predicateObjectMap, encodingLevel_po_map))
	RML_graph.add((encodingLevel_po_map, rr.predicate, bflc.encodingLevel))
	RML_graph.add((encodingLevel_po_map, rr.objectMap, encodingLevel_object_map))
	RML_graph.add((encodingLevel_object_map, rml.reference, Literal("bflc:encodingLevel/@rdf:resource")))
	RML_graph.add((encodingLevel_object_map, rr.termType, rr.IRI))

	"""Predicate-object map for description conventions"""
	# Set variables
	descriptionConventions_po_map = BNode()
	descriptionConventions_object_map = BNode()

	# Add triples to graph
	RML_graph.add((ex.AdminMetadataMap, rr.predicateObjectMap, descriptionConventions_po_map))
	RML_graph.add((descriptionConventions_po_map, rr.predicate, bf.descriptionConventions))
	RML_graph.add((descriptionConventions_po_map, rr.objectMap, descriptionConventions_object_map))
	RML_graph.add((descriptionConventions_object_map, rml.reference, Literal("bf:descriptionConventions/@rdf:resource")))
	RML_graph.add((descriptionConventions_object_map, rr.termType, rr.IRI))

	"""Predicate-object map for source"""
	# Set variables
	source_po_map = BNode()
	source_object_map = BNode()

	# Add triples to graph
	RML_graph.add((ex.AdminMetadataMap, rr.predicateObjectMap, source_po_map))
	RML_graph.add((source_po_map, rr.predicate, bf.source))
	RML_graph.add((source_po_map, rr.objectMap, source_object_map))
	RML_graph.add((source_object_map, rml.reference, Literal("bf:source/@rdf:resource")))
	RML_graph.add((source_object_map, rr.termType, rr.IRI))

	"""Predicate-object map for description language"""
	# Set variables
	descriptionLanguage_po_map = BNode()
	descriptionLanguage_object_map = BNode()

	# Add triples to graph
	RML_graph.add((ex.AdminMetadataMap, rr.predicateObjectMap, descriptionLanguage_po_map))
	RML_graph.add((descriptionLanguage_po_map, rr.predicate, bf.descriptionLanguage))
	RML_graph.add((descriptionLanguage_po_map, rr.objectMap, descriptionLanguage_object_map))
	RML_graph.add((descriptionLanguage_object_map, rml.reference, Literal("bf:descriptionLanguage/@rdf:resource")))
	RML_graph.add((descriptionLanguage_object_map, rr.termType, rr.IRI))

	"""Predicate-object map for creation date"""
	# Set variables
	creationDate_po_map = BNode()
	creationDate_object_map = BNode()

	# Add triples to graph
	RML_graph.add((ex.AdminMetadataMap, rr.predicateObjectMap, creationDate_po_map))
	RML_graph.add((creationDate_po_map, rr.predicate, bf.creationDate))
	RML_graph.add((creationDate_po_map, rr.objectMap, creationDate_object_map))
	RML_graph.add((creationDate_object_map, rml.reference, Literal("bf:creationDate")))
	RML_graph.add((creationDate_object_map, rr.termType, rr.Literal))

	"""Predicate-object map for change date"""
	# Set variables
	changeDate_po_map = BNode()
	changeDate_object_map = BNode()

	# Add triples to graph
	RML_graph.add((ex.AdminMetadataMap, rr.predicateObjectMap, changeDate_po_map))
	RML_graph.add((changeDate_po_map, rr.predicate, bf.changeDate))
	RML_graph.add((changeDate_po_map, rr.objectMap, changeDate_object_map))
	RML_graph.add((changeDate_object_map, rml.reference, Literal("bf:changeDate")))
	RML_graph.add((changeDate_object_map, rr.termType, rr.Literal))

	"""Predicate-object map for description authentication"""
	# Set variables
	descriptionAuthentication_po_map = BNode()
	descriptionAuthentication_object_map = BNode()

	# Add triples to graph
	RML_graph.add((ex.AdminMetadataMap, rr.predicateObjectMap, descriptionAuthentication_po_map))
	RML_graph.add((descriptionAuthentication_po_map, rr.predicate, bf.descriptionAuthentication))
	RML_graph.add((descriptionAuthentication_po_map, rr.objectMap, descriptionAuthentication_object_map))
	RML_graph.add((descriptionAuthentication_object_map, rml.reference, Literal("bf:descriptionAuthentication/@rdf:resource")))
	RML_graph.add((descriptionAuthentication_object_map, rr.termType, rr.IRI))

	"""Predicate-object map to open status blank node"""
	# Set variables
	status_po_map = BNode()
	status_object_map = BNode()

	# Add triples to graph
	RML_graph.add((ex.AdminMetadataMap, rr.predicateObjectMap, status_po_map))
	RML_graph.add((status_po_map, rr.predicate, bf.status))
	RML_graph.add((status_po_map, rr.objectMap, status_object_map))
	RML_graph.add((status_object_map, rr.parentTriplesMap, ex.StatusMap))

	"""Logical source map for status blank node"""
	# Set variables
	status_logical_source = BNode()
	status_iterator = Literal("/rdf:RDF/rdf:Description[bf:code]")

	# Add triples to graph
	RML_graph.add((ex.StatusMap, rdf.type, rr.TriplesMap))
	RML_graph.add((ex.StatusMap, rml.logicalSource, status_logical_source))
	RML_graph.add((status_logical_source, rml.source, default_path))
	RML_graph.add((status_logical_source, rml.referenceFormulation, ql.XPath))
	RML_graph.add((status_logical_source, rml.iterator, status_iterator))

	"""Subject map for status blank node"""
	# Set variables
	status_subject_map = BNode()
	class_property = URIRef('http://www.w3.org/ns/r2rml#class') # throwing me an error when you just enter rr.class

	# Add triples to graph
	RML_graph.add((ex.StatusMap, rr.subjectMap, status_subject_map))
	RML_graph.add((status_subject_map, rr.termType, rr.BlankNode))
	RML_graph.add((status_subject_map, class_property, bf.Status))

	"""Predicate-object map for code"""
	# Set variables
	code_po_map = BNode()
	code_object_map = BNode()

	# Add triples to graph
	RML_graph.add((ex.StatusMap, rr.predicateObjectMap, code_po_map))
	RML_graph.add((code_po_map, rr.predicate, bf.code))
	RML_graph.add((code_po_map, rr.objectMap, code_object_map))
	RML_graph.add((code_object_map, rml.reference, Literal("bf:code")))

	return RML_graph
