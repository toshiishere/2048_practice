#!/usr/bin/env python3
"""
2048 Game in Python.
Usage:
    python 2048_game.py         # Console mode
    python 2048_game.py --gui   # GUI mode with tkinter
"""

import random
import sys

class Game2048:
    def __init__(self, size=4):
        self.size = size
        self.grid = [[0]*size for _ in range(size)]
        self.score = 0
        self.spawn()
        self.spawn()

    def spawn(self):
        empty = [(i, j) for i in range(self.size) for j in range(self.size) if self.grid[i][j] == 0]
        if not empty:
            return
        i, j = random.choice(empty)
        self.grid[i][j] = 4 if random.random() < 0.1 else 2

    def compress(self, row):
        new_row = [num for num in row if num != 0]
        new_row += [0] * (self.size - len(new_row))
        return new_row

    def merge(self, row):
        for i in range(self.size - 1):
            if row[i] != 0 and row[i] == row[i+1]:
                row[i] *= 2
                self.score += row[i]
                row[i+1] = 0
        return row

    def move_left(self):
        moved = False
        for i in range(self.size):
            original = list(self.grid[i])
            row = self.compress(self.grid[i])
            row = self.merge(row)
            row = self.compress(row)
            self.grid[i] = row
            if row != original:
                moved = True
        return moved

    def move_right(self):
        self.reverse()
        moved = self.move_left()
        self.reverse()
        return moved

    def move_up(self):
        self.transpose()
        moved = self.move_left()
        self.transpose()
        return moved

    def move_down(self):
        self.transpose()
        moved = self.move_right()
        self.transpose()
        return moved

    def reverse(self):
        for i in range(self.size):
            self.grid[i].reverse()

    def transpose(self):
        self.grid = [list(row) for row in zip(*self.grid)]

    def can_move(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    return True
                if j+1 < self.size and self.grid[i][j] == self.grid[i][j+1]:
                    return True
                if i+1 < self.size and self.grid[i][j] == self.grid[i+1][j]:
                    return True
        return False

    def is_game_over(self):
        return not self.can_move()

    def print_grid(self):
        print(f"Score: {self.score}")
        for row in self.grid:
            print('+------' * self.size + '+')
            print(
                ''.join(
                    f"|{str(num).center(6) if num != 0 else '      '}" 
                    for num in row
                ) + '|'
            )

        print('+------' * self.size + '+')


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
        print("Use WASD to move (W=up, S=down, A=left, D=right). Press Q to quit.")
        ch = getch()
        moved = False
        if ch == 'w':
            moved = game.move_up()
        elif ch == 's':
            moved = game.move_down()
        elif ch == 'a':
            moved = game.move_left()
        elif ch == 'd':
            moved = game.move_right()
        elif ch == 'q':
            print("Quit!")
            break
        if moved:
            game.spawn()

# GUI version using tkinter
try:
    import tkinter as tk
    from tkinter import messagebox
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False


def gui_play():
    if not GUI_AVAILABLE:
        print("Tkinter not available. Please install tkinter to play GUI mode.")
        return
    game = Game2048()
    root = tk.Tk()
    root.title("2048")
    cells = []
    for i in range(game.size):
        row = []
        for j in range(game.size):
            frame = tk.Frame(root, width=100, height=100, bd=2, relief='ridge')
            frame.grid(row=i, column=j)
            label = tk.Label(frame, text='', font=('Arial', 24), width=4, height=2)
            label.pack()
            row.append(label)
        cells.append(row)

    def update_ui():
        for i in range(game.size):
            for j in range(game.size):
                value = game.grid[i][j]
                cells[i][j].config(text=str(value) if value != 0 else '')
        root.update_idletasks()

    def key_handler(event):
        key = event.keysym
        moved = False
        if key == 'Up':
            moved = game.move_up()
        elif key == 'Down':
            moved = game.move_down()
        elif key == 'Left':
            moved = game.move_left()
        elif key == 'Right':
            moved = game.move_right()
        if moved:
            game.spawn()
            update_ui()
            if game.is_game_over():
                messagebox.showinfo("2048", f"Game Over! Score: {game.score}")

    root.bind("<Key>", key_handler)
    update_ui()
    root.mainloop()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Play 2048 in console or GUI.")
    parser.add_argument('--gui', action='store_true', help='Enable GUI mode')
    args = parser.parse_args()
    if args.gui:
        gui_play()
    else:
        console_play()
