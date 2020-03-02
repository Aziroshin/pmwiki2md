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
		Row(cells=[Cell("1", isHeader=True), Cell("2", isHeader=True)]),\
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
		table.test = "addRowAndCellTest"
		cell.text = "Test"
		row.addCell(cell)
		table.addRow(row) #NOTE: BUG found: does something to trip up tableHasRows.
		textFoundInTableCell = table.rows[0].cells[0].text
		self.assertEqual(textFoundInTableCell, "Test")
		dprint("Table address:", table)
		
	def test_tableIntegrity(self):
		"""
		Tests whether everything's in place in self.basicTestTable.
		Table layout:
			[["A1", "A2"]
			 ["B1", "B2"]]
		This uses, thus tests constructor arguments for
		initialization."""
		
		table = self.basicTestTable
		self.assertEqual(table.rows[0].cells[0].text, "1")
		self.assertEqual(table.rows[0].cells[1].text, "2")
		self.assertEqual(table.rows[1].cells[0].text, "A1")
		self.assertEqual(table.rows[1].cells[1].text, "A2")
		self.assertEqual(table.rows[2].cells[0].text, "B1")
		self.assertEqual(table.rows[2].cells[1].text, "B2")
		
	def test_tableHasRows(self):
		from lib.table import Table
		table = self.basicTestTable
		self.assertTrue(table.hasRows)
		#dprint(Table)
		emptyTable = Table()
		#emptyTable2 = Table()
		#emptyTable3 = Table()
		dprint(emptyTable)
		dprint(emptyTable.rows[0].cells[0].text)
		dprint("Table address:", emptyTable)
		#emptyTable.test = "tableHasRowsTest"
		dprint(emptyTable.test)
		#dprint(emptyTable2)
		#dprint(emptyTable3)
		#Table().rows[0].cells[0].text = "Bee"
		#dprint(Table().rows[0].cells[0].text)
		#self.assertFalse(emptyTable.hasRows)
	
	def test_tableHasHeaders(self):
		from lib.table import Table
		table = self.basicTestTable
		self.assertTrue(table.hasHeaders)
		self.assertFalse(Table().hasHeaders)
	
	def test_tableHeaders(self):
	
		"""
		Are table headers reported correctly?"""
		
		table = self.basicTestTable
		shouldLookLike = ["1", "2"]
		self.assertEqual(table.headers, shouldLookLike)
	
	def test_MdTableRender(self):
		
		"""
		Tries to render self.basicTestTable."""
		
		from lib.table import MdTable, TableTheme
		
		#shouldLookLike = "A1 | A2\nB1 | B2"
		shouldLookLike = "A | B\n--- | ---\nA1 | A2\nB1 | B2"
		renderResult = MdTable(self.basicTestTable).render(TableTheme())
		self.assertEqual(renderResult, shouldLookLike)
		
