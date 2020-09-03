import os

bad_files = {}
bad_input_file_count = 0

"""For input files"""

workList = os.listdir('input/2020_9_2/work')
expressionList = os.listdir('input/2020_9_2/expression')
manifestationList = os.listdir('input/2020_9_2/manifestation')
itemList = os.listdir('input/2020_9_2/item')

for work in workList:
    workID = work.split(".")[0]
    with open(f'input/2020_9_2/work/{work}', 'r') as file:
        identifier_list = []
        for line in file:
            if '<rdf:Description rdf:about="https://trellis.sinopia.io/repository/washington/' in line:
                identifier = line.strip()
                identifier = identifier.split('/')[-1]
                identifier = identifier.rstrip('">')
                identifier_list.append(identifier)
        no_match = True
        for item in identifier_list:
            if item == workID:
                no_match = False
        if no_match == True:
            identifier = identifier_list[0]
            if identifier in bad_files.keys():
                bad_files[identifier][0].append(f'work/{work}')
            else:
                bad_files[identifier] = ([f'work/{work}'], [])
            bad_input_file_count += 1

for expression in expressionList:
    expressionID = expression.split(".")[0]
    with open(f'input/2020_9_2/expression/{expression}', 'r') as file:
        identifier_list = []
        for line in file:
            if '<rdf:Description rdf:about="https://trellis.sinopia.io/repository/washington/' in line:
                identifier = line.strip()
                identifier = identifier.split('/')[-1]
                identifier = identifier.rstrip('">')
                identifier_list.append(identifier)
        no_match = True
        for item in identifier_list:
            if item == expressionID:
                no_match = False
        if no_match == True:
            identifier = identifier_list[0]
            if identifier in bad_files.keys():
                bad_files[identifier][0].append(f'expression/{expression}')
            else:
                bad_files[identifier] = ([f'expression/{expression}'], [])
            bad_input_file_count += 1

for manifestation in manifestationList:
    manifestationID = manifestation.split(".")[0]
    with open(f'input/2020_9_2/manifestation/{manifestation}', 'r') as file:
        identifier_list = []
        for line in file:
            if '<rdf:Description rdf:about="https://trellis.sinopia.io/repository/washington/' in line:
                identifier = line.strip()
                identifier = identifier.split('/')[-1]
                identifier = identifier.rstrip('">')
                identifier_list.append(identifier)
        no_match = True
        for item in identifier_list:
            if item == manifestationID:
                no_match = False
        if no_match == True:
            identifier = identifier_list[0]
            if identifier in bad_files.keys():
                bad_files[identifier][0].append(f'manifestation/{manifestation}')
            else:
                bad_files[identifier] = ([f'manifestation/{manifestation}'], [])
            bad_input_file_count += 1

for item in itemList:
    itemID = item.split(".")[0]
    with open(f'input/2020_9_2/item/{item}', 'r') as file:
        for line in file:
            if '<rdf:Description rdf:about="https://trellis.sinopia.io/repository/washington/' in line:
                identifier = line.strip()
                identifier = identifier.split('/')[-1]
                identifier = identifier.rstrip('">')
                identifier_list.append(identifier)
        no_match = True
        for item in identifier_list:
            if item == itemID:
                no_match = False
        if no_match == True:
            identifier = identifier_list[0]
            if identifier in bad_files.keys():
                bad_files[identifier][0].append(f'item/{item}')
            else:
                bad_files[identifier] = ([f'item/{item}'], [])
            bad_input_file_count += 1

"""For output files"""

work1List = os.listdir('output/2020_9_2/work_1')
work2List = os.listdir('output/2020_9_2/work_2')
instanceList = os.listdir('output/2020_9_2/instance')
itemList = os.listdir('output/2020_9_2/item')

bad_output_file_count = 0

for work_1 in work1List:
    work1ID = work_1.split(".")[0]
    with open(f'output/2020_9_2/work_1/{work_1}', 'r') as file:
        identifier_list = []
        for line in file:
            if "> a bf:Work " in line:
                identifier = line.split('>')[0]
                identifier = identifier.split('/')[-1]
                identifier_list.append(identifier)
        no_match = True
        for item in identifier_list:
            if item == work1ID:
                no_match = False
        if no_match == True:
            identifier = identifier_list[0]
            if identifier in bad_files.keys():
                bad_files[identifier][1].append(f'work_1/{work_1}')
            else:
                bad_files[identifier] = ([], [f'work_1/{work_1}'])
            bad_output_file_count += 1

for work_2 in work2List:
    work2ID = work_2.split(".")[0]
    with open(f'output/2020_9_2/work_2/{work_2}', 'r') as file:
        identifier_list = []
        for line in file:
            if "> a bf:Work " in line:
                identifier = line.split('>')[0]
                identifier = identifier.split('/')[-1]
                identifier_list.append(identifier)
        no_match = True
        for item in identifier_list:
            if item == work2ID:
                no_match = False
        if no_match == True:
            identifier = identifier_list[0]
            if identifier in bad_files.keys():
                bad_files[identifier][1].append(f'work_2/{work_2}')
            else:
                bad_files[identifier] = ([], [f'work_2/{work_2}'])
            bad_output_file_count += 1

for instance in instanceList:
    instanceID = instance.split(".")[0]
    with open(f'output/2020_9_2/instance/{instance}', 'r') as file:
        for line in file:
            if "> a bf:Instance " in line:
                identifier = line.split('>')[0]
                identifier = identifier.split('/')[-1]
                identifier_list.append(identifier)
        no_match = True
        for item in identifier_list:
            if item == instanceID:
                no_match = False
        if no_match == True:
            identifier = identifier_list[0]
            if identifier in bad_files.keys():
                bad_files[identifier][1].append(f'instance/{instance}')
            else:
                bad_files[identifier] = ([], [f'instance/{instance}'])
            bad_output_file_count += 1

for item in itemList:
    itemID = item.split(".")[0]
    with open(f'output/2020_9_2/item/{item}', 'r') as file:
        for line in file:
            if "> a bf:Item " in line:
                identifier = line.split('>')[0]
                identifier = identifier.split('/')[-1]
                identifier_list.append(identifier)
        no_match = True
        for item_ in identifier_list:
            if item_ == itemID:
                no_match = False
        if no_match == True:
            identifier = identifier_list[0]
            if identifier in bad_files.keys():
                bad_files[identifier][1].append(f'item/{item}')
            else:
                bad_files[identifier] = ([], [f'item/{item}'])
            bad_output_file_count += 1

with open('badFileReport.txt', 'w') as output_file:
    output_file.write(f"Total number of bad files: {bad_input_file_count + bad_output_file_count}\nBad input files: {bad_input_file_count}\nBad output files: {bad_output_file_count}\n\n***\n\n")
    for identifier in bad_files.keys():
        input_file_list = bad_files[identifier][0]
        output_file_list = bad_files[identifier][1]

        input_file_list_length = len(input_file_list)
        output_file_list_length = len(output_file_list)

        output_file.write(f"Identifier: {identifier}\nNumber of times repeated: {input_file_list_length}\nAppears in:\n")
        if input_file_list_length > 0:
            output_file.write("Input files:\n")
            for file_ in input_file_list:
                output_file.write(f"\t-- {file_}\n")

        if output_file_list_length > 0:
            output_file.write("Output files:\n")
            for file_ in output_file_list:
                output_file.write(f"\t-- {file_}\n")

        output_file.write("\n***\n\n")