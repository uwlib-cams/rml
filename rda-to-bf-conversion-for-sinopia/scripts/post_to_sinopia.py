"""Python Libraries/Modules/Packages"""
from datetime import date
import os
from progress.bar import Bar
import requests
import time
from timeit import default_timer as timer

"""Imported Functions"""
from scripts.arguments import define_arg

"""Variables"""
# format for naming folder according to date
today = date.today()
currentDate = str(today).replace('-','_')

# arguments from command line
args = define_arg()
output_location = args.output

"""Lists"""
work_1_list = os.listdir(f"{output_location}/{currentDate}/work_1_json/")
work_2_list = os.listdir(f"{output_location}/{currentDate}/work_2_json/")
instance_list = os.listdir(f"{output_location}/{currentDate}/instance_json/")
item_list = os.listdir(f"{output_location}/{currentDate}/item_json/")

resource_dict = {"work_1": work_1_list, "work_2": work_2_list, "instance": instance_list, "item": item_list}

###

num_of_resources = len(work_1_list) + len(work_2_list) + len(instance_list) + len(item_list)

# create dictionaries for report
success_dict = {"work_1": [], "work_2": [], "instance": [], "item": []}
fail_dict = {"work_1": [], "work_2": [], "instance": [], "item": []}

print("Copy and paste a Java Web Token for Sinopia-Stage below.")
jwt = input("> ")

yes_to_all = False

start = timer()
bar = Bar('Posting to Sinopia-Stage', max=num_of_resources, suffix='%(percent)d%%') # progress bar
for entity in resource_dict.keys():
	for resource in resource_dict[entity]:
		resource_loop = True
		while resource_loop == True:
			# set up variables
			headers = {"Authorization": f"Bearer {jwt}", "Content-Type": "application/json"}

			resource_id = resource.split('.')[0]
			resource_iri = f'https://api.sinopia.io/resource/{resource_id}'

			resource = open(f'{output_location}/{currentDate}/{entity}_json/{resource}')
			data = resource.read()

			# post to sinopia
			post_to_sinopia = requests.post(resource_iri, data=data.encode('utf-8'), headers = headers)

			# look for error messages
			if post_to_sinopia.status_code != requests.codes.ok:
				error_code = post_to_sinopia.status_code
				if error_code == 201: # created, not actually an error
					success_dict[entity].append(resource_iri)
					resource_loop = False
				elif error_code == 401: # unauthorized
					print("\nJava Web Token no longer valid.")
					print("Copy and paste a Java Web Token for Sinopia-Stage below.")
					jwt = input("> ")
				elif error_code == 409: # conflict
					if yes_to_all == False:
						print("\nWarning: IRI is not unique. Overwrite existing data? (y/n)")
						overwrite = input("> ")
						if overwrite.lower() == "y":
							requests.put(resource_iri, data=data.encode('utf-8'), headers = headers)
							success_dict[entity].append(resource_iri)
							print("\nOverwrite data for all repeated IRIs? (y/n)")
							overwrite_all = input("> ")
							if overwrite_all.lower() == "y":
								yes_to_all = True
						else:
							fail_dict[entity].append((resource_id, error_code))
					else:
						requests.put(resource_iri, data=data.encode('utf-8'), headers = headers)
						success_dict[entity].append(resource_iri)
					resource_loop = False
				else:
					fail_dict[entity].append((resource_id, error_code))
					resource_loop = False
			else:
				success_dict[entity].append(resource_iri)
				resource_loop = False
		bar.next()
bar.finish()

with open(f'other_files/post_to_sinopia_report_{currentDate}.txt', 'w') as report:
	currentTime = time.strftime("%Y-%m-%dT%H:%M:%S")
	report.write(f"Time of report: {currentTime}\n\n---\n")
	for entity in resource_dict.keys():
		report.write(f"\n{entity.upper()}\n\n")

		if len(success_dict[entity]) > 0:
			report.write("Successes\n\n")
			for resource in success_dict[entity]:
				report.write(f"- {resource}\n")

		if len(fail_dict[entity]) > 0:
			report.write("Failures\n\n")
			for resource in fail_dict[entity]:
				report.write(f"- {resource[0]}.json ({resource[1]})\n")
end = timer()
print(f"Elapsed time: {round((end - start), 2)} s")
