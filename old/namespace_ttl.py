import os
from sys import argv

script, data_directory = argv

work_1List = os.listdir(f'output/{data_directory}/work_1')
work_2List = os.listdir(f'output/{data_directory}/work_2')
instanceList = os.listdir(f'output/{data_directory}/instance')
itemList = os.listdir(f'output/{data_directory}/item')

prefix_list = [
"ns1",
"ns2",
"ns3",
"ns4",
"ns5",
"ns6",
"ns7",
"ns8",
"ns9"
]

namespace_list = [
"http://id.loc.gov/ontologies/bibframe/",
"http://id.loc.gov/ontologies/bflc/",
"http://dbpedia.org/ontology/",
"http://www.loc.gov/mads/rdf/v1#",
"http://rdaregistry.info/Elements/m/datatype/",
"http://rdaregistry.info/Elements/e/",
"http://rdaregistry.info/Elements/i/",
"http://rdaregistry.info/Elements/m/",
"http://rdaregistry.info/Elements/u/",
"http://rdaregistry.info/Elements/w/",
"https://doi.org/10.6069/uwlib.55.d.4#",
"http://sinopia.io/vocabulary/"
]

new_prefix_list = [
"bf",
"bflc",
"dbo",
"madsrdf",
"rdam",
"rdae",
"rdai",
"rdam",
"rdau",
"rdaw",
"rdax",
"sin"
]

def find_and_replace(entity, file, find, replace):
	open_file = open(f"output/{data_directory}/{entity}/{file}", "rt")
	file_replacement = open_file.read()
	file_replacement = file_replacement.replace(find, replace)
	open_file.close()
	open_file = open(f"output/{data_directory}/{entity}/{file}", "wt")
	open_file.write(file_replacement)
	open_file.close()

for work in work_1List:
	for prefix in prefix_list:
		i = 0
		while i <= 11:
			with open(f"output/{data_directory}/work_1/{work}") as f:
				if f"@prefix {prefix}: <{namespace_list[i]}> ." in f.read():
					old_namespace = f"@prefix {prefix}: <{namespace_list[i]}> ."
					new_namespace = f"@prefix {new_prefix_list[i]}: <{namespace_list[i]}> ."
					find_and_replace("work_1", work, old_namespace, new_namespace)
					find_and_replace("work_1", work, f"{prefix}:", f"{new_prefix_list[i]}:")
					i = 12
				else:
					i = i + 1

for work in work_2List:
	for prefix in prefix_list:
		i = 0
		while i <= 11:
			with open(f"output/{data_directory}/work_2/{work}") as f:
				if f"@prefix {prefix}: <{namespace_list[i]}> ." in f.read():
					old_namespace = f"@prefix {prefix}: <{namespace_list[i]}> ."
					new_namespace = f"@prefix {new_prefix_list[i]}: <{namespace_list[i]}> ."
					find_and_replace("work_2", work, old_namespace, new_namespace)
					find_and_replace("work_2", work, f"{prefix}:", f"{new_prefix_list[i]}:")
					i = 12
				else:
					i = i + 1

for instance in instanceList:
	for prefix in prefix_list:
		i = 0
		while i <= 11:
			with open(f"output/{data_directory}/instance/{instance}") as f:
				if f"@prefix {prefix}: <{namespace_list[i]}> ." in f.read():
					old_namespace = f"@prefix {prefix}: <{namespace_list[i]}> ."
					new_namespace = f"@prefix {new_prefix_list[i]}: <{namespace_list[i]}> ."
					find_and_replace("instance", instance, old_namespace, new_namespace)
					find_and_replace("instance", instance, f"{prefix}:", f"{new_prefix_list[i]}:")
					i = 12
				else:
					i = i + 1

for item in itemList:
	for prefix in prefix_list:
		i = 0
		while i <= 11:
			with open(f"output/{data_directory}/item/{item}") as f:
				if f"@prefix {prefix}: <{namespace_list[i]}> ." in f.read():
					old_namespace = f"@prefix {prefix}: <{namespace_list[i]}> ."
					new_namespace = f"@prefix {new_prefix_list[i]}: <{namespace_list[i]}> ."
					find_and_replace("item", item, old_namespace, new_namespace)
					find_and_replace("item", item, f"{prefix}:", f"{new_prefix_list[i]}:")
					i = 12
				else:
					i = i + 1
