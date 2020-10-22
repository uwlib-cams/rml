import os
from datetime import date
#from sys import argv

#script, data_directory = argv

today = date.today()
currentDate = str(today).replace('-', '_')

workList = os.listdir(f'input/{currentDate}/work')
expressionList = os.listdir(f'input/{currentDate}/expression')
manifestationList = os.listdir(f'input/{currentDate}/manifestation')
itemList = os.listdir(f'input/{currentDate}/item')

def find_and_replace(entity, file, prop, URI):
	"""Rewrite lines of RDF/XML so the value goes from being a literal to a URI"""
	open_file = open(f"input/{currentDate}/{entity}/{file}", "rt")
	file_replacement = open_file.read()
	if " " in prop:
		attribute = prop.split(' ')[1]
		prop = prop.split(' ')[0]
		original_line = f"<{prop} {attribute}>{URI}</{prop}>"
	else:
		original_line = f"<{prop}>{URI}</{prop}>"
	file_replacement = file_replacement.replace(original_line, f"<{prop} rdf:resource=\"{URI}\"/>")
	open_file.close()
	open_file = open(f"input/{currentDate}/{entity}/{file}", "wt")
	open_file.write(file_replacement)
	open_file.close()

for work in workList:
	with open(f'input/{currentDate}/work/{work}') as work_xml:
		for line in work_xml:
			if ">http" in line:
				prop = line.split('>')[0]
				prop = prop.strip()
				prop = prop.strip('<')

				URI = line.split('>')[1]
				URI = URI.split('<')[0]

				find_and_replace("work", work, prop, URI)

for expression in expressionList:
	with open(f'input/{currentDate}/expression/{expression}') as expression_xml:
		for line in expression_xml:
			if ">http" in line:
				prop = line.split('>')[0]
				prop = prop.strip()
				prop = prop.strip('<')

				URI = line.split('>')[1]
				URI = URI.split('<')[0]

				find_and_replace("expression", expression, prop, URI)

for manifestation in manifestationList:
	with open(f'input/{currentDate}/manifestation/{manifestation}') as manifestation_xml:
		for line in manifestation_xml:
			if ">http" in line:
				prop = line.split('>')[0]
				prop = prop.strip()
				prop = prop.strip('<')

				URI = line.split('>')[1]
				URI = URI.split('<')[0]

				find_and_replace("manifestation", manifestation, prop, URI)

for item in itemList:
	with open(f'input/{currentDate}/item/{item}') as item_xml:
		for line in item_xml:
			if ">http" in line:
				prop = line.split('>')[0]
				prop = prop.strip()
				prop = prop.strip('<')

				URI = line.split('>')[1]
				URI = URI.split('<')[0]

				find_and_replace("item", item, prop, URI)
