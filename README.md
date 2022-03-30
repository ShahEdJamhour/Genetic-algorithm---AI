# Genetic-algorithm- Graduation topics distribution

-	Aim:
The aim of this project is to distribute the topics based on the student’s selection as much as possible.
-	Factors:
Students, supervisors, topics and order of selection.
-	Constraints:
1)	Each student must assigned a topic.
2)	The topic can be assigned to one group only.
3)	The assignment must be closer as much as possible to the order of selection.
-	Set of variables:
•	Genes:
Each gene expresses a group of students, and the value of this gene represented by integer number from this rang [1-38], to express the project number (this expression is to ensure that the first constraint is met).
-----------------------------------------------------------------------------------
•	length of chromosome:
Since we have 37 group of students, then the length of each chromosome will 37 gene. 
------------------------------------------------------------------------------------
•	Number of population:
N=3 
--------------------------------------------------------------------------------------
•	Probability of crossover Pc:
Pc = 0.9
•	Probability of mutation Pm:
Pm = 0.001
--------------------------------------------------------------------------------------
•	Fitness function:
On each chromosome we calculate the fitness value by adding up the point values. The method for distributing points on genes is as follows:
1. If the value of the gene is from the first choice column, we collect 3 points.
2, If the value of the gene is from the second choice column, we collect 2 points. 
3. If the value of the gene is from the third choice column, we collect 1 point.
4. If the value is not present in any of these columns for this group of students, do not add any points and move on to the next gene.
