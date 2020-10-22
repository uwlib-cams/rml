import csv
import os
from sys import argv

script, data_directory = argv

if not os.path.exists('input/sample_records'):
    os.system('mkdir input/sample_records')

def get_work_property_list():
    csv_file_list = os.listdir("generateRML/csv_dir")
    work_files = []
    for file in csv_file_list:
        if "work" in file:
            work_files.append(file)

    work_property_list = []
    for csv_file in work_files:
        with open(f"""generateRML/csv_dir/{csv_file}""") as file:
            csv_reader = csv.reader(file, delimiter=',')
            line_count = 0
            for line in csv_reader:
                if line_count == 0: # ignore header row
                    pass
                elif line[1].strip('http://rdaregistry.info/Elements/w/') == "P10002": # mapping for this property too complex; writing it in manually
                    pass
                else:
                    prop_IRI = line[1]
                    if "rdaregistry" in prop_IRI:
                        prop_num = prop_IRI.lstrip('http://rdaregistry.info/Elements/w/')
                    else:
                        prop_num = prop_IRI.lstrip('https://doi.org/10.6069/uwlib.55.d.4')
                        prop_num = prop_num.strip('#')

                    work_property_list.append(prop_num)
                line_count += 1

    return work_property_list

def get_expression_property_list():
    csv_file_list = os.listdir("generateRML/csv_dir")
    expression_files = []
    for file in csv_file_list:
        if "expression" in file:
            expression_files.append(file)

    expression_property_list = []
    for csv_file in expression_files:
        with open(f"""generateRML/csv_dir/{csv_file}""") as file:
            csv_reader = csv.reader(file, delimiter=',')
            line_count = 0
            for line in csv_reader:
                if line_count == 0: # ignore header row
                    pass
                else:
                    prop_IRI = line[1]
                    if "rdaregistry" in prop_IRI:
                        prop_num = prop_IRI.lstrip('http://rdaregistry.info/Elements/e/')
                    else:
                        prop_num = prop_IRI.lstrip('https://doi.org/10.6069/uwlib.55.d.4')
                        prop_num = prop_num.strip('#')

                    expression_property_list.append(prop_num)
                line_count += 1

    return expression_property_list

def get_manifestation_property_list():
    csv_file_list = os.listdir("generateRML/csv_dir")
    manifestation_files = []
    for file in csv_file_list:
        if "manifestation" in file:
            manifestation_files.append(file)

    manifestation_property_list = []
    for csv_file in manifestation_files:
        with open(f"""generateRML/csv_dir/{csv_file}""") as file:
            csv_reader = csv.reader(file, delimiter=',')
            line_count = 0
            for line in csv_reader:
                if line_count == 0: # ignore header row
                    pass
                else:
                    prop_IRI = line[1]
                    if "rdaregistry" in prop_IRI:
                        prop_num = prop_IRI.lstrip('http://rdaregistry.info/Elements/m/')
                    else:
                        prop_num = prop_IRI.lstrip('https://doi.org/10.6069/uwlib.55.d.4')
                        prop_num = prop_num.strip('#')

                    manifestation_property_list.append(prop_num)
                line_count += 1

    return manifestation_property_list

def get_item_property_list():
    csv_file_list = os.listdir("generateRML/csv_dir")
    item_files = []
    for file in csv_file_list:
        if "item" in file:
            item_files.append(file)

    item_property_list = []
    for csv_file in item_files:
        with open(f"""generateRML/csv_dir/{csv_file}""") as file:
            csv_reader = csv.reader(file, delimiter=',')
            line_count = 0
            for line in csv_reader:
                if line_count == 0: # ignore header row
                    pass
                else:
                    prop_IRI = line[1]
                    if "rdaregistry" in prop_IRI:
                        prop_num = prop_IRI.lstrip('http://rdaregistry.info/Elements/i/')
                    else:
                        prop_num = prop_IRI.lstrip('https://doi.org/10.6069/uwlib.55.d.4')
                        prop_num = prop_num.strip('#')

                    item_property_list.append(prop_num)
                line_count += 1

    return item_property_list

###

for item in os.listdir(f"generateRML/csv_dir"):
    os.system(f"chmod u+rwx generateRML/csv_dir/{item}")

###

work_list = os.listdir(f"input/{data_directory}/work/")

