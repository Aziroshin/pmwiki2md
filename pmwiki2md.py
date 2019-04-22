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

FoundConvertibleElement = namedtuple("FoundConvertibleElement", ["index", "conversion"])

#=======================================================================================
# Library
#=======================================================================================

class ConversionError(Exception): pass

class ConvertibleFile(object): pass
class ConvertedElement(object): pass

#==========================================================
# Content element basics
#==========================================================

class ConvertibleElement(object):
	
	"""Represents an element of a convertible document, such as a title or code block."""
	
	def __init__(self, content):
		self.content = content
		self._converted = None
	
	@property
	def converted(self):
		if not self._converted == None:
			return self._converted
		else:
			raise ConversionError("Attempted to retrieve converted element content before conversion.")
	
	@converted.setter
	def converted(self, convertedContent):
		self._converted = convertedContent # ?
	
	def convert(self):
		
		return self
	
	def conversion(self):
		
		"""Override this in a subclass to implement the element-specific conversion algorithm."""

class ContentElement(object):
	
	"""A single PM Wiki content element.
		Takes:
			source (string): PM Wiki source code of the element."""
	
	BEGIN = None
	END = None
	def __init__(self, source):
		self.source = source
	@property
	def BEGIN(self):
		return self.__class__.BEGIN
	@property
	def END(self):
		return self.__class__.END
	


class PmwikiContentElement(UserList, ContentElement):
	
	"""PM Wiki content parsing and object oriented representation.
	
	Also manages a list of other PmwikiContent objects representing
	parsed out blocks of the PM Wiki source code further down the markup hierarchy.
	Takes: source (string or this class): PM Wiki content source code."""
	
	def __init__(self, conversions=None, source=None):
		self.data = []
		self.conversions = conversions
		self.source = source
		self.elementType = None
		
	def parse(self):
		# Primitive; stub that will suffice for first tests.
		i = 0
		while i < len(self.source):
			for conversion in self.conversions:
				if self.source.startswith(conversion.FROM.BEGIN,0, len(conversion.FROM.BEGIN)):
					raise Exception("CONTINUE HERE")
			i+=1
		return self
	
	def sourceHasElements(self):
		
		"""Do we contain at least one more PM Wiki markup element?
		Example1: If we are the following element: "this element contains ''italic'' text.",
		this will return 'True', as there's an italic block.
		Example2: If we represent the following element: "This element doesn't contain any other elements.",
		this will return 'False', as there are simply no markup elements."""
		
		pass#TODO
		
	def convert(self, conversions):
		convertedElement = self.__class__()
		if conversions.hasFrom(self.elementType):
			convertedElement.elementType = conversions.byFrom(self.elementType)
		for originalElement in self:
			convertedElement.append(originalElement.convert(conversions))
		return convertedElement
		

class MdContentElement(ContentElement):
	
	""""""
	
	pass#TODO

class ConvertibleContent(object): 
	
	"""Tree of ConvertibleContentElements representing a convertible document."""
	
	def __init__(self, content, conversions, ongoingConversions=[]):
		self.original = content
		self.conversions = conversions
		self.ongoingConversions = ongoingConversions
		# Maybe it should be something like self.convertedElementTree = MdContentElement(self.originalElementTree)? #TODO
		# Or self.convertedElementTree.convert(MdContentElement)? #TODO
		self._converted = None
		self._nextConvertibleElement = None
		
	@property
	def converted(self):
		if not self._converted == None:
			return self._converted
		else:
			raise ConversionError("Attempted to retrieve converted content before conversion.")
		
	@property
	def nextConvertibleElement(self):
		"""Returns the index and conversion for the next convertible element.
		Goes through all conversions in order to find out which one of them matches their
		FROM in the original string with the lowest index.
		
		Returns: namedtuple("FoundConvertibleElement", ["index", "conversion"])
		
		Example: Consider the original string to look like this:
		  "Cucumbers ''might'' be tomatoes if they were %not% already cucumbers."
		  Also, we're assuming '' and % are both indicators of different formatting elements.
		  In that case, we'd return the index at which '' was found in the string, as well as
		  the conversion related to it.
		This information is only determined once and then stored to be returned on
		subsequent calls.
		"""
		if not self._nextConvertibleElement:
			FoundConvertibleElementsByIndex = {}
			for conversion in self.conversions:
				FoundConvertibleElementsByIndex[self.original.find(conversion.FROM.BEGIN)] = conversion
			nextConvertibleElementIndex = min(FoundConvertibleElementsByIndex.keys())
			nextConvertibleElementConversion = FoundConvertibleElementsByIndex[nextConvertibleElementIndex]
			self._nextConvertibleElement = FoundConvertibleElement(\
				index = nextConvertibleElementIndex,\
				conversion = nextConvertibleElementConversion)
		return self._nextConvertibleElement
		
	def assembleConvertedContent(self):
		for convertedElement in self.convertedElements:
			self._converted = "".join(self._converted, convertedElement.converted)
		
	def convert(self):
		nextConvertibleElement = self.nextConvertibleElement

class Pmwiki2MdConvertibleContent(ConvertibleContent):
	
	"""Convenience class of ConvertibleContent for Pmwiki to markdown conversions."""
	
	def __init__(self):
		super().__init__(self,\
			content,\
			conversions=[Pmwiki2MdItalicContentElementConversion],\
			OriginalContentElementClass=PmwikiContentElement,\
			ConvertedContentElementClass=MdContentElement,)

class Conversion(object):
	
	FROM = None
	TO = None
	
	@property
	def FROM(self):
		return self.__class__.FROM
	
	@property
	def TO(self):
		return self.__class__.TO
		
class Conversions(UserList):
	def __init__(self, *conversions):
		self.data = conversions
		self.byFrom = {OriginalElementClass.FROM: OriginalElementClass for OriginalElementClass in conversions}
	
	def hasFrom(self, OriginalElementClass):
		return OriginalElementClass in self.byFrom.keys()
		
#==========================================================
# Content Elements (Pm Wiki)
#==========================================================

class PmwikiItalicContentElement(PmwikiContentElement):
	
	"""Recognizes and parses italic elements."""
	
	BEGIN = "''"
	END = "''"
	
	pass#TODO
	
#==========================================================
# Content Elements (Markdown)
#==========================================================

class MdItalicContentElement(MdContentElement): 
	
	""""""
	
	BEGIN = "*"
	END = "*"
	
	pass#TODO

#==========================================================
# Content Conversions (PM Wiki to Markdown)
#==========================================================

class Pmwiki2MdItalicContentElementConversion(Conversion):
	
	"""Conversion of italic content elements from Pm2Wiki to markdown."""
	
	FROM = PmwikiItalicContentElement
	TO = MdItalicContentElement
	
	pass#TODO
	
