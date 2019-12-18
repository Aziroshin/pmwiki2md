#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Python
from collections import UserList

class NamedList(UserList):
	
	"""Fills in for the absence of subclassable NamedTuples in python 3.5.
	
	Underscore (_) prefixes for members are reserved for implementation.
	As it's based on collections.UserList, self.data is reserved as well and
	may not be used for list item names.
	The list is padded with NONE to be as long as self.__class__.ATTRIBUTES
	
	Usage:
	  Subclass this and set the following class attributes to your liking:
	    - NAME (None || str), default: None
	      The name of the NamedList; if left None, it'll be set to
	      self.__class__.__name__ upon instantiation.
		- ATTRIBUTES ([]): Attribute names, of which the order will correspond
		  to the order in the list. Example: If the list has 5 items, and
		  index 3 of ATTRIBUTES references "cucumber", self.cucumber will
		  return self.data[3].
	
	This is intended to work well enough for the pmwiki2md project, there is
	no intention for this to be an actual, generally viable drop-in replacement
	for NamedTuple.
	
	If anything, this is a terrible caveman hack for compatibility reasons."""
	
	NAME = None
	ATTRIBUTES = []
	
	def __init__(self, *args, **kwargs):
		# Pad our list with None, so it always has the same length
		# as the amount of expected attributes.
		values = [None for pad in range(0, len(self.__class__.ATTRIBUTES))]
		i = 0
		for arg in args:
			values[i] = arg
			i = i+1
		for kwargName in kwargs.keys():
			attrIndex = self._getAttrIndex(kwargName)
			if not attrIndex == None: # Would be None if it wasn't in self.__class__.ATTRIBUTES
				values[attrIndex] = kwargs[kwargName]
		object.__setattr__(self, "data", values)
		# Get name.
		if self.__class__.NAME == None:
			self._name = self.__class__.__name__
		else:
			self._name = self.__class__.NAME
		
	def _getAttrIndex(self, attrName):
		"""Get the index of an attribute name in self.__class__.ATTRIBUTES"""
		i = 0
		for attribute in self.__class__.ATTRIBUTES:
			if attribute == attrName:
				return i
			i = i+1
		
	def __getattr__(self, attrName):
		"""Take values for member names in self.__class__.ATTRIBUTES from self.data."""
		if not attrName in ["_getAttrIndex", "__class__"]:
			if attrName in self.__class__.ATTRIBUTES:
				return self.data[self._getAttrIndex(attrName)]
		return object.__getattribute__(self, attrName)
		
	def __setattr__(self, attrName, attrValue):
		"""Set values for member names in self.__class__.ATTRIBUTES in self.data."""
		if attrName in self.__class__.ATTRIBUTES:
			self.data[self._getAttrIndex(attrName)] = attrValue
		object.__setattr__(self, "attrName", attrValue)
