#=======================================================================================
# Imports
#=======================================================================================

# Python
import unittest

# Local

# DEBUG
from lib.debugging import dprint, cdprint
import time

#=======================================================================================
# Tests
#=======================================================================================

from pmwiki2md import Content, Conversions
class ConversionTests(unittest.TestCase):
	
	def compareConverted(self, original, shouldLookLike, conversion):
		"""Converts and compares the result to what it should look like."""
		converted = conversion().convert(original)
		for lookalike in shouldLookLike:
			self.assertEqual(converted.pop(0).content, lookalike)
	
	#def test_Pmwiki2MdItalicConversion(self):
		#from pmwiki2md import Pmwiki2MdItalicConversion as conversion
		#original = Content("Cucumbers ''might'' be tomatoes.")
		#shouldLookLike = ["Cucumbers ", "_", "might", "_", " be tomatoes."]
		#self.compareConverted(original, shouldLookLike, conversion)
	
	#def test_Pmwiki2MdBoldConversion(self):
		#from pmwiki2md import Pmwiki2MdBoldConversion as conversion
		#original = Content("Cucumbers '''might''' be tomatoes.")
		#shouldLookLike = ["Cucumbers ", "__", "might", "__", " be tomatoes."]
		#self.compareConverted(original, shouldLookLike, conversion)
		
	#def test_Pmwiki2MdItalicBoldConversion(self):
		#from pmwiki2md import Pmwiki2MdItalicBoldConversion as conversion
		#original = Content("Cucumbers '''''might''''' be tomatoes.")
		#shouldLookLike = ["Cucumbers ", "**_", "might", "**_", " be tomatoes."]
		#self.compareConverted(original, shouldLookLike, conversion)
	
	#def test_Pmwiki2MdTitle1Conversion(self):
		#from pmwiki2md import Pmwiki2MdTitle1Conversion as conversion
		#original = Content("\n! Cucumbers might be tomatoes.")
		#shouldLookLike = ["", "\n# ", "Cucumbers might be tomatoes."]
		#self.compareConverted(original, shouldLookLike, conversion)

	#def test_Pmwiki2Md1LevelBulletListConversion(self):
		#from pmwiki2md import Pmwiki2MdBulletListConversion as conversion
		#original = Content("\n* Cucumbers might be tomatoes.")
		#shouldLookLike = ["", "\n* ", "Cucumbers might be tomatoes."]
		#self.compareConverted(original, shouldLookLike, conversion)
		
	def test_Content(self):
		print("")
		from pmwiki2md import Content
		content1 = Content()
		content1.append("a")
		content1Copy = content1.copy()
		content2 = Content()
		self.assertEqual(content1, [])
		self.assertEqual(content2, [])

#=======================================================================================
	
if __name__ == "__main__":
	unittest.main()
