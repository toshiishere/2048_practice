from game_engine import Game2048
from MCTS import Node
import numpy as np
import copy

mcts_time=1000
# moves = [
#             "move_down",
#             "move_up",
#             "move_left",
#             "move_right"
#         ]
moves=['s','w','a','d']

def console_play():
    # Simple cross-platform getch
    try:
        import msvcrt
        def getch():
            return msvcrt.getch().decode().lower()
    except ImportError:
        import sys, tty, termios
        def getch():
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)
            return ch.lower()

    game = Game2048()
    while True:
        game.print_grid()
        if game.is_game_over():
            print("Game Over!")
            break
        print("Use WASD to move (W=up, S=down, A=left, D=right, T=hint from ai). Press Q to quit.")
        # ch = getch()
        ch=asking(game)
        moved = False
        if ch == 'w':
            moved = game.move_up()
        elif ch == 's':
            moved = game.move_down()
        elif ch == 'a':
            moved = game.move_left()
        elif ch == 'd':
            moved = game.move_right()
        elif ch == 't':
            print(asking(game))
        elif ch == 'q':
            print("Quit!")
            break
        if moved:
            game.spawn()

def asking(game):
    root = Node(None, copy.deepcopy(game), visited=True)
    root.expand()
    # Run MCTS iterations
    for _ in range(mcts_time):
        leaf = root.select()
        # Expand leaf if it's unvisited
        if not leaf.visited:
            leaf.expand()
        score = leaf.rollout()
        leaf.backpropagate(score)

    # Choose the move whose child has highest average reward
    avg_scores = [child.w / child.n if child.n > 0 else -np.inf for child in root.children]
    best_idx = int(np.argmax(avg_scores))
    return moves[best_idx]



if __name__ == "__main__":
    console_play()
