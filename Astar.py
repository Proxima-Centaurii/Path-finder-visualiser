import pygame, sys
from queue import PriorityQueue

def heuristic(node, goal):
    # Define the heuristic function to estimate the distance between two nodes using Manhattan distance
    return abs(node[0]-goal[0]) + abs(node[1]-goal[1])

def astar(maze, start_point, destination, draw):
    # Define the A* search function
    
    open_set = PriorityQueue()
    open_set.put((0, heuristic(start_point.get_position(), destination.get_position()), start_point))

    came_from = {}
    came_from[start_point] = None

    g_cost = {block: float("inf") for row in maze for block in row}
    g_cost[start_point] = 0

    open_set_hash = {start_point}

    opened_nodes = 0

    while not open_set.empty():

        #Check for quit events (DO NOT EDIT)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current = open_set.get()[2]
        open_set_hash.remove(current)
        current.make_closed()
        
        #Counting each node that is opened/expanded
        opened_nodes = opened_nodes + 1

        #Check if the current node is already the destination
        if current.id == 3:
            break

        for dx, dy in [(0,-1),(0,1),(-1,0),(1,0)]:
            x = current.col + dx
            y = current.row + dy

            #If the next cell is out of bounds, skip iteration
            if( x < 0 or x >= len(maze[0]) or y < 0 or y >=  len(maze)):
                continue

            new_cell = maze[y][x]

            if new_cell.id != 1:
                    
                new_cost = g_cost[current] + 1
                if new_cost < g_cost[new_cell]:

                    # #This condition is only to avoid displaying closed cells as open ones
                    # if new_cell not in cost_so_far:
                    #     new_cell.make_open()

                    came_from[new_cell] = current

                    g_cost[new_cell] = new_cost
                    h_cost = heuristic(new_cell.get_position(), destination.get_position())
                    f_cost = new_cost + h_cost

                    #Visualiser info
                    new_cell.f_cost = str(f_cost)
                    new_cell.h_cost = str(h_cost)
                    new_cell.g_cost = str(new_cost)
                    
                    if new_cell not in open_set_hash:
                        open_set.put((f_cost, h_cost, new_cell))
                        open_set_hash.add(new_cell)
                        new_cell.make_open()
        
        draw()


    # Retrieve the path by backtracking from the goal node to the start node
    path = []
    current = destination
    while current != start_point:
        path.append(current)

        if current.id != 3:
            current.set_type(4)

        #Using the get function to avoid runtime errors
        current = came_from.get(current)

        #Exit the loop if there is no way to reach back to the starting node
        if(current is None):
            break

        draw()

    #There is no path
    if(len(path) == 1):
        print("No path possible.")
    else:
        path.append(start_point)
        path.reverse()

        print(f'\nPath sequence: {str(path)[1:-1]}')
        print(f'Path length: {len(path)-1}')

    print(f'Opened a total of {opened_nodes} nodes.')
