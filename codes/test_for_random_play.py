from game_engine import Game2048
import numpy as np
import matplotlib.pyplot as plt
import random
from tqdm import tqdm

times = 10000

scores = []

for i in tqdm(range(times)):
    game = Game2048()
    while True:
        if game.is_game_over():
            scores.append(game.score)
            break
        # Try a random move; if it succeeds, spawn a new tile
        moved = random.choice([
            game.move_down(),
            game.move_up(),
            game.move_left(),
            game.move_right()
        ])
        if moved:
            game.spawn()

# Compute a histogram with, say, 50 bins
num_bins = 50
hist, bin_edges = np.histogram(scores, bins=num_bins)

# For plotting, use the midpoints of each bin
x = (bin_edges[:-1] + bin_edges[1:]) / 2
y = hist

plt.plot(x, y, marker='o')
plt.xlabel('Score')
plt.ylabel('Number of Games')
plt.title(f'Distribution of 2048 Scores over {times} Random Games')
plt.grid(True)
plt.show()
