# PlagiarismDetector
Program to detect plagiarism in essays - final project for CMPUT 275
This program is designed to be ran in PyPy instead of the normal Python 3 interpreter.
The reason is that simple python interpreter is just WAY too slow (at least 10 times compared to PyPy)
Which is both detremintal to development and presentation.
The primary bottleneck arises from python's crappy performance with loops, which this program has plenty of.

A working (that is on the VM) distribution of PyPy is included.

To run:

$pypy main.py [directory where essays are located] [threshold for algorithm] [algorithm]

Or with interface

$pypy main.py
