import os
import unittest
from unittest import mock

import yaml

from YamlTagExtensions.core import yte_loader


class TestJ2Loader(unittest.TestCase):

    @mock.patch.dict(os.environ, {"DATABASE_NAME": "sales", "TABLE_NAME": "person"})
    def test_functionality_load(self):
        test_yaml_path = 'resources/functionality_test_load.yaml'
        rendered_str = yaml.load(
            open(test_yaml_path),
            Loader=yte_loader
        )
        expected_result = {
            'setup':
                {
                    'variables_loaded': {
                        'deployment': {
                            'conn_string': 'my_amazing_conn_string_xxxxxxxxxxxxxx'
                        },
                        'variables': {
                            'country': 'Atlantis', 'name': 'Jane Doe'}
                    }
                },
            'simple_job': {
                'conn_string': 'my_amazing_conn_string_xxxxxxxxxxxxxx', 'database_name': 'sales',
                'table_name': 'person',
                'sql': [
                    {'insert_into': {'name': 'JOHN DOE', 'age': 30, 'country': 'Wakanda'}},
                    {'insert_into': {'name': 'JANE DOE', 'age': 28, 'country': 'Atlantis'}}
                ],
                'file': '"Thi$ i$ A TE$T FiL3'
            }
        }
        self.assertEqual(rendered_str, expected_result)

    @mock.patch.dict(os.environ, {"DATABASE_NAME": "sales", "TABLE_NAME": "person"})
    def test_functionality_load_all(self):
        test_yaml_path_load_all = 'resources/functionality_test_load_all.yaml'
        rendered_str = yaml.load_all(
            open(test_yaml_path_load_all),
            Loader=yte_loader
        )
        expected_result = [
            {
                'variables_loaded': {
                    'deployment': {
                        'conn_string': 'my_amazing_conn_string_xxxxxxxxxxxxxx'
                    },
                    'variables': {
                        'country': 'Atlantis', 'name': 'Jane Doe'}
                }
            },
            {
                'simple_job': {
                    'conn_string': 'my_amazing_conn_string_xxxxxxxxxxxxxx', 'database_name': 'sales',
                    'table_name': 'person',
                    'sql': [
                        {'insert_into': {'name': 'JOHN DOE', 'age': 30, 'country': 'Wakanda'}},
                        {'insert_into': {'name': 'JANE DOE', 'age': 28, 'country': 'Atlantis'}}
                    ],
                    'file': '"Thi$ i$ A TE$T FiL3'
                }
            }
        ]

        res_acc = []
        for r in rendered_str:
            res_acc.append(r)
        self.assertEqual(res_acc, expected_result)


if __name__ == '__main__':
    unittest.main()
