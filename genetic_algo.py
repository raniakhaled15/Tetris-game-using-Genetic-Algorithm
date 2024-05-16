import tetris_base as t
import numpy as np
import random
import chromosome as chromosome
np.random.seed(25)


def calc_heights(board):
    # return the heights of each column in the board
    heights = [0 for _ in range(t.BOARDWIDTH)]
    for x in range(t.BOARDWIDTH):
        for y in range(t.BOARDHEIGHT):
            if board[x][y] != t.BLANK:
                heights[x] = np.abs(t.BOARDHEIGHT - y)
                break

    return heights


def calc_bumpiness(heights):
    # return the bumpiness of the board
    # bumpiness is the sum of the absolute differences between the heights of each pair of adjacent columns
    bumpiness = 0
    for i in range(t.BOARDWIDTH - 1):
        bumpiness += np.abs(heights[i] - heights[i + 1])
    return bumpiness


def calc_wells(heights):
    # return the wells of the board
    # wells are the holes that are surrounded by blocks on both sides
    wells = []
    for i in range(len(heights)):
        if i == 0:
            well = heights[1] - heights[0]
            if well <= 0:
                well = 0
        elif i == len(heights) - 1:
            well = heights[i] - heights[i - 1]
            if well <= 0:
                well = 0
        else:
            well1 = heights[i - 1] - heights[i]
            well2 = heights[i + 1] - heights[i]
            well1 = max(0, well1)
            well2 = max(0, well2)
            well = max(well1, well2)
        wells.append(well)
    return wells


def calc_num_wells(wells):
    count = 0
    for well in wells:
        if well > 0:
            count += 1
    return count

def calc_heuristics(board, x):
    """Calculate heuristics

    The heuristics are composed by: number of holes, number of blocks above
    hole and maximum height.

    """
    total_holes = 0
    locals_holes = 0
    blocks_above_holes = 0
    sum_heights = 0

    for y in range(t.BOARDHEIGHT - 1, -1, -1):
        if board[x][y] == t.BLANK:
            locals_holes += 1
        else:
            sum_heights += t.BOARDHEIGHT - y

            if locals_holes > 0:
                total_holes += locals_holes
                locals_holes = 0

            if total_holes > 0:
                blocks_above_holes += 1

    return total_holes, blocks_above_holes, sum_heights


def calc_holes_and_blocking_blocks(board):
    total_holes = 0
    total_blocking_blocks = 0

    for x2 in range(0, t.BOARDWIDTH):
        b = calc_heuristics(board, x2)

        total_holes += b[0]
        total_blocking_blocks += b[1]

    return total_holes, total_blocking_blocks


def generate_pop(num_pop):
    # generate a random population of chromosomes
    population = []
    for i in range(num_pop):
        weights = [random.uniform(-15, 15) for _ in range(9)]
        population.append(chromosome.Chromosome(weights))

    return population


def calculate_fitness_score(score, num_of_played_pieces, win):
    # calculate fitness by getting the avg of points by each played piece
    if win:
        return score/num_of_played_pieces
    else:
        return score/600


def parents_selection(population, num_parents):
    # select the parents based on the roulette wheel selection
    total_fitness = sum([chromo.score for chromo in population])
    selected_parents = []
    for _ in range(num_parents):
        # pick a random number between 0 and the total fitness
        pick = random.uniform(0, total_fitness)
        # iterate through the population and select the chromosome that corresponds to the random number
        current = 0
        for chromo in population:
            current += chromo.score
            if current > pick:
                selected_parents.append(chromo)
                break  # break the loop once you find the chromosome that is greater than the random number

    return selected_parents


def crossover(parents):
    offspring = []
    for i in range(len(parents)):
        for j in range(i+1, len(parents)):
            offspring.append(crossover_two_parents(parents[i], parents[j]))
    return offspring


def crossover_two_parents(parent1, parent2):
    # divides each chromosome in half
    split_point = len(parent1.weights) // 2
    # create a new offspring chromosomes by combining halves of genes from each parent
    offspring = parent1.weights[:split_point] + parent2.weights[split_point:]
    return offspring


def mutation(chromosomes, mutation_rate):
    mutated_chromosomes = []
    # iterate through each chromosome and mutate it based on the mutation rate
    for c in chromosomes:
        chromo = chromosome.Chromosome(c)
        # if the random number is less than the mutation rate, mutate the chromosome
        if random.random() < mutation_rate:
            random_int = random.randint(0, 5)
            chromo.weights[random.randint(0, 5)] = random.uniform(-15.0, 15.0)
        mutated_chromosomes.append(chromo)
    return mutated_chromosomes
