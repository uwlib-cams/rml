import os
from sys import argv

script, csv_dir = argv

"""Lists"""
from lists import entities

"""Imported Functions"""
from kiegel_functions import kiegel_reader

###

if not os.path.exists(f'rmlOutput/'):
	os.system(f'mkdir rmlOutput')

for entity in entities:
	graph = kiegel_reader(csv_dir, entity)
	graph.serialize(destination=f"rmlOutput/{entity}RML.ttl", format="turtle")
