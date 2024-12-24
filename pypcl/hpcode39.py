#!/usr/bin/env python
# -*- coding: utf8 -*-
"""hpcode39.py

Class to Generate BarCode 3-of-9 for Hewlett-Packard PCL Printer.

This class exposes method to help in generating specific PCL command 
enclosed within the PCL Stream to print.
  
Author 2015 DMeurisse <info@mchobby.be> MC Hobby SPRL

Licence: This specific file applies the licence as original code.
         See here under. Special thank to George T. Neill for is great
         work.

--- Original Licence ---

 Program...: CODE39.PRG
 Version...: 1.0
 Function..: Prints 3 of 9 barcodes

 Source....: Clipper (Summer '87)

 Author....: George T. Neill
             2140 Main Street
             La Crosse, WI  54601

 Created...: May 5, 1988  at 10:21 am
 Copyright.: None, released to the public domain as is with no express
             or implied warranty as to suitability or accuracy of this
             program.  The author shall not be held liable for any 
             damages, either direct or non-direct, arising from the use
             of this program.  This program may be modified and/or
             included in any program without any consideration to the
             author.
------------------------------------------------------------------------
History:
  05 feb 2015 - Dominique - create from BarCode39.PRG (clipper)
"""
from pypcl import HpPclDocument
from pypcl import PyPclError

class Barcode39Error( PyPclError ):
	pass
	
