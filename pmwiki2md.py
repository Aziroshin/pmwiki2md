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
		
	@property
	def isEmpty(self):
		return self.content == ""
		
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
	def isEmpty(self):
		return self.content == ""
			
	@property
	def string(self):
		string = ""
		for item in self.data:
			if type(item) is self.__class__:
				string = string+item.string  
			else: # Must be ContentElement
				string = string+item.content
		return string
	
	@property
	def lines(self):
		return self.string.split("\n")
	
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
	PARTITIONED_BEGIN_END_DELIMITED_ELEMENT_CLASS = namedtuple("PartitionedBeginEndDelimitedElement", "beginIndicator element endIndicator")
	
	def __init__(self):
		self.begin = self.__class__.BEGIN
		self.end = self.__class__.END
		self.PartitionedBeginEndDelimitedElement = self.__class__.PARTITIONED_BEGIN_END_DELIMITED_ELEMENT_CLASS
		
	@property
	def beginAsContentElement(self):
		"""The BEGIN delimiter initialized as a ContentElement object."""
		return ContentElement(self.begin, availableForConversion=False)
	
	@property
	def endAsContentElement(self):
		"""The END delimiter initialized as a ContentElement object."""
		return ContentElement(self.end, availableForConversion=False)
		
	def convertDelimited(self, partitionedElement):#OVERRIDE
		"""Converts the specified self.PartitionedBeginEndDelimitedElement.
		Meant to be subclassed; Returns unaltered input by default.
		
		In most cases, this will probably be used for simple replacements
		of the begin and end delimiters."""
		
		return partitionedElement
		
	def getSubElements(self, element):
		
		"""Get a list of new (sub) content elements for any .begin/.end delimited portions found in the specified element.
		
		Inspects the specified content element's content for any sub-strings that start
		with .begin and end with .end, then gets copies of the original element, but with the strings
		of the so identified elements, and adds them to a list in order.
		As the begin and end identifiers also get their own content element, in practice, that means
		that every successfully identified sub-string results in three content elements.
		
		Internally, as far as this and any method related to further processing of this three-pieced
		element representation are concerned, the such partitioned element is represented as
		a namedtuple of the type referenced by self.PartitionedBeginEndDelimitedElement, and defined in
		the class attribute PARTITIONED_BEGIN_END_DELIMITED_ELEMENT_CLASS.
		
		Example: The return value for one content element representing the string "[[a]] [[b]]", with "[[" being
		.begin and "]]" .end, would be a list of 6 content element objects, representing the following 6 strings:
		["[[", "a", "]]", "[[", "b", "]]"]
		Note: We return a list of content element objects, not strings, so the above list isn't literally
		resembling an actual return value. In practice, every one of these strings would be 
		ContentElement objects referencing their string by the appropriate attribute.
		"""
		
		subElements = []
		unprocessed = element
		
		while True:
			
			# Get irrelevant part (partitionedByBegin.before) and relevant part plus
			# the part we'll process in future iterations (partitionedByBegin.after)
			partitionedByBegin = unprocessed.partition(self.begin)
			
			# Are we done?
			# If partitionedByBegin.after is empty, that means there's nothing left to process.
			if partitionedByBegin.after.isEmpty:
				subElements.append(unprocessed)
				break
			
			# Separate relevant part (our sub element) from future iteration part.
			partitionedByEnd = partitionedByBegin.after.partition(self.end)
			
			# Get our spaghettis in a row.
			preceding = partitionedByBegin.before
			subElement = self.PartitionedBeginEndDelimitedElement(\
				beginIndicator = self.beginAsContentElement,
				element = partitionedByEnd.before,
				endIndicator = self.endAsContentElement,
			)
			unprocessed = partitionedByEnd.after # for future iterations.
			# Add our newly found content elements to the list of elements we'll eventually return.
			if not preceding.isEmpty:
				# .partition would have returned an empty string if there was nothing
				# actually preceding our delimited element. Of course, we don't want
				# that in the result, as elements in the element tree should only
				# represent actual content, not emptyness.
				# That's why preceding only enters the element tree when not empty.
				subElements.append(preceding)
			subElements = subElements+[*self.convertDelimited(subElement)]
			
		# If subElements is still an empty list, we haven't found anything to convert.
		if not subElements:
			subElements.append(element)
		return subElements
	
class ConversionOfBeginEndDelimitedToOtherDelimiters(ConversionOfBeginEndDelimitedToSomething):
	
	TO_BEGIN = None
	TO_END = None
	
	@property
	def to_begin(self):
		return self.__class__.TO_BEGIN
	
	@property
	def to_end(self):
		return self.__class__.TO_END
	
	def convertDelimited(self, partitionedElement):
		return self.PartitionedBeginEndDelimitedElement(\
			beginIndicator = ContentElement(self.to_begin, availableForConversion=False),\
			element = partitionedElement.element,\
			endIndicator = ContentElement(self.to_end, availableForConversion=False)
			)
		
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
	
