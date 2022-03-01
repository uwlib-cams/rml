from rdflib import *

"""Basics"""

# open an empty graph
demo_graph = Graph()

# create a triple
subject = URIRef('http://example.org/subject')
predicate = URIRef('http://example.org/predicate')
object = Literal('object')
demo_triple = (subject, predicate, object)

# add triple to graph
demo_graph.add(demo_triple)

# print
for s, p, o in demo_graph:
	print(s, p, o)

# remove triple
demo_graph.remove(demo_triple)

"""Blank Nodes"""
# create a blank node
blank_node = BNode()

# create triples
demo_triple_1 = (subject, predicate, blank_node)
demo_triple_2 = (blank_node, predicate, object)

# add triples to graph
demo_graph.add(demo_triple_1)
demo_graph.add(demo_triple_2)

# serialize graph as turtle
demo_graph.serialize(destination="demo_graph.ttl", format="turtle")

"""Namespaces"""
demo_graph_w_namespace = Graph()

# define namespaces
ex = Namespace('http://example.org/')

# bind to graph
demo_graph_w_namespace.bind('ex', ex)

# add triples to graph
demo_graph_w_namespace.add((subject, predicate, blank_node))
demo_graph_w_namespace.add((blank_node, predicate, object))

# serialize graph as turtle
demo_graph_w_namespace.serialize(destination="demo_graph_w_namespace.ttl", format="turtle")
