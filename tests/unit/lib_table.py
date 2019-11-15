#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#=======================================================================================
# Imports
#=======================================================================================

# Python
import unittest

# Local

# DEBUG
from lib.debugging import dprint, cdprint

#class RowTest(unittest.TestCase):
	#def test

class TableTest(unittest.TestCase):
	
	@property
	def basicTestTable(self):
		from lib.table import Table, Row, Cell
		return Table(rows=[\
			Row(cells=[Cell("A1"), Cell("A2")]),\
			Row(cells=[Cell("B1"), Cell("B2")]),\
			])
	
	def test_addRowAndCell(self):
		"""
		Tests adding one Row with one Cell."""
		from lib.table import Table, Row, Cell
		cell = Cell()
		row = Row()
		table = Table()
		cell.text = "Test"
		row.addCell(cell)
		table.addRow(row)
		textFoundInTableCell = table.rows[0].cells[0].text
		self.assertEqual(textFoundInTableCell, "Test")
		
	def test_tableIntegrity(self):
		"""
		Tests whether everything's in place in self.basicTestTable.
		Table layout:
			[["A1", "A2"]
			 ["B1", "B2"]]
		This uses, thus tests constructor arguments for
		initialization."""
		
		table = self.basicTestTable
		self.assertEqual(table.rows[0].cells[0].text, "A1")
		self.assertEqual(table.rows[0].cells[1].text, "A2")
		self.assertEqual(table.rows[1].cells[0].text, "B1")
		self.assertEqual(table.rows[1].cells[1].text, "B2")
	
	def test_MdTableRender(self):
		
		"""
		Tries to render self.basicTestTable."""
		
		from lib.table import MdTable, TableTheme
		
		shouldLookLike = "<TODO>"
		renderResult = MdTable(self.basicTestTable).render(TableTheme())
		self.assertEqual(renderResult, shouldLookLike)
