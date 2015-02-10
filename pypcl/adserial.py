"""adserial.py

Serial Adaptater to send PclDocument (or derivated class) over a 
serial or usb-serial communication link.
  
Copyright 2015 DMeurisse <info@mchobby.be> MC Hobby SPRL

Licence: CC-BY-SA-NC 

Cannot be reused for commercial product without agreement.
Please, contact us at <info@mchobby.be> 

------------------------------------------------------------------------
History:
  08 feb 2015 - Dominique - v 0.1 created, not yet tested.
"""
from pypcl import *
import serial
import encodings  

class PrinterSerialAdapter( PrinterAdapter ):
	""" Used to send the print stream over a Serial port. 
	
	*** NOT TESTED YET ***
	"""
	
	def __init__( self, serial_device, baud = 9600 ):
		""" initialize an adapter using a serial or serial-over-usb 
		    communication link.
		    
			Parameters:
				serial_device (str): identification of the serial device (eg: /dev/ttyACM1)
				baud (int): baud rate for the serial communication (usually ignored for serial-over-usb). 
		"""
		
		assert isinstance( serial_device, str ), 'serial_device must be a string ( pointing to serial device )'
		PrinterAdapter.__init__( self )
		self.__serial_device = serial_device
		self.__baud = baud
		self.__serial = None
		
	@property
	def printer_device( self ):
		return self.__serial_device
		
	@property
	def printer_baud( self ):
		return self.__baud
		
	def open( self ):
		""" open the printer serial link """
		if self.isopen:
			return
		if self.__serial != None:
			raise PrinterAdapterError( 'serial is already assigned!' )
		
		try:	
			self.__serial = serial.Serial( self.__serial_device, baudrate = self.__baud, timeout = 1 )
		except:
			# assume ressource release
			self.__serial = None
			raise
		
		# Change the isopen flag when every went right
		PrinterAdapter.open( self )
		
	def close( self ):
		""" Close the printer serial link """
		# ensure socket closure what ever can happen
		if self.__serial != None:
			#self.__serial.close()
			self.__serial = None
			
		if not self.isopen:
			return
		
		# change internal flag
		PrinterAdapter.close( self )
		
		# return

	def send( self, bytes_to_send ):
		""" User did call send on the PclDocument. We have to 
		send the bytes of the document """
		
		PrinterAdapter.send( self, bytes_to_send )
		
		self.__serial.write_bytes( bytes_to_send )
		self.__serial.flush()
