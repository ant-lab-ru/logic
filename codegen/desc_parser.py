import os
import re

field_modes = ["ro", "wo", "rw"]

base_types = [
    "uint8_t",
    "int8_t",
    "uint16_t",
    "int16_t",
    "uint32_t",
    "int32_t",
    "char",
    "float",
    "double"
]

def get_field_split(field):
    field_split = {}
    field_words = field.split()
    field_split['mode'] = field_words[0]
    field_split['type'] = field_words[1]
    field_split['name'] = field_words[2].split('[', 1)[0]
    return field_split
    

def check_field_name(name_string):
    if name_string.count('[')==1 and name_string.count(']')==1:
        left = name_string.index('[')
        right = name_string.index(']')
        if left >= right or left==0 or right!=len(name_string)-1:
            return False

        array_size = name_string[left+1:right]
        if not array_size.isdigit():
            return False
    
        name_string = name_string.split('[', 1)[0]

    for i,c in enumerate(name_string):
        if not 'a'<=c<='z' and not 'A'<=c<='Z' and not c=='_' and not '0'<=c<='9':
            return False
        if i == 0 and '0'<=c<='9':
            return False
    return True

def get_fields_string(fields, name):
    field_string = " "*4 + "struct {\n"
    for field in fields:
        field_words = field.split()
        field_string += " "*8 + " ".join(field_words[1:3]) + ";\n"
    
    field_string += " "*4 + "} " + name + "_t;\n"
    return field_string

def get_accessor_prototypes(node_name, fields, name):
    accessor_prototypes_string = "// "+name+"\n"
    for field in fields:
        field_split = get_field_split(field)
        accessor_prototypes_string += "uint8_t "+node_name+"_write_"+name+"_"+field_split.get('name')+"("+node_name+"_node_t* self);\n"
        accessor_prototypes_string += "uint8_t "+node_name+"_read_"+name+"_"+field_split.get('name')+"("+node_name+"_node_t* self);\n\n"
    return accessor_prototypes_string

def get_accessor_definitions(node_name, fields, name):
    accessor_definitions_string = "// "+name+"\n"
    for field in fields:
        field_split = get_field_split(field)
        accessor_definitions_string += "__weak uint8_t "+node_name+"_write_"+name+"_"+field_split.get('name')+"("+node_name+"_node_t* self) {return 0;}\n"
        accessor_definitions_string += "__weak uint8_t "+node_name+"_read_"+name+"_"+field_split.get('name')+"("+node_name+"_node_t* self) {return 0;}\n\n"
    return accessor_definitions_string

class DescParser:

    node_name = ''
    interfaces = []
    ports = []
    types = base_types
    modes = field_modes

    def __init__(self, desc):
        name = desc.get("name")
        self.interfaces = desc.get("interfaces")
        if type(self.interfaces) != list:
            raise ValueError('В описании нет поля "interfaces"')

        self.ports = desc.get("ports")

        if type(name) != str:
            raise ValueError('В описании нет поля "name"')
        self.node_name = name

        usr_types = desc.get("types")
        if type(usr_types) == list:
            self.types.extend(usr_types)


    def generate_fields_t(self):
        fields_string = "typedef struct {\n"
        for interface in self.interfaces:
            name = interface.get("name")
            fields = interface.get("fields")
            if type(name) != str or type(fields) != list:
                continue

            fields_string += get_fields_string(fields, name)

        fields_string += "} " + self.node_name + "_fields_t;\n"
        return fields_string
    
    def generate_accessors_prototypes(self):
        accessors_prototypes = ""
        for interface in self.interfaces:
            name = interface.get("name")
            fields = interface.get("fields")
            if type(name) != str or type(fields) != list:
                continue
            accessors_prototypes += get_accessor_prototypes(self.node_name, fields, name)
        
        return accessors_prototypes
    
    def generate_accessors_weak_definitions(self):
        accessors_definitions = ""
        for interface in self.interfaces:
            name = interface.get("name")
            fields = interface.get("fields")
            if type(name) != str or type(fields) != list:
                continue
            accessors_definitions += get_accessor_definitions(self.node_name, fields, name)
        
        return accessors_definitions
    
    def check_fields(self):
        if type(self.interfaces) != list:
            raise ValueError('В описании нет поля "interfaces"')

        for interface in self.interfaces:
            fields = interface.get("fields")
            for field in fields:
                words = field.split()
                if len(words) < 3:
                    print('Поле',words,'как минимум должно содержать режим, тип и имя')
                    return False
                if words[0] not in self.modes:
                    print('Режима '+words[0]+' нет в списке допустимых режимов', self.modes)
                    return False
                if words[1] not in self.types:
                    print('Типа "'+words[1]+'" нет в списке допустимых типов', self.types)
                    return False
                if not check_field_name(words[2]):
                    print('Некорректное имя"'+words[2]+'"')
                    return False
                if len(words) > 3:
                    if words[3] != "//":
                        print('Ожидался комментарий // вместо"' + words[3] + '"')
                        return False

        return True
