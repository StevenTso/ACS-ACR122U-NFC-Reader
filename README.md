ACS ACR122U NFC Reader / Writer
=========

Python based reader/writer that is used to read tag data from the NFC ISO 14443 Type A and B cards, Mifare, FeliCa, and all 4 types of NFC (ISO/IEC 18092) tags.

Code provides a basic framework used to grab tag data.

#Environment
Tested under OS X Mavericks using a Debian virtual machine. If you are using a virtual machine to boot Linux, Google "Virtual USB Configuration" or use this [link](http://greatxam.wordpress.com/2010/11/23/virtualbox-usb-configuration/). You will have to do this if you are using a VM, otherwise the ACR122U reader will not mount to the virtual machine.

#Tech
[pyscard] - python for smart cards


Installation
--------------

```sh
sudo apt-get install python-pyscard
python NFCReader.py

```


License
----
MIT

[pyscard]:http://pyscard.sourceforge.net/