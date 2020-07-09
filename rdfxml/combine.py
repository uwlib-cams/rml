import os

print("Transforming RDA Work to BF Work...\n")
os.system('java -jar mapper.jar -m ~/rml/rdfxml/maps/workMonographMap.xml.nq -s turtle -o tempWork.nq')

print("Transforming RDA Expression to BF Work...\n")
os.system('java -jar mapper.jar -m ~/rml/rdfxml/maps/expressionMonographMap.xml.nq -s turtle -o tempExpression.nq')

print("Transforming RDA Manifestation to BF Instance...\n")
os.system('java -jar mapper.jar -m ~/rml/rdfxml/maps/manifestationMonographMap.xml.nq -s turtle -o tempManifestation.nq')

print("Transforming RDA Item to BF Item...\n")
os.system('java -jar mapper.jar -m ~/rml/rdfxml/maps/itemMonographMap.xml.nq -s turtle -o tempItem.nq')

print("Transformation complete.\n")

print("Creating complete record...\n")
os.system('touch fullRecord.nq')
os.system('cat tempWork.nq tempExpression.nq tempManifestation.nq tempItem.nq > fullRecord.nq')

print("Full record created.\n")

print("Reserializing...")
os.system('rdf2rdf -in=fullRecord.nq -out=fullRecord.ttl')
# os.system('rapper -i turtle -o ntriples fullRecord.nq > fullRecord.nt')
# os.system('rapper -i ntriples -o turtle fullRecord.nt > ~/rml/rdfxml/output/fullRecord.nq')
# os.system('rm fullRecord.nq fullRecord.nt')

print("Remove individual transformed WEMI files? (y/n)")

response = input("> ")

while True:
    if response == "y":
        os.system('rm tempWork.nq')
        os.system('rm tempExpression.nq')
        os.system('rm tempManifestation.nq')
        os.system('rm tempItem.nq')
        print("Files removed.")
        print("Transformation complete.")
        break

    elif response == "n":
        print("Transformation complete.")
        break

    else:
        print("Input not recognized.")
