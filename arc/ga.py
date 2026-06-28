import numpy as np


def create_population(pop_size, vector_length, min_val, max_val):
    """Create an initial population of random integer vectors."""
    return np.random.randint(min_val, max_val + 1, size=(pop_size, vector_length))


def evaluate_fitness(population, objective_function):
    """Evaluate the fitness of each individual in the population."""
    fitness_values = np.array([objective_function(vector) for vector in population])
    return fitness_values


def select_parents(population, fitness_values):
    """Select parents based on fitness using tournament selection."""
    tournament_size = 3
    selected_parents = []

    for _ in range(len(population)):
        tournament_indices = np.random.choice(len(population), tournament_size, replace=False)
        tournament_fitness = fitness_values[tournament_indices]
        winner_index = tournament_indices[np.argmax(tournament_fitness)]
        selected_parents.append(population[winner_index])

    return np.array(selected_parents)


def crossover(parents, crossover_rate):
    """Perform crossover to create offspring."""
    num_parents, vector_length = parents.shape
    num_offspring = num_parents // 2
    offspring = np.empty((num_offspring, vector_length), dtype=int)

    for i in range(0, num_offspring - 1, 2):
        if np.random.rand() < crossover_rate:
            crossover_point = np.random.randint(1, vector_length - 1)
            parent1 = parents[i]
            parent2 = parents[i + 1]
            offspring[i, :] = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
            offspring[i + 1, :] = np.concatenate((parent2[:crossover_point], parent1[crossover_point:]))
        else:
            offspring[i, :] = parents[i]
            offspring[i + 1, :] = parents[i + 1]

    return offspring


def mutate(offspring, mutation_rate, min_val, max_val):
    """Perform mutation on the offspring."""
    num_offspring, vector_length = offspring.shape

    for i in range(num_offspring):
        for j in range(vector_length):
            if np.random.rand() < mutation_rate:
                # Mutate by adding a random integer in the range [min_val, max_val]
                offspring[i, j] += np.random.randint(-1, 2)  # Add -1, 0, or 1
                offspring[i, j] = np.clip(offspring[i, j], min_val, max_val)

    return offspring


def genetic_algorithm(pop_size, vector_length, generations, min_val, max_val, objective_function):
    """Genetic algorithm to optimize a given objective function."""
    crossover_rate = 0.8
    mutation_rate = 0.01

    # Step 1: Initialize population
    population = create_population(pop_size, vector_length, min_val, max_val)

    for generation in range(generations):
        # Step 2: Evaluate fitness
        fitness_values = evaluate_fitness(population, objective_function)

        # Step 3: Select parents
        parents = select_parents(population, fitness_values)

        # Step 4: Crossover
        offspring = crossover(parents, crossover_rate)

        # Step 5: Mutation
        offspring = mutate(offspring, mutation_rate, min_val, max_val)

        # Step 6: Replace old population with new population
        population[:len(offspring)] = offspring

        # Optional: Monitor and print the best solution in each generation
        best_index = np.argmax(fitness_values)
        best_solution = population[best_index]
        best_fitness = fitness_values[best_index]
        print(f"Generation {generation + 1}: Best Fitness = {best_fitness}, Best Solution = {best_solution}")

    # Return the best solution found
    best_index = np.argmax(fitness_values)
    best_solution = population[best_index]
    return best_solution, fitness_values[best_index]


# Example usage:
def objective_function(vector):
    """Example objective function to maximize."""
    return -np.sum(np.square(vector))  # Negate for maximization


pop_size = 50
vector_length = 10
generations = 100
min_val = -10
max_val = 10

best_solution, best_fitness = genetic_algorithm(pop_size, vector_length, generations, min_val, max_val,
                                                objective_function)

print("\nOptimal Solution:")
print(f"Vector: {best_solution}")
print(f"Objective Function Value: {best_fitness}")
