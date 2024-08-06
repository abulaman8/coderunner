import unittest
from unittest.mock import patch
import io
import sys

# Assuming the function in temp.py is called process_input and we import it here
from temp import process_input


class TestTemp(unittest.TestCase):

    @patch('builtins.input', side_effect=['Hello'])
    def test_case_1(self, mock_input):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        process_input()
        sys.stdout = sys.__stdout__
        expected_output = "HELLO\nhello\nHello\n"
        self.assertEqual(captured_output.getvalue(), expected_output)

    @patch('builtins.input', side_effect=['WORLD'])
    def test_case_2(self, mock_input):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        process_input()
        sys.stdout = sys.__stdout__
        expected_output = "WORLD\nworld\nWORLD\n"
        self.assertEqual(captured_output.getvalue(), expected_output)

    @patch('builtins.input', side_effect=['Python3'])
    def test_case_3(self, mock_input):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        process_input()
        sys.stdout = sys.__stdout__
        expected_output = "PYTHON3\npython3\nPython3\n"
        self.assertEqual(captured_output.getvalue(), expected_output)

    @patch('builtins.input', side_effect=['12345'])
    def test_case_4(self, mock_input):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        process_input()
        sys.stdout = sys.__stdout__
        expected_output = "12345\n12345\n12345\n"
        self.assertEqual(captured_output.getvalue(), expected_output)

    @patch('builtins.input', side_effect=['Hello World!'])
    def test_case_5(self, mock_input):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        process_input()
        sys.stdout = sys.__stdout__
        expected_output = "HELLO WORLD!\nhello world!\nHello World!\n"
        self.assertEqual(captured_output.getvalue(), expected_output)


if __name__ == '__main__':
    unittest.main()
