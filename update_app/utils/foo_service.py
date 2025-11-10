# for TESTING only

from eulxml import xmlmap

class Foo(xmlmap.XmlObject):
    first_baz = xmlmap.IntegerField('bar[1]/baz')
    second_baz = xmlmap.StringField('bar[2]/baz')
    qux = xmlmap.StringListField('qux')


def parse_foo():
    print("Inside 'parse_foo':")
    foo_path = '/home/lydia/Documents/python/update_db/update_app/files/foo.xml'
    foo = xmlmap.load_xmlobject_from_file(foo_path, xmlclass=Foo)
    baz1 = foo.first_baz
    print(baz1)
    return baz1

parse_foo()
