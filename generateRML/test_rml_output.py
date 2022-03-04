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

def select_test_files_2(most_recent_rda_dir):
	test_files = []

	for entity in entity_dict.keys():
		entity_list = entity_dict[entity]
		entity_test_files = []
		while len(entity_test_files) < 20:
			file = random.choice(entity_list)
			if file not in entity_test_files:
				entity_test_files.append(file)

		for filepath in entity_test_files:
			filepath = f'../input/{most_recent_rda_dir}/{entity}/{filepath.split(".")[0]}'
			test_files.append((entity, filepath))

	return test_files

def compare_graphs(graph_1, graph_2):
	graphs_are_the_same = False
	if graph_1 != graph_2:
		# The two graphs are not the same
		bad_triples = [] # list for any triples that are in one graph and not the other
		for s, p, o in graph_1: # for each triple in graph 1...
			if (s, p, o) not in graph_2: # if triple is not in graph 2...
				bad_triple = find_equivalent_triple(graph_2, s, p, o)
				if bad_triple == True:
					bad_triples.append((s, p, o))

		for s, p, o in graph_2: # for each triple in graph 1...
			if (s, p, o) not in graph_1: # if triple is not in graph 2...
				bad_triple = find_equivalent_triple(graph_1, s, p, o)
				if bad_triple == True:
					bad_triples.append((s, p, o))

	if len(bad_triples) == 0:
		# no bad triples found
		if len(graph_1) == len(graph_2):
			# the graphs are the same length
			graphs_are_the_same = True

	return graphs_are_the_same, bad_triples

def find_equivalent_triple(graph, s, p, o):
	bad_triple = False
	if (s, p, o) not in graph: # if triple is not in graph...
		if isinstance(s, rdflib.term.BNode) == False and isinstance(o, rdflib.term.BNode) == False:
			# Neither subject nor object is a blank node, so it's a bad triple
			bad_triple = True
		elif isinstance(s, rdflib.term.BNode) == True and isinstance(o, rdflib.term.BNode) == False:
			# The subject is a blank node, so let's look for that same triple but ignore the subject
			match_found = False
			for s2, p2, o2 in graph:
				if isinstance(s2, rdflib.term.BNode) == True and p == p2 and o == o2:
					match_found = True
			if match_found == False:
				bad_triple = True
			elif isinstance(s, rdflib.term.BNode) == False and isinstance(o, rdflib.term.BNode) == True:
				# The object is a blank node, so let's look for that same triple but ignore the object
				match_found = False
				for s2, p2, o2 in graph:
					if s == s2 and p == p2 and isinstance(o2, rdflib.term.BNode) == True:
						match_found = True
				if match_found == False:
					bad_triple = True
			elif isinstance(s, rdflib.term.BNode) == True and isinstance(o, rdflib.term.BNode) == True:
				# The subject and object are both blank nodes, so let's look for that same triple but ignore the subject and object
				match_found = False
				for s2, p2, o2 in graph:
					if isinstance(s2, rdflib.term.BNode) == True and p == p2 and isinstance(o2, rdflib.term.BNode) == True:
						match_found = True
				if match_found == False:
					bad_triple = True

	return bad_triple

def compare_graphs_2(graph_1, graph_2):
	graphs_are_the_same = False
	if graph_1 != graph_2:
		# The two graphs are not the same
		bad_triples_1 = [] # list for any triples that are in one graph and not the other
		for s, p, o in graph_1: # for each triple in graph 1...
			if (s, p, o) not in graph_2: # if triple is not in graph 2...
				result = find_equivalent_triple_2(graph_2, s, p, o)
				bad_triple = result[0]
				if bad_triple == True:
					explanation = result[1]
					bad_triples_1.append(((s, p, o), explanation))

		bad_triples_2 = [] # list for any triples that are in one graph and not the other
		for s, p, o in graph_2: # for each triple in graph 1...
			if (s, p, o) not in graph_1: # if triple is not in graph 2...
				result = find_equivalent_triple_2(graph_1, s, p, o)
				bad_triple = result[0]
				if bad_triple == True:
					explanation = result[1]
					bad_triples_2.append(((s, p, o), explanation))

	if len(bad_triples_1) == 0 and len(bad_triples_2) == 0:
		# no bad triples found
		graphs_are_the_same = True

	return graphs_are_the_same, bad_triples_1, bad_triples_2

