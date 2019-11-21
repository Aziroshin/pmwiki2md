#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from lib.debugging import dprint

class Row(object):
	
	"""Table row with Cell objects."""
	
	def __init__(self, title="", cells=[]):
		self.title = title
		self.cells = cells
		
	def addCell(self, cell):
		"""Add a new cell to the table.
		Takes:
			cell (Cell)"""
		self.cells.append(cell)
		
class Cell(object):
	"""Table cell; typically part of a Row object."""
	def __init__(self, text=""):
		self.text = text
		
class Table(object):
	"""Table made up of Row objects."""
	
	def __init__(self, rows=[]):
		self.rows = rows
		
	@property
	def titles(self):
		return [r.title for r in self.rows]
	
	def addRow(self, row):
		"""Add Row object to table.
		Takes:
			row (Row)"""
		self.rows.append(row)
		
	def render(self):
		"""Create a human interpretable representation of the table."""
		return "\n".join(self.rows)
		
class TableFromCode(Table):
	
	"""Table initialized from code in string form."""
	
	def fromCode(self, code):
		"""Initialize table from code string.
		Takes:
			code (str)"""
	
class PmwikiTable(TableFromCode):
	
	"""Table initialized from pmwiki code."""
	
	def fromCode(self, code):
		"""Initialize table from pmwiki code.
		Takes:
			code (str)"""
		
		# Get rows.
		codeRows = code.split("\n")
		if codeRows[]
		allRows = []
		for codeRow in codeRows:
			allRows.append(codeRow.strip("||").split("||"))
		if allRows[0][0].strip().startswith("!"):
			
	
class TableFromTableByConversion(Table):
	
	"""A table initialized from another table.
	override self.fromTable in a subclass to
	define conversion behaviour."""
	
	def __init__(self, table):
		super().__init__()
		self.fromTable(table)
		
	def fromTable(self, table):
		"""Override in subclass.
		Takes:
			table (Table): Table to initialize from.
		Returns: self"""
		
		return self
	
class TableTheme(object):
	
	"""Characters for table formatting.
	The default is markdown style tables."""
	
	@property
	def titleSeparator(self):
		return "-"
	@property
	def verticalBorder(self):
		return " | "
	
class MdTable(TableFromTableByConversion):
	
	def fromTable(self, table):
		self.rows = table.rows
	
	def render(self, theme, withTitlesIfAvailable=True):
		renderedRows = []
		if self.titles and withTitlesIfAvailable:
			titleCells = [t for t in self.titles]
			titleSeparatorCells = [theme.titleSeparator*3 for i in range(0, len(self.titles))]
			renderedRows.append(theme.verticalBorder.join(titleCells))
			renderedRows.append(theme.verticalBorder.join(titleSeparatorCells))
		for row in self.rows:
			renderedCells = theme.verticalBorder.join([c.text for c in row.cells])
			renderedRows.append(renderedCells)
		return "\n".join(renderedRows)
