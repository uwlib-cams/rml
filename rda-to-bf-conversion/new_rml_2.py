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
#os.system('chmod u+rwx save_rda_locally.py') # remove before pushing
#import save_rda_locally

#print("...\nCleaning input data")

#print(">> Removing extra descriptions")
#os.system('chmod u+rwx remove_extra_descriptions.py') # remove before pushing
#import remove_extra_descriptions

#print(">> Fixing IRIs typed as literals")
#os.system('chmod u+rwx fix_URIs.py') # remove before pushing
#import fix_URIs

#print(">> Removing blank copyright dates")
#os.system('chmod u+rwx fix_copyright_dates.py') # remove before pushing
#import fix_copyright_dates

"""Transform RDA to BIBFRAME in Turtle"""
os.system('chmod u+rwx transform_rda_to_bf.py') # remove before pushing
import transform_rda_to_bf

print("...\nCleaning output data")

print(">> Fixing language tags")
os.system('chmod u+rwx fix_langtags.py') # remove before pushing
import fix_langtags

print(">> Adding datatypes to dates")
os.system('chmod u+rwx type_dates.py') # remove before pushing
import type_dates

"""Reserialize Turtle as JSON-LD"""
#os.system('chmod u+rwx serialize_ttl_json.py') # remove before pushing
#import serialize_ttl_json

"""Generate new IRIs for JSON-LD resources"""
#os.system('chmod u+rwx new_IDs_json.py') # remove before pushing
#import new_IDs_json

"""Prepare JSON-LD for upload into Sinopia"""

# make the current file contents the value of property "data"

# wrap it all in brackets {} to make it a json object

# inside that object, insert Sinopia admin metadata

# post each file to Sinopia

print("...\nDone!")
