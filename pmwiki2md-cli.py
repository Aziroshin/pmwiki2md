#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# Python
import argparse

# Local
from lib import converter
from lib.converter import FileConverter, FilePairs
from lib.pmwiki2md import AllConversions as Conversions

parser = argparse.ArgumentParser()
parser.add_argument("source", help="Directory of files to be converted.")
parser.add_argument("target", help="Directory to write converted files to.")
args = parser.parse_args()

converter = FileConverter(conversions=Conversions, filePairs=FilePairs(\
	directoryPaths=FilePairs.DIRECTORY_PATHS(\
		source=args.source,\
		target=args.target),\
	suffixes=FilePairs.SUFFIXES(\
		source=".pmwiki",\
		target=".md")))
converter.convert()
