import math
import random
from typing import List
import copy

class City:
    def __init__(self, id: str, x: int, y: int):
        self.id = str(id)
        self.x = x
        self.y = y

    def __eq__(self, other: 'City'):
        return self.id == other.id

class Individual:
    def __init__(self, citiesSequence: str):
        self.citiesSequence = citiesSequence
        self.value = None

    def evaluate(self, dist_dictionary):
        self.value = 0
        for i in range(len(self.citiesSequence) - 1):
            self.value += dist_dictionary[str(self.citiesSequence[i])][str(self.citiesSequence[i + 1])]

    def __eq__(self, other: 'Individual'):
        return self.citiesSequence == other.citiesSequence

def generate_random_cities(numCities: int) -> List[City]:
    cities = []
    for i in range(numCities):
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        cities.append(City(i, x, y))
    return cities

def get_distance(a: City, b: City) -> float:
    return math.sqrt( (a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y))

def gen_dic_with_distance_given_cities(cities: City):
    dist_dict = {c.id:{} for c in cities}
    for idx_1 in range(len(cities)):
        for idx_2 in range(len(cities)):
            city_a = cities[idx_1]
            city_b = cities[idx_2]
            dist = get_distance(city_a, city_b)
            dist_dict[city_a.id][city_b.id] = dist
    return dist_dict

def generate_n_permutations(citiesIds: List[int], n: int) -> List[List[int]]:
    permutations = []
    for i in range(n):
        currPerm = list(citiesIds)
        random.shuffle(currPerm)
        permutations.append(currPerm)
    return permutations

def selection(population: List[Individual]) -> List[Individual]:
    population.sort(key=lambda x: x.value)
    index = int(round((1 / 5) * len(population)))
    if index % 2 == 1:
        index += 1

    return population[0: index]


def cross_parents(parents: List[Individual]) -> List[Individual]:
    if len(parents) % 2 == 1:
        print('Given parents not even number')
        return
    i = 0
    children = []
    while i <= len(parents) - 2:
        ch1, ch2 = crossover_individuals(parents[i], parents[i + 1])
        children.append(ch1)
        children.append(ch2)
        i += 2
    return children

def crossover_individuals(parent1: Individual, parent2: Individual) -> (Individual, Individual):
    ch1, ch2 = crossover_str(parent1.citiesSequence, parent2.citiesSequence)
    return (Individual(ch1), Individual(ch2))

# One point crossover
def crossover_str(parent1: List[int], parent2: List[int]) -> (str, str):
    k = random.randint(1, len(parent1) - 1)
    child1 = parent1[:k]
    child2 = parent2[:k]

    i = 0
    while len(child1) != len(parent2):
        if parent2[i] not in child1:
            child1.append(parent2[i])
        i += 1
    
    i = 0
    while len(child2) != len(parent1):
        if parent1[i] not in child2:
            child2.append(parent1[i])
        i += 1

    return (child1, child2)


# mutate just part of given individuals
def mutation(individuals: List[Individual]):
    for i in range(len(individuals)):
        randInt = random.randint(1, 100)
        if (randInt <= 20): # 20% chance
            mutate(individuals[i])

def mutate(individual: Individual):
    num = len(individual.citiesSequence)
    ind1 = random.randint(0, num - 1)
    ind2 = random.randint(0, num - 1)

    # swap
    individual.citiesSequence[ind1], individual.citiesSequence[ind2] =\
        individual.citiesSequence[ind2], individual.citiesSequence[ind1]

def genetic_alg(N: int):
    cities = generate_random_cities(N)
    dist_dict = gen_dic_with_distance_given_cities(cities)

    citiesStrings = []
    for i in range(N):
        citiesStrings.append(i)

    permutations = generate_n_permutations(citiesStrings, N)  # Think if N is big enough
    population = []
    for i in range(len(permutations)): # == range(N)
        individual = Individual(permutations[i])
        individual.evaluate(dist_dict)
        population.append(individual)

    generationLimit = N * 75
    iter = 0

    while iter <= generationLimit:
        # Selection
        parents = selection(population)

        # Crossover
        children = cross_parents(parents)

        # Mutation, just part of them mutate
        mutation(children)
        
        # Evaluate children
        for i in range(len(children)):
            children[i].evaluate(dist_dict)

        # add to population only if not still added same individuals
        for i in range(len(children)):
            if children[i] not in population:
                population.append(children[i])

        # Normalize population size
        population.sort(key=lambda x: x.value)
        population = population[:N]

        iter += 1

        if iter == 10 or iter == N * 10 or iter == 50 * N or iter == 25 * N:
            print('Population № ' + str(iter) + ' - ' + str(population[0].value))

    print('Population № ' + str(iter) + '(end of alg) - ' + str(population[0].value))


genetic_alg(20)
