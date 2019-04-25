#!/usr/bin/env python3
#-*-coding: utf-8 -*-

#=======================================================================================
# Imports
#=======================================================================================

# Python
from collections import UserList, namedtuple
import copy

#=======================================================================================
# Named Tuples
#=======================================================================================

FoundConversionIndicator = namedtuple("FoundConversionIndicator", ["index", "conversion"])

#=======================================================================================
# Library
#=======================================================================================

class ConversionError(Exception): pass

class ConvertibleFile(object): pass
class ConvertedElement(object): pass

#==========================================================
# Content element basics
#==========================================================

class ContentSplitByIndicator(object):
	def __init__(self, content, indicator):
		self.indicator = indicator
		self.before, self.after = content.partition(indicator)[0::2]

class ContentElement(object):
	def __init__(self, content, conversions=[], availableForConversion=True):
		self.content = content
		self.conversions = conversions
		self.availableForConversion = availableForConversion

class Content(UserList):
	
	def __init__(self, initialData=[]):
		if type(initialData) == list:
			self.data = initialData
		elif type(initialData) == UserList:
			self.data = initialData.data
		else:
			self.data = [ContentElement(initialData)]
	
	def getElementIndex(self, element):
		
		"""Returns the index of the specified ContentElement object."""
		
		index = 0
		for prospectiveElement in self.data:
			if prospectiveElement == element:
				return index
			index += 1
		raise IndexError("Tried to get index of ContentElement object not in list.")
	
	def replaceElement(self, element, replacementElements):
		"""Replace the specified ContentElement object with a list of ContentElement objects."""
		index = self.getElementIndex(element)
		self.pop(index)
		for replacementElement in reversed(replacementElements):
			self.insert(index, replacementElement)
	def copy(self):
		new = self.__class__()
		[new.append(element) for element in self.data]
		return new

class ConvertibleDocument(object): 
	
	"""Tree of ConvertibleContentElements representing a convertible document."""
	
	def __init__(self, contentToConvert, conversions):
		self.content = Content(contentToConvert)
		self.conversions = conversions
		
	def convert(self):
		for conversion in self.conversions:
			self.content = conversion.convert(self.content)

class Conversion(object):
	
	def convert(self):
		pass#Override

class ConversionSubElementsprocessor(object):
	def getSubElements(self, subElements):
		pass#OVERRIDE

class ConversionLeftAdjacentSubElementsProcessor(object):
	def getSubElements(self, element):
		element.content.split(self.old)

class ConversionBySingleCodeReplacement(Conversion):
	
	@property
	def old(self):
		return self.__class__.OLD
	
	@property
	def new(self):
		return self.__class__.NEW
	
	def getSubElements(self, element):
		return [ContentElement(subElement) for subElement in element.content.split(self.old)]
	
	def interleaveWithConvertedIndicators(self, subElements):
		convertedSubElements = []
		for subElement in subElements:
			convertedSubElements.append(subElement)
			convertedSubElements.append(ContentElement(self.new, availableForConversion=False))
		# To simulate proper "".join() behaviour, cut off the excess we've likely added.
		# In case the content element in question ended with a formatting indicator, however,
		# the last sub element will be '', as a result of the the behaviour of "".split.
		if convertedSubElements[-1].content == self.new:
			convertedSubElements.pop()
		return convertedSubElements
	
	def convert(self, content):
		alteredContent = content.copy()
		for element in content:
			if element.availableForConversion:
				subElements = self.getSubElements(element)
				convertedSubElements = self.interleaveWithConvertedIndicators(subElements)
				alteredContent.replaceElement(element, convertedSubElements)
		return alteredContent

class Conversions(UserList):
	
	def __init__(self, *conversions):
		self.data = conversions
		
#==========================================================
# Conversions
#==========================================================

class Pmwiki2MdItalicConversion(ConversionBySingleCodeReplacement):
	OLD = "''"
	NEW = "_"
class Pmwiki2MdTitle1Conversion(ConversionBySingleCodeReplacement):
	OLD = "!"
	NEW = "#"
class Pmwiki2MdTitle2Conversion(ConversionBySingleCodeReplacement):
	OLD = "!!"
	NEW = "##"
class Pmwiki2MdTitle3Conversion(ConversionBySingleCodeReplacement):
	OLD = "!!!"
	NEW = "###"
class Pmwiki2MdListConversion(ConversionBySingleCodeReplacement):
	OLD = "*"
	NEW = "* "
class Pmwiki2MdList2Conversion(ConversionBySingleCodeReplacement):
	OLD = "**"
	NEW = "  * "
class Pmwiki2MdList3Conversion(ConversionBySingleCodeReplacement):
	OLD = "***"
	NEW = "    * "
class Pmwiki2MdDoubleNewlineConversion(ConversionBySingleCodeReplacement):
	OLD = "\\"
	NEW = "\n\n"
class Pmwiki2MdCodeBlockConversion(Conversion):
	def convert(self):
		pass#TODO
class Pmwiki2MdLinkConversion(Conversion):
	def convert(self):
		pass#TODO
