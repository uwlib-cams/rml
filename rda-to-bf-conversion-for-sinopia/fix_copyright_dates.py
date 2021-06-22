from arguments import define_arg
import os
from datetime import date
from progress.bar import Bar
from reserialize import reserialize
from timeit import default_timer as timer
import xml.etree.ElementTree as ET

"""Functions"""

def fix_copyright_dates(entity, file, input_location):
	"""Find literals that contain "©" and nothing else, and remove the triple"""

	num_of_edits = 0

	# open xml parser
	tree = ET.parse(f'{input_location}/{currentDate}/{entity}/{file}')
	root = tree.getroot()

	for child in root: # for each node...
		for prop in child: # for each property in node...
			if prop.text is not None: # if the property has a literal value...
				if prop.text == "©": # and if that literal is the copyright symbol and nothing else...
					child.remove(prop) # remove that property
					num_of_edits += 1

					tree.write(f'{input_location}/{currentDate}/{entity}/{file}')

					reserialize(f'{input_location}/{currentDate}/{entity}/{file}', f'{input_location}/{currentDate}/{entity}/{file}', 'xml')
	return num_of_edits

"""Variables"""

# format for naming folder according to date
today = date.today()
currentDate = str(today).replace('-', '_')

# arguments from command line
args = define_arg()
input_location = args.input

num_of_edits = 0

"""Lists and Dictionaries"""

workList = os.listdir(f'{input_location}/{currentDate}/work')
expressionList = os.listdir(f'{input_location}/{currentDate}/expression')
manifestationList = os.listdir(f'{input_location}/{currentDate}/manifestation')
itemList = os.listdir(f'{input_location}/{currentDate}/item')

resource_dict = {"work": workList, "expression": expressionList, "manifestation": manifestationList, "item": itemList}

###

num_of_resources = len(workList) + len(expressionList) + len(manifestationList) + len(itemList)

bar = Bar(">> Removing blank copyright dates", max=num_of_resources, suffix='%(percent)d%%') # progress bar

start = timer()
for entity in resource_dict.keys():
	for resource in resource_dict[entity]:
		edits_made = fix_copyright_dates(entity, resource, input_location)
		num_of_edits += edits_made
		bar.next()
end = timer()
bar.finish()
print(f"Triples removed: {num_of_edits}")
print(f"Elapsed time: {round((end - start), 1)} s")