def find_equivalent_triple_2(graph, s, p, o):
	bad_triple = False
	explanation = ""
	if (s, p, o) not in graph: # if triple is not in graph...
		format_s = "{}".format(s)
		format_p = "{}".format(p)
		format_o = "{}".format(o)

		if "https://api.sinopia.io/resource/" in format_s:
			s = URIRef('https://api.sinopia.io/resource/1') # URIs will be different between new BF and old BF, so replace it with dummy URI

		prop = format_p.split("/")[-1]
		prop = prop.split("#")[-1]

		# triples which are generated during the RDA-to-BIBFRAME transformation process, not RML itself, and can be ignored in this comparison. ID'd here by their objects.
		transformation_objects = [
			"rda-to-bf-for-sinopia.py",
			"http://id.loc.gov/ontologies/bibframe/GenerationProcess"
		]

		# triples which are generated during the RDA-to-BIBFRAME transformation process, not RML itself, and can be ignored in this comparison. ID'd here by their predicates.
		transformation_predicates = [
			"creationDate",
			"changeDate",
			"sameAs"
		]

		# triples which refer to another Sinopia resource, whose IRIs will be different between the original RDA and the output BIBFRAME from the transformation process. ID'd here by their predicates.
		relationship_predicates = [
			"expressionOf",
			"hasExpression",
			"instanceOf",
			"itemOf",
			"hasReproduction",
			"derivativeOf",
			"hasDerivative",
			"relatedTo"
		]

		if format_o in transformation_objects or format_o[0:24] in transformation_objects or prop in transformation_predicates:
			"""these props are edited/generated during transform; ignore here"""
		elif prop in relationship_predicates and format_o[0:32] == "https://api.sinopia.io/resource/":
			match_found = False
			for s2, p2, o2 in graph:
				format_s2 = "{}".format(s2)
				format_o2 = "{}".format(o2)

				if format_s2[0:32] == "https://api.sinopia.io/resource/":
					s2 = URIRef('https://api.sinopia.io/resource/1')

				if s == s2 and p == p2 and format_o2[0:32] == "https://api.sinopia.io/resource/":
					match_found = True
			if match_found == False:
				bad_triple = True
				explanation = "No match for subject + predicate + object"
				print("No match for\n{} {} {}\n".format(s, p, o))
				for s2, p2, o2 in graph:
					format_s2 = "{}".format(s2)
					format_o2 = "{}".format(o2)

					if format_s2[0:32] == "https://api.sinopia.io/resource/":
						s2 = URIRef('https://api.sinopia.io/resource/1')

					print("{} {} {}".format(s2, p2, o2))
					if s != s2:
						print("> {}".format(s2))
					if p != p2:
						print("> {}".format(p2))
					if format_o2[0:32] != "https://api.sinopia.io/resource/":
						print("> {}".format(o2))
					print("")
				input()
		elif isinstance(s, rdflib.term.BNode) == False and isinstance(o, rdflib.term.BNode) == False:
			# Neither subject nor object is a blank node
			match_found = False
			for s2, p2, o2 in graph:
				format_s2 = "{}".format(s2)
				format_p2 = "{}".format(p2)
				format_o2 = "{}".format(o2)

				if format_s2[0:32] == "https://api.sinopia.io/resource/":
					s2 = URIRef('https://api.sinopia.io/resource/1')
				if s == s2 and p == p2 and o == o2:
					match_found = True
				elif format_s.strip() == format_s2.strip() and format_p.strip() == format_p2.strip() and format_o.strip() == format_o2.strip():
					match_found = True
			if match_found == False:
				bad_triple = True
				explanation = "No match for subject + predicate + object"
		elif isinstance(s, rdflib.term.BNode) == True and isinstance(o, rdflib.term.BNode) == False:
			# The subject is a blank node, so let's look for that same triple but ignore the subject
			match_found = False
			for s2, p2, o2 in graph:
				format_s2 = "{}".format(s2)
				format_p2 = "{}".format(p2)
				format_o2 = "{}".format(o2)

				if isinstance(s2, rdflib.term.BNode) == True and p == p2 and o == o2:
					match_found = True
				elif isinstance(s2, rdflib.term.BNode) == True and format_p.strip() == format_p2.strip() and format_o.strip() == format_o2.strip():
					match_found = True
			if match_found == False:
				bad_triple = True
				explanation = "Subject is BNode; no match for predicate + object"
			elif isinstance(s, rdflib.term.BNode) == False and isinstance(o, rdflib.term.BNode) == True:
				# The object is a blank node, so let's look for that same triple but ignore the object
				match_found = False
				for s2, p2, o2 in graph:
					format_s2 = "{}".format(s2)
					format_p2 = "{}".format(p2)
					format_o2 = "{}".format(o2)

					if s == s2 and p == p2 and isinstance(o2, rdflib.term.BNode) == True:
						match_found = True
					elif format_s.strip() == format_s2.strip() and format_p.strip() == format_p2.strip() and isinstance(o2, rdflib.term.BNode) == True:
						match_found = True
				if match_found == False:
					bad_triple = True
					explanation = "Object is BNode; no match for subject + predicate"
			elif isinstance(s, rdflib.term.BNode) == True and isinstance(o, rdflib.term.BNode) == True:
				# The subject and object are both blank nodes, so let's look for that same triple but ignore the subject and object
				match_found = False
				for s2, p2, o2 in graph:
					format_s2 = "{}".format(s2)
					format_p2 = "{}".format(p2)
					format_o2 = "{}".format(o2)

					if isinstance(s2, rdflib.term.BNode) == True and p == p2 and isinstance(o2, rdflib.term.BNode) == True:
						match_found = True
					elif isinstance(s2, rdflib.term.BNode) == True and format_p.strip() == format_p2.strip() and isinstance(o2, rdflib.term.BNode) == True:
						match_found = True
				if match_found == False:
					bad_triple = True
					explanation = "Subject and object are BNodes; no match for predicate"

	return bad_triple, explanation

