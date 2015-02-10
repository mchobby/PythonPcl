"""adsocket.py

Socket Adaptater to send PclDocument (or derivated class) over an 
Ethernet connexion (as HP Network Printer).
  
Copyright 2015 DMeurisse <info@mchobby.be> MC Hobby SPRL

Licence: CC-BY-SA-NC 

Cannot be reused for commercial product without agreement.
Please, contact us at <info@mchobby.be> 

------------------------------------------------------------------------
History:
  08 feb 2015 - Dominique - v 0.1 created from pypcl.py .
"""
from pypcl import *
import socket
import encodings  

class PrinterSocketAdapter( PrinterAdapter ):
	""" Used to send the print stream over an Ethernet Socket. """
	
	def __init__( self, printer_socket ):
		assert isinstance( printer_socket, tuple ) and len( printer_socket )==2 , 'printer_socket must be a tuple ( printer_ip, printer_port )'
		PrinterAdapter.__init__( self )
		self.__printer_socket = printer_socket
		self.__socket = None
		
	@property
	def printer_socket( self ):
		return self.__printer_socket
		
	def open( self ):
		""" open the printer socket """
		if self.isopen:
			return
		if self.__socket != None:
			raise PrinterAdapterError( 'socket is already assigned!' )
		
		try:	
			self.__socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
			self.__socket.connect( self.__printer_socket )
		except:
			# assume ressource release
			self.__socket = None
			raise
		
		# Change the isopen flag when every went right
		PrinterAdapter.open( self )
		
	def close( self ):
		""" Close the printer socket """
		# ensure socket closure what ever can happen
		if self.__socket != None:
			self.__socket.close()
			self.__socket = None
			
		if not self.isopen:
			return
		
		# change internal flag
		PrinterAdapter.close( self )
		
		# return

	def send( self, bytes_to_send ):
		""" User did call send on the PclDocument. We have to 
		send the bytes of the document """
		
		PrinterAdapter.send( self, bytes_to_send )
		
		self.__socket.sendall( bytes_to_send )
