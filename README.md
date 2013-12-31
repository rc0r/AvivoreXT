#AvivoreXT
###The Twitter-searching Data Miner

Avivore is a Python-based tool that searches Twitter for keywords and then parses any tweets that are
found. A configuration file defines search terms and regular expressions that are used to extract data.

With the sample configuration file Avivore looks for the following sort of data:

* Phone numbers in NPA-NXX format (ex: 604-555-1212)
* IPv4 addresses (127.0.0.1)
* Blackberry PINs (ABCDEF12)

Of course, more data sets can be defined in the configuration file.

It presently uses a SQLite backend to store the data that is found and outputs results via a Console. It 
has only been tested on Ubuntu Linux but there should be no real reason for it not to work under OS X, 
Windows, or any other platform capable of running Python.

###Requirements
* Python 2.7, 3
* SQLite3
* Twitter-Application-Only-Authentication-OAuth-Python (https://github.com/hlt99/Twitter-Application-Only-Authentication-OAuth-Python)