work_output_list = [
"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n",
"<rdf:RDF\n",
"   xmlns:rdaw=\"http://rdaregistry.info/Elements/w/\"\n",
"   xmlns:bf=\"http://id.loc.gov/ontologies/bibframe/\"\n",
"   xmlns:bflc=\"http://id.loc.gov/ontologies/bflc/\"\n",
"   xmlns:rdax=\"https://doi.org/10.6069/uwlib.55.d.4#\"\n",
"   xmlns:sin=\"http://sinopia.io/vocabulary/\"\n",
"   xmlns:madsrdf=\"http://www.loc.gov/mads/rdf/v1#\"\n",
"   xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"\n",
"   xmlns:rdfs=\"http://www.w3.org/2000/01/rdf-schema#\"\n",
">\n",
"  <rdf:Description rdf:about=\"https://trellis.sinopia.io/repository/washington/sample_work\">\n",
"    <rdf:type rdf:resource=\"http://rdaregistry.info/Elements/c/C10001\"/>\n"
]

work_property_list = get_work_property_list()
work_literal_represented_list = []
work_IRI_represented_list = []

for csv_property in work_property_list:
    for work in work_list:
        with open(f"input/{data_directory}/work/{work}") as input_file:
            for line in input_file:
                input_property = line.strip()
                input_property = input_property.split('>')[0]
                input_property = input_property.split(' ')[0]
                if csv_property in input_property:
                    if input_property not in work_literal_represented_list:
                        if input_property not in work_IRI_represented_list:
                            work_output_list.append(line)
                            if "rdf:resource" in line:
                                work_IRI_represented_list.append(input_property)
                            else:
                                work_literal_represented_list.append(input_property)

work_output_ending_list = [
"  </rdf:Description>\n",
"</rdf:RDF>\n"
]

work_output_list = work_output_list + work_output_ending_list

with open("input/sample_records/sample_work_record.xml", "w") as output_file:
    for line in work_output_list:
        output_file.write(line)

###

expression_list = os.listdir(f"input/{data_directory}/expression/")

expression_output_list = [
"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n",
"<rdf:RDF\n",
"   xmlns:rdae=\"http://rdaregistry.info/Elements/e/\"\n",
"   xmlns:bf=\"http://id.loc.gov/ontologies/bibframe/\"\n",
"   xmlns:bflc=\"http://id.loc.gov/ontologies/bflc/\"\n",
"   xmlns:rdax=\"https://doi.org/10.6069/uwlib.55.d.4#\"\n",
"   xmlns:sin=\"http://sinopia.io/vocabulary/\"\n",
"   xmlns:madsrdf=\"http://www.loc.gov/mads/rdf/v1#\"\n",
"   xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"\n",
"   xmlns:rdfs=\"http://www.w3.org/2000/01/rdf-schema#\"\n",
">\n",
"  <rdf:Description rdf:about=\"https://trellis.sinopia.io/repository/washington/sample_expression\">\n",
"    <rdf:type rdf:resource=\"http://rdaregistry.info/Elements/c/C10006\"/>\n"
]

expression_property_list = get_expression_property_list()
expression_literal_represented_list = []
expression_IRI_represented_list = []

for csv_property in expression_property_list:
    for expression in expression_list:
        with open(f"input/{data_directory}/expression/{expression}") as input_file:
            for line in input_file:
                input_property = line.strip()
                input_property = input_property.split('>')[0]
                input_property = input_property.split(' ')[0]
                if csv_property in input_property:
                    if input_property not in expression_literal_represented_list:
                        if input_property not in expression_IRI_represented_list:
                            expression_output_list.append(line)
                            if "rdf:resource" in line:
                                expression_IRI_represented_list.append(input_property)
                            else:
                                expression_literal_represented_list.append(input_property)

expression_output_ending_list = [
"  </rdf:Description>\n",
"</rdf:RDF>\n"
]

expression_output_list = expression_output_list + expression_output_ending_list

with open("input/sample_records/sample_expression_record.xml", "w") as output_file:
    for line in expression_output_list:
        output_file.write(line)

###

manifestation_list = os.listdir(f"input/{data_directory}/manifestation/")

