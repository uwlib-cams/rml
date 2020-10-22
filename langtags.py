import os
from datetime import date
#from sys import argv

#script, data_directory = argv

today = date.today()
currentDate = str(today).replace('-', '_')

work_1List = [] # os.listdir(f'output/{currentDate}/work_1')
work_2List = [] # os.listdir(f'output/{currentDate}/work_2')
instanceList = os.listdir(f'output/{currentDate}/instance')
itemList = [] # os.listdir(f'output/{currentDate}/item')

lang_tag_fix_list = [
("@ara", "@ar"), # arabic
("@bur", "@my"), # burmese/myanmar
("@chi", "@zh"), # chinese
("@deu", "@de"), # german
("@eng", "@en"), # english
("@fra", "@fr"), # french
("@heb", "@he"), # hebrew
("@jpn", "@ja"), # japanese
("@kor", "@ko"), # korean
("@mac", "@mk"), # macedonian
("@rus", "@ru"), # russian
("@spa", "@es"), # spanish
("@srp", "@sr"), # serbian
("@ukr", "@uk"), # ukrainian
("@zxx", "") # no linguistic content
]

def find_and_replace(entity, file, find_replace):
    """Find instances of an incorrect language tag, replace with correct language tag"""
    open_file = open(f"output/{currentDate}/{entity}/{file}", "rt")
    file_replacement = open_file.read()
    file_replacement = file_replacement.replace(f"{find_replace[0]}", f"{find_replace[1]}")
    open_file.close()
    open_file = open(f"output/{currentDate}/{entity}/{file}", "wt")
    open_file.write(file_replacement)
    open_file.close()

for work in work_1List:
    for langtag in lang_tag_fix_list:
        find_and_replace("work_1", work, langtag)

for work in work_2List:
    for langtag in lang_tag_fix_list:
        find_and_replace("work_2", work, langtag)

for instance in instanceList:
    for langtag in lang_tag_fix_list:
        find_and_replace("instance", instance, langtag)

for item in itemList:
    for langtag in lang_tag_fix_list:
        find_and_replace("item", item, langtag)
