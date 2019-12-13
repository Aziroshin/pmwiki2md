#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# Python
import argparse

# Local
from lib import converter
from lib.converter import FileConverter, FilePairs
from pmwiki2md import AllConversions as Conversions

converter = FileConverter(conversions=Conversions, filePairs=FilePairs(\
	directoryPaths=FilePairs.DIRECTORY_PATHS(\
		source="/data/development/software/pmwiki2md/pmwiki2md/tests/integration/conversionFiles/pmwiki",\
		target="/home/yawgmoth/pmwiki2md/target"),\
	suffixes=FilePairs.SUFFIXES(\
		source=".pmwiki",\
		target=".md")))
converter.convert().string
