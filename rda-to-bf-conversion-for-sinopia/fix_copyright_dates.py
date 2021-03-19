import os
from datetime import date

"""Variables"""
today = date.today()
currentDate = str(today).replace('-', '_')

"""Lists"""
workList = os.listdir(f'../input/{currentDate}/work')
expressionList = os.listdir(f'../input/{currentDate}/expression')
manifestationList = os.listdir(f'../input/{currentDate}/manifestation')
itemList = os.listdir(f'../input/{currentDate}/item')

###

for work in workList:
	with open(f'../input/{currentDate}/work/{work}', 'r') as work_xml:
		work_line_list = []
		for line in work_xml:
			if "©" in line:
				value = line.split(">")[1]
				value = value.split("<")[0]
				is_copyright_date = False
				for character in value:
					if character.isnumeric():
						is_copyright_date = True
				if is_copyright_date == True:
					work_line_list.append(line)
			else:
				work_line_list.append(line)
	with open(f'../input/{currentDate}/work/{work}', 'w') as work_xml:
		for line in work_line_list:
			work_xml.write(line)

for expression in expressionList:
	with open(f'../input/{currentDate}/expression/{expression}', 'r') as expression_xml:
		expression_line_list = []
		for line in expression_xml:
			if "©" in line:
				value = line.split(">")[1]
				value = value.split("<")[0]
				is_copyright_date = False
				for character in value:
					if character.isnumeric():
						is_copyright_date = True
				if is_copyright_date == True:
					expression_line_list.append(line)
			else:
				expression_line_list.append(line)
	with open(f'../input/{currentDate}/expression/{expression}', 'w') as expression_xml:
		for line in expression_line_list:
			expression_xml.write(line)

for manifestation in manifestationList:
	with open(f'../input/{currentDate}/manifestation/{manifestation}', 'r') as manifestation_xml:
		manifestation_line_list = []
		for line in manifestation_xml:
			if "©" in line:
				value = line.split(">")[1]
				value = value.split("<")[0]
				is_copyright_date = False
				for character in value:
					if character.isnumeric():
						is_copyright_date = True
				if is_copyright_date == True:
					manifestation_line_list.append(line)
			else:
				manifestation_line_list.append(line)
	with open(f'../input/{currentDate}/manifestation/{manifestation}', 'w') as manifestation_xml:
		for line in manifestation_line_list:
			manifestation_xml.write(line)

for item in itemList:
	with open(f'../input/{currentDate}/item/{item}', 'r') as item_xml:
		item_line_list = []
		for line in item_xml:
			if "©" in line:
				value = line.split(">")[1]
				value = value.split("<")[0]
				is_copyright_date = False
				for character in value:
					if character.isnumeric():
						is_copyright_date = True
				if is_copyright_date == True:
					item_line_list.append(line)
			else:
				item_line_list.append(line)
	with open(f'../input/{currentDate}/item/{item}', 'w') as item_xml:
		for line in item_line_list:
			item_xml.write(line)
