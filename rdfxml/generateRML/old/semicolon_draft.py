map = """identifiedBy >> Identifier > rdf:value > note >> Note > rdfs:label="Access point" > noteType="type of identifier" """

map_list = map.split(" ")

# some constant literal values will have spaces in them that shouldn't be split; the following code will look for these instances and fix them

map_list_length = len(map_list)

map_list_range = range(0, map_list_length)

index_list = []

for n in map_list_range:
    literal_value = "x" # random value assignment

    item = map_list[n]
    print(item + "\n")
    # noteType="type

    if len(item) > 0: # make sure it has characters to check
        continue_search = True
        print("yes characters\n")
    else:
        continue_search = False

    if continue_search == True: # check if constant
        if "=" in item:
            continue_search = True
            print("yes constant\n")
        else:
            continue_search = False

    if continue_search == True: # check if literal constant
        if '"' in item:
            continue_search = True
            print("yes literal\n")
        else:
            continue_search = False

    if continue_search == True: # check if the last character is "
        if item[-1] != '"': # if it is not ", the rest of the literal has been cut off
            literal_value = item # start new literal
            print(literal_value + "\n")
            index_list.append(n) # record index in list
            continue_search = True
        else:
            continue_search = False

    while continue_search == True: # searching for the rest of the literal that has been split off
        n = n + 1
        item = map_list[n]
        literal_value = literal_value + " " + item # add to literal
        print(literal_value + "\n")
        index_list.append(n) # record index in list

        if item[-1] != '"': # check if the literal is over now
            continue_search = True
            print("literal is over\n")
        else:
            continue_search = False

    if literal_value != "x": # if the literal_value has changed from "x"
        for num in reversed(index_list):
            map_list.pop(num) # remove unnecessarily separated values
        map_list.insert(index_list[0], literal_value) # replace with full literal

        remaining_broken_constants = 0

        for item in map_list:
            if "=" in item:
                if item[-1] != '"':
                    remaining_broken_constants = remaining_broken_constants + 1

        if remaining_broken_constants == 0:
            break


for line in map_list:
    print(line)
