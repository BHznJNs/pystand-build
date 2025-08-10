import unittest
import os
import shutil
import tempfile
import sys
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))
from copy_files import process_input, main

class TestCopyFiles(unittest.TestCase):

    def setUp(self):
        # 创建一个临时目录作为测试环境
        self.test_dir = tempfile.mkdtemp()
        self.build_dir = os.path.join(self.test_dir, 'build')
        os.makedirs(self.build_dir)
        self.source_dir = os.path.join(self.test_dir, 'source')
        os.makedirs(self.source_dir)

        # 创建一些测试文件和目录
        self.test_file1 = os.path.join(self.source_dir, 'file1.txt')
        self.test_file2 = os.path.join(self.source_dir, 'file2.py')
        self.test_subdir = os.path.join(self.source_dir, 'subdir')
        os.makedirs(self.test_subdir)
        self.test_subfile = os.path.join(self.test_subdir, 'subfile.txt')

        with open(self.test_file1, 'w') as f:
            f.write('This is file1.')
        with open(self.test_file2, 'w') as f:
            f.write('print("This is file2.")')
        with open(self.test_subfile, 'w') as f:
            f.write('This is a subfile.')

    def tearDown(self):
        # 清理临时目录
        shutil.rmtree(self.test_dir)

    def test_process_input_empty(self):
        self.assertEqual(process_input(''), [])

    def test_process_input_single_line(self):
        self.assertEqual(process_input('file.txt'), ['file.txt'])

    def test_process_input_multiple_lines(self):
        input_str = 'file1.txt\nfile2.py\n  spaced_file.txt  \n\n'
        expected = ['file1.txt', 'file2.py', 'spaced_file.txt']
        self.assertEqual(process_input(input_str), expected)

    @patch('sys.exit')
    @patch('builtins.print')
    def test_main_missing_env_var(self, mock_print, mock_exit):
        mock_exit.side_effect = SystemExit(1)
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 1)
            mock_exit.assert_called_once_with(1)
            mock_print.assert_called() # Check that print was called

    @patch('builtins.print')
    def test_main_copy_operations(self, mock_print):
        with patch.dict(os.environ, {
            'BUILD_PATH': self.build_dir,
            'INCLUDED_FILES': f'{self.test_file1}\n{self.test_subdir}\nnon_existent_file.txt',
            'PYSTAND_ENTRY_FILE': self.test_file2,
            'APPLICATION_NAME': 'my_app'
        }):
            # 确保在测试前 build_dir 是空的
            for item in os.listdir(self.build_dir):
                shutil.rmtree(os.path.join(self.build_dir, item)) if os.path.isdir(os.path.join(self.build_dir, item)) else os.remove(os.path.join(self.build_dir, item))

            main()

            # 检查文件和目录是否被复制
            self.assertTrue(os.path.exists(os.path.join(self.build_dir, 'file1.txt')))
            self.assertTrue(os.path.isdir(os.path.join(self.build_dir, 'subdir')))
            self.assertTrue(os.path.exists(os.path.join(self.build_dir, 'subdir', 'subfile.txt')))
            self.assertTrue(os.path.exists(os.path.join(self.build_dir, 'my_app.py')))

            # 检查警告信息
            print_args_list = [call_args[0][0] for call_args in mock_print.call_args_list]
            self.assertTrue(any("Item does not exist, skipped." in args for args in print_args_list))
            self.assertTrue(any("non_existent_file.txt" in args for args in print_args_list))

    @patch('builtins.print')
    def test_main_only_entry_file(self, mock_print):
        with patch.dict(os.environ, {
            'BUILD_PATH': self.build_dir,
            'INCLUDED_FILES': '',
            'PYSTAND_ENTRY_FILE': self.test_file1,
            'APPLICATION_NAME': 'app_with_no_includes'
        }):
            # 确保在测试前 build_dir 是空的
            for item in os.listdir(self.build_dir):
                shutil.rmtree(os.path.join(self.build_dir, item)) if os.path.isdir(os.path.join(self.build_dir, item)) else os.remove(os.path.join(self.build_dir, item))

            main()
            self.assertTrue(os.path.exists(os.path.join(self.build_dir, 'app_with_no_includes.py')))
            self.assertFalse(os.path.exists(os.path.join(self.build_dir, 'file1.txt')))


if __name__ == '__main__':
    unittest.main()
