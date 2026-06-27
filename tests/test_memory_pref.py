import unittest
import os
import re
from backend.api.routes import ALLOWED_EXTENSIONS, MAX_FILE_SIZE
from backend.security.auth import sanitize_input

class TestSecurityAndPreferences(unittest.TestCase):
    def test_allowed_extensions(self):
        self.assertIn(".pdf", ALLOWED_EXTENSIONS)
        self.assertIn(".docx", ALLOWED_EXTENSIONS)
        self.assertNotIn(".exe", ALLOWED_EXTENSIONS)
        self.assertNotIn(".py", ALLOWED_EXTENSIONS)
        
    def test_file_size_limit(self):
        self.assertEqual(MAX_FILE_SIZE, 10 * 1024 * 1024)
        
    def test_input_sanitization(self):
        dirty_input = "<script>alert('hack')</script>Normal Strategic Plan"
        clean = sanitize_input(dirty_input)
        self.assertEqual(clean, "Normal Strategic Plan")

if __name__ == "__main__":
    unittest.main()
