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
def admin_metadata_mapping(RML_graph, entity):
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

	# ex.{Entity}Map po map for ex.AdminMetadataMap
	entity_po = BNode()
	entity_object_map = BNode()

	RML_graph.add((default_map, rr.predicateObjectMap, entity_po))
	RML_graph.add((entity_po, rr.predicate, bf.adminMetadata))
	RML_graph.add((entity_po, rr.objectMap, entity_object_map))
	RML_graph.add((entity_object_map, rr.parentTriplesMap, ex.AdminMetadataMap))

	# ex.AdminMetadataMap logical source
	admin_metadata_logical_source = BNode()
	admin_metadata_iterator = Literal("/RDF/Description[catalogerID]")

	RML_graph.add((ex.AdminMetadataMap, rdf.type, rr.TriplesMap))
	RML_graph.add((ex.AdminMetadataMap, rml.logicalSource, admin_metadata_logical_source))
	RML_graph.add((admin_metadata_logical_source, rml.source, default_path))
	RML_graph.add((admin_metadata_logical_source, rml.referenceFormulation, ql.XPath))
	RML_graph.add((admin_metadata_logical_source, rml.iterator, admin_metadata_iterator))

	# ex.AdminMetadataMap subject map
	admin_metadata_subject_map = BNode()
	class_property = URIRef('http://www.w3.org/ns/r2rml#class') # throws an error when you just enter rr.class

	RML_graph.add((ex.AdminMetadataMap, rr.subjectMap, admin_metadata_subject_map))
	RML_graph.add((admin_metadata_subject_map, rr.termType, rr.BlankNode))
	RML_graph.add((admin_metadata_subject_map, class_property, bf.AdminMetadata))

	# ex.AdminMetadataMap po map -- cataloger ID
	catalogerID_po_map = BNode()
	catalogerID_object_map = BNode()

	RML_graph.add((ex.AdminMetadataMap, rr.predicateObjectMap, catalogerID_po_map))
	RML_graph.add((catalogerID_po_map, rr.predicate, bflc.catalogerID))
	RML_graph.add((catalogerID_po_map, rr.objectMap, catalogerID_object_map))
	RML_graph.add((catalogerID_object_map, rml.reference, Literal("catalogerID")))
	RML_graph.add((catalogerID_object_map, rr.termType, rr.Literal))

	# ex.AdminMetadataMap po map -- status
	status_po_map = BNode()
	status_object_map = BNode()

	RML_graph.add((ex.AdminMetadataMap, rr.predicateObjectMap, status_po_map))
	RML_graph.add((status_po_map, rr.predicate, bf.status))
	RML_graph.add((status_po_map, rr.objectMap, status_object_map))
	RML_graph.add((status_object_map, rr.parentTriplesMap, ex.StatusMap))

	# ex.AdminMetadataMap po map -- encoding level
	encodingLevel_po_map = BNode()
	encodingLevel_object_map = BNode()

	RML_graph.add((ex.AdminMetadataMap, rr.predicateObjectMap, encodingLevel_po_map))
	RML_graph.add((encodingLevel_po_map, rr.predicate, bflc.encodingLevel))
	RML_graph.add((encodingLevel_po_map, rr.objectMap, encodingLevel_object_map))
	RML_graph.add((encodingLevel_object_map, rml.reference, Literal("encodingLevel/@resource")))
	RML_graph.add((encodingLevel_object_map, rr.termType, rr.IRI))

	# ex.AdminMetadataMap po map -- description conventions
	descriptionConventions_po_map = BNode()
	descriptionConventions_object_map = BNode()

	RML_graph.add((ex.AdminMetadataMap, rr.predicateObjectMap, descriptionConventions_po_map))
	RML_graph.add((descriptionConventions_po_map, rr.predicate, bf.descriptionConventions))
	RML_graph.add((descriptionConventions_po_map, rr.objectMap, descriptionConventions_object_map))
	RML_graph.add((descriptionConventions_object_map, rml.reference, Literal("descriptionConventions/@resource")))
	RML_graph.add((descriptionConventions_object_map, rr.termType, rr.IRI))

	# ex.AdminMetadataMap po map -- source
	source_po_map = BNode()
	source_object_map = BNode()

	RML_graph.add((ex.AdminMetadataMap, rr.predicateObjectMap, source_po_map))
	RML_graph.add((source_po_map, rr.predicate, bf.source))
	RML_graph.add((source_po_map, rr.objectMap, source_object_map))
	RML_graph.add((source_object_map, rml.reference, Literal("source/@resource")))
	RML_graph.add((source_object_map, rr.termType, rr.IRI))

	# ex.AdminMetadataMap po map -- description language
	descriptionLanguage_po_map = BNode()
	descriptionLanguage_object_map = BNode()

	RML_graph.add((ex.AdminMetadataMap, rr.predicateObjectMap, descriptionLanguage_po_map))
	RML_graph.add((descriptionLanguage_po_map, rr.predicate, bf.descriptionLanguage))
	RML_graph.add((descriptionLanguage_po_map, rr.objectMap, descriptionLanguage_object_map))
	RML_graph.add((descriptionLanguage_object_map, rml.reference, Literal("descriptionLanguage/@resource")))
	RML_graph.add((descriptionLanguage_object_map, rr.termType, rr.IRI))

	# ex.AdminMetadataMap po map -- creation date
	creationDate_po_map = BNode()
	creationDate_object_map = BNode()

	RML_graph.add((ex.AdminMetadataMap, rr.predicateObjectMap, creationDate_po_map))
	RML_graph.add((creationDate_po_map, rr.predicate, bf.creationDate))
	RML_graph.add((creationDate_po_map, rr.objectMap, creationDate_object_map))
	RML_graph.add((creationDate_object_map, rml.reference, Literal("creationDate")))
	RML_graph.add((creationDate_object_map, rr.termType, rr.Literal))

	# ex.AdminMetadataMap po map -- change date
	changeDate_po_map = BNode()
	changeDate_object_map = BNode()

	RML_graph.add((ex.AdminMetadataMap, rr.predicateObjectMap, changeDate_po_map))
	RML_graph.add((changeDate_po_map, rr.predicate, bf.changeDate))
	RML_graph.add((changeDate_po_map, rr.objectMap, changeDate_object_map))
	RML_graph.add((changeDate_object_map, rml.reference, Literal("changeDate")))
	RML_graph.add((changeDate_object_map, rr.termType, rr.Literal))

	# ex.AdminMetadataMap po map -- description authentication
	descriptionAuthentication_po_map = BNode()
	descriptionAuthentication_object_map = BNode()

	RML_graph.add((ex.AdminMetadataMap, rr.predicateObjectMap, descriptionAuthentication_po_map))
	RML_graph.add((descriptionAuthentication_po_map, rr.predicate, bf.descriptionAuthentication))
	RML_graph.add((descriptionAuthentication_po_map, rr.objectMap, descriptionAuthentication_object_map))
	RML_graph.add((descriptionAuthentication_object_map, rml.reference, Literal("descriptionAuthentication/@resource")))
	RML_graph.add((descriptionAuthentication_object_map, rr.termType, rr.IRI))

	# ex.StatusMap logical source
	status_logical_source = BNode()
	status_iterator = Literal("/RDF/Description[code]")

	RML_graph.add((ex.StatusMap, rdf.type, rr.TriplesMap))
	RML_graph.add((ex.StatusMap, rml.logicalSource, status_logical_source))
	RML_graph.add((status_logical_source, rml.source, default_path))
	RML_graph.add((status_logical_source, rml.referenceFormulation, ql.XPath))
	RML_graph.add((status_logical_source, rml.iterator, status_iterator))

	# ex.StatusMap subject map
	status_subject_map = BNode()
	class_property = URIRef('http://www.w3.org/ns/r2rml#class') # throws an error when you just enter rr.class

	RML_graph.add((ex.StatusMap, rr.subjectMap, status_subject_map))
	RML_graph.add((status_subject_map, rr.termType, rr.BlankNode))
	RML_graph.add((status_subject_map, class_property, bf.Status))

	# ex.StatusMap po map -- code
	code_po_map = BNode()
	code_object_map = BNode()

	RML_graph.add((ex.StatusMap, rr.predicateObjectMap, code_po_map))
	RML_graph.add((code_po_map, rr.predicate, bf.code))
	RML_graph.add((code_po_map, rr.objectMap, code_object_map))
	RML_graph.add((code_object_map, rml.reference, Literal("code")))

	return RML_graph
