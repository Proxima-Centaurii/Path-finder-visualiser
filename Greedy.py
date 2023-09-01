import pygame, sys, heapq, math

# Define heuristic function (Manhattan distance)
def heuristic(source, destination):
    return abs(source[0]-destination[0]) + abs(source[1]-destination[1])


def greedy(maze, start_point, destination, draw):
    # Define possible moves from each cell (up, down, left, right)
    moves = [(0,-1), (0,1), (-1,0), (1,0)]

    # Initialize priority queue with start point and its heuristic value
    queue = [(heuristic(start_point.get_position(), destination.get_position()), start_point)]

    # Initialize dictionary to keep track of parents
    parents = {start_point: None}

    opened_nodes = 0

    # Perform greedy search
    while queue:

        #Check for quit events (DO NOT EDIT)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        cell = heapq.heappop(queue)[1]
        cell.make_closed()

        #Counting each node that is opened/expanded
        opened_nodes = opened_nodes + 1

        if cell.id == 3:
            break

        for move in moves:
            #Calculate the next cell
            delta_cell = (cell.col + move[0], cell.row + move[1])
            
            #Check if the next cell is within maze bounds. Skip iteration if not within bounds
            if(delta_cell[0] < 0 or delta_cell[0] >= len(maze[0]) or delta_cell[1] < 0 or delta_cell[1] >= len(maze)):
                continue
            
            new_cell = maze[delta_cell[1]][delta_cell[0]]
            
            #Check if the new cell is an obstacle and add it to the queue
            if (new_cell.id != 1 and new_cell not in parents):
                parents[new_cell] = cell
                h_val = heuristic(new_cell.get_position(), destination.get_position())
                
                #Programming artefact from group coursework, f_cost value is set because it's the big number displayed in the middle of the block
                new_cell.f_cost = str(h_val)

                heapq.heappush(queue, (h_val, new_cell))
                new_cell.make_open()
        
        draw()

    # Reconstruct path from destination to start point
    path = [destination]
    while path[-1] != start_point:
        #Using the get function to avoid runtime errors
        path_cell = parents.get(path[-1])
   
        #Exit the loop if there is no way to reach back to the starting node
        if(path_cell is None):
            break

        if(path_cell.id != 2):
            path_cell.set_type(4)

        path.append(path_cell)

        draw()

    #There is no path
    if(len(path) == 1):
        print("No path possible.")
    else:
        path.reverse()
        print(f'Path sequence: {str(path)[1:-1]}')
        print(f'Path length: {len(path)-1}')
    
    print(f'Opened a total of {opened_nodes} nodes.')