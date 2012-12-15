
Hydrometer
==

Want to submit package updates to homebrew?

Don't want to find packages that need updating by hand?

This is a script to help automate the review process for over a thousand packages!

Installation
===

This is python3 code.  Install python3 (and pip3) from brew like so:

	brew install python3

Now you can install BeautifulSoup, a python3 html parser the scripts rely on:

	pip3 install beautifulsoup4

Goto the terminal and type 'python3' to start a new shell.  Then type 'import bs4'.

If this looks like what you see (no angry messages about errors), you're good to go!

	$ python3
	Python 3.3.0 (default, Nov  3 2012, 09:45:08) 
	[GCC 4.2.1 Compatible Apple Clang 4.1 ((tags/Apple/clang-421.11.66))] on darwin
	Type "help", "copyright", "credits" or "license" for more information.
	>>> import bs4
	>>> 


Basic usage
===

Currently hydrometer supports the following options:

	-s, --sourceforge:  this will scan for sourceforge updates (~500 packages)
	-c, --googlecode:  this will scan for googlecode updates (~160 packages)
	-g, --gnuftp:  this will scan for gnu ftpmirror updates (~170 packages)
	-b, --github:  this will scan for github tag updates (~220 packages)

You're more than welcome to run the script interactively, but you'll probably want something like:

	python3 hydrometer.py -s > sourceforge_updates.txt

The end result will be a file that contains:

	1) a line from sourceforge packages
	2) hydrometer's best guess for the cooresponding package's latest version/downloads
	3) some spacing to keep things sane

Now, you just need to look through sourceforge_updates.txt for packages that need updating.


Final step
===

Update the package.  Submit a patch.  Have a beer to celebrate. :3


Future improvements
===

The googlecode/github parsers could be made less verbose.
There are 90 aspell libraries, they could be ignored.
More error checking, perhaps.
Things are hardcoded to /usr/local.


