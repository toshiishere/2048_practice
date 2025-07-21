import numpy as np
import matplotlib.pyplot as plt
import random
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed
from game_engine import Game2048

def simulate_game(_):
    game = Game2048()
    while not game.is_game_over():
        # pick and apply a random move
        moved = random.choice([
            game.move_down(),
            game.move_up(),
            game.move_left(),
            game.move_right()
        ])
        if moved:
            game.spawn()
    return game.score

if __name__ == '__main__':
    times = 100000

    # Run simulations in parallel
    scores = []
    with ProcessPoolExecutor(max_workers=8) as executor:
        # submit all tasks
        futures = [executor.submit(simulate_game, i) for i in range(times)]
        # collect results as they complete
        for f in tqdm(as_completed(futures), total=times, desc="Simulating"):
            scores.append(f.result())

    # Build and plot the histogram
    num_bins = 50
    hist, bin_edges = np.histogram(scores, bins=num_bins)
    x = (bin_edges[:-1] + bin_edges[1:]) / 2
    y = hist

    plt.plot(x, y, marker='o')
    plt.xlabel('Score')
    plt.ylabel('Number of Games')
    plt.title(f'Distribution of 2048 Scores over {times} Random Games')
    plt.grid(True)
    plt.show()
