import os
from datetime import date
#from sys import argv

#script, data_directory = argv

today = date.today()
currentDate = str(today).replace('-', '_')

def fix_work_1_output(work1List):
	for work in work1List:
		with open(f"output/{currentDate}/work_1/{work}", "r") as input_file: # open it up
			row_count = 0 # start at 0
			output_file_lines = [] # start with empty list
			for line in input_file: # iterate throgh each line in the input file
				if "@prefix" in line: # if the line contains "@prefix"
					row_count += 1 # add one to row count
					output_file_lines.append(line)

				elif "rdfs:" in line:
					if "rml.py SNAPSHOT:" in line:
						spacing = line.split('rdfs:')[0]
						edited_line = line.strip()
						punctuation = "] " + edited_line[-1] # see if line ends in ;, ,, or .
						edited_line = edited_line.strip(punctuation)
						edited_line = edited_line.strip()
						edited_line = spacing + edited_line + f"^^xsd:dateTime {punctuation}\n"
						output_file_lines.append(edited_line) # add to list
					else:
						output_file_lines.append(line)

				else:
					# isolate the name of the property
					property_ = line.split('bf:')[-1]
					property_ = property_.split(' ')[0]

					if property_ in bf_date_prop_list:
						spacing = line.split('bf:')[0] # preserve whitespace at the beginning of the line
						edited_line = line.strip() # remove whitespaces
						dash_count = 0 # start at 0
						for character in edited_line: # iterate through characters in line
							if character == "-":
								dash_count += 1 # count the number of dashes
						punctuation = edited_line[-1] # see if line ends in ;, ,, or .
						if dash_count == 0: # no dashes, e.g. "1886"
							edited_line = edited_line.strip(punctuation)
							edited_line = edited_line.strip()
							edited_line = spacing + edited_line + f"^^xsd:gYear {punctuation}\n"
						elif dash_count == 1: # one dash, e.g. "1886-02"
							edited_line = edited_line.strip(punctuation)
							edited_line = edited_line.strip()
							edited_line = spacing + edited_line + f"^^xsd:gYearMonth {punctuation}\n"
						elif dash_count == 2: # two dashes, e.g. "1886-02-14"
							edited_line = edited_line.strip(punctuation)
							edited_line = edited_line.strip()
							edited_line = spacing + edited_line + f"^^xsd:date {punctuation}\n"
						output_file_lines.append(edited_line) # add to list
					else: # if the line does not have a date in it
						output_file_lines.append(line) # add it to list with no edits

			output_file_lines[row_count] = output_file_lines[row_count].strip() + "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\n" # add prefix for datatypes after last prefix
		with open(f"output/{currentDate}/work_1/{work}", "w") as output_file:
			for line in output_file_lines:
				output_file.write(line)

def fix_work_2_output(work2List):
	for work in work2List:
		with open(f"output/{currentDate}/work_2/{work}", "r") as input_file: # open it up
			row_count = 0 # start at 0
			output_file_lines = [] # start with empty list
			for line in input_file: # iterate throgh each line in the input file
				if "@prefix" in line: # if the line contains "@prefix"
					row_count += 1 # add one to row count
					output_file_lines.append(line)

				elif "rdfs:" in line:
					if "rml.py SNAPSHOT:" in line:
						spacing = line.split('rdfs:')[0]
						edited_line = line.strip()
						punctuation = "] " + edited_line[-1] # see if line ends in ;, ,, or .
						edited_line = edited_line.strip(punctuation)
						edited_line = edited_line.strip()
						edited_line = spacing + edited_line + f"^^xsd:dateTime {punctuation}\n"
						output_file_lines.append(edited_line) # add to list
					else:
						output_file_lines.append(line)

				else:
					# isolate the name of the property
					property_ = line.split('bf:')[-1]
					property_ = property_.split(' ')[0]

					if property_ in bf_date_prop_list:
						spacing = line.split('bf:')[0] # preserve whitespace at the beginning of the line
						edited_line = line.strip() # remove whitespaces
						dash_count = 0 # start at 0
						for character in edited_line: # iterate through characters in line
							if character == "-":
								dash_count += 1 # count the number of dashes
						punctuation = edited_line[-1] # see if line ends in ;, ,, or .
						if dash_count == 0: # no dashes, e.g. "1886"
							edited_line = edited_line.strip(punctuation)
							edited_line = edited_line.strip()
							edited_line = spacing + edited_line + f"^^xsd:gYear {punctuation}\n"
						elif dash_count == 1: # one dash, e.g. "1886-02"
							edited_line = edited_line.strip(punctuation)
							edited_line = edited_line.strip()
							edited_line = spacing + edited_line + f"^^xsd:gYearMonth {punctuation}\n"
						elif dash_count == 2: # two dashes, e.g. "1886-02-14"
							edited_line = edited_line.strip(punctuation)
							edited_line = edited_line.strip()
							edited_line = spacing + edited_line + f"^^xsd:date {punctuation}\n"
						output_file_lines.append(edited_line) # add to list
					else: # if the line does not have a date in it
						output_file_lines.append(line) # add it to list with no edits

			output_file_lines[row_count] = output_file_lines[row_count].strip() + "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\n" # add prefix for datatypes after last prefix
		with open(f"output/{currentDate}/work_2/{work}", "w") as output_file:
			for line in output_file_lines:
				output_file.write(line)

