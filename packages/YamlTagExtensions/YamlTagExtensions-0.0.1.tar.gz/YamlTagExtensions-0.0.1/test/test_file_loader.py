import unittest

from YamlTagExtensions.file_loader import FileLoader


class TestFileLoader(unittest.TestCase):
    test_path = 'resources/file_loader/sample_file.txt'

    def test_constructor(self):
        self.assertEqual(FileLoader(self.test_path).path, self.test_path)

    def test_file_fetch(self):
        self.assertEqual(
            FileLoader(self.test_path).fetch(),
            '"Thi$ i$ A TE$T FiL3'
        )


if __name__ == '__main__':
    unittest.main()
