# test: global for recursion

numbers = ['a', 'b', 'c', 'd', 'e']

layer = {}
counter = 0

def recursive_function(number):
    global counter
    counter += 1
    layer[number] = {'lft': counter}
    print("NUMBER: ", number, layer[number])
    subnumbers = [i for i in numbers if i > number]
    print("SUBNUMBERS: ", subnumbers)
    
    if subnumbers != []:
        recursive_function(subnumbers[0])
        counter += 1
        layer[number] = {'rgt': counter}
        print("NUMBER: ", number, layer[number])
    else:
        counter += 1
        layer[number] = {'rgt': counter}
        print("NUMBER: ", number, layer[number])
        return layer
        

number = numbers[0]
l = recursive_function(number)
print(l)

# Vgl. funktioniert so!!!
from lxml import etree

def hash_xml(xml_file):
    # create hash value from xml file for comparison
    with open(xml_file, 'rb') as f:
        return hash(f.read())

xml_file_path_1 = "/home/lydia/Documents/python/update_db/update_app/files/fixture_1.3.0.xml"
parsed_xml_file_1 = etree.parse(xml_file_path_1)
xml_file_1 = etree.tostring(parsed_xml_file_1)
h1 = hash_xml(xml_file_path_1)
print("HASH: ", h1)

xml_file_path_2 = "/home/lydia/Documents/python/update_db/update_app/files/fixture_1.3.0_hashtest.xml"
parsed_xml_file_2 = etree.parse(xml_file_path_2)
xml_file_2 = etree.tostring(parsed_xml_file_2)
h2 = hash_xml(xml_file_path_2)
print("HASH: ", h2)

if h1 == h2:
    print("same")
else:
    print("different")