def fix_instance_output(instanceList):
	for instance in instanceList:
		with open(f"output/{currentDate}/instance/{instance}", "r") as input_file: # open it up
			row_count = 0 # start at 0
			output_file_lines = [] # start with empty list
			for line in input_file: # iterate throgh each line in the input file
				if "@prefix" in line: # if the line contains "@prefix"
					row_count += 1 # add one to row count
					output_file_lines.append(line)

				elif "rdfs:" in line:
					if "rml.py SNAPSHOT:" in line:
						spacing = line.split('rdfs:')[0]
						edited_line = line.strip()
						punctuation = "] " + edited_line[-1] # see if line ends in ;, ,, or .
						edited_line = edited_line.strip(punctuation)
						edited_line = edited_line.strip()
						edited_line = spacing + edited_line + f"^^xsd:dateTime {punctuation}\n"
						output_file_lines.append(edited_line) # add to list
					else:
						output_file_lines.append(line)

				else:
					# isolate the name of the property
					property_ = line.split('bf:')[-1]
					property_ = property_.split(' ')[0]

					if property_ in bf_date_prop_list:
						spacing = line.split('bf:')[0] # preserve whitespace at the beginning of the line
						edited_line = line.strip() # remove whitespaces
						dash_count = 0 # start at 0
						for character in edited_line: # iterate through characters in line
							if character == "-":
								dash_count += 1 # count the number of dashes
						punctuation = edited_line[-1] # see if line ends in ;, ,, or .
						if dash_count == 0: # no dashes, e.g. "1886"
							edited_line = edited_line.strip(punctuation)
							edited_line = edited_line.strip()
							edited_line = spacing + edited_line + f"^^xsd:gYear {punctuation}\n"
						elif dash_count == 1: # one dash, e.g. "1886-02"
							edited_line = edited_line.strip(punctuation)
							edited_line = edited_line.strip()
							edited_line = spacing + edited_line + f"^^xsd:gYearMonth {punctuation}\n"
						elif dash_count == 2: # two dashes, e.g. "1886-02-14"
							edited_line = edited_line.strip(punctuation)
							edited_line = edited_line.strip()
							edited_line = spacing + edited_line + f"^^xsd:date {punctuation}\n"
						output_file_lines.append(edited_line) # add to list
					else: # if the line does not have a date in it
						output_file_lines.append(line) # add it to list with no edits

			output_file_lines[row_count] = output_file_lines[row_count].strip() + "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\n" # add prefix for datatypes after last prefix
		with open(f"output/{currentDate}/instance/{instance}", "w") as output_file:
			for line in output_file_lines:
				output_file.write(line)

def fix_item_output(itemList):
	for item in itemList:
		with open(f"output/{currentDate}/item/{item}", "r") as input_file: # open it up
			row_count = 0 # start at 0
			output_file_lines = [] # start with empty list
			for line in input_file: # iterate throgh each line in the input file
				if "@prefix" in line: # if the line contains "@prefix"
					row_count += 1 # add one to row count
					output_file_lines.append(line)

				elif "rdfs:" in line:
					if "rml.py SNAPSHOT:" in line:
						spacing = line.split('rdfs:')[0]
						edited_line = line.strip()
						punctuation = "] " + edited_line[-1] # see if line ends in ;, ,, or .
						edited_line = edited_line.strip(punctuation)
						edited_line = edited_line.strip()
						edited_line = spacing + edited_line + f"^^xsd:dateTime {punctuation}\n"
						output_file_lines.append(edited_line) # add to list
					else:
						output_file_lines.append(line)

				else:
					# isolate the name of the property
					property_ = line.split('bf:')[-1]
					property_ = property_.split(' ')[0]

					if property_ in bf_date_prop_list:
						spacing = line.split('bf:')[0] # preserve whitespace at the beginning of the line
						edited_line = line.strip() # remove whitespaces
						dash_count = 0 # start at 0
						for character in edited_line: # iterate through characters in line
							if character == "-":
								dash_count += 1 # count the number of dashes
						punctuation = edited_line[-1] # see if line ends in ;, ,, or .
						if dash_count == 0: # no dashes, e.g. "1886"
							edited_line = edited_line.strip(punctuation)
							edited_line = edited_line.strip()
							edited_line = spacing + edited_line + f"^^xsd:gYear {punctuation}\n"
						elif dash_count == 1: # one dash, e.g. "1886-02"
							edited_line = edited_line.strip(punctuation)
							edited_line = edited_line.strip()
							edited_line = spacing + edited_line + f"^^xsd:gYearMonth {punctuation}\n"
						elif dash_count == 2: # two dashes, e.g. "1886-02-14"
							edited_line = edited_line.strip(punctuation)
							edited_line = edited_line.strip()
							edited_line = spacing + edited_line + f"^^xsd:date {punctuation}\n"
						output_file_lines.append(edited_line) # add to list
					else: # if the line does not have a date in it
						output_file_lines.append(line) # add it to list with no edits

			output_file_lines[row_count] = output_file_lines[row_count].strip() + "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\n" # add prefix for datatypes after last prefix
		with open(f"output/{currentDate}/item/{item}", "w") as output_file:
			for line in output_file_lines:
				output_file.write(line)

work1List = [] # os.listdir(f"output/{currentDate}/work_1/")
work2List = [] # os.listdir(f"output/{currentDate}/work_2/")
instanceList = os.listdir(f"output/{currentDate}/instance/")
itemList = [] # os.listdir(f"output/{currentDate}/item/")

bf_date_prop_list = ["date", "originDate", "legalDate", "copyrightDate", "changeDate", "creationDate", "generationDate"]

#

#fix_work_1_output(work1List)
#fix_work_2_output(work2List)
fix_instance_output(instanceList)
#fix_item_output(itemList)
