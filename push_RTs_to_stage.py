import json
import os
import requests
from rdflib import *
import time

###

"""Functions"""

def pull_data_from_sinopia():
    response = requests.get('https://api.sinopia.io/resource?limit=1000&group=washington')
    with open('uw_list.json', 'w') as output_file:
        output_file.write(response.text)

def extract_URIs_from_data():
    os.system('java -jar mapper.jar -m find_URIs_rml.ttl -o uw_uri_list.nq')

def list_RT_URIs():
    ex = Namespace('http://example.org/rules/')
    g = Graph()
    g.bind('ex', ex)
    g.load('file:uw_uri_list.nq', format='nquads')

    RT_list = []
    for s, p, o in g:
        if "https://api.sinopia.io/resource/WAU:RT:" in o:
            uri = "{}".format(o)
            RT_list.append(uri)

    return RT_list

def pull_RT_and_push_to_stage(RT_list):
    print("Copy and paste a Java Web Token for Sinopia-Stage below.")
    jwt = input("> ")

    oops_error = []
    success = []
    for RT_URI in RT_list:
        response = requests.get(RT_URI)
        with open('old_json.json', 'w') as output_file:
            output_file.write(response.text)
        id = edit_json()
        iri = f"https://api.stage.sinopia.io/resource/{id}"
        RT_file = open('new_json.json')
        RT_data = RT_file.read()

        headers = {"Authorization": f"Bearer {jwt}", "Content-Type": "application/json"}
        post_to_sinopia = requests.post(iri, data=RT_data.encode('utf-8'), headers = headers)
        if post_to_sinopia.status_code != requests.codes.ok:
            error_code = post_to_sinopia.status_code
            if error_code == 401:
                print("\nJava Web Token not valid.")
                exit()
            elif error_code == 409:
                print(f"\nWarning: IRI is not unique:\n- {iri}\n\nOverwrite existing RT? (y/n)")
                overwrite = input("> ")
                if overwrite.lower() == "y":
                    overwrite_to_sinopia = requests.put(iri, data=RT_data.encode('utf-8'), headers = headers)

                    if overwrite_to_sinopia.status_code == requests.codes.ok:
                        success.append(id)
                    elif overwrite_to_sinopia.status_code == 201: # created, not actually an error
                        success.append(id)
                    elif overwrite_to_sinopia.status_code == 409: # we're overwriting so it's fine
                        success.append(id)
                    else:
                        print(f"Error: {overwrite_to_sinopia.status_code}")
                        exit()
            elif error_code != 201: # created, not actually an error
                RT_tuple = (id, error_code)
                oops_error.append(RT_tuple)
            else:
                success.append(id)

    if len(success) != 0:
        print("\nThe following RTs were uploaded successfully:")
        for yay in success:
            print(f"> {yay}")

    if len(oops_error) != 0:
        print("\nThe following RTs were *NOT* uploaded successfully:")
        for oops in oops_error:
            print(f"> {oops[0]} ({oops[1]})")

def edit_json():
    with open('old_json.json', 'r') as input_file:
        old_json = json.load(input_file)
        new_json = {}
        new_data = []
        for object in old_json["data"]:
            old_object = object
            new_object = {}
            for object_key in object.keys():
                if object_key == "@id" and "https://api.sinopia.io/resource/WAU:RT:" in object[object_key]:
                    old_iri = object[object_key]
                    old_id = old_iri.split("/")[-1]
                    new_iri = f"https://api.stage.sinopia.io/resource/{old_id}"
                    new_object[object_key] = new_iri
                elif object_key == "http://sinopia.io/vocabulary/hasDate":
                    old_date_list = object[object_key]
                    old_date_dict = old_date_list[0]
                    new_date_dict = {}
                    for old_date_key in old_date_dict.keys():
                        if old_date_key == "@value":
                            currentDate = time.strftime("%Y-%m-%d")
                            new_date_dict[old_date_key] = currentDate
                        else:
                            new_date_dict[old_date_key] = old_date_dict[old_date_key]
                    new_date_list = [new_date_dict]
                    new_object[object_key] = new_date_list
                else:
                    new_object[object_key] = object[object_key]
            new_data.append(new_object)
        new_json["data"] = new_data
        new_json["user"] = old_json["user"]
        new_json["group"] = old_json["group"]
        new_json["templateId"] = old_json["templateId"]
        new_json["types"] = old_json["types"]
        new_json["bfAdminMetadataRefs"] = old_json["bfAdminMetadataRefs"]
        new_json["bfItemRefs"] = old_json["bfItemRefs"]
        new_json["bfInstanceRefs"] = old_json["bfInstanceRefs"]
        new_json["bfWorkRefs"] = old_json["bfWorkRefs"]
        new_json["id"] = old_json["id"]
        new_json["uri"] = f"https://api.stage.sinopia.io/resource/{old_json['id']}"
        new_json["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    with open('new_json.json', 'w') as output_file:
        json_output = json.dumps(new_json)
        output_file.write(json_output)

    new_id = new_json["id"]
    return new_id

###

"""Run code"""

pull_data_from_sinopia()

extract_URIs_from_data()

RT_URI_list = list_RT_URIs()

pull_RT_and_push_to_stage(RT_URI_list)

# remove files generated in the process that are no longer necessary
os.system('rm new_json.json')
os.system('rm old_json.json')
os.system('rm uw_list.json')
os.system('rm uw_uri_list.nq')
