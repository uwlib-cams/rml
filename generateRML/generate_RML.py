"""Python Libraries/Modules/Packages"""
import os
from sys import argv

script, csv_dir = argv

"""Lists"""
from functions.lists import entities

"""Imported Functions"""
from functions.parse_kiegel import kiegel_reader

###

if not os.path.exists(f'rmlOutput/'):
	os.system(f'mkdir rmlOutput')

for entity in entities:
	graph = kiegel_reader(csv_dir, entity)
	graph.serialize(destination=f"rmlOutput/{entity}RML.ttl", format="turtle")
