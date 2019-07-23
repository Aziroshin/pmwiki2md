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
	
	def compareConverted(self, original, shouldLookLike, Conversion):
		"""Converts and compares the result to what it should look like."""
		converted = Conversion().convert(original)
		for lookalike in shouldLookLike:
			self.assertEqual(converted.pop(0).content, lookalike)
			
	def compareMultiConverted(self, original, shouldLookLike, conversions):
		converted = conversions.convert(original)
		for lookalike in shouldLookLike:
			self.assertEqual(converted.pop(0).content, lookalike)
			
	def test_Pmwiki2MdItalicConversion(self):
		from pmwiki2md import Pmwiki2MdItalicConversion as Conversion
		original = Content("Cucumbers ''might'' be tomatoes.")
		shouldLookLike = ["Cucumbers ", "_", "might", "_", " be tomatoes."]
		self.compareConverted(original, shouldLookLike, Conversion)
	
	def test_Pmwiki2MdBoldConversion(self):
		from pmwiki2md import Pmwiki2MdBoldConversion as Conversion
		original = Content("Cucumbers '''might''' be tomatoes.")
		shouldLookLike = ["Cucumbers ", "__", "might", "__", " be tomatoes."]
		self.compareConverted(original, shouldLookLike, Conversion)
		
	def test_Pmwiki2MdUnderscoreConversion(self):
		from pmwiki2md import Conversions, Pmwiki2MdUnderscoreBeginConversion, Pmwiki2MdUnderscoreEndConversion
		original = Content("Cucumbers {+might+} be tomatoes.")
		shouldLookLike = ["Cucumbers ", "''", "might", "''", " be tomatoes."]
		conversions = Conversions(Pmwiki2MdUnderscoreBeginConversion, Pmwiki2MdUnderscoreEndConversion)
		self.compareMultiConverted(original, shouldLookLike, conversions)
		
	def test_Pmwiki2MdStrikethroughConversion(self):
		from pmwiki2md import Conversions, Pmwiki2MdStrikethroughBeginConversion, Pmwiki2MdStrikethroughEndConversion
		original = Content("Cucumbers {-might-} be tomatoes.")
		shouldLookLike = ["Cucumbers ", "~~", "might", "~~", " be tomatoes."]
		conversions = Conversions(Pmwiki2MdStrikethroughBeginConversion, Pmwiki2MdStrikethroughEndConversion)
		self.compareMultiConverted(original, shouldLookLike, conversions)
		
	def test_Pmwiki2MdSmallSubscriptConversion(self):
		from pmwiki2md import Conversions, Pmwiki2MdSmallSubscriptBeginConversion, Pmwiki2MdSmallSubscriptEndConversion
		original = Content("Cucumbers [--might--] be tomatoes.")
		shouldLookLike = ["Cucumbers ", "<sub>", "might", "</sub>", " be tomatoes."]
		conversions = Conversions(Pmwiki2MdSmallSubscriptBeginConversion, Pmwiki2MdSmallSubscriptEndConversion)
		self.compareMultiConverted(original, shouldLookLike, conversions)
	
	def test_Pmwiki2MdSubscriptConversion(self):
		from pmwiki2md import Conversions, Pmwiki2MdSubscriptBeginConversion, Pmwiki2MdSubscriptEndConversion
		original = Content("Cucumbers [-might-] be tomatoes.")
		shouldLookLike = ["Cucumbers ", "<sub>", "might", "</sub>", " be tomatoes."]
		conversions = Conversions(Pmwiki2MdSubscriptBeginConversion, Pmwiki2MdSubscriptEndConversion)
		self.compareMultiConverted(original, shouldLookLike, conversions)
		
	def test_Pmwiki2MdSuperscriptConversion(self):
		from pmwiki2md import Conversions, Pmwiki2MdSuperscriptBeginConversion, Pmwiki2MdSuperscriptEndConversion
		original = Content("Cucumbers [+might+] be tomatoes.")
		shouldLookLike = ["Cucumbers ", "<sup>", "might", "</sup>", " be tomatoes."]
		conversions = Conversions(Pmwiki2MdSuperscriptBeginConversion, Pmwiki2MdSuperscriptEndConversion)
		self.compareMultiConverted(original, shouldLookLike, conversions)
		
	def test_Pmwiki2MdBigSuperscriptsConversion(self):
		from pmwiki2md import Conversions, Pmwiki2MdBigSuperscriptBeginConversion, Pmwiki2MdBigSuperscriptEndConversion
		original = Content("Cucumbers [++might++] be tomatoes.")
		shouldLookLike = ["Cucumbers ", "<sup>", "might", "</sup>", " be tomatoes."]
		conversions = Conversions(Pmwiki2MdBigSuperscriptBeginConversion, Pmwiki2MdBigSuperscriptEndConversion)
		self.compareMultiConverted(original, shouldLookLike, conversions)
		
	def test_Pmwiki2MdItalicBoldConversion(self):
		from pmwiki2md import Pmwiki2MdItalicBoldConversion as Conversion
		original = Content("Cucumbers '''''might''''' be tomatoes.")
		shouldLookLike = ["Cucumbers ", "**_", "might", "**_", " be tomatoes."]
		self.compareConverted(original, shouldLookLike, Conversion)
		
	def test_Pmwiki2MdTitle1Conversion(self):
		from pmwiki2md import Pmwiki2MdTitle1Conversion as Conversion
		original = Content("\n! Cucumbers might be tomatoes.")
		shouldLookLike = ["", "\n# ", "Cucumbers might be tomatoes."]
		self.compareConverted(original, shouldLookLike, Conversion)
		
	def test_Pmwiki2Md1LevelBulletListConversion(self):
		from pmwiki2md import Pmwiki2MdBulletListConversion as Conversion
		original = Content("\n* Cucumbers might be tomatoes.")
		shouldLookLike = ["", "\n  - ", "Cucumbers might be tomatoes."]
		self.compareConverted(original, shouldLookLike, Conversion)
		
	def test_ConversionOfBeginEndDelimitedToSomething(self):
		
		from pmwiki2md import ConversionOfBeginEndDelimitedToSomething
		
		class Conversion(ConversionOfBeginEndDelimitedToSomething):
			
			BEGIN = "[["
			END = "]]"
			
		original = Content("[[a]] [[b]]")
		shouldLookLike = ["[[", "a", "]]", " ", "[[", "b", "]]"]
		self.compareConverted(original, shouldLookLike, Conversion)
		
	def test_ContentCopy(self):
		from pmwiki2md import Content
		content1 = Content()
		content1.append("a")
		content1Copy = content1.copy()
		content2 = Content()
		self.assertEqual(content1, ["a"])
		self.assertEqual(content2, [])
		
#=======================================================================================
	
if __name__ == "__main__":
	unittest.main()
