"""Python Libraries/Modules/Packages"""
from datetime import date
from datetime import datetime
import os
from progress.bar import Bar
import rdflib
from rdflib import *
from timeit import default_timer as timer

"""Imported Functions"""
from scripts.arguments import define_arg

"""Variables"""
today = date.today()
currentDate = str(today).replace('-','_')

# arguments from command line
args = define_arg()
output_location = args.output

"""Lists and Dictionaries"""
bf_date_prop_list = ["date", "originDate", "legalDate", "copyrightDate", "changeDate", "creationDate", "generationDate"]

work_1_list = os.listdir(f"{output_location}/{currentDate}/work_1_xml/")
work_2_list = os.listdir(f"{output_location}/{currentDate}/work_2_xml/")
instance_list = os.listdir(f"{output_location}/{currentDate}/instance_xml/")
item_list = os.listdir(f"{output_location}/{currentDate}/item_xml/")

resource_dict = {"work_1": work_1_list, "work_2": work_2_list, "instance": instance_list, "item": item_list}

"""Functions"""
def determine_date_type(value):
	gYear_format = "%Y"
	gYearMonth_format = "%Y-%m"
	date_format = "%Y-%m-%d"

	# check for date
	try:
		test = bool(datetime.strptime(value, date_format))
		# if successful...
		date_type = "date"
		return date_type
		continue_test = False
	except ValueError:
		# if unsuccessful...
		continue_test = True

	if continue_test == True:
		# check for gYearMonth
		try:
			test = bool(datetime.strptime(value, gYearMonth_format))
			# if successful...
			date_type = "gYearMonth"
			return date_type
			continue_test = False
		except ValueError:
			# if unsuccessful...
			continue_test = True

	if continue_test == True:
		# check for gYear
		try:
			test = bool(datetime.strptime(value, gYear_format))
			# if successful...
			date_type = "gYear"
			return date_type
			continue_test = False
		except ValueError:
			# if unsuccessful...
			continue_test = True

	if continue_test == True:
		# no date format found
		date_type = ""
		return date_type

def add_dates_in_xml(entity, file, output_location):
	num_of_edits = 0
	edits_made = False

	g = Graph()
	g.load(f'{output_location}/{currentDate}/{entity}_xml/{file}', format='xml')

	for s, p, o in g:
		if p.split('/')[-1] in bf_date_prop_list:
			if isinstance(o, rdflib.term.Literal) == True and o.datatype == None:
				date_type = determine_date_type(o)
				if date_type != "":
					date_type = URIRef(f"http://www.w3.org/2001/XMLSchema#{date_type}")
					new_object = Literal(o, datatype=date_type)
					g.remove((s, p, o))
					g.add((s, p, new_object))
					num_of_edits += 1
					edits_made = True

	if edits_made == True:
		g.serialize(destination=f'{output_location}/{currentDate}/{entity}_xml/{file}', format='xml')

	return num_of_edits

###

num_of_resources = len(work_1_list) + len(work_2_list) + len(instance_list) + len(item_list)
num_of_edits = 0

start = timer()
bar = Bar(">> Adding datatypes to dates", max=num_of_resources, suffix='%(percent)d%%') # progress bar
for entity in resource_dict.keys():
	for resource in resource_dict[entity]:
		edits_made = add_dates_in_xml(entity, resource, output_location)
		num_of_edits += edits_made
		bar.next()
end = timer()
bar.finish()

print(f"Datatypes added: {num_of_edits}")
print(f"Elapsed time: {round((end - start), 1)} s")
