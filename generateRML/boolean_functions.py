"""Python Libraries/Modules/Packages"""
from rdflib import *

"""Namespaces"""
ex = Namespace('http://example.org/entity/')
rml = Namespace('http://semweb.mmlab.be/ns/rml#')

"""Imported Functions"""
from formatting_functions import split_by_space

"""Functions"""
def constant_only_test(node_list, start_point):
	num_of_nodes = len(node_list)
	start_num = 0
	bnode = ""
	for num in range(0, num_of_nodes):
		node = node_list[num].strip()
		if node == start_point:
			start_num = 1
		if start_num > 0:
			bnode = bnode + node + " "
		else:
			pass
	bnode_contents = bnode.split(" >> ")[1:]
	bnode_contents = (" >> ").join(bnode_contents)
	bnode_contents_list = split_by_space(bnode_contents)
	if "" in bnode_contents_list:
		bnode_contents_list.remove("")
	only_constants = True
	for node in bnode_contents_list:
		if node[0].isupper() == True: # class
			pass
		elif node == ">":
			pass
		elif node == ">>":
			only_constants = False
		else:
			if "*" in node: # IRI
				only_constants = False
			elif "=" not in node: # literal
				only_constants = False
	return only_constants

def class_test(node):
	its_a_class = False

	if ":" in node:
		node = node.split(":")[-1]

	if node[0].isupper() == True:
		its_a_class = True

	return its_a_class