class Barcode39( object ):
	""" Barcode39 manage le code and sequences related to Barcode 3-of-9
	generation """
	
	owner = None 
	
	bc_height = 1 # Height of the drawed BareCode 
                  # ( multiplication factor of the normal printer character
                  #  tested with 1 and 2)
	
	# Basic characters to generate barcodes escape sequences
	#   nb = narrow bar character
    #   wb = wide bar character
    #   ns = narrow space
    #   ws = wide space
	_nb = None
	_wb = None 
	_ns = None 
	_ws = None 
	_bc_start = None
	_bc_end = None
	_char39 = None # { <uppercase_character>: 'descriptor of sequence nb wb... to be send ' }
	
	def __init__( self, owner, barcode_height = 1 ):
		""" constructor. The Owner must be a HpPclDocument instance """
		assert isinstance( owner, HpPclDocument ), "Owner must be an HpPclDocument"
		assert isinstance( barcode_height, int ), "barcode_height must be integer (1 or 2)"
		
		self.owner = owner
		self.bc_height = barcode_height
		# Create the internal structure needed for printing the barcode
		self.basic_char_setup()
		
	def basic_char_setup( self ):
		""" Defines characters for HP LaserJet.
		Initialize the nb,wb,ns variables """
		small_bar = 3                         # number of points per bar
		wide_bar = round(small_bar * 2.25,0)  # 2.25 x small_bar
		dpl = 50                              # dots per line 300dpi/6lpi = 50dpl
		self._nb = bytes( self.owner.PRINTER_ESC   +
						   ( '*c%02ia%ib0P' % (small_bar, self.bc_height*dpl) ) + 
						   self.owner.PRINTER_ESC  + 
						   ("*p+%02iX" % small_bar) )
		self._wb = bytes( self.owner.PRINTER_ESC +
						   ('*c%02ia%ib0P' % (wide_bar, self.bc_height*dpl) )+
						   self.owner.PRINTER_ESC +
						   ('*p+%02iX' % wide_bar ) )
		self._ns = bytes( self.owner.PRINTER_ESC + ( '*p+%02iX' % small_bar ) )
		self._ws = bytes( self.owner.PRINTER_ESC + ( '*p+%02iX' % wide_bar ) )
        
		# DONE nb = bc39_esc+"*c"+TRANSFORM(small_bar,'99')+"a"+Alltrim(STR(bc39_height*dpl))+"b0P"+bc39_esc+"*p+"+TRANSFORM(small_bar,'99')+"X"
		# DONE wb = bc39_esc+"*c"+TRANSFORM(wide_bar,'99')+"a"+Alltrim(STR(bc39_height*dpl))+"b0P"+bc39_esc+"*p+"+TRANSFORM(wide_bar,'99')+"X"
		# DONE ns = bc39_esc+"*p+"+TRANSFORM(small_bar,'99')+"X"
		# DONE ws = bc39_esc+"*p+"+TRANSFORM(wide_bar,'99')+"X"
  
		# adjust cusor position to start at top of line and return to bottom of line
		self._bc_start = bytes( self.owner.PRINTER_ESC + '*p-50Y' )
		self._bc_end   = bytes( self.owner.PRINTER_ESC + '*p+50Y' )
		# DONE bc39_start = bc39_esc+"*p-50Y"
		# DONE bc39_END   = bc39_esc+"*p+50Y"

		# setup the structure allowing to print the code codebar section for various LETTERS
		self._char39 = { u'1' : 'wb+ns+nb+ws+nb+ns+nb+ns+wb' ,  
						  u'2' : 'nb+ns+wb+ws+nb+ns+nb+ns+wb' ,         
						  u'3' : 'wb+ns+wb+ws+nb+ns+nb+ns+nb' ,         
						  u'4' : 'nb+ns+nb+ws+wb+ns+nb+ns+wb' ,          
						  u'5' : 'wb+ns+nb+ws+wb+ns+nb+ns+nb' ,         
						  u'6' : 'nb+ns+wb+ws+wb+ns+nb+ns+nb' ,        
						  u'7' : 'nb+ns+nb+ws+nb+ns+wb+ns+wb' ,         
						  u'8' : 'wb+ns+nb+ws+nb+ns+wb+ns+nb' ,         
						  u'9' : 'nb+ns+wb+ws+nb+ns+wb+ns+nb' ,         
						  u'0' : 'nb+ns+nb+ws+wb+ns+wb+ns+nb' ,         
						  u'A' : 'wb+ns+nb+ns+nb+ws+nb+ns+wb' ,        
						  u'B' : 'nb+ns+wb+ns+nb+ws+nb+ns+wb' ,        
						  u'C' : 'wb+ns+wb+ns+nb+ws+nb+ns+nb' ,        
						  u'D' : 'nb+ns+nb+ns+wb+ws+nb+ns+wb' ,        
						  u'E' : 'wb+ns+nb+ns+wb+ws+nb+ns+nb' ,         
						  u'F' : 'nb+ns+wb+ns+wb+ws+nb+ns+nb' ,        
						  u'G' : 'nb+ns+nb+ns+nb+ws+wb+ns+wb' ,        
						  u'H' : 'wb+ns+nb+ns+nb+ws+wb+ns+nb' ,         
						  u'I' : 'nb+ns+wb+ns+nb+ws+wb+ns+nb' ,        
						  u'J' : 'nb+ns+nb+ns+wb+ws+wb+ns+nb' ,        
						  u'K' : 'wb+ns+nb+ns+nb+ns+nb+ws+wb' ,         
						  u'L' : 'nb+ns+wb+ns+nb+ns+nb+ws+wb' ,         
						  u'M' : 'wb+ns+wb+ns+nb+ns+nb+ws+nb' ,         
						  u'N' : 'nb+ns+nb+ns+wb+ns+nb+ws+wb' ,        
						  u'O' : 'wb+ns+nb+ns+wb+ns+nb+ws+nb' ,         
						  u'P' : 'nb+ns+wb+ns+wb+ns+nb+ws+nb' ,         
						  u'Q' : 'nb+ns+nb+ns+nb+ns+wb+ws+wb' ,         
						  u'R' : 'wb+ns+nb+ns+nb+ns+wb+ws+nb' ,         
						  u'S' : 'nb+ns+wb+ns+nb+ns+wb+ws+nb' ,         
						  u'T' : 'nb+ns+nb+ns+wb+ns+wb+ws+nb' ,         
						  u'U' : 'wb+ws+nb+ns+nb+ns+nb+ns+wb' ,        
						  u'V' : 'nb+ws+wb+ns+nb+ns+nb+ns+wb' ,        
						  u'W' : 'wb+ws+wb+ns+nb+ns+nb+ns+nb' ,        
						  u'X' : 'nb+ws+nb+ns+wb+ns+nb+ns+wb' ,         
						  u'Y' : 'wb+ws+nb+ns+wb+ns+nb+ns+nb' ,        
						  u'Z' : 'nb+ws+wb+ns+wb+ns+nb+ns+nb' ,         
						  u'-' : 'nb+ws+nb+ns+nb+ns+wb+ns+wb' ,         
						  u'.' : 'wb+ws+nb+ns+nb+ns+wb+ns+nb' ,         
						  u' ' : 'nb+ws+wb+ns+nb+ns+wb+ns+nb' ,         
						  u'*' : 'nb+ws+nb+ns+wb+ns+wb+ns+nb' ,        
						  u'$' : 'nb+ws+nb+ws+nb+ws+nb+ns+nb' ,         
						  u'/' : 'nb+ws+nb+ws+nb+ns+nb+ws+nb' ,         
						  u'+' : 'nb+ws+nb+ns+nb+ws+nb+ws+nb' , 
						  u'%' : 'nb+ns+nb+ws+nb+ws+nb+ws+nb'  }

	def char_to_seq( self, uchar ):
		""" Return a list of escape sequences nb+ns+nb+ws+nb+ws+nb+ws+nb 
		to be send to the printer for a given character (eg: '+').
		It returns a list of bytes types.
		
		'%' -> [ bytes for nb, bytes for ns, bytes for nb, .... ] """
		
		lstParts = self._char39[ uchar ].split( '+' ) # [ 'nb', 'ns', 'nb', ... ]
		# Force evaluation with globals definition and local object definition (say on self.x)
		return [ eval( '_'+code, globals(), self.__dict__ ) for code in lstParts ]
		
	def code_to_sequences( self, ucode ):
		""" Transforme the code to include in the barcore INTO  into a full list of 
		escape sequences as produced by char_to_seq(). 
		
		Example:
		print( code_to_sequences( u'MCHP00157' )  """
		
		assert isinstance( ucode, unicode ), 'ucode must be unicode string!' 
		
		for uchar in ucode:
			if not( uchar in self._char39 ):
				raise Barcode39Error( '%s char is not listed in Barcode39 characters [0..9,A..Z,space,9,-,.,$,/,+,%]' )

		result = []
		for uchar in ucode:
			result = result + self.char_to_seq(uchar) 
			
		return result

	def write( self, ucode ):
		""" write the barcode corresponding to ucode in the ower document.
		Do not include the header and trailing * in the ucode!"""
		assert isinstance( ucode, unicode ), "the code to compute in barcode must be a unicode string"  
		
		# code barre message must starts and finish with *
		ucode = u'*%s*' % ucode.strip()
		
		self.owner.write_bytes( self._bc_start )
		# Transfert every computed esc sequence into the document 
		for bytes_seq in self.code_to_sequences( ucode ):
			self.owner.write_bytes( bytes_seq )
			self.owner.write_bytes( eval( '_ns', globals(), self.__dict__ ) ) # add a ns after each caracter sequence
		self.owner.write_bytes( self._bc_end )

	def barcode_message( self, ucode ):
		""" return the message as enclosed with the barcode picture.
		That message must have a special format (as returned). 
		
		Do not include the header and trailing * in the ucode!"""
		assert isinstance( ucode, unicode ), "the code to compute in barcode must be a unicode string"  

		for uchar in ucode:
			if not( uchar in self._char39 ):
				raise Barcode39Error( '%s char is not listed in Barcode39 characters [0..9,A..Z,space,9,-,.,$,/,+,%]' )
	
		return u'*%s*' % ucode.strip()
