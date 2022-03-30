import pandas as pd
import random
from legacy import xrange
import numpy as np
# Group class
# each object related to e student group, their choices and final assigned valueclass Group:
class Group:
    def __init__(self, students,groupnum, firstc, secondc, thirdc, assigned):
        self.students=students
        self.groupnum=groupnum
        self.firstc= firstc
        self.secondc=secondc
        self.thirdc=thirdc
        self.assigned=assigned

    def __str__ (self):
        return str(self.students),str(self.groupnum), str(self.firstc), str(self.secondc), str(self.thirdc),str(self.assigned)

#======================================================================================================================
# Read the data from input file
data = pd.read_excel (r'C:\Users\Farhoud\OneDrive\Desktop\4-1st samaster\AI\Students+selections.xlsx')
students = pd.DataFrame(data, columns=['Groups']).values.tolist()# Read the column called Groups and save it in student list
firstc = pd.DataFrame(data, columns=['First Choice']).values.tolist()# Read the column called First Choice and save it in firstc list
secondc = pd.DataFrame(data, columns=['Second Choice']).values.tolist()# Read the column called Second Choice and save it in secondc list
thirdc = pd.DataFrame(data, columns=['nan']).values.tolist()# Read the column called nan and save it in thirdc list

groups =[] # List of Group objects
c = 0
# Fill in the groups list
for c in range(0, len(students)):
	groups.append(Group(students[c],c+1,firstc[c],secondc[c],thirdc[c],0))
#======================================================================================================================
#Chromosome class
targetFitness = 66
NUM_OF_ELITE_CHROMOSOMES = 1 # number of chromosome that will not be subjected to crossover or mutation from one generation to the next
TOURNAMENT_SELECTION_SIZE = 2
population_size = 3
MUTATION_RATE = .01
class chromosome:
    def __init__(self):
        # random 1-38 without repetition
        self._genes = list(xrange(1, 38))  # list of integers from 1 to 38
        # adjust this boundaries to fit your needs
        self._fitness = 0 # to representing the fitness of each chromosome
        random.shuffle(self._genes) # <- List of unique random numbers

    def get_genes(self):
        return self._genes

    def get_geneByIndex(self ,index):
        return self._genes[index]

    def set_genByIndex(self, index, value):
        self._genes[index] = value

    def get_fitness(self):
        i = 0
        self._fitness = 0 # intially the fitness = 0
        # To get the fitness of chromsome we make the following loop that visit each gene and compare the value of gene with student's choices
        while i < groups.__len__():
            first = groups[i].firstc[0]
            second = groups[i].secondc[0]
            third = groups[i].thirdc[0]
            # If gene = first choice --> add 3 points to fitness
            if (self.get_geneByIndex(i) == first):
                self._fitness += 3
            else:
                # If gene = second choice --> add 2 points to fitness
                if (self.get_geneByIndex(i) == second ):
                 self._fitness += 2
                else:
                    # If gene = third choice --> add 1 points to fitness
                    if (self.get_geneByIndex(i) == third):
                        self._fitness += 1
            i += 1 # go to the next gene
        return self._fitness
#===================================================================================================================
class population():
    # in this class we will use the size to instantiate new chromosmes and put them in list
   def __init__(self,size):
       self._chromsomes = []# list of chrmosome objects
       i = 0
       while i < size:
           self._chromsomes.append(chromosome())
           i += 1

   def get_chromosomes(self):
       return self._chromsomes
