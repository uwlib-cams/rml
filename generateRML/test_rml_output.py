"""Python Libraries/Modules/Packages"""
import os
import random
from rdflib import *
import rdflib

"""Functions"""
def replace_default_with_filepath(entity, filepath):
	original = open(f"rmlOutput/{entity}RML.ttl", "rt")
	find_and_replace = original.read()
	find_and_replace = find_and_replace.replace(f"!!{entity}_filepath!!", filepath)
	original.close()
	new = open(f"rmlOutput/{entity}RML.ttl", "wt")
	new.write(find_and_replace)
	new.close()

def replace_filepath_with_default(entity, filepath):
	original = open(f"rmlOutput/{entity}RML.ttl", "rt")
	find_and_replace = original.read()
	find_and_replace = find_and_replace.replace(filepath, f"!!{entity}_filepath!!")
	original.close()
	new = open(f"rmlOutput/{entity}RML.ttl", "wt")
	new.write(find_and_replace)
	new.close()

def create_rda_dict():
	rda_list = os.listdir('../input')
	most_recent_rda_dir = rda_list[-1]

	work_list = os.listdir(f'../input/{most_recent_rda_dir}/work')
	expression_list = os.listdir(f'../input/{most_recent_rda_dir}/expression')
	manifestation_list = os.listdir(f'../input/{most_recent_rda_dir}/manifestation')
	item_list = os.listdir(f'../input/{most_recent_rda_dir}/item')
	entity_dict = {
		"work": work_list,
		"expression": expression_list,
		"manifestation": manifestation_list,
		"item": item_list
	}

	return most_recent_rda_dir, entity_dict

def select_test_files(most_recent_rda_dir):
	test_files = []

	for entity in entity_dict.keys():
		entity_list = entity_dict[entity]
		file_1 = random.choice(entity_list)
		file_2 = file_1
		while file_2 == file_1:
			file_2 = random.choice(entity_list)
		filepath_1 = f'../input/{most_recent_rda_dir}/{entity}/{file_1.split(".")[0]}'
		filepath_2 = f'../input/{most_recent_rda_dir}/{entity}/{file_2.split(".")[0]}'
		test_files.append((entity, filepath_1))
		test_files.append((entity, filepath_2))

	return test_files

def compare_graphs(graph_1, graph_2):
	graphs_are_the_same = False
	if graph_1 != graph_2:
		# The two graphs are not the same
		bad_triples = [] # list for any triples that are in one graph and not the other
		for s, p, o in graph_1: # for each triple in graph 1...
			if (s, p, o) not in graph_2: # if triple is not in graph 2...
				bad_triple = False
				if isinstance(s, rdflib.term.BNode) == False and isinstance(o, rdflib.term.BNode) == False:
					# Neither subject nor object is a blank node, so it's a bad triple
					bad_triple = True
				elif isinstance(s, rdflib.term.BNode) == True and isinstance(o, rdflib.term.BNode) == False:
					# The subject is a blank node, so let's look for that same triple but ignore the subject
					if find_triple_in_graph((None, p, o), graph_2) == False:
						bad_triple = True
				elif isinstance(s, rdflib.term.BNode) == False and isinstance(o, rdflib.term.BNode) == True:
					# The object is a blank node, so let's look for that same triple but ignore the object
					if find_triple_in_graph((s, p, None), graph_2) == False:
						bad_triple = True
				elif isinstance(s, rdflib.term.BNode) == True and isinstance(o, rdflib.term.BNode) == True:
					# The subject and object are both blank nodes, so let's look for that same triple but ignore the subject and object
					if find_triple_in_graph((None, p, None), graph_2) == False:
						bad_triple = True

				if bad_triple == True:
					bad_triples.append((s, p, o))

	if len(bad_triples) == 0:
		# no bad triples found
		if len(graph_1) == len(graph_2):
			# the graphs are the same length
			graphs_are_the_same = True

	return graphs_are_the_same

def find_triple_in_graph(triple_tuple, graph):
	triple_in_graph = True
	if triple_tuple not in graph:
		triple_in_graph = False

	return triple_in_graph

###

"""Create lists of RDA resources"""
most_recent_rda_dir = create_rda_dict()[0]
entity_dict = create_rda_dict()[1]

"""Select random test files"""
test_files = select_test_files(most_recent_rda_dir)

"""Test files"""
for tuple in test_files:
	entity = tuple[0]
	filepath = tuple[1]

	replace_default_with_filepath(entity, filepath)

	# run RML on a file
	os.system(f'java -jar mapper.jar -m rmlOutput/{entity}RML.ttl -s turtle -o {entity}_output_1.ttl')
	# add output to graph
	output_1 = Graph()
	output_1.load(f'{entity}_output_1.ttl', format='ttl')

	# run RML again on the same file
	os.system(f'java -jar mapper.jar -m rmlOutput/{entity}RML.ttl -s turtle -o {entity}_output_2.ttl')
	# add output to new graph
	output_2 = Graph()
	output_2.load(f'{entity}_output_2.ttl', format='ttl')

	replace_filepath_with_default(entity, filepath)

	"""Compare two outputs"""
	result = compare_graphs(output_1, output_2)
	if result == False:
		print("Outputs are different.")
		quit()
	else:
		os.system(f'rm {entity}_output_1.ttl {entity}_output_2.ttl')

print("All good!")
