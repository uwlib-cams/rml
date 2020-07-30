import os

workList = os.listdir('data/2020_7_28/work/')
expressionList = os.listdir('data/2020_7_28/expression')
manifestationList = os.listdir('data/2020_7_28/manifestation')
itemList = os.listdir('data/2020_7_28/item')

prefix_list = [
"ns1",
"ns2",
"ns3",
"ns4",
"ns5",
"ns6",
"ns7",
"ns8",
"ns9"
]

namespace_list = [
"http://id.loc.gov/ontologies/bibframe/",
"http://id.loc.gov/ontologies/bflc/",
"http://dbpedia.org/ontology/",
"http://www.loc.gov/mads/rdf/v1#",
"http://rdaregistry.info/Elements/m/datatype/",
"http://rdaregistry.info/Elements/e/",
"http://rdaregistry.info/Elements/i/",
"http://rdaregistry.info/Elements/m/",
"http://rdaregistry.info/Elements/u/",
"http://rdaregistry.info/Elements/w/",
"https://doi.org/10.6069/uwlib.55.d.4#",
"http://sinopia.io/vocabulary/"
]

new_prefix_list = [
"bf",
"bflc",
"dbo",
"madsrdf",
"rdam",
"rdae",
"rdai",
"rdam",
"rdau",
"rdaw",
"rdax",
"sin"
]

def find_and_replace(entity, file, find, replace):
    open_file = open(f"data/2020_7_28/{entity}/{file}", "rt")
    file_replacement = open_file.read()
    file_replacement = file_replacement.replace(find, replace)
    open_file.close()
    open_file = open(f"data/2020_7_28/{entity}/{file}", "wt")
    open_file.write(file_replacement)
    open_file.close()

for work in workList:
    for prefix in prefix_list:
        i = 0
        while i <= 11:
            with open(f"data/2020_7_28/work/{work}") as f:
                if f'xmlns:{prefix}="{namespace_list[i]}"' in f.read():
                    old_namespace = f'xmlns:{prefix}="{namespace_list[i]}"'
                    new_namespace = f'xmlns:{new_prefix_list[i]}="{namespace_list[i]}"'
                    find_and_replace("work", work, old_namespace, new_namespace)
                    find_and_replace("work", work, f"<{prefix}:", f"<{new_prefix_list[i]}:")
                    i = 12
                else:
                    i = i + 1

for expression in expressionList:
    for prefix in prefix_list:
        i = 0
        while i <= 11:
            with open(f"data/2020_7_28/expression/{expression}") as f:
                if f'xmlns:{prefix}="{namespace_list[i]}"' in f.read():
                    old_namespace = f'xmlns:{prefix}="{namespace_list[i]}"'
                    new_namespace = f'xmlns:{new_prefix_list[i]}="{namespace_list[i]}"'
                    find_and_replace("expression", expression, old_namespace, new_namespace)
                    find_and_replace("expression", expression, f"<{prefix}:", f"<{new_prefix_list[i]}:")
                    i = 12
                else:
                    i = i + 1

for manifestation in manifestationList:
    for prefix in prefix_list:
        i = 0
        while i <= 11:
            with open(f"data/2020_7_28/manifestation/{manifestation}") as f:
                if f'xmlns:{prefix}="{namespace_list[i]}"' in f.read():
                    old_namespace = f'xmlns:{prefix}="{namespace_list[i]}"'
                    new_namespace = f'xmlns:{new_prefix_list[i]}="{namespace_list[i]}"'
                    find_and_replace("manifestation", manifestation, old_namespace, new_namespace)
                    find_and_replace("manifestation", manifestation, f"<{prefix}:", f"<{new_prefix_list[i]}:")
                    i = 12
                else:
                    i = i + 1

for item in itemList:
    for prefix in prefix_list:
        i = 0
        while i <= 11:
            with open(f"data/2020_7_28/item/{item}") as f:
                if f'xmlns:{prefix}="{namespace_list[i]}"' in f.read():
                    old_namespace = f'xmlns:{prefix}="{namespace_list[i]}"'
                    new_namespace = f'xmlns:{new_prefix_list[i]}="{namespace_list[i]}"'
                    find_and_replace("item", item, old_namespace, new_namespace)
                    find_and_replace("item", item, f"<{prefix}:", f"<{new_prefix_list[i]}:")
                    i = 12
                else:
                    i = i + 1