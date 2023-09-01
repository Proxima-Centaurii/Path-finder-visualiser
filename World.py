import pygame
import Colours

OBJECT_TYPES = {
   0: {'name': 'AIR', 'default_colour': Colours.WHITE, 'open_colour': Colours.GREEN, 'closed_colour': Colours.RED}, #AIR
   1: {'name': 'OBSTACLE','default_colour': Colours.GREY, 'open_colour': Colours.LIGHT_GRAY, 'closed_colour': Colours.DARK_GRAY}, #OBSTACLE
   2: {'name': 'AGENT', 'default_colour': Colours.ORANGE}, #AGENT
   3: {'name': 'GOAL', 'default_colour': Colours.TURQUOISE},  #GOAL
   4: {'name': 'PATH', 'default_colour': Colours.PURPLE}     #PATH
}


class Block():
    
    def __init__(self, row, col, size, id):
        self.row = row
        self.col = col
        self.x = col * size
        self.y = row * size
        self.size = size
        self.f_cost = ""
        self.h_cost = ""
        self.g_cost = ""
    
        self.set_type(id)

    def make_open(self):
        self.colour = self.data.get('open_colour', self.colour)

    def make_closed(self):
        self.colour = self.data.get('closed_colour', self.colour)

    def reset(self):
        self.colour = self.data['default_colour']

    #COL, ROW -> X, Y
    def get_position(self):
        return (self.col, self.row)

    def set_type(self, id):
        self.id = id

        #Check if the given id is valid and if not set the block to be an air block
        self.data  = OBJECT_TYPES.get(id, None)
        if(self.data == None):
            self.id = 0
            self.data = OBJECT_TYPES[0]

        self.colour = self.data['default_colour']


    def draw(self, surface):
        pygame.draw.rect(surface, self.colour, (self.x, self.y, self.size, self.size))

    def __str__(self):
        return f'({self.col},{self.row})'
    
    def __repr__(self):
        return f'({self.col},{self.row})'
    
    #This function performs the comparison '<'
    #Needs to be implemented to work with certain data structures
    def __lt__(self, other):
        return self.get_position() < other.get_position()


