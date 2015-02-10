#!/usr/bin/env python
# -*- coding: utf8 -*-
"""hp-ip-minimal.py

Test the minimal document printing on a NETWORKED HP Printer. 
  
Copyright 2015 DMeurisse <info@mchobby.be> MC Hobby SPRL

Licence: CC-BY-SA-NC 

Cannot be reused for commercial product without agreement.
Please, contact us at <info@mchobby.be> 

------------------------------------------------------------------------
History:
  02 feb 2015 - Dominique - v 0.1 (first release)
""" 
from pypcl import *
from pypcl import HpPclDocument

PRINTER_IP = '192.168.1.206'
PRINTER_PORT = 9100
PRINTER_ENCODING = 'cp850'

def print_minimal_doc( printer_socket ):
	""" Generate the mininal PCL document and print it on network printer.
	
	parameters:
		printer_socket : tuple (PRINTER_IP, PRINTER_PORT). On which
						 socket to print.
	"""
	
	print( 'Minimal Hp Document printing' )
	print( '----------------------------' )
	print( 'Printer IP: %s\nPrinter Port: %i' % printer_socket )
	medium = PrinterSocketAdapter( printer_socket )
	
	# Very simple printout + usual initialization commands
	d = HpPclDocument( 'cp850', medium)
	d.reset_printer() # PCL to reset the printer
	d.spacing()       # Set the default Fixed spacing
	d.horizontal_motion_index() # Set the default HMI to 0 = no horizontal motion
	d.paper_source()  # Set the default paper source to Tray + eject current page if any.
	d.symbol_set()    # Set the default symbol set (PC-850)
	
	d.writeln( u'This is my first document' )
	d.writeln( u'which accept ecute é and others' )
	d.writeln( u'Funny test' )
	d.writeln( u'' )
	
	
	# Writing in various pitch (cpi=caracter per inch)
	for cpi in d.PRINTER_CPI:
		d.pitch( cpi )
		d.writeln( u'print with cpi=%i' % cpi )
	d.writeln( u'' )
	
		
	medium.open() # Open the media for transmission
	try:
		d.send() # Send the content of the current document
	finally:
		medium.close()
	
	del( d )
	del( medium )
    
if __name__ == '__main__':
	print_minimal_doc( (PRINTER_IP, PRINTER_PORT) )
