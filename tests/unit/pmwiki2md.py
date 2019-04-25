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

from pmwiki2md import Content, Conversions
class ConversionTests(unittest.TestCase):
	
	def compareConverted(self, converted, shouldLookLike):
		for lookalike in shouldLookLike:
			self.assertEqual(converted.pop(0).content, lookalike)
	
	def test_Pmwiki2MdItalicConversion(self):
		from pmwiki2md import Pmwiki2MdItalicConversion
		original = Content("Cucumbers ''might'' be tomatoes.")
		shouldLookLike = ["Cucumbers ", "_", "might", "_", " be tomatoes."]
		conversions = Conversions(Pmwiki2MdItalicConversion)
		converted = Pmwiki2MdItalicConversion().convert(original)
		self.compareConverted(converted, shouldLookLike)

#=======================================================================================
	
if __name__ == "__main__":
	unittest.main()
