import unittest

from YamlTagExtensions.variable_loader import VariableLoader


class TestJ2Loader(unittest.TestCase):
    variable_files = {
        "deployment": 'resources/variable_loader/deployment.yaml',
        "variables": 'resources/variable_loader/variables.yaml'
    }

    def test_constructor(self):
        variable_loader = VariableLoader()
        self.assertTrue('env' in variable_loader.variables.keys())

    def test_var_loader_set_vars(self):
        variable_loader = VariableLoader()
        variable_loader.set_vars(
            var_files=self.variable_files
        )
        self.assertTrue('env' in variable_loader.variables.keys())
        self.assertTrue('deployment' in variable_loader.variables.keys())
        self.assertTrue('variables' in variable_loader.variables.keys())

    def test_var_loader_fetch(self):
        variable_loader = VariableLoader()
        variable_loader.set_vars(
            var_files=self.variable_files
        )
        self.assertEqual(variable_loader.fetch('.variables.country'), 'Atlantis')
        self.assertEqual(variable_loader.fetch('.variables.name'), 'Jane Doe')
        self.assertEqual(variable_loader.fetch('.deployment.conn_string'), "my_amazing_conn_string_xxxxxxxxxxxxxx")


if __name__ == '__main__':
    unittest.main()