class World():

    __BLOCK_SIZE = 40
    __GRID_COLOUR = Colours.BLACK
    __GRID_THICKNESS = 1
    __BIG_FONT = pygame.font.SysFont("Verdana", 16)
    __MEDIUM_FONT = pygame.font.SysFont("Verdana", 12)

    def __init__(self, maze=None, width = 0, height = 0):    
        #Private variables
        self.__maze = []
        self.__agent_pos = (-1,-1)
        self.__end_point_pos = (-1,-1)

        #This is a lamda function (reference to a function) that point to the agent's algorithm entry point
        self.__agent_algorithm = None

        empty_maze = True if maze is None else False

        #Create a block table based on the id table provided
        if(not empty_maze):
            width = len(maze[0])
            height = len(maze)

        for i in range(height):
            new_row = []
            for j in range(width):
                id = 0 if empty_maze else maze[i][j]
                
                if(id == 2):
                    self.__agent_pos = (j, i)
                elif(id == 3):
                    self.__end_point_pos = (j,i)

                new_row.append(Block(i, j,self.__BLOCK_SIZE, id))
            self.__maze.append(new_row)

        #Calculate area of the display surface
        self.__display_area = (width * self.__BLOCK_SIZE, height * self.__BLOCK_SIZE)

        #Create an internal surface
        self.internal_surface = pygame.Surface(self.__display_area)
        
        #Create a surface for drawing the grid (supports transparency)
        #This will cache the grid by drawing it to an image once, the drawing that image on top of the maze each frame later on
        self.grid_surface = pygame.Surface(self.__display_area, pygame.SRCALPHA)

        self.__initial_grid_draw(width, height, self.__display_area[0], self.__display_area[1])
        

    def set_agent(self, x, y, algorithm = None):
        #If the agent was already set, change the block to an air block (reset)
        if(self.__agent_pos != (-1,-1)):
            self.__maze[self.__agent_pos[1]][self.__agent_pos[0]].set_type(0)

        #Set the agent to the new position
        self.__maze[y][x].set_type(2)
        self.__agent_pos = (x, y)
        
        if(algorithm is not None):
            self.__agent_algorithm = algorithm


    def set_end_point(self, x, y):
        #If the end point was already set, change the block to an air block (reset)
        if(self.__end_point_pos != (-1, -1)):
            self.__maze[self.__end_point_pos[1]][self.__end_point_pos[0]].set_type(0)

        self.__maze[y][x].set_type(3)
        self.__end_point_pos = (x, y)

    #XXX Added code (individual work)
    def reset_agent_position(self):
        if(self.__agent_pos != (-1,-1)):
            self.__maze[self.__agent_pos[1]][self.__agent_pos[0]].set_type(0)
            self.__agent_pos = (-1, -1)

    def reset_end_position(self):
        if(self.__end_point_pos != (-1, -1)):
            self.__maze[self.__end_point_pos[1]][self.__end_point_pos[0]].set_type(0)
            self.__end_point_pos = (-1, -1)

    def set_agent_algorithm(self, algorithm):
        self.__agent_algorithm = algorithm


    #Changes the type of the specified block
    def set_block(self, x, y, type):
        block = self.__maze[y][x]
        
        #The agent and destination block can only be modified through their respective functions
        if(block.id == 2 or block.id == 3):
            return False
        
        self.__maze[y][x].set_type(type)

        return True

    def block_type_at(self, x,y):
        return self.__maze[y][x].id

    def clear_world(self):
        self.reset_agent_position()
        self.reset_end_position()
        for row in self.__maze:
            for block in row:
                block.set_type(0)
                
                block.f_cost = ""
                block.h_cost = ""
                block.g_cost = ""

    
    def get_display_area(self):
        return self.__display_area
    
    def touch_indices(self, pos, size):
        col = int((pos[0] * (self.__display_area[0]/size[1]))) // self.__BLOCK_SIZE
        row = int((pos[1] * (self.__display_area[1]/size[1]))) // self.__BLOCK_SIZE

        return row, col

    #-------------

    def reset_world(self):
        for row in self.__maze:
            for block in row:
                if(block.id == 4):
                    block.set_type(0)
                else:
                    block.reset()
                
                block.f_cost = ""
                block.h_cost = ""
                block.g_cost = ""
        

    def run_agent(self):
        if(self.__agent_algorithm is None):
            print("No agent algorithm has been set. (Agent failed to start!)")
            return

        if(self.__agent_pos == (-1, -1)):
            print("Agent's position in the world has not been set!")
            return

        if(self.__end_point_pos == (-1, -1)):
            print("The destination has not been set!")
            return
        
        self.__agent_algorithm(self.__maze,self.__maze[self.__agent_pos[1]][self.__agent_pos[0]], self.__maze[self.__end_point_pos[1]][self.__end_point_pos[0]])

  
    #Private method that makes an initial draw of the grid which will be reused later to display the grid
    def __initial_grid_draw(self, width, height, area_width, area_height):
        
        #Drawing horizontal grid lines 
        for h_line in range(self.__BLOCK_SIZE, height * self.__BLOCK_SIZE, self.__BLOCK_SIZE):
            pygame.draw.line(self.grid_surface, self.__GRID_COLOUR, (0, h_line),(area_width, h_line), self.__GRID_THICKNESS)

        #Drawing vertical grid lines
        for v_line in range(self.__BLOCK_SIZE, width * self.__BLOCK_SIZE, self.__BLOCK_SIZE):
            pygame.draw.line(self.grid_surface, self.__GRID_COLOUR, (v_line, 0), (v_line, area_height), self.__GRID_THICKNESS)


    def draw(self, win):
        #Draw each block into the internal surface
        for row in self.__maze:
            for block in row:
                block.draw(self.internal_surface)
                self.internal_surface.blit(self.__BIG_FONT.render(block.f_cost, False, Colours.DARK_GRAY), (block.x+12, block.y+14))
                self.internal_surface.blit(self.__MEDIUM_FONT.render(block.h_cost, False, Colours.LIGHT_GRAY), (block.x+2, block.y))
                self.internal_surface.blit(self.__MEDIUM_FONT.render(block.g_cost, False, Colours.LIGHT_GRAY), (block.x+25, block.y))

        
        #Draw the grid on top of the internal surface
        self.internal_surface.blit(self.grid_surface, (0,0))
        
        #Draw everything to the application window
        win.blit(pygame.transform.scale(self.internal_surface, win.get_size()), (0,0))
        