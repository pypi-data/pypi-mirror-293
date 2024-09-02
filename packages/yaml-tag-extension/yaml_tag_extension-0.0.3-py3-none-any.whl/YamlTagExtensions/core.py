import yaml

from YamlTagExtensions.file_loader import construct_file_read
from YamlTagExtensions.j2_loader import construct_template
from YamlTagExtensions.variable_loader import variable_constructor, read_variable_constructor

yte_loader = yaml.SafeLoader
yte_loader.add_constructor("!Template", construct_template)
yte_loader.add_constructor('!template', construct_template)
yte_loader.add_constructor('!TEMPLATE', construct_template)
yte_loader.add_constructor('!VARIABLES', variable_constructor)
yte_loader.add_constructor('!variables', variable_constructor)
yte_loader.add_constructor('!Variables', variable_constructor)
yte_loader.add_constructor('!$', read_variable_constructor)
yte_loader.add_constructor('!FILE', construct_file_read)
yte_loader.add_constructor('!file', construct_file_read)
yte_loader.add_constructor('!File', construct_file_read)
