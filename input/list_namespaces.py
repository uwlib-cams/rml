import os
from sys import argv

script, data_dir = argv # input requires file path to directory with files to analyze

"""Make list containing files in directory"""

list_of_directories = os.listdir(data_dir)
list_of_files = []

for directory in list_of_directories:
    new_list = os.listdir(f"{data_dir}/{directory}")
    for item in new_list:
        list_of_files.append(f"{data_dir}/{directory}/{item}")

"""Add all lines of code in data directory to a list"""
big_data_list = []

for file_name in list_of_files:
    with open(f'{file_name}', 'r') as data_file:
        for line in data_file:
            big_data_list.append(line)

"""Make a dictionary in which the keys are namespaces, and the values are their respective prefixes"""
namespace_prefix_dict = {}

for line in big_data_list:
    if "xmlns:" in line: # this only works for xml files; will need more options for turtle, etc.
        namespace = line.split('=')[-1]
        namespace = namespace.strip()
        namespace = namespace.strip('"')

        prefix = line.split('=')[0]
        prefix = prefix.split(':')[-1]
        prefix = prefix.strip()

        namespace_prefix_dict[namespace] = prefix

"""Make a dictionary in which the keys are namespaces, and the values are lists containing all properties using that namespace"""
property_dict = {}
for namespace in namespace_prefix_dict.keys(): # add empty lists to dictionary for each namespace
    property_dict[namespace] = []

for line in big_data_list:
    for namespace in namespace_prefix_dict.keys():
        prefix = "<" + namespace_prefix_dict[namespace] + ":"
        if prefix in line:
            line = line.strip()
            if "xmlns" in line: # ignore lines that declare namespace
                pass
            else:
                has_attribute = False
                if ' ' in line.split('>')[0]: # this is specific to formatting in xml
                    has_attribute = True

                if has_attribute == True:
                    property = line.split(' ')[0]
                else:
                    property = line.split('>')[0]

                property = property.split(':')[1]
                property_dict[namespace].append(property)

"""Get rid of duplicates in property lists"""
for namespace in property_dict.keys():
    property_list = property_dict[namespace]
    new_property_list = []
    for property in property_list:
        if property not in new_property_list:
            new_property_list.append(property)
    new_property_list = sorted(new_property_list)
    property_dict[namespace] = new_property_list


"""Write to output file"""
with open('namespaces.txt', 'a') as output_file:
    for namespace in namespace_prefix_dict.keys():
        line = f"Namespace: <{namespace}>\nProperties:\n"
        output_file.write(line)
        for property in property_dict[namespace]:
            output_file.write(f"\t-- {property}\n")
        output_file.write('\n')
