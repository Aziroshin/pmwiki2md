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
	
	ContentElementPartitions = namedtuple("ContentElementPartitions", ["before", "separator", "after"])
	
	def __init__(self, content, conversions=[], availableForConversion=True):
		self.content = content
		self.conversions = conversions
		self.availableForConversion = availableForConversion
		
	def copy(self):
		"""Return a shallow copy of this object."""
		return copy.copy(self)
	
	def copyWithNewContent(self, newContent):
		"""Return a copy of this object, except with a different, specified content string."""
		copy = self.copy()
		copy.content = newContent
		return copy
		
	def getPartitioned(self, contentParts):
		
		"""Take a .partition result 3-tuple and return self.__class__ objects for each string.
		Returns:
		  - self.__class__.ContentElementPartitions 3-namedtuple, with each attribute holding
		  a self.__class__ object with the corresponding .partition result string:
		    [0]: before
			[1]: separator
			[2]: after"""
		
		contentElementParts = self.__class__.ContentElementPartitions(\
			before = self.copyWithNewContent(contentParts[0]),\
			separator = self.copyWithNewContent(contentParts[1]),\
			after = self.copyWithNewContent(contentParts[2])
		)
		
		#contentElementParts.before = self.copyWithNewContent(contentParts[0])
		#contentElementParts.separator = self.copyWithNewContent(contentParts[1])
		#contentElementParts.after = self.copyWithNewContent(contentParts[2])
		return contentElementParts
		
	def partition(self, separator):
		return self.getPartitioned(self.content.partition(separator))
	
	def rpartition(self, separator):
		return self.getPartitioned(self.content.rpartition(separator))
	

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
			self.data = []
		elif type(initialData) is list:
			self.data = initialData
		elif type(initialData) is UserList:
			self.data = initialData.data
		else:
			self.data = [ContentElement(initialData)]
	
	@property
	def string(self):
		string = ""
		for item in self.data:
			if type(item) is self.__class__:
				string = string+item.string  
			else: # Must be ContentElement
				string = string+item.content
		return string
	
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
		pass#OVERRIDE

class ElementByElementConversion(Conversion):
	
	def getSubElements(self, element):
		
		"""Breaks the element down into other elements.
		Override in sub-class to meet the specific break-down
		needs of the conversion in question.
		
		Returns the specified element unaltered if not overriden."""
		
		return element#OVERRIDE
	
	def convertSubElements(self, subElements):
		
		"""Takes elements (probably broken down by .getSubElements) and does stuff.
		Override in sub-class to determine what stuff that is.
		
		Returns the specified element list unaltered if not overriden."""
		
		return subElements#OVERRIDE
	
	def convert(self, content):
		"""Goes through each ContentElement and converts the ones marked availableForConversion."""
		alteredContent = content.copy()
		for element in content:
			if element.availableForConversion:
				subElements = self.getSubElements(element)
				convertedSubElements = self.convertSubElements(subElements)
				alteredContent.replaceElement(element, convertedSubElements)
		return alteredContent

class ConversionOfBeginEndDelimitedToSomething(ElementByElementConversion):
	
	BEGIN = None #OVERRIDE
	END = None #OVERRIDE
	
	def __init__(self):
		self.begin = self.__class__.BEGIN
		self.end = self.__class__.END
		
	def getSubElements(self, element):
		
		"""Get a list of new (sub) content elements for any .begin/.end delimited portions found in the specified element.
		
		Inspects the specified content element's content for any sub-strings that start and start
		with .begin and end with .end, then gets copies of the original element, but with the strings
		of the so identified elements, and adds them to a list in order.
		As the begin and end identifiers also get their own content element, in practice, that means
		that every successfully identified sub-string results in three content elements.
		
		Example: The return value for one content element representing the string "[[a]] [[b]]", with "[[" being
		.begin and "]]" .end, would be a list of 6 content element objects, representing the following 6 strings:
		["[[", "a", "]]", "[[", "b", "]]"]
		Note: We return a list of content element objects, not strings, so the above list isn't literally
		resembling an actual return value.
		"""
		
		subElements = []
		unprocessedElement = element
		
		while True:
			#dprint("Unprocessed:", unprocessedElement.content)
			
			# Get irrelevant part (partitionedByBegin.before) and relevant part plus
			# the part we'll process in future iterations (partitionedByBegin.after)
			partitionedByBegin = unprocessedElement.partition(self.begin)
			#dprint(partitionedByBegin)
			
			#dprint("partitionedByBegin:", ",".join([item.content for item in  partitionedByBegin]))
			
			# If partitionedByBegin.separator is empty, that means there's nothing left to process.
			if partitionedByBegin.after.content == "":
				break
			
			# Separate relevant part (our sub element) from future iteration part.
			partitionedByEnd = partitionedByBegin.after.partition(self.end)
			#dprint("partitionedByEnd:", ",".join([item.content for item in partitionedByEnd]))
			
			# Get our spaghettis in a row.
			elementBeginIndicator = partitionedByBegin.separator
			subElement = partitionedByEnd.before
			elementEndIndicator = partitionedByEnd.separator
			unprocessedElement = partitionedByEnd.after # for future iterations.
			
			# Add our newly found content elements to the list of elements we'll eventually return.
			subElements = subElements+[elementBeginIndicator, subElement, elementEndIndicator]
			
		# If subElements is still an empty list, we haven't found anything to convert.
		if not subElements:
			subElements.append(element)
		
		return subElements

class ConversionBySingleCodeReplacement(ElementByElementConversion):
	
	"""Replaces single occurrences with something else; no context, no frills.
	Sub-classes are configured by setting two class attributes:
	  - OLD (str): The occurrence to be replaced.
	  - NEW (str): What to replace it with."""
	
	OLD = None
	NEW = None
	
	def __init__(self):
		self.old = self.__class__.OLD
		self.new = self.__class__.NEW
	
	def interleaveWithConvertedIndicators(self, subElements):
		"""Interleaves the list of content elements with ones representing NEW.
		This is based on the assumption that said list came to be by splitting
		a content element by OLD.
		Assumption example: """
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
	
	def getSubElements(self, element):
		return [ContentElement(subElement) for subElement in element.content.split(self.old)]
	
	def convertSubElements(self, subElements):
		return self.interleaveWithConvertedIndicators(subElements)

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
		
	def convert(self, content):
		contentBeingConverted = content
		for Conversion in self.data:
			contentBeingConverted = Conversion().convert(contentBeingConverted)
		return contentBeingConverted
	
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

class Pmwiki2MdLinkConversion(ConversionOfBeginEndDelimitedToSomething):
	def convert(self, content):
		pass

class AllConversions(Conversions):
	def __init__(self):
		self.data = [\
			Pmwiki2MdBoldConversion,\
			Pmwiki2MdItalicConversion
			]
