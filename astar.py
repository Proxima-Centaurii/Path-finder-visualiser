import pygame
import math
from queue import PriorityQueue

MAX_BLEVEL = 1
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
DARK_PURPLE = (88, 0, 88)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
LIGHT_GRAY = (180, 180, 180)
DARK_GRAY = (50, 50, 50)
TURQUOISE = (64, 224, 208)

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED or self.color == DARK_GRAY

    def is_open(self):
        return self.color == GREEN or self.color == LIGHT_GRAY

    def is_barrier(self):
        return self.color == BLACK or self.color == LIGHT_GRAY or self.color == DARK_GRAY or self.color == DARK_PURPLE

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = DARK_GRAY if self.is_barrier() else RED

    def make_open(self):
        self.color = LIGHT_GRAY if self.is_barrier() else GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = DARK_PURPLE if self.is_barrier() else PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []

        # LEFT
        if self.col > 0:
            self.neighbors.append(grid[self.row][self.col - 1])

        # DOWN
        if self.row < self.total_rows - 1:
            self.neighbors.append(grid[self.row + 1][self.col])

        # UP
        if self.row > 0:
            self.neighbors.append(grid[self.row - 1][self.col])

        # RIGHT
        if self.col < self.total_rows - 1:
            self.neighbors.append(grid[self.row][self.col + 1])


    def __lt__(self, other):
        return False

    def __str__(self):
        return ("(%d,%d)" % (self.row, self.col))


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, b_level, draw):
    next_level = False

    while current in came_from[b_level]:

        current = came_from[b_level][current]
        if not current.is_start():
            current.make_path()

        if(next_level):
            b_level = b_level + 1
            next_level = False

        if current.is_barrier():
            next_level = True
        draw()


def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = [{} for i in range(MAX_BLEVEL+1)]
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
    b_level = {spot: int(MAX_BLEVEL) for row in grid for spot in row}
    b_level[start] = MAX_BLEVEL

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, b_level[current],draw)
            end.make_end()
            print("Path length:" + str(g_score[current] + 1))
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            temp_b_level = b_level[current] - (1 if neighbor.is_barrier() else 0)

            if (temp_g_score < g_score[neighbor] and not(neighbor.is_barrier() and b_level[current] <= 0)) or (temp_b_level > b_level[neighbor] ):

                b_level[neighbor] = temp_b_level

                came_from[temp_b_level][neighbor] = current

                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid

def reset_grid(rows, width, grid):
    for i in range(rows):
        for j in range(rows):
            spot = grid[i][j]

            if(spot.is_barrier()):
                spot.make_barrier()
            elif(not(spot.is_start() or spot.is_end())):
                spot.reset()


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def main(win, width):
    ROWS = 20
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]: # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    reset_grid(ROWS, width, grid)
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

                if event.key == pygame.K_r:
                    reset_grid(ROWS, width, grid)

    pygame.quit()

main(WIN, WIDTH)
