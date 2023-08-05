import json
import os

def get_fields_string(fields, name):
    field_string = " "*4 + "struct {\n"
    for field in fields:
        field_words = field.split()
        field_words.pop(0)
        field_string += " "*8 + " ".join(field_words) + ";\n"
    
    field_string += " "*4 + "} " + name + "_t;\n"
    return field_string


class DescParser:

    node_name = ''
    interfaces = []
    types = []
    ports = []

    def __init__(self, path):
        file_name = os.path.basename(path)
        self.node_name = os.path.splitext(file_name)[0]

        with open(path) as file_desc:
            desc = json.load(file_desc)
            self.interfaces = desc.get("interfaces")
            self.types = desc.get("types")
            self.ports = desc.get("ports")


    def generate_fields(self):
        if type(self.interfaces) != list:
            return ""

        fields_string = "typedef struct {\n"
        for interface in self.interfaces:
            name = interface.get("name")
            fields = interface.get("fields")
            if type(name) != str or type(fields) != list:
                continue

            fields_string += get_fields_string(fields, name)

        fields_string += "} " + self.node_name + "_fields_t;\n"
        return fields_string
