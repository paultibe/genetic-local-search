import random
import numpy as np

constraints = [
    lambda node: node['A'] > node['G'] if 'A' in node and 'G' in node else True,  # A > G
    lambda node: node['A'] <= node['H'] if 'A' in node and 'H' in node else True,  # A ≤ H
    lambda node: abs(node['F'] - node['B']) == 1 if 'F' in node and 'B' in node else True,  # |F-B| = 1
    lambda node: node['G'] < node['H'] if 'G' in node and 'H' in node else True,  # G < H
    lambda node: abs(node['G'] - node['C']) == 1 if 'G' in node and 'C' in node else True,  # |G-C| = 1
    lambda node: (node['H'] - node['C']) % 2 == 0 if 'H' in node and 'C' in node else True,  # |H-C| is even
    lambda node: node['H'] != node['D'] if 'H' in node and 'D' in node else True,  # H != D
    lambda node: node['D'] >= node['G'] if 'D' in node and 'G' in node else True,  # D ≥ G
    lambda node: node['D'] != node['C'] if 'D' in node and 'C' in node else True,  # D != C
    lambda node: node['E'] != node['C'] if 'E' in node and 'C' in node else True,  # E != C
    lambda node: node['E'] < node['D'] - 1 if 'E' in node and 'D' in node else True,  # E < D-1
    lambda node: node['E'] != node['H'] - 2 if 'E' in node and 'H' in node else True,  # E != H-2
    lambda node: node['G'] != node['F'] if 'G' in node and 'F' in node else True,  # G != F
    lambda node: node['H'] != node['F'] if 'H' in node and 'F' in node else True,  # H != F
    lambda node: node['C'] != node['F'] if 'C' in node and 'F' in node else True,  # C != F
    lambda node: node['D'] != node['F'] - 1 if 'D' in node and 'F' in node else True,  # D != F-1
    lambda node: abs(node['E'] - node['F']) % 2 == 1 if 'E' in node and 'F' in node else True,  # |E-F| is odd
]

variables = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

initial_population = [1,1,1,1,1,1,1,1], [2,2,2,2,2,2,2,2], [3,3,3,3,3,3,3,3], [4,4,4,4,4,4,4,4], [1,2,3,4,1,2,3,4], [4,3,2,1,4,3,2,1], [1,2,1,2,1,2,1,2], [3,4,3,4,3,4,3,4]


# helper function for compute_fitness_scores
def num_constraints_satisfied(node):
  result = 0
  for constraint in constraints:
    if constraint(node):
      result += 1
  
  return result

# converts an array of 8 digits to a dictionary with values assigned to the eight variables in our CSP
def convert_to_node(individual):
  node = {}
  # initialize dictionary with values of 0
  # enumerate produces index-value pairs
  for i, var in enumerate(variables):
    node[var] = individual[i]
  return node


# population is 2D array containing the eight individuals in our population
def compute_fitness_scores(population):
  result = []
  for i in range(0, 8):
    node = convert_to_node(population[i])
    result.append(num_constraints_satisfied(node))
  print(f"Fitness scores computed: {result}")
  return result

def compute_probabilities(scores):
  probs = []
  sum = 0
  for score in scores:
    sum += score

  for i in range(0, 8):
    probs.append(scores[i] / sum)

  print(f"Probabilities computed: {probs}")
  return probs

def run_genetic_algorithm(init_population, num_generations):
  # domains = {var: [1, 2, 3, 4] for var in variables} # dictionary for domains. eg. A: [1,2,3,4]
  # evolve population num_generations times
  population = init_population
  for generation in range(num_generations):
      population = evolve_population(population)
      print(f"Generation {generation} evolved\n")
      print(f"New population: {population}")

# evolve population
def evolve_population(population):
    scores = compute_fitness_scores(population)
    probabilities = compute_probabilities(scores)
    parents = select_parents(population, probabilities)
    next_generation = create_next_generation(parents)
    return next_generation

