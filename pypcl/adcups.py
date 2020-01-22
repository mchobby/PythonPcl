"""adcups.py

CUPS Adaptater to send PclDocument (or derivated class) over a
CUPS printer manager.

Copyright 2015 DMeurisse <info@mchobby.be> MC Hobby SPRL

Licence: CC-BY-SA-NC

Cannot be reused for commercial product without agreement.
Please, contact us at <info@mchobby.be>

------------------------------------------------------------------------
History:
  08 feb 2015 - Dominique - v 0.1 create.
"""
from pypcl import *
import encodings
import cups
import tempfile

class PrinterCupsAdapter( PrinterAdapter ):
	""" Used to send the print stream over the CUPS print queue. """

	__cups_conn = None
	__printer_queue_name = None
	__temp_file = None     # File object to store temporary file (zpl document)
	__temp_filename = None # Filename of the temporary File object (for CUPS usage)

	def __init__( self, printer_queue_name = None ):
		""" initialize an adapter using the Print Queue Name. The Queue
			should be configured as Generic -> RAW

			Parameters:
				printer_queue_name (str): identification of the printer queue (eg: "zebra-raw")
		"""

		assert (printer_queue_name == None) or isinstance( printer_queue_name, str ), 'printer_queue_name must be a string ( pointing to a valid printer queue )'
		PrinterAdapter.__init__( self )
		self.__printer_queue_name = printer_queue_name

	@property
	def printer_queue_name( self ):
		return self.__printer_queue_name

	@printer_queue_name.setter
	def printer_queue_name_setter( self, value ):
		assert isinstance( value, str ), 'printer_queue_name must be a string'
		self.__printer_queue_name = value


	@property
	def printers( self ):
		""" Return the list of cups printers """
		if not self.isopen:
			raise PyPclError( 'Adapter must first be open!' )
		return self.__cups_conn.getPrinters()

	def dump_printers( self ):
		""" Just print the list of printer queue available on the computer """
		printers = self.printers
		for printer in printers:
			print printer, printers[printer]["device-uri"]

	def open( self ):
		""" open the CUPS link """
		if self.isopen:
			return
		if self.__cups_conn != None:
			raise PrinterAdapterError( 'Already connected to CUPS!' )

		try:
			self.__cups_conn = cups.Connection()
		except:
			# assume ressource release
			self.__cups_conn = None
			raise

		# Change the isopen flag when every went right
		PrinterAdapter.open( self )

	def close( self ):
		""" Close the CUPS link """
		# ensure CUPS closure what ever can happen
		if self.__cups_conn != None:
			self.__cups_conn = None

		if not self.isopen:
			return

		# change internal flag
		PrinterAdapter.close( self )
		# return

	def send( self, bytes_to_send ):
		""" User did call send on the PclDocument. We have to
		send the bytes of the document """

		if self.__temp_file == None:
			self.__temp_file = tempfile.NamedTemporaryFile( suffix = '.zpl', delete = False ) # Do not delete on closure
			self.__temp_filename = self.__temp_file.name

		# call ancestor
		PrinterAdapter.send( self, bytes_to_send )

		self.__temp_file.write( bytes_to_send )

	def flush( self ):
		""" Flushing is implemented in CUPS to allow to send the
		document file to CUPS printer manager """
		if self.__temp_file:
			# Close the file
			self.__temp_file.flush()
			self.__temp_file.close()
			self.__temp_file = None
			# Send file to CUPS
			self.__cups_conn.printFile( self.__printer_queue_name, self.__temp_filename, 'Zpl Label %s' % self.doc_title, {} )

		#print( 'PrinterCupsAdapter.flush()' )

		# Ensure the ancestor the flag the flush operation ;-)
		PrinterAdapter.flush( self )
