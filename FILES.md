
* pypcl/      Will contain the files for controling printers with PCL or
			  alike (ZPL).

* res/        Contains many informations/links helping me to develop 
              this project. Please, have a look to the file ressources.txt
              Also contains a copy of Zebra ZPL Programming guide 
              (Zebra ZPLII-Prog.pdf, I didn't find a reliable link on 
              the Net). 
              
* res/pcl-symbol-set/ 
              Many PCL symbol set sheet. Almost all coming from
              www.pclviewer.com

* test/       Contains the various scripts used to test the classes
			  and use cases.
			  
* test/test-classes/
			  Test the features of bases classes and how to use it.
			  
* test/test-printer/
              Test the features of PCL Printing on physical printers
              
* test/test-printer/hp/
			  Test the Hewlett Packard PCL printing on physical 
			  HP printers	
			  
* test/test-printer/zebra/
              Test the Zebra label printer using ZPL.
              Most of the samples uses PrinterCupsAdapter to print 
                on the raw print queue attached to the Zebra Printer 