# select parents based on probabilities. parents MUST be different for each pair.
def select_parents(population, probabilities):
    selected_parents = []
    num_pairs = 4 

    for _ in range(num_pairs):
        # randomly select two different according to probability distribution
        # numpy implicitly does np.arrange(len(population)) to generate indices for the population
        parent_indices = np.random.choice(len(population), size=2, replace=False, p=probabilities)
        # create new tuple of parent pair
        pair = (population[parent_indices[0]], population[parent_indices[1]])
        selected_parents.append(pair)

    print(f"Parents selected: {selected_parents}")
    return selected_parents

# Create the next generation from selected parents
def create_next_generation(parents):
    next_generation = []
    # cross over and mutate (maybe) each pair of parents
    for i in range(len(parents)):
        # perform_crossover returns two offspring
        offspring1, offspring2 = perform_crossover(parents[i][0], parents[i][1])
        # maybe mutate each offspring
        offspring1 = maybe_mutate(offspring1, i*2)
        offspring2 = maybe_mutate(offspring2, (i*2) + 1)
        # add offspring to the next generation
        next_generation.append(offspring1)
        next_generation.append(offspring2)
    return next_generation
# 
def perform_crossover(parent1, parent2):
    # to avoid extremes
    # crossover_point is the index before which we draw the separating line
    crossover_point = random.randint(1, len(parent1) - 2)
    print(f"Crossoverpoint selected: {crossover_point}")

    # each parent is split into two chunks based on crossover point
    parent1_chunk1 = parent1[0:crossover_point]
    parent1_chunk2 = parent1[crossover_point:]
    parent2_chunk1 = parent2[0:crossover_point]
    parent2_chunk2 = parent2[crossover_point:]

    # do crossover
    # append the chunks into single array
    offspring1 = parent1_chunk1 + parent2_chunk2
    offspring2 = parent2_chunk1 + parent1_chunk2
    print(f"Offspring produced: {offspring1, offspring2}")
    return offspring1, offspring2

def maybe_mutate(individual, individual_index):
    mutation_chance = 0.3 
    # random.random() generates a value between 0.0 and 1.0 including 0.0 but excluding 1.0
    if random.random() < mutation_chance:
        # do mutation:
        # randomly select variable
        mutation_index = random.randint(0, len(individual) - 1)
        # randomly assign new value between 1 and 4
        previous = individual[mutation_index]
        new = random.randint(1, 4)
        individual[mutation_index] = new
        print(f"Individual {individual_index} mutated! Variable {variables[mutation_index]} changed from {previous} to {new}")
    return individual

# run!
# run_genetic_algorithm(initial_population, 3)

### TESTING
# print(convert_to_node([1,1,1,1,1,1,1,1]))
# print(maybe_mutate([1,1,1,1,1,1,1,1]))
# perform_crossover([1,2,3,4,1,2,3,4], [1,1,1,1,1,1,1,1])
# print(compute_fitness_scores(initial_population))
# testprobs = compute_probabilities(compute_fitness_scores(initial_population))
# selected_parents = (select_parents(initial_population, testprobs))
# print(create_next_generation(selected_parents))
# # print(num_constraints_satisfied())
initial_population = [1,1,1,1,1,1,1,1], [2,2,2,2,2,2,2,2], [3,3,3,3,3,3,3,3], [4,4,4,4,4,4,4,4], [1,2,3,4,1,2,3,4], [4,3,2,1,4,3,2,1], [1,2,1,2,1,2,1,2], [3,4,3,4,3,4,3,4]
my_population = [[3, 3, 1, 1, 4, 3, 1, 3], [1, 2, 1, 2, 1, 2, 1, 2], [3, 3, 1, 1, 4, 3, 1, 3], [1, 2, 1, 2, 1, 2, 1, 2], [1, 3, 2, 4, 3, 4, 3, 4], [1, 2, 3, 2, 1, 2, 1, 2], [4, 3, 2, 2, 1, 2, 1, 2], [3, 3, 1, 1, 1, 2, 1, 2]]
# print(len(my_population))
probs = compute_fitness_scores(my_population)
compute_probabilities(probs)
