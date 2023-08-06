import os
from desc_parser import DescParser

def generate_types_h(folder, parser):
    path = folder+parser.node_name+"_node_accessors.h";
    print("Generate "+path)
    prot = parser.generate_accessors_prototypes()
    with open(path, 'w') as fid:
        fid.write('#pragma once\n\n#include <stdint.h>\n\n#ifdef __cplusplus\nextern "C" {\n#endif\n\n')
        fid.write(prot)
        fid.write('#ifdef __cplusplus\n}\n#endif\n')
        fid.close()
