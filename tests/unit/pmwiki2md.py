#=======================================================================================
# Imports
#=======================================================================================

# Python
import unittest

# Local
from pmwiki2md import ConvertibleContent, Conversions,\
	PmwikiContentElement, MdContentElement, Pmwiki2MdItalicContentElementConversion

# DEBUG
from lib.debugging import dprint
import time

#=======================================================================================
# Tests
#=======================================================================================

from pmwiki2md import ConvertibleContent, Conversions,\
	PmwikiContentElement, MdContentElement, Pmwiki2MdItalicContentElementConversion
class ConvertItalicPmwiki2MdTest(unittest.TestCase):

	def test_convertWithSingleConversion(self):
		original = """''italic''"""
		shouldLookLikeThis = "*italic*"
		conversions = Conversions(Pmwiki2MdItalicContentElementConversion)
		converted = ConvertibleContent(original, conversions).convert()
		self.assertEqual(converted, shouldLookLikeThis)

#=======================================================================================

from pmwiki2md import Conversions, PmwikiItalicContentElement, Pmwiki2MdItalicContentElementConversion
class ConversionsTest(unittest.TestCase):
	
	def test_byFrom(self):
		conversions = Conversions(Pmwiki2MdItalicContentElementConversion)
		self.assertEqual(conversions.byFrom[PmwikiItalicContentElement], Pmwiki2MdItalicContentElementConversion)
		
	def test_hasFrom(self):
		conversions = Conversions(Pmwiki2MdItalicContentElementConversion)
		self.assertEqual(conversions.hasFrom(PmwikiItalicContentElement), True)

from pmwiki2md import Conversions, ConvertibleContent, PmwikiItalicContentElement
class ConvertibleContentTest(unittest.TestCase):
	
	def test_nextConvertibleElementIndex(self):
		content = "Cucumbers ''might'' be tomatoes if they were not already cucumbers."
		conversions = Conversions(Pmwiki2MdItalicContentElementConversion)
		convertibleContent = ConvertibleContent(content=content, conversions=conversions)
		self.assertEqual(convertibleContent.nextConvertibleElement.index, 10)
		
	def test_nextConvertibleElementConversion(self):
		content = "Cucumbers ''might'' be tomatoes if they were not already cucumbers."
		conversions = Conversions(Pmwiki2MdItalicContentElementConversion)
		convertibleContent = ConvertibleContent(content=content, conversions=conversions)
		self.assertEqual(convertibleContent.nextConvertibleElement.conversion, Pmwiki2MdItalicContentElementConversion)

#=======================================================================================
	
if __name__ == "__main__":
	unittest.main()