#====================================================================================================================
class GeneticAlgorithm:
    @staticmethod
    # this function call crossover function and pass to it the population, it will retrun new population
    # after doing crossover we will do mutation on the retruned population from crossover function
    def evolve(pop):
        return GeneticAlgorithm._mutate_population(GeneticAlgorithm._crossover_population(pop))

    @staticmethod
    # generate crossover population and return it
    def _crossover_population(pop):
        crossover_pop = population(0) # empty population
        # fisrt we will move elite chromosome as is to the new population
        for i in range(NUM_OF_ELITE_CHROMOSOMES):
            crossover_pop.get_chromosomes().append(pop.get_chromosomes()[i])
        i = NUM_OF_ELITE_CHROMOSOMES # to exclude the elite chromosome
        # now do the crossover operation on the rest of the population
        while i < population_size:
            # first select 2 ramdom chromosome by using select_population function
            selected_pop = GeneticAlgorithm._select_population(pop).get_chromosomes()
            chromosome1 = selected_pop[0]
            chromosome2 = selected_pop[1]
            # make sure that 2 chromosome are not the same
            while (chromosome1.get_genes() == chromosome2.get_genes()):
                chromosome2 = GeneticAlgorithm._select_population(pop).get_chromosomes()[0]
            # now do the crossover operation in the two selected chromosome by crossover_chromosome function
            # after doing crossover the crossover_chromosome function will retrun 2 child we will add them to the crossover population
            childs = GeneticAlgorithm._crossover_chromosomes(chromosome1,chromosome2)
            #print(type(childs[0]))
            crossover_pop.get_chromosomes().append(childs[0])
            crossover_pop.get_chromosomes().append(childs[1])
            #print("===========")
            #print(len(crossover_pop.get_chromosomes()))
            i += 2 # because we add two chromsomes to the crossover population
        # when have the new population fully return it
        return crossover_pop

    @staticmethod
    # this function do the crossover operation between two chromosomes
    def _crossover_chromosomes(chromosome1,chromosome2):
        # Get length of chromosome
        chromosome_length = len(chromosome1.get_genes())
        # Pick crossover point, avoding ends of chromsome
        crossover_points = random.sample(range(0, chromosome_length), 2)  # generate 2 random start and end points
        # if the cut off section inculde all length of chromosome select new start and end points
        while((crossover_points[0] == 0 and crossover_points[1] == chromosome_length) or (crossover_points[0] == chromosome_length and crossover_points[1] == 0)):
            crossover_points = random.sample(range(0, chromosome_length), 2) # generate 2 random start and end points
        # performing ordered X1 crossover
        endpoint = 0 # the end point of cut off region
        start = 0 # the start oint of cut off region
        ##print("chromsome1=",chromosome1.get_genes())
        ##print("chromsome2=", chromosome2.get_genes())
        # because we select two random number we need to put the smaller in start variable and the bigger in the endpoint variable
        if crossover_points[0] > crossover_points[1]:
            start = crossover_points[1]
            endpoint = crossover_points[0]
        else:
            start = crossover_points[0]
            endpoint = crossover_points[1]
        #print("Start at = ",start)
        #print("End point at = ",endpoint)
        child_1 = chromosome() # child 1 will have the cut off region from chromosome 1 and the rest of genes from chromosome 2
        child_2 = chromosome() # child 2 will have the cut off region from chromosome 2 and the rest of genes from chromosome 1
        crossValue1 = [] # this list to save the values on the cut off region 1 ( which will be in child 1)
        crossValue2 = [] # this list to save the values on the cut off region 2 ( which will be in child 2)
        index1 = 0 # this variable to index the genes on child 1
        index2 = 0 # this variable to index the genes on child 2
        x = 0
        # initializing the new lists with zeros
        # for i in range(0,chromosome_length):
        #     child_1.append(0)
        #     child_2.append(0)
        # do the cross over operation between chromosome1 and chromosome 2

        # this loop just to copy the cut off region from chromosome 1 to child 1 at the same index
        for i in range(0,chromosome_length):
            # check if we reach to cut off region on chromosome 1
            if ( i == start):
                # if yes then copy the values from start point to end point then break
                for j in range(start,endpoint):
                    child_1.set_genByIndex(j,chromosome1.get_geneByIndex(j))
                    crossValue1.append(chromosome1.get_geneByIndex(j))
                    child_2.set_genByIndex(j, chromosome2.get_geneByIndex(j))
                    #child_2[j]=chromosome2.get_geneByIndex(j)
                    crossValue2.append(chromosome2.get_geneByIndex(j))
                break
            # else increase i and go to the next gene on chromosome 1
            continue

        #print("Length of crossvalue",len(crossValue1))
        # this loop will to fill the rest of genes of child 1 from chromosome 2
        # s variable will be used to index the genes on chromosome 1 and chromosome 2
        for s in range(chromosome_length):
            # index1 indicates the index of genes of the child 1
            if (index1 < 37):
        #        print("s==",s)
        #        print("start",start)
        #        print("end",endpoint)
        # check if index 1 not in cut off region ( because we fill it befor in the previous loop)
                if (index1 < start or index1 > endpoint):
                    # if the index 1 not in the cut off region we will fill this index by gene from chromosome 2
        #            print("Not cut off, s=",s)
                    x = 0
                    # but fisrt we need to check if the value of the gene(s in chromosome 2) is not in the cut off region (in child 1)
                    # This is because we have a constraint that do not allow repetition
                    # the next loop wraps on crossValue list to check if the gene in index s in chromosome 2 in one of the list item
                    # if the value of the gene in the list make x = 1 else x = 0
                    for k in range(0,len(crossValue1)):
                        #print("k =",k)
                        if ( chromosome2.get_geneByIndex(s) == crossValue1[k]):
       #                     print("not valid, cross = ",crossValue1[k],"chromsome value = ",chromosome2.get_geneByIndex(s))
                            x = 1
                            break
                        else:
                            continue
                    # if x != 1 then the value of the gene is valid so we can copy it to the child at index 1
                    if ( x != 1):
        #                print("index1 = ", index1)
        #                print("s=", s)
                        if (index1 < start or index1 >= endpoint):
        #                    print("ADD value")
                            child_1.set_genByIndex(index1,chromosome2.get_geneByIndex(s))
        #                    print("child value at index",index1,"=",child_1,"from chrom = ",chromosome2.get_geneByIndex(s))
                            index1 += 1 # move to the next index
        #                    print("index now = ",index1)
                # if the index 1 was in the cut off region we need to shift it
                elif (index1 <= start and index1 <= endpoint):
        #            print("shift the index!")
                    index1 = index1 + (endpoint - start) # we will shift it by the length of cut off region
        #            print("PPPPindex = ", index1)
        #            print("Not cut off, s=", s)
                    # after shift the index we need to check if the value of the gene at index s is valid or not
                    x = 0
                    for k in range(0, len(crossValue1)):
                        #print("k =", k)
                        if (chromosome2.get_geneByIndex(s) == crossValue1[k]):
        #                    print("not valid, cross = ", crossValue1[k], "chromsome value = ",
        #                          chromosome2.get_geneByIndex(s))
                            x = 1
                            break
                        else:
                            continue
                    if (x != 1):
        #                print("index1 = ", index1)
        #                print("s=", s)
                        if (index1 < start or index1 >= endpoint):
        #                    print("ADD value")
                            child_1.set_genByIndex(index1, chromosome2.get_geneByIndex(s))
                            #child_1[index1] = chromosome2.get_geneByIndex(s)
        #                    print("child value at index", index1, "=", child_1, "from chrom = ",
        #                          chromosome2.get_geneByIndex(s))
                            index1 += 1
        #                    print("index now = ", index1)
