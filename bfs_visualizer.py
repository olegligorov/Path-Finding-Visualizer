from tkinter import messagebox, Tk
import pygame, sys

window_width = 600
window_height = 600

columns = 30
rows = 30

cell_width = window_width // columns
cell_height = window_height // rows

grid = []
queue = []
path = []

UNVISITED_COLOR = (50, 50, 50)
START_COLOR = (0, 200, 200)
WALL_COLOR = (90, 90, 90)
TARGET_COLOR = (200, 200, 0)
QUEUED_COLOR = (200, 0, 0)
VISITED_COLOR = (129, 178, 91)
PATH_COLOR = (0, 0, 139)

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("BFS visualizer")

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.start = False
        self.wall = False
        self.target = False
        self.queued = False
        self.visited = False
        self.neighbours = []
        self.parent = None
        self.is_path = False
    
    def draw(self, win, color):
        # cell_width -2 and cell_height - 2 to create a margin and display visible cells
        pygame.draw.rect(win, color, (self.x * cell_width, self.y * cell_height, cell_width - 2, cell_height - 2))

    def set_neighbours(self):
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y])
        if self.x < columns - 1:
            self.neighbours.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbours.append(grid[self.x][self.y + 1])

def create_grid():
    for i in range(rows):
        arr = []
        for j in range(columns):
            arr.append(Cell(i, j))
        grid.append(arr)
    
    for i in range(rows):
        for j in range(columns):
            grid[i][j].set_neighbours()

def draw_cells():
    for i in range(rows):
        for j in range(columns):
            cell = grid[i][j]
            cell.draw(window, UNVISITED_COLOR)
            if cell.queued:
                cell.draw(window, QUEUED_COLOR)
            if cell.visited:
                cell.draw(window, VISITED_COLOR)
            if cell.is_path:
                cell.draw(window, PATH_COLOR)
            if cell.start:
                cell.draw(window, START_COLOR)
            if cell.wall:
                cell.draw(window, WALL_COLOR)
            if cell.target:
                cell.draw(window, TARGET_COLOR)

def reset_grid():
    grid.clear()
    create_grid()


def main():
    create_grid()

    start_cell = grid[0][0]
    start_cell.start = True
    start_cell.visited = True

    begin_search = False
    target_cell_set = False
    searching = True

    creating_wall = False
        
    # set the target box by pressing right click
    target_cell = None

    while True:
        for event in pygame.event.get():
            # Quit the window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
             

            # Controls
            # when moving the mouse change the x and y positions 
            elif event.type == pygame.MOUSEMOTION and not begin_search:                
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                               
                # Draw the wall
                # C toggles creating the wall
                if event.buttons[0] and creating_wall:
                    i = x // cell_width
                    j = y // cell_height
                    grid[i][j].wall = True

                if event.buttons[0] and not creating_wall:
                    i = x // cell_width
                    j = y // cell_height
                    if grid[i][j].wall:
                        continue

                    if start_cell:
                        start_cell.start = False
                        start_cell.visited = False

                    start_cell = grid[i][j]  
                    start_cell.start = True
                    start_cell.visited = True
                
                # Set the target
                if event.buttons[2]:
                    i = x // cell_width
                    j = y // cell_height

                    if grid[i][j].wall:
                        continue
                    # remove the last target_cell                    
                    if target_cell:
                        target_cell.target = False

                    target_cell_set = True
                    target_cell = grid[i][j]
                    target_cell.target = True
                
            if event.type == pygame.KEYDOWN:
                # Reset the game on R
                if event.key == pygame.K_r:
                    reset_grid()
                    start_cell = grid[0][0]
                    start_cell.start = True
                    start_cell.visited = True
                    begin_search = False
                    target_cell_set = False
                    searching = True
                    creating_wall = False                        
                    target_cell = None

                if event.key == pygame.K_c:
                    creating_wall = not creating_wall

                if event.key == pygame.K_SPACE and target_cell_set:
                    begin_search = True
                    queue.append(start_cell)

            
        if begin_search:
            if len(queue) and searching:
                current_cell = queue.pop(0)
                current_cell.visited = True

                if current_cell == target_cell:
                    searching = False
                    temp = current_cell
                    while temp:
                        path.append(temp)
                        temp.is_path = True
                        temp = temp.parent

                else:
                    for neighbour in current_cell.neighbours:
                        if not neighbour.wall and not neighbour.queued and not neighbour.visited:
                            queue.append(neighbour)
                            neighbour.queued = True
                            neighbour.parent = current_cell

            else:
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No solution", "There is no solution!")
                    searching = False
                
        window.fill((0, 0, 0))

        draw_cells()
        
        pygame.display.flip()

main()
