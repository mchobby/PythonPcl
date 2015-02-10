#!/usr/bin/env python
# -*- coding: utf8 -*-
"""pypcl.py

Base class used to print documents using the Printer Control Langage 
(also known as PCL) and derivated.

This class is a "container" and is not supposed to be used as it.
Please have a look to HpPclDocument class.
  
Copyright 2015 DMeurisse <info@mchobby.be> MC Hobby SPRL

Licence: CC-BY-SA-NC 

Cannot be reused for commercial product without agreement.
Please, contact us at <info@mchobby.be> 

------------------------------------------------------------------------
History:
  01 feb 2015 - Dominique - v 0.1 (première release)
"""
import encodings  

class PyPclError( Exception ):
	""" exception for pypcl project """
	pass
	
class PrinterAdapterError( PyPclError ):
	""" raised by PrinterAdapter descendant in case of issue """
	pass
	
class PclDataType( object ):
	""" Enumerate the types of PCL data enclosed within an PclDocument item """ 
	
	PCL  = 1 # Content is supposed to be PCL command, possibly escape sequence
	TEXT = 2 # Content is supposed to be TEXT to be printed.
	BINARY = 3 # Content is supposed to be BINARY content (contained into bytes)
	
	items = { PCL: 'PCL command stream', TEXT: 'Text stream', BINARY: 'Bytes stream' } 

PCL_DATA_TYPE = PclDataType()
	
class PclDocument( list ):
	""" Class storing content to print. 
	
	Content is stored as tuple (data_type, unicode_str). 
	PCL sequence are stored with data_type = pcl_type + unicode string
	   containing the escape sequence.
	
	Normal text flow are stored with data_type = text_type + unicode.
	
	The content is send to the printer via a PrinterAdapter which
	take care of printer encoding AND transmission layer.
	"""
	PRINTER_CRLF = chr(13)+chr(10) # Go to begin of next line, should be override in descendant class
		
	def __init__( self, target_encoding = 'cp850', printer_adapter = None, title = '' ):
		""" initialisisation of PclDocument class.
		
		printer_adapter : (PrinterAdapter) - object derived from 
						  PrinterAdapter and used to send the 
						  data to the physical printer throught a
						  dedicated hardware layer. Can possibly 
						  been fixed later."""
		assert isinstance( target_encoding, str ), 'target_encoding must be a string. eg: cp850 or utf8'
		
		self.__target_encoding = target_encoding				  
		list.__init__( self )
		self.__printer_adapter = printer_adapter
		self.__target_encoding = target_encoding
		self.__title           = title # Optional document title
		
	def append( self, item ):
		assert isinstance( item, tuple ), 'PclDocument can only append tuple (pcl_type!=binary, unicode_data) or (pcl_type==binary, bytes)'
		assert isinstance( item[0], int ), 'tuple[0] must be an data_type (int)'
		assert item[0] in PCL_DATA_TYPE.items.keys(), 'data_type is not valid' 
		assert ((item[0] != PCL_DATA_TYPE.BINARY) and isinstance( item[1], unicode )) or ((item[0] == PCL_DATA_TYPE.BINARY) and isinstance( item[1], bytes )), 'tuple[1] must be an unicode string or binary!'  
		list.append( self, item )
		
	def __add__( self, item ):
		self.append( item )
		return self

	def insert( self, index, item ):
		raise NotImplementedError( 'insert not supported yet' )
		
	def clear( self ):
		""" Clear the document structure in memory """
		del( self[:] ) # remove every element from list
		
	def send( self ):
		""" main function for sending of data over the medium (aka PrinterAdapter) """ 
		# Relay document title to the Printer Adapter
		if self.__printer_adapter:
			self.__printer_adapter.doc_title = self.__title
			
		# sending process
		if not self.before_sending():
			return
		self.sending()
		self.after_sending()
				
	def before_sending( self ):
		""" override this if you want to perform something before sending
		the data over the medium (aka PrinterAdapter)"""
		return True # continue processing
		
	def sending( self ):
		""" override this to effectively send your data over the medium
		(aka PrinterAdapter) """
		pass
	
	def after_sending( self ):
		""" override this if you want to perform something after sending
		of the data over the medium (aka PrinterAdapter). 
		Eg: Clear the current PclDocument in memory"""
		pass

	@property
	def printer_adapter( self ):
		return self.__printer_adapter

	@property
	def target_encoding( self ):
		return self.__target_encoding
				
	@printer_adapter.setter
	def printer_adapter( self, value ):
		raise NotImplementedError( "still to do" )
	
	@property
	def title( self ):
		return self.__title # document title
		
	@title.setter
	def title( self, value ):
		assert isinstance( value, str ), 'document title must be a string!'
		self.__title = value
	
	# === General Tools ===
	def write_bytes( self, data ):
		""" allows to inject bytes (binary data), very usefull for
		escape sequences. data must be bytes() type """
		self.append( (PCL_DATA_TYPE.BINARY, data ) )
		
	def write( self, unicode_text ):
		self.append( (PCL_DATA_TYPE.TEXT,unicode_text) )
		
	def writeln( self, unicode_text = u'' ):
		self.write( unicode_text+self.PRINTER_CRLF )
		


class PrinterAdapter( object ):
	""" Base class used to abstract the physical transmission to the
	printer. This class should not be called directly, you should 
	instanciate descendant class that take care about transmission media."""
	
	def __init__( self ):
		""" initialize the PrinterAdapter object """
		self.__isopen = False
		self.__isflushed = True
		self.__doc_title = '' # Document title. 
							  # Such information be use when sending over the media.
							  # Eg: PrinterCupsAdapter use this to indentify the document in the queue
								
		
	@property 
	def isopen( self ):
		""" indicates is the physical layer is already open or not """
		return self.__isopen
		
	@property
	def isflushed( self ):
		""" indicates that the physical layer has flushed is data """
		return self.__isflushed
		
	@property 
	def doc_title( self ):
		""" Return the document name as mentionned by the PclDocument.send() """
		return self.__doc_title
		
	@doc_title.setter
	def doc_title( self, value ):
		""" Store the new document name as mentionned by the PclDocument.send() """
		assert isinstance( value, str )
		self.__doc_title = value
		
	def open( self ):
		""" open the physical layer (should be overriden) to print """
		self.__isopen = True
		self.__isflushed = False
		
	def close( self ):
		""" close the physical layer (should be overriden) to end printing
		and release ressources """
		if self.__isopen and not( self.__isflushed ):
			self.flush()
		self.__isopen = False 
		
	def send( self, bytes_to_send ):
		""" Send the piece of data as bytes. Should be overwrite by descendant to 
		physically send the data over the transmission layer.
		
		Only responsible for the transmission of data... not the encoding!
		
		parameter:
		
		"""	
		assert isinstance( bytes_to_send, bytes ), 'bytes_to_send must be bytes' 
		if not self.__isopen:
			raise PrinterAdapterError( 'Adapter is not yet open!' )
		self.__flushed = False
		
	def flush( self ):
		""" takes the appropriate actions to flush the data on the media.
		On most of the case, this method does not need to be overrided
		and does nothing.  But this may be kindly usefull on particular
		cases """
		self.__isflushed = True # Mention the media as Flushed
		
