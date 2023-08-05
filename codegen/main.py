import os
import json
from desc_parser import DescParser

with open("codegen/test.json") as file_desc:
    desc = json.load(file_desc)
    a = DescParser(desc)
    print(a.check_fields())
    print(a.generate_fields_t())
    print(a.generate_accessors_prototypes())
    print(a.generate_accessors_weak_definitions())

    