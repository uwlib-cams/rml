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

print("...\nCleaning output data")

print(">> Adding datatypes to dates")
import type_dates

print("...\nDone!")
