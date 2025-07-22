from game_engine import Game2048
import numpy as np
import matplotlib.pyplot as plt
import random
from tqdm import tqdm
import copy

C=np.sqrt(2)
default_ROLLOUT_DEPTH = 50
MCTS_time=1000

moves = [
            Game2048.move_down,
            Game2048.move_up,
            Game2048.move_left,
            Game2048.move_right
        ]

class Node:
    def __init__(self,parent,game,visited=False):
        self.game=game
        self.parent=parent
        self.children=[]
        self.w=0.0
        self.n=0
        self.visited=visited

    def select(self):
        if not self.visited or not self.children: return self
        ucb_values = [child.calc_ucb() for child in self.children]
        best_idx = int(np.argmax(ucb_values))
        return self.children[best_idx].select()
    
    def calc_ucb(self):
        if (not self.visited or self.n == 0): return float('inf')
        explore=C*np.sqrt(np.log(self.parent.n/self.n))
        exploit=self.w//self.n
        return explore+exploit

    def expand(self):
        for move in moves:
            new_game = copy.deepcopy(self.game)
            if move(new_game):
                new_game.spawn()
                self.children.append(Node(self, new_game, visited=False))
            else:
                self.children.append(Node(self, new_game, visited=True))#TODO not sure if this work
        self.visited = True
        
    #TODO should be score diff from original rather than f(score)
    def rollout(self):
        new_game = copy.deepcopy(self.game)
        depth=0
        while not new_game.is_game_over() and depth < default_ROLLOUT_DEPTH:
            move = random.choice(moves)
            if move(new_game):
                new_game.spawn()
                depth+=1
        return np.log2(new_game.score)/2 - 3    #return log of the score as if it is 2, 1, 0 score

    def backpropagate(self,score=0):
        self.w+=score
        self.n+=1
        if self.parent is not None:
            self.parent.backpropagate(score)
    
def calc_result(game):
    root = Node(None, copy.deepcopy(game), visited=True)
    root.expand()#first expand should ensure all the moves are valid TODO
    root.visited=1
    for _ in range(MCTS_time):
        leaf=root.select()
        if(not leaf.visited):leaf.expand()
        score=leaf.rollout()
        leaf.backpropagate(score)

    avg_scores = [child.w / child.n if child.n > 0 else -np.inf for child in root.children]
    best_idx = int(np.argmax(avg_scores))
    return moves[best_idx]
        

if __name__ == "__main__":

    times = 100
    scores = []

    for i in tqdm(range(times)):
        game = Game2048()
        while True:
            if game.is_game_over():
                scores.append(game.score)
                break

            # implement MCTS
            choice = calc_result(game)
            if choice(game):
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