import random
from collections import deque
class SudokuCreator():

    def __init__(self, grid_size=9):
        self.grid_size = grid_size

    
    def generate_empty_board(self):
        self.board = [[0]*9]*9
        


    def draw_board(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                print(self.get_number((i, j)), end=' ')
            print()
    def get_number(self, cell):
        return self.board[cell[0]][cell[1]]
   
    
    
    

    def initialize_domains(self):
        self.domains = {}
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.domains[(i, j)] = set(random.sample(range(1, 10), 9))  # Each cell can initially take any value from 1 to 9
        
    def create_puzzle(self):
        self.initialize_domains()
        self.generate_empty_board() 
        while True:
            self.generate_empty_board() 
            
            board = [row.copy() for row in self.board]  # Create a copy of the board
            assignment = {}  # Initialize assignment as a dictionary
            row = random.randint(0, 8)  # Random row index between 0 and 8
            col = random.randint(0, 8)  # Random column index between 0 and 8
            value = random.randint(1, 9)  # Random value between 1 and 9
            board[row][col]=value
            assignment[(row, col)] = value  # Assign value to the (row, col) key in the dictionary
            temp = self.backtrack(assignment, board)  # Pass the dictionary and the board copy to the backtrack method
            if temp is not None:
                # Convert the assignment to a 2D list and assign it to self.board
                self.board = [[temp.get((i, j), 0) for j in range(self.grid_size)] for i in range(self.grid_size)]
                break
        
        return self.board

    


    def select_unassigned_variable(self, assignment):
        # unassigned_variables = [v for v in self.domains if v not in assignment]
        # return min(unassigned_variables, key=lambda v: (len(self.domains[v])))

        unassigned_variables = [v for v in self.domains if v not in assignment]
        min_domain_vars = []
        min_domain_size = 10
        
        for v in unassigned_variables:
            domain_size = len(self.domains[v])
            min_domain_size = min(min_domain_size, domain_size)
        
        for v in unassigned_variables:
            if len(self.domains[v]) == min_domain_size:
                min_domain_vars.append(v)  # Append to the list instead of assigning directly
        
        return random.choice(min_domain_vars)

    def assignment_complete(self, assignment):
        
        for v in self.domains:
            if v not in assignment:
                return False
        return True
        
    def backtrack(self, assignment, board):
        if self.assignment_complete(assignment):
            self.board = board  # Update self.board with the complete board
            return assignment

        var = self.select_unassigned_variable(assignment)
        original_domain = self.domains[var].copy()

        for value in self.domains[var].copy():
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                board[var[0]][var[1]] = value  # Update the local copy of the board

                # Keep track of the original domains of the other cells
                original_domains = {v: self.domains[v].copy() for v in self.domains}

                # Update the domains of the other cells
                self.update_domains(var, value)

                result = self.backtrack(assignment, board)

                if result:
                    return result

                del assignment[var]
                board[var[0]][var[1]] = 0  # Reset the local copy of the board
                self.domains[var] = original_domain  # Restore the original domain

                # Restore the original domains of the other cells
                self.domains = original_domains

        return None
    def update_domains(self, var, value):
        # Remove value from the domains of cells in the same row
        for i in range(self.grid_size):
            if value in self.domains[(i, var[1])]:
                self.domains[(i, var[1])].remove(value)

        # Remove value from the domains of cells in the same column
        for i in range(self.grid_size):
            if value in self.domains[(var[0], i)]:
                self.domains[(var[0], i)].remove(value)

        # Remove value from the domains of cells in the same 3x3 grid
        start_x, start_y = 3 * (var[0] // 3), 3 * (var[1] // 3)
        for i in range(3):
            for j in range(3):
                if value in self.domains[(start_x + i, start_y + j)]:
                    self.domains[(start_x + i, start_y + j)].remove(value)

    def is_consistent(self, var, value, assignment):
        # Check rows
        for i in range(self.grid_size):
            if (i, var[1]) in assignment and assignment[(i, var[1])] == value:
                return False

        # Check columns
        for i in range(self.grid_size):
            if (var[0], i) in assignment and assignment[(var[0], i)] == value:
                return False

        # Check 3x3 grid
        start_x, start_y = 3 * (var[0] // 3), 3 * (var[1] // 3)
        for i in range(3):
            for j in range(3):
                if (start_x + i, start_y + j) in assignment and assignment[(start_x + i, start_y + j)] == value:
                    return False

        return True




def main():
    game =SudokuCreator()
    board=game.create_puzzle()
    
    for i in range(9):
        for j in range(9):
            print(board[i][j], end=' ')
        print()

    
if __name__ == "__main__":
    main()

