from datetime import date
import os
from progress.bar import Bar
import time
from timeit import default_timer as timer

"""Variables"""

# format for naming folder according to date
today = date.today()
currentDate = str(today).replace('-', '_')

"""Lists and Dictionaries"""
work_1List = os.listdir(f'../output/{currentDate}/work_1_json')
work_2List = os.listdir(f'../output/{currentDate}/work_2_json')
instanceList = os.listdir(f'../output/{currentDate}/instance_json')
itemList = os.listdir(f'../output/{currentDate}/item_json')

resource_dict = {"work_1": work_1List, "work_2": work_2List, "instance": instanceList, "item": itemList}

rt_dict = {"work_1": "WAU:RT:BF2:Work", "work_2": "WAU:RT:BF2:Work", "instance": "WAU:RT:BF2:Instance", "item": "WAU:RT:BF2:Item"}

class_dict = {"work_1": "http://id.loc.gov/ontologies/bibframe/Work", "work_2": "http://id.loc.gov/ontologies/bibframe/Work", "instance": "http://id.loc.gov/ontologies/bibframe/Instance", "item": "http://id.loc.gov/ontologies/bibframe/Item"}

new_line_list = [
"{\n", # 0
"  \"data\": [\n", # 1
"  ],\n", # 2
"  \"user\": \"mcm104\",\n", # 3
"  \"group\": \"washington\",\n", # 4
"  \"types\": [\n", # 5
"  ],\n", # 6
"}\n" # 7
]

###

num_of_resources = len(work_1List) + len(work_2List) + len(instanceList) + len(itemList)

start = timer()
print("...\nEditing JSON-LD for upload to Sinopia")
bar = Bar(max=num_of_resources, suffix='%(percent)d%%') # progress bar
for entity in resource_dict.keys():
	for resource in resource_dict[entity]:
		output_list = []

		for new_line in new_line_list[0:2]:
			output_list.append(new_line)

		with open(f'../output/{currentDate}/{entity}_json/{resource}', 'r') as original_file:
			max_line_count = 0
			for line in original_file:
				max_line_count += 1
			max_line_count = max_line_count - 1
		with open(f'../output/{currentDate}/{entity}_json/{resource}', 'r') as original_file:
			line_count = 0
			for line in original_file:
				if line_count == 0:
					pass
				elif line_count == max_line_count:
					pass
				else:
					output_list.append(f"  {line}")
				line_count += 1

		for new_line in new_line_list[2:5]:
			output_list.append(new_line)

		rt = rt_dict[entity]
		output_list.append(f"  \"templateId\": \"{rt}\",\n")

		output_list.append(new_line_list[5])

		class_IRI = class_dict[entity]
		output_list.append(f"    \"{class_IRI}\"\n")
		output_list.append(new_line_list[6])

		resource_id = resource.split('.')[0]
		output_list.append(f"  \"id\": \"{resource_id}\",\n")

		resource_uri = f"https://api.stage.sinopia.io/resource/{resource_id}"
		output_list.append(f"  \"uri\": \"{resource_uri}\",\n")

		currentTime = time.strftime("%Y-%m-%dT%H:%M:%S")
		output_list.append(f"  \"timestamp\": \"{currentTime}\"\n")

		output_list.append(new_line_list[7])

		with open(f'../output/{currentDate}/{entity}_json/{resource}', 'w') as edited_file:
			for line in output_list:
				edited_file.write(line)

		bar.next()
end = timer()
bar.finish()

print(f"Elapsed time: {round((end - start), 1)} s")
