import os
import json
from desc_parser import DescParser
import codegen 

path = "codegen/test.json"
print("Code generator v0.0.1")
print("Path: " + path)

with open(path) as file_desc:
    desc = json.load(file_desc)
    a = DescParser(desc)

    if a.check_fields():
        print("Check: OK")
    else:
        raise ValueError('Invalid description')

    codegen.generate_types_h("./out/", a)

    # print(a.generate_fields_t())
    # print(a.generate_accessors_prototypes())
    # print(a.generate_accessors_weak_definitions())