class ConversionByIterativeSingleCodeReplacementAtBeginOfLine(ConversionBySingleCodeReplacement):
	
		def oldByLevel(self, level):
			return self.__class__.OLD*level
		
		def newByLevel(self, level):
			return self.__class__.NEW*level
		
		def highestLevel(self, content):
			"""Returns the highest count of OLD indicators found in all line beginnings throughout the content."""
			maxContentLevel = 1
			for line in content.lines:
				maxLineLevel = 0
				if len(line) > 0:
					previousChar = self.old
					for char in line:
						if not char == previousChar:
							break
						maxLineLevel += 1
						previousChar = char
				if maxLineLevel > maxContentLevel:
					maxContentLevel = maxLineLevel
			return maxContentLevel
	
class ListConversion(ConversionByIterativeSingleCodeReplacementAtBeginOfLine):
	
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
		
		# 'old' and 'new' as originally specified when the conversion rules were defined
		# (e.g. as OLD and NEW class attributes). These will then get added up as the conversion
		# code descends into deeper nested list levels (e.g. "*" becomes "***" on the third level
		# of nesting).
		
		contentBeforeConversion = content
		convertedContent = None
		
		for level in range(1, self.highestLevel(content)):
			# We spoof what we need to for our parent class to be none the wiser.
			self.old = os.linesep+self.oldByLevel(level)+" "
			self.new = os.linesep+"  "*level+self.newByLevel(1)+" "
			
			# Our parent class can take over.
			print("\n")
			print("================ BEGIN ================")
			dprint("\n", "theNewOld: "+self.old.replace(" ", "S")+"\ntheNewNew: "+self.new.replace(" ", "S"))
			print("contentBeforeConversion:")
			cdprint(contentBeforeConversion)
			convertedContent = super().convert(contentBeforeConversion)
			print("convertedContent:")
			cdprint(convertedContent)
			print("================ END ================")
			print("\n")
			
			# There might be a better way to determine that
			# there are no lists of any greater levels anymore.
			# Right now, we're just looking at whether there
			# was anything to convert during the last pass.
			if not len(convertedContent) == len(contentBeforeConversion):
				contentBeforeConversion = convertedContent
			level += 1
			dprint("level", level)
		
		if not convertedContent == None:
			return convertedContent
		else:
			return contentBeforeConversion
	
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

# Emphasis
class Pmwiki2MdItalicConversion(ConversionBySingleCodeReplacement):
	OLD = "''"
	NEW = "_"
class Pmwiki2MdBoldConversion(ConversionBySingleCodeReplacement):
	OLD = "'''"
	NEW = "__"
class Pmwiki2MdItalicBoldConversion(ConversionBySingleCodeReplacement):
	OLD = "'''''"
	NEW = "**_"
class Pmwiki2MdUnderscoreBeginConversion(ConversionBySingleCodeReplacement):
	OLD = "{+"
	NEW = "''"
class Pmwiki2MdUnderscoreEndConversion(ConversionBySingleCodeReplacement):
	OLD = "+}"
	NEW = "''"

# Strikethrough
class Pmwiki2MdStrikethroughBeginConversion(ConversionBySingleCodeReplacement):
	OLD = "{-"
	NEW = "~~"
class Pmwiki2MdStrikethroughEndConversion(ConversionBySingleCodeReplacement):
	OLD = "-}"
	NEW = "~~"

# Small & Big
class Pmwiki2MdSmallSmallBeginConversion(ConversionBySingleCodeReplacement):
	OLD = "[--"
	NEW = "<sub>"
class Pmwiki2MdSmallSmallEndConversion(ConversionBySingleCodeReplacement):
	OLD = "--]"
	NEW = "</sub>"
class Pmwiki2MdSmallBeginConversion(ConversionBySingleCodeReplacement):
	OLD = "[-"
	NEW = "<sub>"
class Pmwiki2MdSmallEndConversion(ConversionBySingleCodeReplacement):
	OLD = "-]"
	NEW = "</sub>"
class Pmwiki2MdBigBeginConversion(ConversionBySingleCodeReplacement):
	OLD = "[+"
	NEW = "<sup>"
class Pmwiki2MdBigEndConversion(ConversionBySingleCodeReplacement):
	OLD = "+]"
	NEW = "</sup>"
class Pmwiki2MdBigBigBeginConversion(ConversionBySingleCodeReplacement):
	OLD = "[++"
	NEW = "<sup>"
class Pmwiki2MdBigBigEndConversion(ConversionBySingleCodeReplacement):
	OLD = "++]"
	NEW = "</sup>"

# Titles/Headers
class Pmwiki2MdTitle1Conversion(ConversionBySingleCodeReplacement):
	OLD = "\n! "
	NEW = "\n# "
class Pmwiki2MdTitle2Conversion(ConversionBySingleCodeReplacement):
	OLD = "\n!! "
	NEW = "\n## "
class Pmwiki2MdTitle3Conversion(ConversionBySingleCodeReplacement):
	OLD = "\n!!! "
	NEW = "\n### "

# Sub and Superscript
class Pmwiki2MdSubscriptConversion(ConversionOfBeginEndDelimitedToOtherDelimiters):
	BEGIN = "'_"
	END = "_'"
	TO_BEGIN = "<sub>"
	TO_END = "</sub>"
class Pmwiki2MdSuperscriptConversion(ConversionOfBeginEndDelimitedToOtherDelimiters):
	BEGIN = "'^"
	END = "^'"
	TO_BEGIN = "<sup>"
	TO_END = "</sup>"

# Lists
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
