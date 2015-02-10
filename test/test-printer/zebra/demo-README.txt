=================
 demo-README.txt
=================
The content of this file is also available in French at the following
location
  http://domeu.blogspot.be/2015/02/imprimante-zebra-usb-zpl-et-cups-damned.html
  
--- Zebra Label Printer, ZPL and Linux ---

At MCHobby, we are using Linux (Linux Mint) for all our task and development.
So we wired our USB Zebra LP 2824 on the computer and tries to send 
  ZPL command toward the printer. ZPL command allows you to control
  directly the printer.
  
As suggested by Zebra documentation, we did created a small demo file.
See the file demo.zpl created with Geany, LineFeed line separator, UTF-8 encoding.

Next, we wanted to send that file directly to the printer with
  cat demo.zpl > /dev/usb/lp0
and continuously get the error "/dev/usb/lp0: Permission denied"

This error is due to the printer management system (CUPS).
We cannot address directly the device because of CUPS, but can't remove
CUPS because we do still need to print on other printers (like our
networked HP3015)

--- Damned CUPS! ---
This simple tasks of sending a raw file to the Zebra was one of the most
complicated to do. CUPS was not really the faulty point... it was my
leak of knowledge about CUPS printer management.

What we have to do is to install the Zebra as a RAW printer Queue... not
as a Zebra one.

see the file demo-zebra-raw-queue-cups.pdf 

--- send demo.zpl to Zebra Printer ---
As you can see on the PDF file mentionned here upper, we did created the
"zebra-raw" queue for our beloved Zebra LP 2824 Plus.

Then after, it would be possible to send RAW files containing ZPL command
directly to the printer with:

  lp -d zebra-raw demo.zpl

That's it and it work greats!
