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
		#cdprint(Conversion().convert(original))
		self.assertEqual(len(converted), len(shouldLookLike))
		for lookalike in shouldLookLike:
			self.assertEqual(converted.pop(0).content, lookalike)
			
	def compareMultiConverted(self, original, shouldLookLike, conversions):
		converted = conversions.convert(original)
		self.assertEqual(len(converted), len(shouldLookLike))
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
		
	def test_Pmwiki2MdSmallSmallConversion(self):
		from pmwiki2md import Conversions, Pmwiki2MdSmallSmallBeginConversion, Pmwiki2MdSmallSmallEndConversion
		original = Content("Cucumbers [--might--] be tomatoes.")
		shouldLookLike = ["Cucumbers ", "<sub>", "might", "</sub>", " be tomatoes."]
		conversions = Conversions(Pmwiki2MdSmallSmallBeginConversion, Pmwiki2MdSmallSmallEndConversion)
		self.compareMultiConverted(original, shouldLookLike, conversions)
	
	def test_Pmwiki2MdSmallConversion(self):
		from pmwiki2md import Conversions, Pmwiki2MdSmallBeginConversion, Pmwiki2MdSmallEndConversion
		original = Content("Cucumbers [-might-] be tomatoes.")
		shouldLookLike = ["Cucumbers ", "<sub>", "might", "</sub>", " be tomatoes."]
		conversions = Conversions(Pmwiki2MdSmallBeginConversion, Pmwiki2MdSmallEndConversion)
		self.compareMultiConverted(original, shouldLookLike, conversions)
		
	def test_Pmwiki2MdBigConversion(self):
		from pmwiki2md import Conversions, Pmwiki2MdBigBeginConversion, Pmwiki2MdBigEndConversion
		original = Content("Cucumbers [+might+] be tomatoes.")
		shouldLookLike = ["Cucumbers ", "<sup>", "might", "</sup>", " be tomatoes."]
		conversions = Conversions(Pmwiki2MdBigBeginConversion, Pmwiki2MdBigEndConversion)
		self.compareMultiConverted(original, shouldLookLike, conversions)
		
	def test_Pmwiki2MdBigBigsConversion(self):
		from pmwiki2md import Conversions, Pmwiki2MdBigBigBeginConversion, Pmwiki2MdBigBigEndConversion
		original = Content("Cucumbers [++might++] be tomatoes.")
		shouldLookLike = ["Cucumbers ", "<sup>", "might", "</sup>", " be tomatoes."]
		conversions = Conversions(Pmwiki2MdBigBigBeginConversion, Pmwiki2MdBigBigEndConversion)
		self.compareMultiConverted(original, shouldLookLike, conversions)
		
	def test_Pmwiki2MdItalicBoldConversion(self):
		from pmwiki2md import Pmwiki2MdItalicBoldConversion as Conversion
		original = Content("Cucumbers '''''might''''' be tomatoes.")
		shouldLookLike = ["Cucumbers ", "**_", "might", "**_", " be tomatoes."]
		self.compareConverted(original, shouldLookLike, Conversion)
		
	def test_Pmwiki2MdTitle1Conversion(self):
		from pmwiki2md import Pmwiki2MdTitle1Conversion as Conversion
		original = Content("\n!Cucumbers might be tomatoes.")
		shouldLookLike = ["", "\n# ", "Cucumbers might be tomatoes."]
		self.compareConverted(original, shouldLookLike, Conversion)
		
	def test_Pmwiki2MdTitle2Conversion(self):
		from pmwiki2md import Pmwiki2MdTitle2Conversion as Conversion
		original = Content("\n!!Cucumbers might be tomatoes.")
		shouldLookLike = ["", "\n## ", "Cucumbers might be tomatoes."]
		self.compareConverted(original, shouldLookLike, Conversion)
		
	def test_Pmwiki2MdTitle3Conversion(self):
		from pmwiki2md import Pmwiki2MdTitle3Conversion as Conversion
		original = Content("\n!!!Cucumbers might be tomatoes.")
		shouldLookLike = ["", "\n### ", "Cucumbers might be tomatoes."]
		self.compareConverted(original, shouldLookLike, Conversion)
		
	def test_Pmwiki2MdSubscriptConversion(self):
		from pmwiki2md import Pmwiki2MdSubscriptConversion as Conversion
		original = Content("Cucumbers '_might_' be tomatoes.")
		shouldLookLike = ["Cucumbers ", "<sub>", "might", "</sub>", " be tomatoes."]
		self.compareConverted(original, shouldLookLike, Conversion)
		
	def test_Pmwiki2MdSuperscriptConversion(self):
		from pmwiki2md import Pmwiki2MdSuperscriptConversion as Conversion
		original = Content("Cucumbers '^might^' be tomatoes.")
		shouldLookLike = ["Cucumbers ", "<sup>", "might", "</sup>", " be tomatoes."]
		self.compareConverted(original, shouldLookLike, Conversion)
		
	def test_Pmwiki2Md1LevelBulletListConversion(self):
		from pmwiki2md import Pmwiki2MdBulletListConversion as Conversion
		original = Content("\n*Cucumbers might be tomatoes.")
		shouldLookLike = ["", "\n  - ", "Cucumbers might be tomatoes."]
		self.compareConverted(original, shouldLookLike, Conversion)
		
	def test_Pmwiki2Md2LevelBulletListConversion(self):
		from pmwiki2md import Pmwiki2MdBulletListConversion as Conversion
		original = Content("\n**Cucumbers might be tomatoes.")
		shouldLookLike = ["", "\n    - ", "Cucumbers might be tomatoes."]
		self.compareConverted(original, shouldLookLike, Conversion)
		
	def test_Pmwiki2Md3LevelBulletListConversion(self):
		from pmwiki2md import Pmwiki2MdBulletListConversion as Conversion
		original = Content("\n***Cucumbers might be tomatoes.")
		shouldLookLike = ["", "\n      - ", "Cucumbers might be tomatoes."]
		self.compareConverted(original, shouldLookLike, Conversion)
		
	def test_ConversionOfBeginEndDelimitedToSomething(self):
		
		from pmwiki2md import ConversionOfBeginEndDelimitedToSomething
		
		class Conversion(ConversionOfBeginEndDelimitedToSomething):
			
			BEGIN = "[["
			END = "]]"
			
		original = Content("[[a]] [[b]]")
		shouldLookLike = ["[[", "a", "]]", " ", "[[", "b", "]]"]
		self.compareConverted(original, shouldLookLike, Conversion)
		
	def test_Pmwiki2MdNamelessLinkPointyBracketsConversion(self):
		from pmwiki2md import Pmwiki2MdLinkConversion as Conversion
		original = Content("[[http://example.com]]")
		shouldLookLike = ["<", "http://example.com", ">"]
		self.compareConverted(original, shouldLookLike, Conversion)
		
	def test_Pmwiki2MdNamedLinkConversion(self):
		from pmwiki2md import Pmwiki2MdLinkConversion as Conversion
		original = Content("[[http://example.com | Example]]")
		shouldLookLike = ["[", "Example", "]", "(", "http://example.com", ")"]
		cdprint(Conversion().convert(original))
		self.compareConverted(original, shouldLookLike, Conversion)
		
	def test_Pmwiki2MdImageConversion(self):
		from pmwiki2md import Pmwiki2MdImageConversion as Conversion
		original = Content("[[http://example.com/example.png]]")
		shouldLookLike = ["![", "Example", "]", "(", "http://example.com/example.png", ")"]
		cdprint(Conversion().convert(original))
		self.compareConverted(original, shouldLookLike, Conversion)
		
	def test_ConversionByIterativeSingleCodeReplacementAtBeginOfLine_highestLevel(self):
		from pmwiki2md import ConversionByIterativeSingleCodeReplacementAtBeginOfLine
		class __Test(ConversionByIterativeSingleCodeReplacementAtBeginOfLine):
			OLD = "*"
			NEW = "-"
		toBeCounted = Content("\n*X\n**XXXX\n*\n*******XXX\n**XXXXXXXX\n****XX")
		countShouldBe = 7
		count = __Test().highestLevel(toBeCounted)
		self.assertEqual(count, countShouldBe)
		
	def test_Pmwiki2MdPreFormattedInlineConversion(self):
		from pmwiki2md import Pmwiki2MdPreFormattedInlineConversion as Conversion
		original = Content("[@Cucumbers *might* be tomatoes.@]")
		shouldLookLike = ["`", "Cucumbers *might* be tomatoes.", "`"]
		cdprint(Conversion().convert(original))
		self.compareConverted(original, shouldLookLike, Conversion)
		
	def test_UrlValid(self):
		from pmwiki2md import Url
		#NOTE: Libraries used in implementation might
		# filter out example.com (not sure, just be wary).
		validUrl = "https://example.com/example.png"
		invalidUrl = "cucumbers"
		self.assertTrue(Url(validUrl).valid)
		self.assertFalse(Url(invalidUrl).valid)
		
	def test_UrlLooksLikeImageUrl(self):
		from pmwiki2md import Url
		validUrl = "https://example.com/example.png"
		invalidUrl = "https://example.com/example.html"
		self.assertTrue(Url(validUrl).looksLikeImageUrl)
		self.assertFalse(Url(invalidUrl).looksLikeImageUrl)
		
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
