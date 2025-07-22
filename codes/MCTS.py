from game_engine import Game2048
import numpy as np
import matplotlib.pyplot as plt
import random
from tqdm import tqdm

C=np.sqrt(2)
depth=10
MCTS_time=1000

moves = [
            Game2048.move_down,
            Game2048.move_up,
            Game2048.move_left,
            Game2048.move_right
        ]

class node:
    def __init__(self,parent,game,visited=0):
        self.game=game
        self.parent=parent
        self.childs=[]
        self.w=0
        self.n=0
        self.visited=visited

    def select(self):
        if(not self.visited):return self
        UCBs=[]
        UCBs = (self.calc_UCB(i) for i in self.child)
        return self.childs[np.argmax(np.array(UCBs))].select() #recursively find the leaf node
    
    def calc_UCB(self):
        if(not self.visited): return float('inf')
        explore=C*np.sqrt(np.log(self.parent.n//self.n))
        exploit=self.w//self.n
        return explore+exploit

    def expand(self):
        for move in moves:
            new_game = Game2048(self.game)
            if move(new_game):
                self.childs.append(node(self, new_game, 0))
            else:
                self.childs.append(node(self, new_game, 1))#cannot move, treated as if visited
        
    def rollout(self):
        new_game = Game2048(self.game)
        self.visited=1
        depth=0
        while True:
            if new_game.is_game_over() or depth>10:
                return np.log2(new_game.score)/2 - 3    #return log of the score as if it is 2, 1, 0 score
            move = random.choice(moves)
            if move(new_game):
                new_game.spawn()
                depth+=1

    def backpropagate(self,score=0):
        if(self.parent):
            self.w+=score
            self.n+=1
            self.parent.backpropagate
    
def calc_result(game):
    root=node(False,game)
    node.expand()
    root.visited=1
    for i in range(MCTS_time):
        point=root.select()
        if(point.visited):point.expand()
        else: score=point.rollout()
        point.backpropagate(score)

    scores=np.array()
    for i in root.childs:
        scores.append(i.w//i.n)
    return moves[np.argmax(scores)]
        



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