#==============================================================================================================
        # print("Length of crossvalue",len(crossValue1))
        # now we will do the same thing to child 2 put the different is :
        # in child 1 the cut off region is from chromsome 1 and the rest of genes in from chromosome 2
        # in child 2 the cut off region is from chromsome 2 and the rest of genes in from chromosome 1
        for s in range(chromosome_length):
            if (index2 < 37):
                #        print("s==",s)
                #        print("start",start)
                #        print("end",endpoint)
                if (index2 < start or index2 > endpoint):
                    #            print("Not cut off, s=",s)
                    x = 0
                    for k in range(0, len(crossValue2)):
                        # print("k =",k)
                        if (chromosome1.get_geneByIndex(s) == crossValue2[k]):
                            #                     print("not valid, cross = ",crossValue1[k],"chromsome value = ",chromosome2.get_geneByIndex(s))
                            x = 1
                            break
                        else:
                            continue
                    if (x != 1):
                        #                print("index1 = ", index1)
                        #                print("s=", s)
                        if (index2 < start or index2 >= endpoint):
                            #                    print("ADD value")
                            child_2.set_genByIndex(index2, chromosome1.get_geneByIndex(s))
                            #child_2[index2] = chromosome1.get_geneByIndex(s)
                            #                    print("child value at index",index1,"=",child_1,"from chrom = ",chromosome2.get_geneByIndex(s))
                            index2 += 1
                #                    print("index now = ",index1)

                elif (index2 <= start and index2 <= endpoint):
                    #            print("shift the index!")
                    index2 = index2 + (endpoint - start)
                    #            print("PPPPindex = ", index1)
                    #            print("Not cut off, s=", s)
                    x = 0
                    for k in range(0, len(crossValue2)):
                        # print("k =", k)
                        if (chromosome1.get_geneByIndex(s) == crossValue2[k]):
                            #                    print("not valid, cross = ", crossValue1[k], "chromsome value = ",
                            #                          chromosome2.get_geneByIndex(s))
                            x = 1
                            break
                        else:
                            continue
                    if (x != 1):
                        #                print("index1 = ", index1)
                        #                print("s=", s)
                        if (index2 < start or index2 >= endpoint):
                            #                    print("ADD value")
                            child_2.set_genByIndex(index2, chromosome1.get_geneByIndex(s))
                            #child_2[index2] = chromosome1.get_geneByIndex(s)
                            #                    print("child value at index", index1, "=", child_1, "from chrom = ",
                            #                          chromosome2.get_geneByIndex(s))
                            index2 += 1
        #                    print("index now = ", index1)

        # finally return two childs as a list
        print("#############################################")
        print("parant 1=")
        print(chromosome1.get_genes(),"fitness",chromosome1.get_fitness())
        print("parant 2=")
        print(chromosome2.get_genes(),"fitness",chromosome2.get_fitness())
        print("After cross-over")
        print("start at: "+str(start)+ ",end at: "+str(endpoint))
        print("child 1=")
        print(child_1.get_genes(),"fitness",child_1.get_fitness())
        print("child 2=")
        print(child_2.get_genes(),"fitness",child_2.get_fitness())
        print(" ")
        return [child_1,child_2]

    @staticmethod
    # generate mutate population and return it
    def _mutate_population(pop):
        mutate_pop = population(0) # empty population
        # fisrt we will move elite chromosome as is to the new population
        for i in range(NUM_OF_ELITE_CHROMOSOMES):
            mutate_pop.get_chromosomes().append(pop.get_chromosomes()[i])
        i = NUM_OF_ELITE_CHROMOSOMES # to exclude the elite chromosome
        # now do the mutate operation on the rest of the population
        while i < population_size:
            # first exclude the elite chromosomes then call mutate_chromosome function for each chromosome
            mutate_pop.get_chromosomes().append(GeneticAlgorithm._mutate_chromosome(pop.get_chromosomes()[i]))
            i += 1
        # when have the new population fully return it
        #print("mutate pop ",mutate_pop)
        #print("type mutate pop",type(mutate_pop.get_chromosomes()[1]))
        return mutate_pop

    @staticmethod
    # this function do the mutate operation for each chromosome
    def _mutate_chromosome(chromosome):
        # for each gene in the chromosome if the random number is less the mutation rate the do the mutate operation
        # else the gene will be the same and go to the next gene
        # the mutate operation is just a swap function that will swap two genes
        #print("chromosoe",chromosome)
        print("----------------------------------------------------------")
        print("Chromosome before mutation:")
        print(chromosome.get_genes(),"fitness",chromosome.get_fitness())
        for i in range(len(chromosome.get_genes())):
            x = random.random()
            #print("random num = ",x)
            if (x < MUTATION_RATE):
                #print("eter the loop")
                # we will swap the gene in index i with gene in random index
                swapWith = int(random.random() * len(chromosome.get_genes())) # select random index
                #print("i = ",i,"swap with = ",swapWith)
                # make sure that the 2 index is not the same
                while (swapWith == i):
                    #print("they are the same")
                    swapWith = int(random.random() * len(chromosome.get_genes()))  # select random index
                # do the swap operation
                value1 = chromosome.get_geneByIndex(i)
                value2 = chromosome.get_geneByIndex(swapWith)
                chromosome.set_genByIndex(i,value2)
                chromosome.set_genByIndex(swapWith,value1)
           # print("new chromsome= ",chromosome)
        print(" ")
        print("Chromosome after mutation:")
        print(chromosome.get_genes(),"fitness",chromosome.get_fitness())
        return chromosome

    @staticmethod
    # this function select (select size number) chromosome randomly from the population
    # and retrun a new population ordered by fitness
    def _select_population(pop):
        select_pop = population(0)# create new empty population
        i = 0
        # make a loop in each one add to selected population new random chromosome from pass population
        # until we reach the required number
        while i < TOURNAMENT_SELECTION_SIZE:
            # select random chromosome
            select_pop.get_chromosomes().append(pop.get_chromosomes()[random.randrange(0,population_size-1)])
            i += 1
            # stort the population
        select_pop.get_chromosomes().sort(key=lambda x: x.get_fitness(),reverse=True)
        return select_pop


