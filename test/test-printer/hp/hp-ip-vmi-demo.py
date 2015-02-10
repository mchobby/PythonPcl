#!/usr/bin/env python
# -*- coding: utf8 -*-
"""hp-ip-minimal.py

  Generate the PCL document printing a same line with various 
  Vertical Motion Index values (HMI). Test on a NETWORKED HP Printer.
		
  Then setting VMI to 0, the printer use the appropriate VMI 
		   corresponding to the font and pitch (cpi).
  By setting the HMI yourself, you can increase space between
		   lines.  
  
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
	vmi_start = 6     # Value corresponding to pitch = 10 cpi.
	
	# How to calculate the default/starting VMI value
	#               (see technical reference on Vertical Motion Index)
    #
    # Common setting:
	#	  vmi = 7.27 -> allow to print 66 lines on a portrait page
	#	                 (with a half inch margin on the top and bottom)
	#	       (10 inch-height / 66 lines-per-page ) x 48 = 7.27 
	#	       
	#	  vmi = 5.45 -> allow to print 66 lines on a landscape letter page
	#	                 (with a half inch margin on the top and bottom)
    #
	#	       (7.5 inch-heigh / 66 lines-per-page ) x 48 = 5.45
	#	       
	#	  vmi = 6 -> allow to print up to 84 lignes on a A4 page!
	#				 should be verified!
	#			29.5cm - 1.1cm margin top - 1.7cm margin bottom = 26.7cm
	#			26.7cm / 2.54 cm-per-inch = 10.51 inch
	#			
	#			vmi = 11.51 inch / 84 lines-per-page * 48 = 6.57
	#			
	#	  vmi = 8 -> allow to print up to 63 lines on a A4 page!
	#				 should be verified
	#				 
	#			29.5cm - 1.1cm margin top - 1.7cm margin bottom = 26.7cm
	#			26.7cm / 2.54 cm-per-inch = 10.51 inch
    # 
	#			vmi = 11.51 inch / 63 lines-per-page * 48 = 8.007 
    #  
  
	d.vertical_motion_index( 0 ) # Disable
	d.writeln( u'This is a demo about the usage of VMI' )
	d.writeln( u'and how it can impact your print out' )
	d.writeln()
	
	d.vertical_motion_index( 6 ) # Set the value to 8 lines/inch
	                             # 84 lines-per-page
	d.writeln( u'But this better to have a proper value' )
	d.writeln( u'when printing stuff' ) 

    # Increasing the vertical motion index to put more lines in the 
    # same space.
	for vmi_value in range( vmi_start, vmi_start  + 10 ): 
		d.vertical_motion_index( vmi_value ) 
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
