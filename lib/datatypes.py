#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Python

class NamedList(object):
	
	"""Pretends NamedTuples are subclassable in Python 3.5.
	Underscore (_) prefixes for members are reserved for implementation.
	Doesn't take keyword arguments."""
	
	NAME = None
	ATTRIBUTES = []
	
	def __init__(self, *args):
		# Get name.
		if self.__class__.NAME == None:
			self._name = self.__class__.__name__
		else:
			self._name = self.__class__.NAME
		# Get Attributes.
		self._attributes = self.__class__.ATTRIBUTES
		self.data = [item for item in args]
		
	def _getAttrIndex(self, attrName):
		i = 0
		for attribute in self._attributes:
			if attribute == attrName:
				return i
			i =+ i
		
	def __getattr__(self, attrName):
		if attrName in self._attributes:
			return self.data[self._getAttrIndex]
		else:
			return super().__getattr__(attrName)
		
	def __setattr__(self, attrName, attrValue):
		if attrName in self._attributes:
			self.data[self._getAttrIndex(attrName)] = attrValue
		super().__setattr(attrName, attrValue)
