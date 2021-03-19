import os

rml_list = ['workRML.ttl', 'expressionRML.ttl', 'manifestationRML.ttl', 'itemRML.ttl']

for file in rml_list:
	with open(file, 'r') as rml_file:
		line_count = 1
		test_line = 0

		for line in rml_file:
			if line_count != test_line:
				line = line.strip()
				if line == "ex:ExpressionMap rr:predicateObjectMap [":
					test_line = line_count + 3
			else:
				line = line.strip()
				if "rr:parentTriplesMap" not in line:
					print(f"{file}: {line} ({str(line_count)})")
				test_line = 0
			line_count += 1
