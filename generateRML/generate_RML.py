import os
from sys import argv

script, csv_dir = argv

"""Lists"""
from lists import entities

###

if not os.path.exists(f'rmlOutput/'):
	os.system(f'mkdir rmlOutput')

for entity in entities:
	if entity == "work":
		from RML_for_works import generate_rml_for_works
		work_graph = generate_rml_for_works(csv_dir)
		work_graph.serialize(destination="rmlOutput/workRML.ttl", format="turtle")
	if entity == "expression":
		from RML_for_expressions import generate_rml_for_expressions
		expression_graph = generate_rml_for_expressions(csv_dir)
		expression_graph.serialize(destination="rmlOutput/expressionRML.ttl", format="turtle")
	elif entity == "manifestation":
		from RML_for_manifestations import generate_rml_for_manifestations
		manifestation_graph = generate_rml_for_manifestations(csv_dir)
		manifestation_graph.serialize(destination="rmlOutput/manifestationRML.ttl", format="turtle")
	elif entity == "item":
		from RML_for_items import generate_rml_for_items
		item_graph = generate_rml_for_items(csv_dir)
		item_graph.serialize(destination="rmlOutput/itemRML.ttl", format="turtle")
