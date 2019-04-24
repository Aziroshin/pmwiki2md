#=======================================================================================
# Imports
#=======================================================================================

# Python
import unittest

# Local

# DEBUG
from lib.debugging import dprint
import time

#=======================================================================================
# Tests
#=======================================================================================

from pmwiki2md import Content, Pmwiki2MdItalicConversion, Conversions
class ConversionTests(unittest.TestCase):
	
	def test_Pmwiki2MdItalicConversion(self):
		content = Content("Cucumbers ''might'' be tomatoes if they were not already cucumbers.")
		conversions = Conversions(Pmwiki2MdItalicConversion)
		converted = Pmwiki2MdItalicConversion().convert(content)
		self.assertEqual(content[0].content, "Cucumbers *might* be tomatoes if they were not already cucumbers.")

#=======================================================================================
	
if __name__ == "__main__":
	unittest.main()
