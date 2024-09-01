import unittest
import os
import tempfile
import shutil

from src.directory_info_extractor.extractor import get_directory_info, _get_project_structure, _get_file_contents, _should_include, _should_exclude

class TestExtractor(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory structure for testing
        self.test_dir = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.test_dir, 'subdir1'))
        os.makedirs(os.path.join(self.test_dir, 'subdir2'))
        os.makedirs(os.path.join(self.test_dir, 'test'))
        
        with open(os.path.join(self.test_dir, 'file1.txt'), 'w') as f:
            f.write('Content of file1')
        with open(os.path.join(self.test_dir, 'subdir1', 'file2.txt'), 'w') as f:
            f.write('Content of file2')
        with open(os.path.join(self.test_dir, 'subdir2', 'file3.py'), 'w') as f:
            f.write('print("Hello, World!")')
        with open(os.path.join(self.test_dir, 'test', 'test_file.py'), 'w') as f:
            f.write('def test_function():\n    pass')

    def tearDown(self):
        # Remove the temporary directory after the test
        shutil.rmtree(self.test_dir)

    def test_get_directory_info(self):
        result = get_directory_info(self.test_dir)
        self.assertIn('Directory Name:', result)
        self.assertIn('Project Structure:', result)
        self.assertIn('File Contents:', result)
        self.assertIn('file1.txt', result)
        self.assertIn('subdir1', result)
        self.assertIn('subdir2', result)
        self.assertIn('file2.txt', result)
        self.assertIn('file3.py', result)
        self.assertIn('Content of file1', result)
        self.assertIn('Content of file2', result)
        self.assertIn('print("Hello, World!")', result)

    def test_get_directory_info_exclude_patterns(self):
        result = get_directory_info(self.test_dir, exclude_patterns=['*.py'])
        self.assertIn('file1.txt', result)
        self.assertIn('file2.txt', result)
        self.assertNotIn('file3.py', result)
        self.assertNotIn('test_file.py', result)

    def test_get_directory_info_include_patterns(self):
        result = get_directory_info(self.test_dir, include_patterns=['*.py'])
        self.assertNotIn('file1.txt', result)
        self.assertNotIn('file2.txt', result)
        self.assertIn('file3.py', result)
        self.assertIn('test_file.py', result)

    def test_get_directory_info_exclude_test_folder(self):
        result = get_directory_info(self.test_dir, exclude_patterns=['test/*', '*/test/*'])
        self.assertIn('file1.txt', result)
        self.assertIn('file2.txt', result)
        self.assertIn('file3.py', result)
        self.assertNotIn('test_file.py', result)

    def test_get_directory_info_no_project_structure(self):
        result = get_directory_info(self.test_dir, include_project_structure=False)
        self.assertNotIn('Project Structure:', result)
        self.assertIn('File Contents:', result)

    def test_get_directory_info_no_file_contents(self):
        result = get_directory_info(self.test_dir, include_file_contents=False)
        self.assertIn('Project Structure:', result)
        self.assertNotIn('File Contents:', result)

    def test_get_directory_info_non_recursive(self):
        result = get_directory_info(self.test_dir, recursive=False)
        self.assertIn('file1.txt', result)
        self.assertNotIn('file2.txt', result)
        self.assertNotIn('file3.py', result)

    def test_get_project_structure(self):
        structure = _get_project_structure(self.test_dir)
        self.assertIn('subdir1', structure)
        self.assertIn('subdir2', structure)
        self.assertIn('file1.txt', structure)
        self.assertIn('file2.txt', structure)
        self.assertIn('file3.py', structure)

    def test_get_project_structure_exclude_patterns(self):
        structure = _get_project_structure(self.test_dir, exclude_patterns=['*.py'])
        self.assertIn('file1.txt', structure)
        self.assertIn('file2.txt', structure)
        self.assertNotIn('file3.py', structure)

    def test_get_file_contents(self):
        contents = _get_file_contents(self.test_dir)
        self.assertIn('Content of file1', contents)
        self.assertIn('Content of file2', contents)
        self.assertIn('print("Hello, World!")', contents)

    def test_get_file_contents_exclude_patterns(self):
        contents = _get_file_contents(self.test_dir, exclude_patterns=['*.py'])
        self.assertIn('Content of file1', contents)
        self.assertIn('Content of file2', contents)
        self.assertNotIn('print("Hello, World!")', contents)

    def test_should_include(self):
        self.assertTrue(_should_include('file.py', ['*.py'], []))
        self.assertFalse(_should_include('file.txt', ['*.py'], []))
        self.assertFalse(_should_include('file.py', ['*.py'], ['*.py']))

    def test_should_exclude(self):
        self.assertTrue(_should_exclude('test/file.py', ['test/*']))
        self.assertFalse(_should_exclude('src/file.py', ['test/*']))

if __name__ == '__main__':
    unittest.main()