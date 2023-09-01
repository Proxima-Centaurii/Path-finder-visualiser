import pygame
import sys
from collections import deque

def bfs(maze, start_point, destination, draw):

    # Define possible moves from each cell (up, down, left, right)
    moves = [(0,-1), (0,1), (-1,0), (1,0)]

    # Initialize queue with start point
    queue = deque([start_point])

    # Initialize dictionary to keep track of parents
    parents = {start_point: None}

    opened_nodes = 0

    # Perform BFS
    while queue:

        #Check for quit events (DO NOT EDIT)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current_cell = queue.popleft()
        current_cell.make_closed()

        #Counting each node that is opened/expanded
        opened_nodes = opened_nodes + 1

        #Check if destination has been reached
        if current_cell.id == 3:
            break

        for move in moves:
            #Calculate the next cell
            delta_cell = (current_cell.col+move[0], current_cell.row+move[1])

            #Skip this iteration if the new cell is not within maze bounds (invalid position)
            if(delta_cell[0] < 0 or delta_cell[0] >= len(maze[0]) or delta_cell[1] < 0 or delta_cell[1] >= len(maze)):
                continue
            
            new_cell = maze[delta_cell[1]][delta_cell[0]]

            #If the new cell is not an obstacle and if its not in the open cells queue
            if (new_cell.id != 1 and new_cell not in parents):
                parents[new_cell] = current_cell
                queue.append(new_cell)
                new_cell.make_open()

        draw()

    # Reconstruct path from destination to start point
    path = [destination]
    while path[-1] != start_point:
        #Using the get function to avoid runtime errors
        path_cell = parents.get(path[-1])

        #Exit the loop if there is no way to reach back to the starting node
        if(path is None):
            break

        if(path_cell.id != 2):
            path_cell.set_type(4)

        path.append(path_cell)
        
        draw()

    #There is no path
    if(len(path) == 1):
        print("No path possible")
    else:
        path.reverse()
        print(f'Path sequence: {str(path)[1:-1]}')
        print(f'Path length: {len(path)-1}')

    print(f'Opened a total of {opened_nodes} nodes.')