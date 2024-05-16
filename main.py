import genetic_algo as ga
import play_ai as ai
import copy
import chromosome as chromosome
import numpy as np
np.random.seed(25)


def get_best_two(generation):
    best_chromo = generation[0]
    for g in generation:
        if g.fitness_score > best_chromo.fitness_score:
            best_chromo = g
    second_best_chromo = generation[1]
    for g in generation:
        if g.fitness_score > second_best_chromo.fitness_score and g != best_chromo:
            second_best_chromo = g
    return [best_chromo, second_best_chromo]


def train():
    population_num = 20
    mut_rate = 0.2
    evaluation_num = 19
    init_pop = ga.generate_pop(population_num)
    generations = []
    pp = 1
    pop = copy.deepcopy(init_pop)
    best_two_over_generations = []
    for i in range(evaluation_num):
        best_two_over_generations.append(get_best_two(pop))
        for chrom in pop:
            game_state = ai.play_game(chrom, 600, 20000)
            chrom.fitness_score = ga.calculate_fitness_score(game_state[1], game_state[0], game_state[2]) + game_state[2] * 500
            chrom.scores.append(chrom.fitness_score)
            print(pp)
            pp += 1
        selected_parents = ga.parents_selection(pop, 7)
        offspring = ga.crossover(selected_parents)
        mutated_children = ga.mutation(offspring, mut_rate)
        generations = mutated_children
        pop = generations
        best_two_over_generations.append(get_best_two(generations))
        print("generation:", i+1)
    for g in generations:
        game_state = ai.play_game(g, 600, 20000)
        g.score = game_state[1]
        g.fitness_score = ga.calculate_fitness_score(game_state[1], game_state[0], game_state[2])
        g.scores.append(g.fitness_score)
        print(pp)
        pp += 1
    best_chromo, second_best_chromo = best_two_over_generations(generations)
    print(best_chromo.weights)
    print(best_chromo.fitness_score)
    print(second_best_chromo.weights)
    print(second_best_chromo.fitness_score)
    # Open a file in append mode
    with open('output.txt', 'a') as file:
        # Append content to the file
        for w in best_chromo.weights:
            file.write(str(w) + '\n')
        file.write(str(best_chromo.fitness_score)+'\n')
        for w in second_best_chromo.weights:
            file.write(str(w) + '\n')
        file.write(str(best_chromo.fitness_score)+'\n')

    ai.play_game(best_chromo, 600, 10000)


def main():
    choice = int(input("1-train\n2-test\n"))
    if choice == 1:
        train()
    elif choice == 2:
        optimal_weights = [-1.7805889055979645, -5.5895424820377375, 0.43600461690098413, -0.44424023508529586, 3.056983896157945, -11.90924387515746, 12.28318497820915, 12.035482528534502, 7.870694757392034]
        ai.play_game(chromosome.Chromosome(optimal_weights), 600, 10000)


if __name__ == '__main__':
    main()
