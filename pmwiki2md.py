#!/usr/bin/env python3
#-*-coding: utf-8 -*-

#=======================================================================================
# Imports
#=======================================================================================

# Python
from collections import UserList, namedtuple
import copy, os

# Debugging
import time
from lib.debugging import dprint, cdprint

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
	
	def __init__(self, initialData=None):
		#dprint("initialData type: ", type(initialData))
		if initialData is None:
			# NOTE: This is a hackaround for an unhandled bug.
			#
			# If the parameter for initial data is configured as initialData=[],
			# it somehow ends up taking self.data from another instance of the
			# class. There's something I'm missing, and this works around it
			# for now. It's not graceful, but I won't stall progress on the
			# project any longer for a wild goose chase. Perhaps another time.
			#
			# If there is any further weirdness of the sort, this is probably
			# a good starting point.
			#dprint("initialData is None: ", initialData)
			self.data = []
		elif type(initialData) is list:
			#dprint("initialData is list: ", initialData)
			self.data = initialData
		elif type(initialData) is UserList:
			#dprint("initialData is UserList: ", initialData)
			self.data = initialData.data
		else:
			#dprint("initialData is something else: ", initialData)
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
		#dprint("will see initial data messages:")
		new = self.__class__()
		#dprint("End of initial data messages.")
		#dprint("my data id:\t\t", id(self.data))
		#dprint("new data id:\t\t", id(new.data))
		#dprint("my id:\t\t", id(self))
		#dprint("new id:\t\t", id(new))
		#dprint("self, self.data, new, class, class: \n", self, "\n", self.data, "\n", new, "\n", Content(), "\n", Content())

		#i = 0
		for element in self.data:
			new.append(element)
			#print(self.data)
			#i += 1
			#if i == 10:
			#	#raise Exception("INFINITE LOOP")
			#	time.sleep(100000000)
		
		#[dprint("Copying forever?"+str(new.append(element))) for element in self.data]
		#dprint("REMOVE ABOVE LINE AND UNCOMMENT LINE BELOW.")
		#[new.append(element) for element in self.data]
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
	
	def convert(self, content):
		pass#Override

class ConversionBySingleCodeReplacement(Conversion):
	
	def __init__(self):
		self.old = self.__class__.OLD
		self.new = self.__class__.NEW
	
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
		#dprint("Content before copying: ", content)
		#dprint("Content class comparison in super().convert before copy: ", Content(), Content())
		#dprint("content object id before copy: ", id(content))
		alteredContent = content.copy()
		#dprint("content alteredContent, content ids after copy: ", id(alteredContent), id(content))
		#dprint("Content class comparison in super().convert after copy: ", Content(), Content())
		for element in content:
			if element.availableForConversion:
				subElements = self.getSubElements(element)
				convertedSubElements = self.interleaveWithConvertedIndicators(subElements)
				alteredContent.replaceElement(element, convertedSubElements)
		return alteredContent

class ListConversion(ConversionBySingleCodeReplacement):

	def convert(self, content):
		
		"""Convert nested lists from PmWiki to Markdown.
		The class attribute OLD just takes the basic indication character
		used to indicate a certain type of PmWiki list.
		The class attribute NEW works the same, but for the markdown
		counterpart."""
		# Technically, this first takes the OLD and NEW indicators
		# as they were specified as class attributes and then
		# assembles the actual, final indicators that will be used
		# for conversion by the base class.
		
		# Indent the markdown list indicator by two spaces per list level.
		level = 1
		contentBeforeConversion = content
		while True:
			indentedNew = "".join(["  " for level in range(0, level)]+[self.new])
			theNewOld = os.linesep+self.old+" "
			theNewNew = os.linesep+indentedNew+" "
			
			# We spoof what we need to for our parent class to be none the wiser.
			self.old = theNewOld
			self.new = theNewNew
			
			# Our parent class can take over.
			#dprint("content before super()", convertedContent)
			#dprint("Content class comparison before super(): ", Content(), Content())
			convertedContent = super().convert(contentBeforeConversion)
			#dprint("content after super()", convertedContent)
			#dprint("Content class comparison after super(): ", Content(), Content())
			#cdprint(contentBeforeConversion)
			#cdprint(convertedContent)
			# There might be a better way to determine that
			# there are no lists of any greater levels anymore.
			# Right now, we're just looking at whether there
			# was anything to convert during the last pass.
			if len(convertedContent) == len(contentBeforeConversion):
				break
			contentBeforeConversion = convertedContent
		return convertedContent

class Conversions(UserList):
	
	def __init__(self, *conversions):
		self.data = conversions
		
#==========================================================
# Conversions
#==========================================================

class Pmwiki2MdItalicConversion(ConversionBySingleCodeReplacement):
	OLD = "''"
	NEW = "_"
class Pmwiki2MdBoldConversion(ConversionBySingleCodeReplacement):
	OLD = "'''"
	NEW = "__"
class Pmwiki2MdItalicBoldConversion(ConversionBySingleCodeReplacement):
	OLD = "'''''"
	NEW = "**_"
class Pmwiki2MdTitle1Conversion(ConversionBySingleCodeReplacement):
	OLD = "\n! "
	NEW = "\n# "
class Pmwiki2MdTitle2Conversion(ConversionBySingleCodeReplacement):
	OLD = "\n!! "
	NEW = "\n## "
class Pmwiki2MdTitle3Conversion(ConversionBySingleCodeReplacement):
	OLD = "\n!!! "
	NEW = "\n### "

class Pmwiki2MdBulletListConversion(ListConversion):
	OLD = "*"
	NEW = "-"

#class Pmwiki2MdListConversion(ConversionBySingleCodeReplacement):
	#OLD = "*"
	#NEW = "-"
	#def convert(self, content):
		
		#"""Convert nested lists from PmWiki to Markdown.
		#The class attribute OLD just takes the basic indication character
		#used to indicate a certain type of PmWiki list.
		#The class attribute NEW works the same, but for the markdown
		#counterpart."""
		## Technically, this first takes the OLD and NEW indicators
		## as they were specified as class attributes and then
		## assembles the actual, final indicators that will be used
		## for conversion by the base class.
		
		## Indent the markdown list indicator by two spaces per list level.
		#level = 1
		#while True:
			
			#indentedNew = "".join(["  " for level in range(0, level)]+[self.new])
			#theNewOld = os.linesep+self.old+" "
			#theNewNew = os.linesep+indentedNew+" "
			
			## Now, we spoof what we need to for our parent class to be none the wiser.
			#self.old = theNewOld
			#self.new = theNewNew
			
			## Now, our parent class can take over.
			#convertedContent = super().convert(content)
			
			## There might be a better way to determine that
			## there are no lists of any greater levels anymore.
			## Right now, we're just looking at whether there
			## was anything to convert during the last pass.
			#if len(convertedContent) == len(content):
				#break
		#return convertedContent

class Pmwiki2MdDoubleNewlineConversion(ConversionBySingleCodeReplacement):
	OLD = "\\"
	NEW = "\n\n"
class Pmwiki2MdCodeBlockConversion(Conversion):
	def convert(self):
		pass#TODO
class Pmwiki2MdLinkConversion(Conversion):
	def convert(self):
		pass#TODO
