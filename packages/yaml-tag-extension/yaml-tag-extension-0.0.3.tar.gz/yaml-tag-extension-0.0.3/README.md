# Yaml Tag Extensions

## Quick Guide

`pip install YamlTagExtensions`

## Tags supported

#### !VARIABLE

```YAML
# variables.yaml
country: Atlantis
name: Jane Doe
```

```YAML
# deployment.yaml
conn_string: my_amazing_conn_string_xxxxxxxxxxxxxx
```

Use the tag to initialize settings / variables that needs to be accessed in the yaml.

The !variable / !VARIABLE / !Variable can be invoked as follows.  
This approach requires to end the document using ---  
Use yaml.load_all feature if this approach is chosen.

```YAML
!VARIABLES
- '../test/resources/variable_loader/deployment.yaml'
- '../test/resources/variable_loader/variables.yaml'
---
person:
  name: Jane Doe
  country: !$ '.variables.country'
```

Assign a key before defining the !Variables.

Ending the document is not necessary, and yaml.load can be used.

```YAML
setup: !VARIABLES
  - '../test/resources/variable_loader/deployment.yaml'
  - '../test/resources/variable_loader/variables.yaml'
```

#### !$

Use this tag to access the !Variables set into the loader context.

To access `country` value from `variables.yaml`

```YAML
person:
  name: Jane Doe
  country: !$ '.variables.country' # .<file_name>.<attribute>
```

Also allows fetching of nested values / attributes.

Env variables can also be accessed using `!$` detected by the presence of `.env` prefix in the fetch string.

```YAML
database: !$ '.env.DATABASE_NAME' # .env.<attribute>
```

#### !FILE

Read a file and attach it as verbatim to a desired YAML location.   
The read uses smart-open pkg for type resolution.

```YAML
  my_file_contents: !FILE
    path: resources/file_loader/sample_file.txt
```

#### !TEMPLATE

Leverage the power of templating with Jinja2 + YAML.  
Create a Jinja2 template / Yaml with Jinja2 syntax's, to create reusable configurations that render a YAML dynamically.

```YAML
simple_job:
  database_name: DB
  table_name: person
  sql:
    - !TEMPLATE
      path: "resources/j2_loader/insert_into_template.j2"
      params:
        name: John Doe
        age: 30
        country: Wakanda
    - !Template
      path: "resources/j2_loader/insert_into_template.j2"
      params:
        name: !$ '.variables.name'
        age: 28
        country: !$ '.variables.country'
```

```YAML
# insert_into_template.j2
insert_into:
  name: {{ name | upper }}
  age: {{ age }}
  country: {{ country }}

```


Rendered YAML

```YAML
simple_job:
  database_name: DB
  table_name: person
  sql:
    - insert_into:
        age: 30
        country: Wakanda
        name: JOHN DOE
    - insert_into:
        age: 28
        country: Atlantis
        name: JANE DOE
```

#### Initialize and load yaml using YTE

```Python
import yaml
from YamlTagExtensions.core import yte_loader

yaml.load_all(
    open('<PATH TO THE YAML FILE>'),
    Loader=yte_loader
)
```

```Python
import yaml
from YamlTagExtensions.core import yte_loader

yaml.load(
    open('<PATH TO THE YAML FILE>'),
    Loader=yte_loader
)
```
