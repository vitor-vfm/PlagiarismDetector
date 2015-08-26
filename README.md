# PlagiarismDetector
Program to detect plagiarism in essays - final project for CMPUT 275

This program is designed to run in PyPy instead of the normal Python 3 interpreter.
The regular python interpreter is just WAY too slow (at least 10 times compared to PyPy),
which is detrimental to both development and presentation.

The primary bottleneck arises from python's bad performance with loops, which this program has plenty of.

A working (that is on the VM) distribution of PyPy is included. Or do apt-get install pypy

To run:

$pypy main.py [directory where essays are located] [threshold for algorithm] [algorithm]

Or with interface

$pypy main.py

The interface has 2 options:

Full-Scan and Single-File

For Full-Scan you provide a folder in which all files are checked against each other for plagiarism and the output is sorted by score.

For Single File mode you provide a file (for example there is a catchmeifyoucan.txt so you would type ./catchmeifyoucan.txt -- the dot is important) and a folder. In this mode the file is compared against all the files in the folder and the potential plagiarisms are then displayed.
