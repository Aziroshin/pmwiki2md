#!/usr/bin/env python3
#-*-coding: utf-8 -*-

class ConvertibleFile: pass
class ConvertedElement: pass
class ConvertibleElement:
	def __init__(self, content):
	"""Represents an element of a convertible document, such as a title or code block."""
	self.content = content
	def convert(self):
		self.converted = ""
		
class ConvertibleContent: 
	"""Tree of ConvertibleContentElements reprsenting a convertible document."""
	def __init__(self):
		self.originalElements = [] # List of ConvertibleElements in order.
		self.convertedElements = []
		
	def convert(self):
		for element in self.originalElements:
			self.convertedElements.append(element.convert())
