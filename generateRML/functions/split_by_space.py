"""Functions"""
def split_by_space(map):
	"""Takes in a kiegel map as a string, and returns the elements in the map separated as a list"""
	map = map.strip()
	map_list = map.split(" ")

	# some constant literal values will have spaces in them that shouldn't be split; the following code will look for these instances and fix them
	if '="' in map:
		continue_search = False
		new_map_list = []
		for item in map_list:
			if len(item) < 1:
				pass
			else:
				item = item.strip()
				if item.split('=')[-1][0] == '"' and item[-1] != '"': # first character after = is " and the last character of string is NOT "...
					broken_constant_list = []
					broken_constant_list.append(item)
					continue_search = True
				else:
					if continue_search == True:
						broken_constant_list.append(item)
						if item[-1] == '"': # if the last character is ", the broken constant list has all the parts of the literal
							continue_search = False
							fixed_constant = " ".join(broken_constant_list)
							new_map_list.append(fixed_constant)
					else:
						new_map_list.append(item)

		map_list = new_map_list

	return map_list