def find_triple_in_graph(triple_tuple, graph):
	triple_in_graph = True
	if triple_tuple not in graph:
		triple_in_graph = False

	return triple_in_graph

###

"""***STEP ONE: Use generated RML to transform RDA data to BIBFRAME twice, and compare the two outputs to make sure they are the same***"""

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
	result = compare_graphs(output_1, output_2)[0]
	if result == False:
		print("Outputs are different.")
		quit()
	else:
		os.system(f'rm {entity}_output_1.ttl {entity}_output_2.ttl')

"""***STEP TWO: Use generated RML to transform RDA to BIBFRAME, and compare results to most recent cataloger-reviewed BIBFRAME. Review to make sure that changes in BIBFRAME are intentional, and not due to errors in RML generator.***"""

"""Create lists of RDA resources"""
most_recent_rda_dir = create_rda_dict()[0]
entity_dict = create_rda_dict()[1]

"""Select random test files"""
test_files = select_test_files_2(most_recent_rda_dir)

"""Test files"""
for tuple in test_files:
	entity = tuple[0]
	filepath = tuple[1]

	replace_default_with_filepath(entity, filepath)

	# run RML on a file
	os.system(f'java -jar mapper.jar -m rmlOutput/{entity}RML.ttl -s turtle -o {entity}_output.ttl')
	# add output to graph
	output_1 = Graph()
	output_1.load(f'{entity}_output.ttl', format='ttl')

	replace_filepath_with_default(entity, filepath)

	# load second graph with old BIBFRAME
	rda_graph = Graph()
	rda_graph.load(f"{filepath}.xml") # load old rda into a graph
	output_2 = Graph()
	for o in rda_graph.objects(None, URIRef('http://www.w3.org/2002/07/owl#sameAs')): # get ID for its BIBFRAME output
		uri = "{}".format(o)
		id = uri.split("/")[-1]
	if entity == "work":
		bf_entity = "work_1"
	elif entity == "expression":
		bf_entity = "work_2"
	elif entity == "manifestation":
		bf_entity = "instance"
	elif entity == "item":
		bf_entity = "item"
	output_2.load(f"../output/{most_recent_rda_dir}/{bf_entity}_xml/{id}.xml", format="xml") # load BIBFRAME into graph

	"""Compare outputs"""
	result = compare_graphs_2(output_1, output_2)
	if result[0] == False:
		print("Outputs are different.")
		print("In new output, missing from OG BIBFRAME")
		bad_triples_1 = result[1]
		for tuple in bad_triples_1:
			trpl = tuple[0]
			s = trpl[0]
			p = trpl[1]
			o = trpl[2]
			explanation = tuple[1]
			print("{} {} {}".format(s, p, o))
			print(explanation)
			print()
		print("In OG BIBFRAME, missing from new output")
		bad_triples_2 = result[2]
		for tuple in bad_triples_2:
			trpl = tuple[0]
			s = trpl[0]
			p = trpl[1]
			o = trpl[2]
			explanation = tuple[1]
			print("{} {} {}".format(s, p, o))
			print(explanation)
			print()

		g_rda = Graph()
		g_rda.load(f'{filepath}.xml', format='xml')
		g_rda.serialize(destination=f'rda_{entity}_input.ttl', format='ttl')
		os.system(f'wsl-open rda_{entity}_input.ttl')

		os.system(f'wsl-open {entity}_output.ttl')

		g_bf = Graph()
		g_bf.load(f'../output/{most_recent_rda_dir}/{bf_entity}_xml/{id}.xml', format='xml')
		g_bf.serialize(destination=f'old_{entity}_output.ttl', format='ttl')
		os.system(f'wsl-open old_{entity}_output.ttl')

		input('Press Ctrl+C to quit. Press ENTER to continue.\n> ')
		os.system(f'rm rda_{entity}_input.ttl')
		os.system(f'rm old_{entity}_output.ttl')
	else:
		os.system(f'rm {entity}_output.ttl')

print("All good!")
