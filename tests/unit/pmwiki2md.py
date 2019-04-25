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
		original = Content("Cucumbers ''might'' be tomatoes.")
		shouldLookLike = ["Cucumbers ", "_", "might", "_", " be tomatoes."]
		conversions = Conversions(Pmwiki2MdItalicConversion)
		converted = Pmwiki2MdItalicConversion().convert(original)
		dprint("\n")
		dprint([c.content for c in original])
		dprint("\n")
		dprint(shouldLookLike)
		dprint("\n")
		dprint([c.content for c in converted])
		dprint("\n")
		#self.assertEqual(content[0].content, "Cucumbers _might_ be tomatoes if they were not already cucumbers.")
		for lookalike in shouldLookLike:
			self.assertEqual(converted.pop(0).content, lookalike)

#=======================================================================================
	
if __name__ == "__main__":
	unittest.main()
