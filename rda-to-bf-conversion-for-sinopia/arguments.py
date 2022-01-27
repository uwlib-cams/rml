import argparse

def define_arg():
	parser = argparse.ArgumentParser(description='Convert data from RDA/RDF to BIBFRAME and post to Sinopia.')
	parser.add_argument('-s', '--source', default='https://api.sinopia.io/resource?limit=1000&group=washington', help='URI for RDA data')
	parser.add_argument('-i', '--input', default='RDA', help='desired location of RDA files')
	parser.add_argument('-o', '--output', default='BIBFRAME', help='desired location of BIBFRAME files')
	parser.add_argument('-v', '--version', action='version', version='Last updated 2022-01-27')

	args = parser.parse_args()

	return args
