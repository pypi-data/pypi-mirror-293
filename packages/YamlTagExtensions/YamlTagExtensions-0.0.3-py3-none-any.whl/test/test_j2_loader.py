import unittest

from YamlTagExtensions.file_loader import FileLoader
from YamlTagExtensions.j2_loader import Jinja2Loader


class TestJ2Loader(unittest.TestCase):
    template_path = 'resources/j2_loader/template.j2'
    params = {"message": "YTE - Yaml Tag Extensions", "list_data": ['a', 'b', 'c']}

    def test_constructor(self):
        j2_loader = Jinja2Loader(
            path=self.template_path,
            params=self.params
        )
        self.assertEqual(j2_loader.path, self.template_path)
        self.assertEqual(j2_loader.params, self.params)

    def test_j2_render(self):
        j2_rendered = Jinja2Loader(
            path=self.template_path,
            params=self.params
        ).render()
        expected_render = {'greeting': {'message': 'YTE - Yaml Tag Extensions'}, 'list_data': ['a', 'b', 'c']}
        self.assertEqual(j2_rendered, expected_render)


if __name__ == '__main__':
    unittest.main()
