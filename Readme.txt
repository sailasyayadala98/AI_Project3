--------------------------------------------------------------------------------------------------------------------------------
Name		: Sai Lasya Yadala
UTA Id	: 1002029134
--------------------------------------------------------------------------------------------------------------------------------
Language Used for Implementation:

Language : Python
--------------------------------------------------------------------------------------------------------------------------------

Task1 -  calculated probabilty values in for B, G,C, F.

Task 2 - Bayesian Networks

Implemention:
-> A class is created called BayesianNetwork
-> All the probabilities given in the table are initialezed in the constructor.
-> Find all possible probabilty values in computeProbability(B,G,C,F) 

Task3: 

-------------------------------------------------------------------------------------------------------------------------------
task 1, 2 : Command to run the Problem:

    $ python bnet.py <training_data> <Bt/Bf> <Gt/Gf> <Ct/Cf> <Ft/Ff>

Example:
    $ python bnet.py training_data bt gf ct ff

task 3 : command line to run the problem:
    bnet.py <training_data> <query variable values> [given <evidence variable values>]

Example:
    $ python bnet.py training_data.txt Bt Gf given Ff

---------------------------------------------------------------------------------------------------------------------------------
Sample Execution:

 python bnet.py bt gf cf ff
	Probability:  0.00254733286584824
 python bnet.py training_data.txt Bt Gf given Ff
      o/p : 0.01352866399051832
---------------------------------------------------------------------------------------------------------------------------------- 
Code location Folder:
--> For task1 and task2 :
    sxy9134_assmt3\Task1_Task2\bnet

---> For task3 :
     sxy9134_assmt3\Task3\bnet 


training_data has given data 
