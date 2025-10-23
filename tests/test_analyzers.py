import unittest
import os
from src.analyzers import detect_python_smells, detect_javascript_smells

class TestAnalyzers(unittest.TestCase):
    def test_python_analyzer_missing_file(self):
        issues = detect_python_smells("non_existent_file.py")
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]['type'], "error")
    
    def test_javascript_analyzer_missing_file(self):
        issues = detect_javascript_smells("non_existent_file.js")
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]['type'], "error")

if __name__ == '__main__':
    unittest.main()