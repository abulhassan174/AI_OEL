import random 

# Number of individuals in each generation 
POPULATION_SIZE = 100

# Valid genes 
GENES = '''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOP 
ABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890, .-;:_!"#%&/()=?@${[]}'''

class Individual(object): 
    ''' 
    Class representing individual in population 
    '''
    def __init__(self, chromosome, target): 
        self.chromosome = chromosome 
        self.target = target
        self.fitness = self.cal_fitness() 

    @classmethod
    def mutated_genes(cls): 
        ''' 
        Create random genes for mutation 
        '''
        global GENES 
        gene = random.choice(GENES) 
        return gene 

    @classmethod
    def create_gnome(cls, target): 
        ''' 
        Create chromosome or string of genes 
        '''
        gnome_len = len(target) 
        return [cls.mutated_genes() for _ in range(gnome_len)] 

    def mate(self, par2):
        ''' 
        Perform single-point crossover and produce new offspring 
        '''
        # Select a random crossover point
        crossover_point = random.randint(0, len(self.chromosome) - 1)
        
        # Create offspring by combining chromosomes
        child_chromosome = self.chromosome[:crossover_point] + par2.chromosome[crossover_point:]
        
        # Perform mutation on some genes in the offspring
        for i in range(len(child_chromosome)):
            # Apply mutation with a certain probability
            if random.random() < 0.05:  # 5% mutation chance
                child_chromosome[i] = self.mutated_genes()

        # Create new Individual (offspring) using the generated chromosome
        return Individual(child_chromosome, self.target) 

    def cal_fitness(self): 
        ''' 
        Calculate fitness score. It is the number of 
        characters in string which differ from target string. 
        '''
        fitness = 0
        for gs, gt in zip(self.chromosome, self.target): 
            if gs != gt: 
                fitness += 1
        return fitness 

# Driver code 
def main(): 
    global POPULATION_SIZE 

    # Take the target string as input from the user
    TARGET = input("Enter the target string: ").strip()
    if not TARGET:
        print("Target string cannot be empty. Please try again.")
        return

    # Current generation 
    generation = 1

    found = False
    population = [] 

    # Create initial population 
    for _ in range(POPULATION_SIZE): 
        gnome = Individual.create_gnome(TARGET) 
        population.append(Individual(gnome, TARGET))
 

    while not found: 
        # Sort the population in increasing order of fitness score 
        population = sorted(population, key=lambda x: x.fitness) 

        # If the individual having the lowest fitness score (0) is found, break the loop 
        if population[0].fitness <= 0: 
            found = True
            break

        # Otherwise generate new offsprings for the new generation 
        new_generation = [] 

        # Perform elitism: the top 10% of the fittest population 
        # goes to the next generation 
        s = int((10 * POPULATION_SIZE) / 100) 
        new_generation.extend(population[:s]) 

        # From 50% of the fittest population, individuals 
        # will mate to produce offspring 
        s = int((90 * POPULATION_SIZE) / 100) 
        for _ in range(s): 
            parent1 = random.choice(population[:50]) 
            parent2 = random.choice(population[:50]) 
            child = parent1.mate(parent2) 
            new_generation.append(child) 

        population = new_generation 

        # Print generation info
        print(f"Generation: {generation}")
        for i, individual in enumerate(population[:4]):  # Display the top 4 individuals
            print(f"  {i+1}. String: {''.join(individual.chromosome)} Fitness: {individual.fitness}")

        generation += 1

    # Print final result
    print("\nFinal result:")
    print(f"Target: {TARGET}")
    print(f"Result: {''.join(population[0].chromosome)} Fitness: {population[0].fitness}")
        
if __name__ == '__main__': 
    main()