manifestation_output_list = [
"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n",
"<rdf:RDF\n",
"   xmlns:rdam=\"http://rdaregistry.info/Elements/m/\"\n",
"   xmlns:rdamdt=\"http://rdaregistry.info/Elements/m/datatype/\"\n",
"   xmlns:bf=\"http://id.loc.gov/ontologies/bibframe/\"\n",
"   xmlns:bflc=\"http://id.loc.gov/ontologies/bflc/\"\n",
"   xmlns:rdax=\"https://doi.org/10.6069/uwlib.55.d.4#\"\n",
"   xmlns:sin=\"http://sinopia.io/vocabulary/\"\n",
"   xmlns:madsrdf=\"http://www.loc.gov/mads/rdf/v1#\"\n",
"   xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"\n",
"   xmlns:rdfs=\"http://www.w3.org/2000/01/rdf-schema#\"\n",
">\n",
"  <rdf:Description rdf:about=\"https://trellis.sinopia.io/repository/washington/sample_manifestation\">\n",
"    <rdf:type rdf:resource=\"http://rdaregistry.info/Elements/c/C10007\"/>\n"
]

manifestation_property_list = get_manifestation_property_list()
manifestation_literal_represented_list = []
manifestation_IRI_represented_list = []

for csv_property in manifestation_property_list:
    for manifestation in manifestation_list:
        if ".ttl" in manifestation:
            print(manifestation)
            pass
        else:
            with open(f"input/{data_directory}/manifestation/{manifestation}") as input_file:
                for line in input_file:
                    input_property = line.strip()
                    input_property = input_property.split('>')[0]
                    input_property = input_property.split(' ')[0]
                    if csv_property in input_property:
                        if input_property not in manifestation_literal_represented_list:
                            if input_property not in manifestation_IRI_represented_list:
                                manifestation_output_list.append(line)
                                if "rdf:resource" in line:
                                    manifestation_IRI_represented_list.append(input_property)
                                else:
                                    manifestation_literal_represented_list.append(input_property)

manifestation_output_ending_list = [
"  </rdf:Description>\n",
"</rdf:RDF>\n"
]

manifestation_output_list = manifestation_output_list + manifestation_output_ending_list

with open("input/sample_records/sample_manifestation_record.xml", "w") as output_file:
    for line in manifestation_output_list:
        output_file.write(line)

###

item_list = os.listdir(f"input/{data_directory}/item/")

item_output_list = [
"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n",
"<rdf:RDF\n",
"   xmlns:rdai=\"http://rdaregistry.info/Elements/i/\"\n",
"   xmlns:bf=\"http://id.loc.gov/ontologies/bibframe/\"\n",
"   xmlns:bflc=\"http://id.loc.gov/ontologies/bflc/\"\n",
"   xmlns:rdax=\"https://doi.org/10.6069/uwlib.55.d.4#\"\n",
"   xmlns:sin=\"http://sinopia.io/vocabulary/\"\n",
"   xmlns:madsrdf=\"http://www.loc.gov/mads/rdf/v1#\"\n",
"   xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"\n",
"   xmlns:rdfs=\"http://www.w3.org/2000/01/rdf-schema#\"\n",
">\n",
"  <rdf:Description rdf:about=\"https://trellis.sinopia.io/repository/washington/sample_item\">\n",
"    <rdf:type rdf:resource=\"http://rdaregistry.info/Elements/c/C10003\"/>\n"
]

item_property_list = get_item_property_list()
item_literal_represented_list = []
item_IRI_represented_list = []

for csv_property in item_property_list:
    for item in item_list:
        with open(f"input/{data_directory}/item/{item}") as input_file:
            for line in input_file:
                input_property = line.strip()
                input_property = input_property.split('>')[0]
                input_property = input_property.split(' ')[0]
                if csv_property in input_property:
                    if input_property not in item_literal_represented_list:
                        if input_property not in item_IRI_represented_list:
                            item_output_list.append(line)
                            if "rdf:resource" in line:
                                item_IRI_represented_list.append(input_property)
                            else:
                                item_literal_represented_list.append(input_property)

item_output_ending_list = [
"  </rdf:Description>\n",
"</rdf:RDF>\n"
]

item_output_list = item_output_list + item_output_ending_list

with open("input/sample_records/sample_item_record.xml", "w") as output_file:
    for line in item_output_list:
        output_file.write(line)
