"""Python Libraries/Modules/Packages"""
import os

###

"""Retrieve RDA Data"""
print("Saving RDA data locally in RDF/XML")
import scripts.save_rda_locally

print("...\nCleaning input data")

"""Remove descriptions that are not about the resource in question"""
import scripts.remove_extra_descriptions

"""Fix IRIs that have been typed as literals"""
import scripts.fix_URIs

"""Remove empty copyright dates"""
import scripts.fix_copyright_dates

"""Transform RDA to BIBFRAME in XML"""
print("...\nTransforming RDA data into BIBFRAME in RDF/XML")
import scripts.transform_rda_to_bf

print("...\nCleaning output data")

"""Replacing RDA IRIs with BIBFRAME IRIs"""
import scripts.fix_related_IRIs

"""Adding datatypes to dates"""
import scripts.type_dates

"""Prepare JSON-LD for upload into Sinopia"""
print("...\nConverting into JSON-LD for upload into Sinopia")
import scripts.edit_json

"""Upload into Sinopia"""
print("...\nUploading into Sinopia")
import scripts.post_to_sinopia

print("...\nDone!")
