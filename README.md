# python-polymorphic-virus
Python virus that shows a simple message and infects other python scripts (i.e., .py and .pyw), using polymorphism to have different random encryptions of the virus 
for each infected file. The virus applies the concept of metamorphism to cause the original python script to change its own code after each execution by performing 
random changes while maintaining its original logic.

The reach of the virus can be adjusted by changing the varuable DEPTH near the start of the script. Originally, DEPTH = 0, which causes it to only infect python scripts 
in the same directory.
