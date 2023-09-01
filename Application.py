import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

import Greedy, Astar, BFS, DFS

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 800
WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("AI-coursework - Algorithm: Greedy")

#Frames per second - determines how many times the window will update each second
FPS = 10
clock = pygame.time.Clock()

#Initialise the fonts module
pygame.font.init()

#A tuple representing the colour used to clear the screen each frame
#(RED, GREEN, BLUE) - values must be from 0 to 255
CLEAR_COLOUR = (0,0,0)

from World import World
world = World(width=10,height=10)

def draw():
    WIN.fill(CLEAR_COLOUR)

    world.draw(WIN)

    pygame.display.update()
    clock.tick(FPS)

ALGORITHMS = [("Greedy",lambda maze, start_block, destination_block: Greedy.greedy(maze=maze,start_point=start_block,destination=destination_block,draw=draw)),
              ("A star", lambda maze, start_block, destination_block: Astar.astar(maze=maze, start_point=start_block,destination=destination_block,draw=draw)),
              ("Depth first", lambda maze, start_block, destination_block: DFS.dfs(maze=maze, start_point=start_block,destination=destination_block,draw=draw)),
              ("Breadth first", lambda maze, start_block, destination_block: BFS.bfs(maze=maze, start_point=start_block,destination=destination_block,draw=draw))]
current_algorithm = 0


def get_clicked_pos(pos, virtual_display):
    gap = (WINDOW_WIDTH // virtual_display[0], WINDOW_HEIGHT // virtual_display[1])
    #gap = width // rows
    y, x = pos

    row = y // gap[1]
    col = x // gap[0]

    return row, col

def print_help_menu():
    print("==HOW TO EDIT==")
    print("First block you will be placing will be the agent followed by the end point, after placing these you will be able to place obstacle blocks.")
    print("You can't select which block type to place, the type is derived from the order aformentioned.")
    print("\n==CONTROLS==")
    print("LEFT CLICK - place a block")
    print("RIGHT CLICK - remove a block")
    print("SPACE - start the simulation")
    print("R - Reset simulation")
    print("C - Clear maze blocks")
    print("H - Displays this help menu")
    print("S - Switch the algorithm used for the agent. Options: A star, Greedy, DFS, and BFS")

def switch_algorithm():
    global current_algorithm
    #Loop through the algorithms list
    current_algorithm = (current_algorithm + 1) % len(ALGORITHMS)
    #Set the new algorithm in the world
    world.set_agent_algorithm(ALGORITHMS[current_algorithm][1])
    #Set the window title so it reflects the change
    pygame.display.set_caption(f"AI-coursework - Algorithm: {ALGORITHMS[current_algorithm][0]}")

def main():
    world_display_area = world.get_display_area

    world.set_agent_algorithm(lambda maze, start_block, destination_block: Greedy.greedy(maze=maze,start_point=start_block,destination=destination_block,draw=draw))

    set_start = False
    set_end = False

    # Set to true when the user tries to edit the world after a
    # run of the visualisation finishes. Used to tell if the world 
    # should be reset to the point right before running the visualisation. 
    should_auto_reset = False 

    print_help_menu()

    run = True
    while run:
        draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
            #Adding blocks to the world
            if pygame.mouse.get_pressed()[0]: # LEFT
                if(should_auto_reset):
                    world.reset_world()
                    should_auto_reset = False

                pos = pygame.mouse.get_pos()
                #row, col = get_clicked_pos(pos, world_display_area)
                row, col = world.touch_indices(pos, WIN.get_size())
                type_of_selected = world.block_type_at(col, row)
                #Set the agent position
                if not set_start and type_of_selected != 3:
                    world.set_agent(col, row)
                    set_start = True

                #Set destination
                elif not set_end and type_of_selected != 2:
                    world.set_end_point(col, row)
                    set_end = True

                #Set an obstacle
                else:
                    world.set_block(col, row, 1)

            #Removing objects from the world
            elif pygame.mouse.get_pressed()[2]: # RIGHT
                if(should_auto_reset):
                    world.reset_world()
                    should_auto_reset = False

                pos = pygame.mouse.get_pos()
                #row, col = get_clicked_pos(pos, world_display_area)
                row,col = world.touch_indices(pos, WIN.get_size())
                type_of_selected = world.block_type_at(col, row)

                #Remove agent
                if type_of_selected == 2:
                    world.reset_agent_position()
                    set_start = False
                #Remove destination
                elif type_of_selected == 3:
                    world.reset_end_position()
                    set_end = False
                else:
                    world.set_block(col,row,0)

            #Simulation control keys
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE and set_start and set_end:
                    global current_algorithm
                    print(f'\n{"="*3}RESULTS OF: {ALGORITHMS[current_algorithm][0]}{"="*3}')      
                    world.reset_world()
                    world.run_agent()

                    should_auto_reset = True

                if event.key == pygame.K_c:
                    set_start = False
                    set_end = False
                    world.clear_world()
                    should_auto_reset = False

                if event.key == pygame.K_r:
                    world.reset_world()
                    should_auto_reset = False
                
                if event.key == pygame.K_h:
                    print_help_menu()

                #Switch to a different agent algorithm
                if event.key == pygame.K_s:
                    switch_algorithm()

    pygame.quit()

if __name__ == "__main__":
    main()