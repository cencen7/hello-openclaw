"""
coding 考了 tiktactoe，自定义行列和胜利条件 followup 模拟ai 下棋，就是调用一下 random api

Coding 是tic-tac-toe 这两道题都准备过 直接用的DSU 都过了 但是写testing的时候特别头疼 自己选了3*4的matrix 然后下棋的顺序function没给 一人一步 所以要自己看要怎么下棋可以满足那个test case

Tic-Tac-Toe
Followup 是让你给function 加一个 boolean param: isAi.当 isAi 的时候自动下一个子。然后要能输赢 or 平局
"""
from typing import List

class TicTacToe:
    def __init__(self):
        self.grid = [[' ' for _ in range(3)] for _ in range(3)]
        self.empty_positions = set((i, j) for i in range(3) for j in range(3))
        self.moves = 0


    def move(self, row: int, col: int, player: int) -> int:
        if (row, col) not in self.empty_positions:
            raise ValueError("Position already occupied")
        self.grid[row][col] = 'X' if player == 1 else 'O'
        self.empty_positions.remove((row, col))
        self.moves += 1

    def check_winner(self) -> int:
        if self.moves < 5:
            return "Pending"
        
        winner = {"X": 1, "O": 2}
        for i in range(3):
            if self.grid[i][0] == self.grid[i][1] and self.grid[i][1] == self.grid[i][2] and self.grid[i][0] != " ":
                return winner[self.grid[i][0]]
            if self.grid[0][i] == self.grid[1][i] and self.grid[1][i] == self.grid[2][i] and self.grid[0][i] != " ":
                return winner[self.grid[0][i]]

        if self.grid[0][0] == self.grid[1][1] and self.grid[1][1] == self.grid[2][2]:
            if self.grid[0][0] != " ":
                return winner[self.grid[0][0]]
        if self.grid[2][0] == self.grid[1][1] and self.grid[1][1] == self.grid[0][2]:
            if self.grid[2][0] != " ":
                return winner[self.grid[2][0]]
        
        return "Draw" if self.moves == 9 else "Pending"
        
    def ai_move(self) -> List[int]:
        import random
        if not self.empty_positions:
            return []
        move = random.choice(list(self.empty_positions))
        self.move(move[0], move[1], 2)
        return [move[0], move[1]]
    

if __name__ == "__main__":
    game = TicTacToe()
    game.move(0, 0, 1)  # A
    game.move(1, 1, 2)  # B
    game.move(0, 1, 1)  # A
    game.move(1, 0, 2)  # B
    game.move(0, 2, 1)  # A wins
    print(game.check_winner())  # Output: 1

    # Followup: AI move
    game = TicTacToe()
    turn = 1  # 1 for player A, 2 for AI B
    while game.check_winner() == "Pending":
        if turn == 1:
            try:
                row, col = map(int, input("Enter your move (row and column): ").split())
                game.move(row, col, 1)
            except ValueError as e:
                print(f"error: {e} Invalid input. Please enter two integers separated by space.")
                continue
            turn = 2
        else:
            ai_move = game.ai_move()
            print(f"AI moved at: {ai_move}")
            turn = 1
        

    
        

class Solution:
    def tictactoe(self, moves: List[List[int]]) -> str:
       # fill the grid
        grid = [[' ' for i in range(3)] for j in range(3)]
        for idx, move in enumerate(moves):
            if idx % 2 == 0:
                simbol = 'X'
            else:
                simbol = 'O'
            grid[move[0]][move[1]] = simbol
        
        winner = {"X": "A", "O": "B"}
        
        # check condition
        for i in range(3):
            if grid[i][0] == grid[i][1] and grid[i][1] == grid[i][2]:
                if grid[i][0] != " ":
                    return winner[grid[i][0]]
            if grid[0][i] == grid[1][i] and grid[1][i] == grid[2][i]:
                if grid[0][i] != " ":
                    return winner[grid[0][i]]

        if grid[0][0] == grid[1][1] and grid[1][1] == grid[2][2]:
            if grid[0][0] != " ":
                return winner[grid[0][0]]
        if grid[2][0] == grid[1][1] and grid[1][1] == grid[0][2]:
            if grid[2][0] != " ":
                return winner[grid[2][0]]
        
        return "Draw" if len(moves) == 9 else "Pending"
    