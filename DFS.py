import pygame
import sys

# start_point = (0, 0)
# destination = (4, 5)

def dfs(maze, start_point, destination, draw):
    # Stack keeps track of the cells to visit
    stack = [start_point]

    # visited keeps track of the visited nodes
    visited = set()

    # parents dictionary keeps track of the parent nodes for each visited node
    parents = {start_point: None}

    opened_nodes = 0

    while stack:

        #Check for quit events (DO NOT EDIT)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current_node = stack.pop()
        visited.add(current_node)
        current_node.make_closed()

        #Counting each node that is opened/expanded
        opened_nodes = opened_nodes + 1

        # If we have reached the destination, we can stop the search
        if current_node == destination:
            break

        # Check the neighbors of the current node
        for delta_col, delta_row in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            neighbour_col, neighbour_row = current_node.col + delta_col, current_node.row + delta_row
            
            #if the next delta cell is out of bounds skip this iteration
            if(neighbour_col < 0 or neighbour_col >= len(maze[0]) or neighbour_row < 0 or neighbour_row >= len(maze)):
                continue
            
            neighbour = maze[neighbour_row][neighbour_col]
            # If the neighbour is a valid cell and has not been visited, add it to the stack
            if ((neighbour.id != 1) and
                neighbour not in visited):

                neighbour.make_open()
                stack.append(neighbour)

                parents[neighbour] = current_node

                draw()

    # If we have not found the destination, return None
    if destination not in parents:
        return None

    #Backtrack from the destination to the start point to get the path
    path = [destination]
    
    while path[-1] != start_point:
        #Using the get function to avoind runtime errors
        path_cell = parents.get(path[-1])

        #Exit the loop if there is no way to reach back to the starting point
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
    

