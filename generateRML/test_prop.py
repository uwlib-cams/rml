import os
from sys import argv

script, csv_dir, prop = argv

prop = prop.split(',')

"""Lists"""
from lists import entities

###

if prop[0][1] == "1":
	entity = "work"
elif prop[0][1] == "2":
	entity = "expression"
elif prop[0][1] == "3":
	entity = "manifestation"
elif prop[0][1] == "4":
	entity = "item"
else:
	entity = input("Enter entity of property: >>")

	acceptable_entities = ["work", "expression", "manifestation", "item"]

	if entity not in acceptable_entities:
		print("Invalid entity.")
		quit()

###

if entity == "work":
	from RML_for_works import generate_rml_for_testing_work_prop
	RML_graph = generate_rml_for_testing_work_prop(csv_dir, prop)
elif entity == "expression":
	from RML_for_expressions import generate_rml_for_testing_expression_prop
	RML_graph = generate_rml_for_testing_expression_prop(csv_dir, prop)
elif entity == "manifestation":
	from RML_for_manifestations import generate_rml_for_testing_manifestation_prop
	RML_graph = generate_rml_for_testing_manifestation_prop(csv_dir, prop)
elif entity == "item":
	from RML_for_items import generate_rml_for_testing_item_prop
	RML_graph = generate_rml_for_testing_item_prop(csv_dir, prop)

###

if not os.path.exists(f'rmlOutput_test/'):
	os.system(f'mkdir rmlOutput_test')

RML_graph.serialize(destination=f"rmlOutput_test/{entity}RML.ttl", format="turtle")
