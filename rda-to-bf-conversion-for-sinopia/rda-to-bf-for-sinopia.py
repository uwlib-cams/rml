import os

"""Retrieve RDA Data"""
print("Saving RDA data locally in RDF/XML")
import save_rda_locally

print("...\nCleaning input data")

"""Remove descriptions that are not about the resource in question"""
import remove_extra_descriptions

"""Fix IRIs that have been typed as literals"""
import fix_URIs

"""Remove empty copyright dates"""
import fix_copyright_dates

"""Transform RDA to BIBFRAME in XML"""
print("...\nTransforming RDA data into BIBFRAME in RDF/XML")
import transform_rda_to_bf

print("...\nCleaning output data")

"""Replacing RDA IRIs with BIBFRAME IRIs"""
import fix_related_IRIs

"""Adding datatypes to dates"""
import type_dates

"""Prepare JSON-LD for upload into Sinopia"""
import edit_json

"""Upload into Sinopia"""
import post_to_sinopia

print("...\nDone!")
