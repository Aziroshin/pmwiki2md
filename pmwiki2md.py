#!/usr/bin/env python3
#-*-coding: utf-8 -*-

#=======================================================================================
# Imports
#=======================================================================================

# Python
from collections import UserList, namedtuple

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
	def __init__(self, contentToConvert):
		self.data = [ContentElement(contentToConvert)]

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
		
class ConversionBySingleCodeReplacement(Conversion):
	
	@property
	def old(self):
		return self.__class__.OLD
	
	@property
	def new(self):
		return self.__class__.NEW
	
	def convert(self, content):
		for element in content:
			if element.availableForConversion:
				element.content = element.content.replace(self.old, self.new)
				element.conversions.append(self)
		
class Conversions(UserList):
	
	def __init__(self, *conversions):
		self.data = conversions
		
#==========================================================
# Conversions
#==========================================================

class Pmwiki2MdItalicConversion(ConversionBySingleCodeReplacement):
	
	"""Conversion of italic content elements from Pm2Wiki to markdown."""
	
	OLD = "''"
	NEW = "*"
	
