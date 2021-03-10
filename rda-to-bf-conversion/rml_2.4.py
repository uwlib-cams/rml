from sys import argv
import os
import time
from rdflib import *
import rdflib
from datetime import date
import uuid
from progress.bar import Bar
import requests
import csv
import xml.etree.ElementTree as ET

###

"""Retrieve RDA Data"""
import save_rda_locally

print("...\nCleaning input data")

print(">> Removing extra descriptions")
import remove_extra_descriptions

print(">> Fixing IRIs typed as literals")
import fix_URIs

print(">> Removing blank copyright dates")
import fix_copyright_dates

"""Transform RDA to BIBFRAME in XML"""
import transform_rda_to_bf

"""Separate blank nodes from resources"""
import separate_bnodes

# need to reserialize output as turtle

print("...\nCleaning output data")

print(">> Adding datatypes to dates")
import type_dates

"""Reserialize Turtle as JSON-LD"""
import serialize_ttl_json

"""Generate new IRIs for JSON-LD resources"""
import new_IDs_json

"""Prepare JSON-LD for upload into Sinopia""" # still in progress

# make the current file contents the value of property "data"

# wrap it all in brackets {} to make it a json object

# inside that object, insert Sinopia admin metadata

# post each file to Sinopia

print("...\nDone!")
