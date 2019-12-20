#-*- coding: utf-8 -*-

#=======================================================================================
# Imports
#=======================================================================================

# Python
import inspect
import os

#=======================================================================================
# Library
#=======================================================================================

def dprint(*args, stackLevel=1):
	
	"""Print a debugging message with automagically added context information."""

	parentStackContext = inspect.stack()[stackLevel]
	
	contextLocals = parentStackContext[0].f_locals
	className = ""
	
	if len(args) == 0:
		message  = ""
	elif len(args) == 1:
		message = args[0]
	else:
		message = " ".join([str(arg) for arg in args])
	
	if "self" in contextLocals.keys():
		className = "{name}.".format(\
			name=contextLocals["self"].__class__.__name__)
		
	print("[DEBUG:{fileName}:{line}:{className}{functionName}] {message}"\
		.format(\
			fileName = parentStackContext.filename.rpartition(os.sep)[2],\
			message = message,\
			line = parentStackContext.lineno,\
			className = className,\
			functionName=parentStackContext.function) )
	
def cdprint(content):
	"""Print .content of the ContentElement objs. in the specified Content obj."""
	dprint([contentElement.content for contentElement in content], stackLevel=2)
