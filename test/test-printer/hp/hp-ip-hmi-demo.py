#!/usr/bin/env python
# -*- coding: utf8 -*-
"""hp-ip-minimal.py

  Generate the PCL document printing a same line with various 
  Horizontal Motion Index values (HMI). Test on a NETWORKED HP Printer.
		
  Then setting HMI to 0, the printer use the appropriate HMI 
		   corresponding to the font and pitch (cpi).
  By setting the HMI yourself, you can increase space between
		   characters.  
  
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

def print_hmi_demo( printer_socket ):
	""" Generate the PCL document printing a same line 
		with various Horizontal Motion Index values (HMI).
		
	parameters:
		printer_socket : tuple (PRINTER_IP, PRINTER_PORT). On which
						 socket to print.
	"""
	
	print( 'Horizontal Motion Index demo' )
	print( '----------------------------' )
	print( 'Printer IP: %s\nPrinter Port: %i' % printer_socket )
	medium = PrinterSocketAdapter( printer_socket )
	
	# Very simple printout + usual initialization commands
	d = HpPclDocument( 'cp850', medium)
	d.reset_printer() # PCL to reset the printer
	d.symbol_set()    # Set the default symbol set (PC-850)
	d.paper_source()  # Set the default paper source to Tray + eject current page if any.
	
	d.pitch( 10 )     # Set 10 cpi size characters
	hmi_start = 11 # Value corresponding to pitch = 10 cpi.
	
	# How to calculate the default/starting HMI value
	#               (see technical reference on Horizontal Motion Index)
    #
    #  A4 Width (inch) = 2338 dots wide / 300 dpi = 7.793 Inches
    #
    #  Lets say we want 80 chars per lines.
    #  cpi = 80 characters per line / 7.793 Inch wide = 10.266 cpi
    #        so call d.pitch( 10 ) to fix font size to 10 cpi
    #
    #  HMI value = 120 HMI Units / 10.266 char per inch = 11.689 
    #        so HMI starts at 11 (or 12 if you prefer). 
    #        over that value, the printed caracter will be "more espaced"
  

    # Increasing the horizontal motion index to put more space between
    # characters.
	for hmi_value in range( hmi_start, hmi_start + 10 ): 
		d.horizontal_motion_index( hmi_value ) 
		d.writeln( u'0123456789abcdef' )
			
	medium.open() # Open the media for transmission
	try:
		d.send() # Send the content of the current document
	finally:
		medium.close()
	
	del( d )
	del( medium )
    
if __name__ == '__main__':
	print_hmi_demo( (PRINTER_IP, PRINTER_PORT) )
