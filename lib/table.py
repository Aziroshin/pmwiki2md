#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from lib.debugging import dprint
from typing import NamedTuple

class Row(object):
	
	"""Table row with Cell objects."""
	
	def __init__(self, cells=[]):
		self.cells = cells
		
	def addCell(self, cell):
		"""Add a new cell to the table.
		Takes:
			cell (Cell)"""
		self.cells.append(cell)
		
	def _getCellListByType(self, pad=False, headersRequested=True):
		
		"""Get either header or data Cell object list."""
		
		if pad:
			paddedCellList = [] 
			for cell in self.cells:
				if cell.isHeader == headersRequested:
					# Add actual header.
					paddedCellList.append(cell)
				else:
					# Add empty padding.
					paddedCellList.append(Cell())
			return paddedCellList
		else:
			# Only return header cells; a potentially smaller list.
			return [c for c in self.cells if c.isHeader == headersRequested]
		
	@property
	def hasHeaderCells(self):
		"""Returns true if we have header cells, false if not."""
		return any([c.isHeader for c in self.cells])
	
	def getHeaderCells(self, pad=False):
		
		"""List of header cells, with or without padding.
		
		Takes:
			
			- pad (bool) [False]:
			
			If True, returns a list with the same size as
			self.cells, with any cell that isn't a header represented by an
			empty Cell object (no text). If the row contains no header cells,
			the list will only contain empty Cell objects.
			
			If False (the default) it returns a potentially smaller list with
			only header cells. If the row contains no header cells, the list
			is empty."""
			
		return self._getCellListByType(pad, headersRequested=True)
		
	def getDataCells(self, pad=False):
		
		"""List of data cells, with or without padding.
		Takes:
		
			- pad (boot) [False]:
			
			If True, returns a list with the same size as
			self.cells, with any header cell being represented by an
			empty Cell object (no text). If the row contains no data cells,
			the list will only contain empty Cell objects.
			
			If False (the default) it returns a potentially smaller list with
			only data cells. If the row contains no data cells, the list
			is empty."""
			
		return self._getCellListByType(pad, headersRequested=False)
	
class Cell(object):
	"""Table cell; typically part of a Row object."""
	def __init__(self, text="", isHeader=False):
		self.text = text
		self.isHeader = isHeader
		
class Table(object):
	"""Table made up of Row objects."""
	
	class NoHeadersError(Exception): pass
	
	def __init__(self, rows=[]):
		dprint(rows)
		self.rows = rows
		
	@property
	def hasRows(self):
		return len(self.rows) > 0
		
	@property
	def hasHeaders(self):
		if self.hasRows:
			return self.rows[0].hasHeaderCells
		else:
			return False
		
	@property
	def headers(self):
		if self.hasHeaders:
			return self.rows[0].getHeaderCells(pad=True)
		else:
			raise self.__class__.NoHeadersError(\
				"Table headers requested when there are none.")
	
	def addRow(self, row):
		"""Add Row object to table.
		Takes:
			row (Row)
		Returns: self (chainable)"""
		self.rows.append(row)
		return self
		
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
		
		rows = []
		for rowText in code.split("\n"):
			row = Row()
			for cellText in rowText.strip("||").split("||"):
				cell = Cell(cellText.strip())
				if cell.text.startswith("!"):
					cell.isHeader = True
				row.addCell(cell)
			rows.append(row)
			
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
	def headerSeparator(self):
		return "-"
	@property
	def verticalBorder(self):
		return " | "
	
class MdTable(TableFromTableByConversion):
	
	def fromTable(self, table):
		self.rows = table.rows
	
	def render(self, theme, withHeadersIfAvailable=True):
		renderedRows = []
		if self.headers and withHeadersIfAvailable:
			headerCells = [t for t in self.headers]
			headerSeparatorCells = [theme.headerSeparator*3 for i in range(0, len(self.headers))]
			renderedRows.append(theme.verticalBorder.join(headerCells))
			renderedRows.append(theme.verticalBorder.join(headerSeparatorCells))
		for row in self.rows:
			renderedCells = theme.verticalBorder.join([c.text for c in row.cells])
			renderedRows.append(renderedCells)
		return "\n".join(renderedRows)
