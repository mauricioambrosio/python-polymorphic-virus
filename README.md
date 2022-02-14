# python-polymorphic-virus
Python virus that shows a simple message and infects other python scripts (i.e., .py and .pyw), using polymorphism to have different random encryptions of the virus 
for each infected file. The virus applies the concept of metamorphism to cause the original python script to change its own code after each execution by performing 
random changes while maintaining its original logic.

The reach of the virus can be adjusted by changing the varuable DEPTH near the start of the script. Originally, DEPTH = 0, which causes it to only infect python scripts 
in the same directory.


Example of infected script:

![image](https://user-images.githubusercontent.com/27931441/153881872-98c6934e-4134-4762-95c6-8d6368d154ac.png)

![image](https://user-images.githubusercontent.com/27931441/153882180-b8cb24ac-861c-4449-a934-2b15f7232181.png)

![image](https://user-images.githubusercontent.com/27931441/153882243-cdb0eed6-7e1e-4778-a459-0a086c088873.png)


