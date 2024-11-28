import random

class Individual:
    def __init__(self, chromosome, items, max_weight):
        self.chromosome = chromosome
        self.items = items
        self.max_weight = max_weight
        self.fitness = self.cal_fitness()

    @classmethod
    def mutated_genes(cls):
        # Randomly pick whether to include an item (1) or not (0)
        return random.choice([0, 1])

    @classmethod
    def create_gnome(cls, items):
        # Randomly generate a chromosome based on the number of items
        return [cls.mutated_genes() for _ in range(len(items))]

    def mate(self, par2):
        # Perform single-point crossover
        crossover_point = random.randint(0, len(self.chromosome) - 1)
        child_chromosome = self.chromosome[:crossover_point] + par2.chromosome[crossover_point:]
        return Individual(child_chromosome, self.items, self.max_weight)

    def cal_fitness(self):
        total_value = 0
        total_weight = 0
        for i in range(len(self.chromosome)):
            if self.chromosome[i] == 1:
                total_value += self.items[i][0]
                total_weight += self.items[i][1]
        
        # Penalize solutions that exceed the weight limit
        if total_weight > self.max_weight:
            return 0
        return total_value

    def print_selected_items(self):
        total_value = 0
        total_weight = 0
        selected_items = []
        for i in range(len(self.chromosome)):
            if self.chromosome[i] == 1:
                selected_items.append(i + 1)  # Store the index of the selected item (1-based)
                total_value += self.items[i][0]
                total_weight += self.items[i][1]
        
        print(f"Selected Items: {selected_items}")
        print(f"Total Value: {total_value}")
        print(f"Total Weight: {total_weight}")

def tournament_selection(population, tournament_size=5):
    # Tournament selection: pick the best individual from a random subset of the population
    tournament = random.sample(population, tournament_size)
    tournament = sorted(tournament, key=lambda x: x.fitness, reverse=True)
    return tournament[0]

def main():
    # Take user input
    max_weight = int(input("Enter the maximum weight capacity of the knapsack: "))
    n_items = int(input("Enter the number of items: "))
    
    items = []
    for i in range(n_items):
        value = int(input(f"Enter value for item {i + 1}: "))
        weight = int(input(f"Enter weight for item {i + 1}: "))
        items.append((value, weight))
    
    population_size = int(input("Enter the population size: "))

    generation = 1
    found = False
    population = [Individual(Individual.create_gnome(items), items, max_weight) for _ in range(population_size)]
    
    while not found:
        # Sort the population by fitness (descending order)
        population = sorted(population, key=lambda x: x.fitness, reverse=True)

        # Check if the best individual has been found
        if population[0].fitness > 0:
            found = True
            break

        # Create a new generation using elitism and crossover
        new_generation = []

        # Perform elitism: top 10% of the population goes to the next generation
        s = int((10 * population_size) / 100)
        new_generation.extend(population[:s])

        # Perform crossover for the remaining individuals
        s = int((90 * population_size) / 100)
        for _ in range(s):
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)
            child = parent1.mate(parent2)
            new_generation.append(child)

        population = new_generation

        # Print generation info
        print(f"Generation: {generation}")
        print(f"Best Fitness: {population[0].fitness}")
        generation += 1

    print("\nFinal Result:")
    print(f"Best Knapsack Value: {population[0].fitness}")
    population[0].print_selected_items()  # Print selected items, value, and weight

if __name__ == '__main__':
    main()
