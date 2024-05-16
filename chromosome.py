# import genetic_algo as ga
import tetris_base as t


class Chromosome:
    def __init__(self, weights):
        # Initialize the chromosome with random genetic information
        self.fitness_score = 0
        self.weights = weights
        self.scores = []

    def calculate_fitness(self, fitness):
        # Calculate the fitness of the chromosome based on game performance
        # Update self.fitness accordingly
        self.fitness_score = fitness

    def get_best_position(self, board, piece, show_game=False):
        best_score = -5000
        best_x = 0
        best_r = 0
        best_y = 0
        num_holes_bef, num_blocking_blocks_bef, heights_bef = t.calc_initial_move_info(board)
        for r in range(len(t.PIECES[piece['shape']])):
            for x in range(-2, t.BOARDWIDTH - 2):
                move_info = t.calc_move_info(board, piece, x, r, num_holes_bef, num_blocking_blocks_bef, heights_bef)
                if move_info[0]:
                    move_score = 0
                    for i in range(1, len(move_info)):
                        move_score += self.weights[i-1] * move_info[i]
                    if move_score > best_score:
                        best_score = move_score
                        best_x = x
                        best_r = r
                        best_y = piece['y']
        if show_game:
            piece['y'] = best_y
        else:
            piece['y'] = -2
        piece['x'] = best_x
        piece['rotation'] = best_r
        piece['y'] = best_y
        return best_score, best_r, best_x, best_y