def print_p(pop,gen_number):
    print("\n---------------------------------------------------------------------------------------------------------")
    print("Generation #", gen_number)
    i=0
    for x in pop.get_chromosomes():
        print("chromosome #",i,": ",x.get_genes(),"fitness",x.get_fitness())
        i += 1

p = population(population_size)
p.get_chromosomes().sort(key=lambda x: x.get_fitness(), reverse = True)
#newp = population(population_size)
print_p(p,0)

# 12 min
generation_number = 1
lastFit = 0
numberOftimes = 1000
lastFit = p.get_chromosomes()[0].get_fitness()
while p.get_chromosomes()[0].get_fitness() < targetFitness:
    if (lastFit == p.get_chromosomes()[0].get_fitness() and numberOftimes != 0):
        numberOftimes -= 1
        # print("type of object 1 is:",type(p.get_chromosomes()[2]))
        newp = GeneticAlgorithm.evolve(p)
        # print("type of object 1 is:", type(newp.get_chromosomes()[2]))
        p = newp
        # print("type of object 2 is:",type(p.get_chromosomes()[2]))

        # sorted(p.get_chromosomes(), key=lambda c: c.get_fitness())
        p.get_chromosomes().sort(key=lambda x: x.get_fitness(), reverse=True)
        # sorted(student_objects, key=lambda student: student.age)
        print_p(p, generation_number)
        generation_number += 1
    elif(lastFit != p.get_chromosomes()[0].get_fitness()):
        numberOftimes = 1000
        lastFit = p.get_chromosomes()[0].get_fitness()
        # print("type of object 1 is:",type(p.get_chromosomes()[2]))
        newp = GeneticAlgorithm.evolve(p)
        # print("type of object 1 is:", type(newp.get_chromosomes()[2]))
        p = newp
        # print("type of object 2 is:",type(p.get_chromosomes()[2]))

        # sorted(p.get_chromosomes(), key=lambda c: c.get_fitness())
        p.get_chromosomes().sort(key=lambda x: x.get_fitness(), reverse=True)
        # sorted(student_objects, key=lambda student: student.age)
        print_p(p, generation_number)
        generation_number += 1
    elif(numberOftimes == 0):
        break



