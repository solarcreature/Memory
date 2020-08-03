

import pygame, random, time


# User-defined functions

def main():
   # initialize all pygame modules (some need initialization)
   pygame.init()
   # create a pygame display window
   pygame.display.set_mode((500, 400))
   # set the title of the display window
   pygame.display.set_caption('Memory')   
   # get the display surface
   w_surface = pygame.display.get_surface() 
   # create a game object
   game = Game(w_surface)
   # start the main game loop by calling the play method on the game object
   game.play() 
   # quit pygame and clean up the pygame window
   pygame.quit() 


# User-defined classes

class Game:
   # An object in this class represents a complete game.

   def __init__(self, surface):
      # Initialize a Game.
      # - self is the Game to initialize
      # - surface is the display window surface object

      # === objects that are part of every game that we will discuss
      self.surface = surface
      self.bg_color = pygame.Color('black')
      
      self.FPS = 60
      self.game_Clock = pygame.time.Clock()
      self.close_clicked = False
      self.continue_game = True
      
      # === game specific objects
      self.board = []
      self.board_size = 4
      self.image_list = [] 
      self.create_board()
      self.create_image_list()
      self.scoreboard = 0
      self.time = 0
      self.flipped = False
      self.comparison_list = []
      
   def play(self):
      # Play the game until the player presses the close box.
      # - self is the Game that should be continued or not.

      while not self.close_clicked:  # until player clicks close box
         if self.decide_continue():
            # play frame
            self.handle_events()
            self.draw()    
            self.update()
            self.compare_images()
            
         self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second 

   def handle_events(self):
      # Handle each user event by changing the game state appropriately.
      # - self is the Game whose events will be handled

      events = pygame.event.get()
      for event in events:
         if event.type == pygame.QUIT:
            self.close_clicked = True
         if event.type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_event(event.pos)
            
   def handle_mouse_event(self,pos):
      #for each tile in the board, if the tile was selected correctly, add the tile to a list and let it know that the image has flipped revealing the real image
      for row in self.board:
         for tile in row:
            if tile.select(pos):
               self.comparison_list.append(tile)
               tile.flipped = True

   def draw(self):
      # Draw all game objects.
      # - self is the Game to draw
      
      self.surface.fill(self.bg_color) # clear the display surface first
       
      for row in self.board:
         for tile in row:
            tile.draw()
            
      self.draw_scoreboard()
         
      pygame.display.update() # make the updated surface appear on the display  

   def update(self):
      # Update the game objects for the next frame.
      # - self is the Game to update
      
      #gets the time in milliseconds and divides by 1000 to get seconds and then updates the timer/scoreboard
      self.time = pygame.time.get_ticks()//1000   
      self.scoreboard = self.time   
 
   def decide_continue(self):
      # Check and remember if the game should continue
      # - self is the Game to check
        
      counter = 0
      
      #for every tile on the board, if the image was flipped, increase the counter by one
      for row in self.board:
         for tile in row:
            if tile.flipped == True:
               counter = counter + 1
      
      #if every tile was flipped, the game will stop, otherwise continue the game
      if counter == 16:
         return False
      
      return True
         
   def create_board(self):
      Tile.set_surface(self.surface)
      
      self.create_image_list()
      image = pygame.image.load('image0.bmp')
      placement = 0
      
      #the question mark image and the flipped image will be sent to Tile class to be drawn
      width = image.get_width()
      height = image.get_height()
      for row_index in range(0, self.board_size):
         row = []
         for col_index in range(0,self.board_size):
            x = width * col_index
            y = height * row_index
            tile = Tile(x,y,image,self.image_list[placement])
            placement += 1
            row.append(tile)
         self.board.append(row) 
   
   def create_image_list(self):
      #a loop will run through from numbers 1 to 8 loading in the images
      #the image will then be appended into the image list
      for x in range(1,9):
         image = pygame.image.load('image' + str(x) + '.bmp')
         self.image_list.append(image) 
      
      placement = 0

      #as the game needs 16 images, the list will be duplicated and the shuffled
      self.image_list = self.image_list + self.image_list
      random.shuffle(self.image_list)
   
   def draw_scoreboard(self):
      #draws what the scoreboard will look like
      score_font = pygame.font.SysFont('', 48)
      scoreboard_image = (pygame.font.SysFont('', 75)).render(str(self.scoreboard),True,pygame.Color('white'))
      self.surface.blit(scoreboard_image,(440,0)) 
      
   def compare_images(self):
      #if there are currently 2 tiles that have been flipped
      if len(self.comparison_list) == 2:
         
         #if the images of the two tiles do not equal to each other
         if self.comparison_list[0].new_image != self.comparison_list[1].new_image:
            
            #the program will sleep for half a second and be flipped back to the question mark image again
            time.sleep(.5)
            self.comparison_list[0].flipped = False
            self.comparison_list[1].flipped = False
            
         #resets the list to be used for the next pair for comparison
         self.comparison_list = []

class Tile:
   # An object in this class represents a Dot that moves 
   # Shared Attrbutes or Class Attributes
   surface = None
   border_size = 3
   border_color = pygame.Color('black')
   
   @classmethod
   def set_surface(cls,game_surface):
      cls.surface = game_surface
   # Instance Methods
   
   def __init__(self,x,y,question_mark_image, flipped_image):
      self.question_mark = question_mark_image
      self.new_image = flipped_image
      width = self.question_mark.get_width()
      height = self.question_mark.get_height()
      self.rect = pygame.Rect(x,y,width,height)
      self.flipped = False
      
   def draw(self):
      
      #if the image is not clicked on, it will draw the question mark image
      if not self.flipped:
         pygame.draw.rect(Tile.surface,Tile.border_color,self.rect,Tile.border_size)
         Tile.surface.blit(self.question_mark,self.rect)   
         
      #if the image is clicked on, it will draw the real image
      else:
         pygame.draw.rect(Tile.surface,Tile.border_color,self.rect,Tile.border_size)
         Tile.surface.blit(self.new_image,self.rect)
   
   def select(self, position):
      #if the mouse clicks on to a tile and it has not been flipped yet, return True, otherwise return False
      if self.rect.collidepoint(position) and not self.flipped:
         return True
      else:
         return False   
   
main()