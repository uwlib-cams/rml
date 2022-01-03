"""Functions"""
def class_test(node):
	"""Determine if a term is a property or a class. Returns True if class, returns False if property."""
	its_a_class = False

	if ":" in node:
		node = node.split(":")[-1]

	if node[0].isupper() == True:
		its_a_class = True

	return its_a_class
