import os
from desc_parser import DescParser

a = DescParser("codegen/test.json")
print(a.generate_fields())

    