from xmldiff import main
from lxml import etree
# from parser import parse_wms_capabilities
# from models import Layer
from django.db import transaction

xml_file_1 = '/home/lydia/Documents/python/update_db/update_app/files/fixture_1.3.0.xml'
xml_file_2 = '/home/lydia/Documents/python/update_db/update_app/files/fixture_1.3.0_modified.xml'

def compare_xml():
    # xml_file_1 = '/home/lydia/Documents/python/update_db/update_app/files/fixture_1.3.0.xml'
    # xml_file_2 = '/home/lydia/Documents/python/update_db/update_app/files/fixture_1.3.0_modified.xml'

    edit_file = main.diff_files(xml_file_1, xml_file_2)
    if edit_file:
        print("update needed")
    else:
        print("ok")

    return edit_file

diff = compare_xml()
print(diff)

"""
def compare_lxml_tree():
    tree1 = etree.parse(xml_file_1)
    tree2 = etree.parse(xml_file_2)

    edit_file = main.diff_trees(tree1, tree2)
    if edit_file:
        print("update needed")
    else:
        print("ok")

    return edit_file

tree_diff = compare_lxml_tree()
print(tree_diff)
"""
