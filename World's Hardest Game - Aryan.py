# Name: Aryan Aggarwal, id. 898707
# Description: This program uses the tkinter module to make a recreation of the
#              World's Hardest Game


# Import necessary modules
# Imports necessary GUI functions
from tkinter import Tk, Canvas, Event, Button, PhotoImage
# Imports math for extra math functions
import math

# Decorator function for logging the entry and exit of function calls
# for debugging purposes
def log_function_call(func):
    """Decorator for logging the entry and exit of a function call.

    Args:
    func (function): The function to be decorated.

    Returns:
    function: The wrapper function with added logging functionality.
    """
    def wrapper(*args, **kwargs):
        """Wrapper function for the decorator.

        Logs the entry and exit of the function call.

        Args:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

        Returns:
        Any: The result of the function call.
        """
        print(f"Entering: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Exiting: {func.__name__}")
        return result
    return wrapper

# Class representing a moving object in the game (like player or obstacles)
class MovingObject:
    # Constructor for initializing a moving object
    def __init__(self, canvas, x, y, size, color, **kwargs):
        """Initializes a moving object on the canvas.

        Args:
        canvas (Canvas): The canvas on which to draw the object.
        x (int): Initial x-coordinate of the object.
        y (int): Initial y-coordinate of the object.
        size (int): Size of the object.
        color (str): Color of the object.
        **kwargs: Additional attributes such as speed and shape type.

        Returns:
        None
        """
        self._canvas = canvas # Canvas the object is being drawn on
        self._x = x # X-coordinate of the object (weakly private)
        self._y = y # Y-coordinate of the object (weakly private)
        self.size = size # Size of the object
        self.color = color # Color of the object
        
        # Optional attributes, defaulting to 0 speed and rectangle shape
        self._x_speed = kwargs.get('x_speed', 0)
        self._y_speed = kwargs.get('y_speed', 0)
        self.shape_type = kwargs.get('shape_type', 'rectangle')
        
        # Creating the shape on the canvas based on type
        if self.shape_type == 'oval':
            self.shape = self._canvas.create_oval(self._x, self._y, self._x +
                                                  size, self._y + size,
                                                  fill=self.color)
        else:
            self.shape = self._canvas.create_rectangle(self._x, self._y,
                                                       self._x + size,
                                                       self._y + size,
                                                       fill=self.color)
            
        # Assigning any additional attributes passed in kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    # Methods to get and set the X and Y coordinates of the object, and update
    # its position on the canvas
    def get_x(self):
        """Returns the x-coordinate of the object.

        Returns:
        int: The current x-coordinate.
        """
        return self._x

    def get_y(self):
        """Returns the y-coordinate of the object.

        Returns:
        int: The current y-coordinate.
        """
        return self._y

    def set_x(self, x):
        """Sets a new x-coordinate for the object and updates its position.

        Args:
        x (int): The new x-coordinate.

        Returns:
        None
        """
        self._x = x
        self.update_position()

    def set_y(self, y):
        """Sets a new y-coordinate for the object and updates its position.

        Args:
        y (int): The new y-coordinate.

        Returns:
        None
        """
        self._y = y
        self.update_position()
    
    # Properties for getting and setting the object's speed, with constraints
    # on speed limits
    @property
    def x_speed(self):
        """Gets the x-axis speed of the object.

        Returns:
        int: The current x-axis speed.
        """
        return self._x_speed

    @x_speed.setter
    def x_speed(self, value):
        """Sets the x-axis speed of the object.

        Args:
        value (int): The new x-axis speed.

        Returns:
        None
        """
        self._x_speed = max(min(value, 10), -10)  # Limit speed to a range of
                                                  # -10 to 10

    @property
    def y_speed(self):
        """Gets the y-axis speed of the object.

        Returns:
        int: The current y-axis speed.
        """
        return self._y_speed

    @y_speed.setter
    def y_speed(self, value):
        """Sets the y-axis speed of the object.

        Args:
        value (int): The new y-axis speed.

        Returns:
        None
        """
        self._y_speed = max(min(value, 10), -10)  # Limit speed to a range of
                                                  # -10 to 10

    # Method to update the object's position on the canvas
    def update_position(self):
        """Updates the object's position on the canvas based on its current
        coordinates.

        Returns:
        None
        """
        self._canvas.coords(self.shape, self._x, self._y, self._x + self.size,
                            self._y + self.size)

    
# Subclass for the player character, inheriting from MovingObject
class Player(MovingObject):
    # Sets initial players score to 100
    max_score = 100
    # Constructor initializing the player with attributes like position, size,
    # color, speed, and the game instance
    def __init__(self, canvas, x, y, size, color, speed, game):
        """Initializes the player object with specific attributes.

        Args:
        canvas (Canvas): The canvas on which the player is drawn.
        x (int): The x-coordinate of the player.
        y (int): The y-coordinate of the player.
        size (int): The size of the player.
        color (str): The color of the player.
        speed (int): The speed of the player.
        game (Game): Reference to the game instance.

        Returns:
        None
        """
        super().__init__(canvas, x, y, size, color)
        self.speed = speed # Players speed
        self.game = game # game instance
        self.score = 100  # Starting score
        # Tracks keys pressed
        self.keys_pressed = {'Up': False, 'Down': False, 'Left': False,
                             'Right': False}
        # Boolean variable for checking if the player is moving
        self.is_moving = False 

    # Decorated method to handle player movement, adjusting position based on
    # key presses and game logic
    @log_function_call
    def move(self):
        """Handles the movement of the player based on key presses.

        Calculates the new position considering the current speed and updates
        the player's position.

        Returns:
        None
        """
        dx, dy = 0, 0
        if self.keys_pressed['Up']:
            dy -= self.speed
        if self.keys_pressed['Down']:
            dy += self.speed
        if self.keys_pressed['Left']:
            dx -= self.speed
        if self.keys_pressed['Right']:
            dx += self.speed
        
        # Calculate the distance to the nearest obstacle
        distance = self.game.distance_to_obstacle(self, dx, dy)
        actual_dx = min(abs(dx), distance) * (1 if dx > 0 else -1)
        actual_dy = min(abs(dy), distance) * (1 if dy > 0 else -1)

        # Move the player
        self.set_x(self.get_x() + actual_dx)
        self.set_y(self.get_y() + actual_dy)
        
        if self.is_moving:
            self._canvas.after(30, self.move)

    # Methods to start and stop continuous player movement
    def start_movement(self):
        """Starts the player's continuous movement.

        Initiates the movement process if the player is not already moving.

        Returns:
        None
        """
        if not self.is_moving:
            self.is_moving = True
            self.move()

    def stop_movement(self):
        """Stops the player's continuous movement.

        Halts the movement process if the player is currently moving.

        Returns:
        None
        """
        self.is_moving = False

    # Event handlers for key press and release, to control player movement
    def key_down(self, event: Event):
        """Handles the key down event for player movement.

        Marks the corresponding direction as active upon key press.

        Args:
        event (Event): The key press event containing the key symbol.

        Returns:
        None
        """

        self.keys_pressed[event.keysym] = True
        self.start_movement()

    def key_up(self, event: Event):
        """Handles the key up event for player movement.

        Marks the corresponding direction as inactive upon key release.

        Args:
        event (Event): The key release event containing the key symbol.

        Returns:
        None
        """
        self.keys_pressed[event.keysym] = False
        if not any(self.keys_pressed.values()):
            self.stop_movement()
    
    # Overloaded operators for adding/subtracting values to/from player's score
    def __add__(self, value):
        """Overloads the addition operator for the Player object.

        Args:
        value (int or float): The value to be added to the player's score.

        Returns:
        Player: The instance of the Player, with updated score.
        """
        if isinstance(value, (int, float)):
            self.score = min(max(self.score + value, 0), Player.max_score)
            if Game.high_score >= 100:
                # Apply bonus if the high score is 100 or more
                bonus = 10  # Define the bonus value
                self.score = min(self.score + bonus, Player.max_score)
            return self
        return NotImplemented

    def __sub__(self, value):
        """Overloads the subtraction operator for the Player object.

        Args:
        value (int or float): The value to be subtracted from the player's
        score.

        Returns:
        Player: The instance of the Player, with updated score.
        """
        if isinstance(value, (int, float)):
            new_score = max(self.score - value, 0)
            if new_score < Game.high_score / 2:
                # Apply penalty if new score is less than half of the high
                # score
                penalty = 5  # Define the penalty value
                # Ensure score doesn't go below 0 after penalty
                new_score = max(new_score - penalty, 0)  
            self.score = new_score
            return self
        return NotImplemented
    
    def __gt__(self, other):
        """Overloads the greater than operator for comparing the Player's score
        with another value.

        Args:
        other (Player, int, or float): The object or value to compare against.

        Returns:
        bool: True if the Player's score is greater than the other value, False
        otherwise.
        """
        if isinstance(other, Player):
            return self.score > other.score
        elif isinstance(other, (int, float)):
            return self.score > other
        return NotImplemented
    
    # Method to reduce player's score based on collisions
    def reduce_score(self):
        """Reduces the player's score by a fixed amount.

        Returns:
        None
        """
        # Reduce score by 10, not going below 0
        self.score = max(self.score - 10, 0)  

# Main game class handling the game logic and UI
class Game:
    # Sets initial high score of the player to 0
    high_score = 0
    # Constructor for setting up the game window, canvas, and initial game state
    def __init__(self, width, height):
        """Initializes the game environment.

        Args:
        width (int): Width of the game window.
        height (int): Height of the game window.

        Returns:
        None
        """
        self.window = Tk() # Initializes window
        self.window.title("World's Hardest Game") # Sets a title for the window
        # Disallows the user from changing the window size
        self.window.resizable(False, False)
        # Creates the canvas
        self.canvas = Canvas(self.window, width=width, height=height,
                             bg='black')
        self.canvas.pack(fill='both', expand=True)
        self.moving_objects = [] # Initializes the list for moving objects
        self.walls = [] # Initializes the list for wall coordinates
        self.death_count = 0 # Initializes the players death count
        # Adds a death counter
        self.death_counter_disp = self.canvas.create_text(850, 26,
                                                             text="DEATHS: 0",
                                                             fill="white",
                                                             font=("Arial", 24))
        # Adds the end area for the player
        self.victory_zone = (771, 216, 893, 474)
        # Boolean if the game is complete or not
        self.game_over = False
        self.show_start_screen()

    # Class method to create a game instance with default settings
    @classmethod
    def create_default_game(cls):
        """Creates a new game instance with default settings.

        Returns:
        Game: A new instance of the Game class.
        """
        return cls(1024, 644)
    
    # Method to display the start screen of the game
    def show_start_screen(self):
        """Displays the start screen of the game.

        Initializes and shows the game's start screen, including the title and
        start button.

        Returns:
        None
        """
        # Add the title image
        self.start_image = PhotoImage(file='title.png')

        # Clear the canvas and set up the start screen
        self.canvas.delete("all")
        # Create the background
        self.canvas.create_rectangle(0, 49, 1026, 646, fill='#b4b6fe')
        # Display the title
        self.canvas.create_image(512, 322, image=self.start_image,
                                 anchor='center')
        # Create a Play Game button
        start_button = Button(self.canvas, text="Play Game",
                              command=self.show_rules_screen, 
                              font=("Arial", 16), padx=20, pady=10)
        start_button_window = self.canvas.create_window(512, 500,
                                                        window=start_button)
        
    # Method to display the game's rules screen    
    def show_rules_screen(self):
        """Displays the game rules screen.

        Shows the screen with instructions and rules of the game.

        Returns:
        None
        """
        self.canvas.delete("all")
        
        # Create the background
        self.canvas.create_rectangle(0, 0, 1026, 646, fill='#b4b6fe')

        # Create the rules text with highlighted colors
        self.canvas.create_text(386, 100, text="You are the", fill="black",
                                font=("Arial", 24))
        self.canvas.create_text(555, 100, text="red", fill="red",
                                font=("Arial", 24))
        self.canvas.create_text(682, 100, text="square.", fill="black",
                                font=("Arial", 24))
        self.canvas.create_text(380, 180, text="Avoid the", fill="black",
                                font=("Arial", 24))
        self.canvas.create_text(538, 180, text="blue", fill="blue",
                                font=("Arial", 24))
        self.canvas.create_text(670, 180, text="circles.", fill="black",
                                font=("Arial", 24))
        self.canvas.create_text(512, 260,
                                text="Move to the green area to complete" +
                                " the level.", fill="black", font=("Arial", 24))
        self.canvas.create_text(155, 260, text="Move to the", fill="black",
                                font=("Arial", 24))
        self.canvas.create_text(356, 260, text="green", fill="green",
                                font=("Arial", 24))
        self.canvas.create_text(712, 260, text="area to complete the level.",
                                fill="black", font=("Arial", 24))
        self.canvas.create_text(512, 340,
                                text="The less times you die, the better.",
                                fill="black", font=("Arial", 24))

        # Create a "Play" button to start the game
        play_button = Button(self.canvas, text="Play Game",
                             command=self.start_game, font=("Arial", 16),
                             padx=20, pady=10)
        play_button_window = self.canvas.create_window(512, 500,
                                                       window=play_button)
    
    # Method to initialize game elements like the player, obstacles,
    # death counter, etc.
    def initialize_game_elements(self):
        """Initializes all game elements for a new game session.

        Sets up the player, obstacles, and other game elements to their initial
        state.

        Returns:
        None
        """
        self.canvas.delete("all")
        self.create_background()
        self.moving_objects = []
        
        # Add player
        self.player = Player(self.canvas, 178, 329, 31, 'red', 10, self)
        self.add_moving_object(self.player)
        
        # Display the death counter
        self.death_counter_disp = self.canvas.create_text(850, 26,
                                                          text=f"DEATHS: "+
                                                          f"{self.death_count}",
                                                             fill="white",
                                                             font=("Arial", 24))

        # Add moving obstacles (balls)
        ball1 = MovingObject(game.canvas, 302, 270, 24, 'blue', x_speed=9.5,
                             shape_type='oval', custom_attr='value')
        ball2 = MovingObject(game.canvas, 700, 313, 24, 'blue', x_speed=-9.5,
                             shape_type='oval', custom_attr='value')
        ball3 = MovingObject(game.canvas, 302, 356, 24, 'blue', x_speed=9.5,
                             shape_type='oval', custom_attr='value')
        ball4 = MovingObject(game.canvas, 700, 399, 24, 'blue', x_speed=-9.5,
                             shape_type='oval', custom_attr='value')

        game.add_moving_object(ball1)
        game.add_moving_object(ball2)
        game.add_moving_object(ball3)
        game.add_moving_object(ball4)
        
        # Rebind the key events to the new player object
        self.window.bind('<KeyPress>', self.player.key_down)
        self.window.bind('<KeyRelease>', self.player.key_up)
        
        self.game_over = False
          
    # Method to start the game, setting up the game elements and beginning the
    # animation loop 
    def start_game(self):
        """Starts the game.

        Triggers the beginning of the game, including setting up the
        environment and starting the animation loop.

        Returns:
        None
        """
        self.initialize_game_elements()
        self.window.bind('<KeyPress>', self.player.key_down)
        self.window.bind('<KeyRelease>', self.player.key_up)
        self.animate()
        
    # Method to create the game's background, including the grid, start and
    # end zones   
    def create_background(self):
        """Creates the game's background environment.

        Draws the background, grid, and start/end zones for the game.

        Returns:
        None
        """
        # Drawing background, grid, start and end zones
        green_color = '#befeb2'
        grey_color = '#e6e6ff'
        white_color = '#f7f7ff'
        square_size = 43
        start_x, start_y = 299, 259
        end_x, end_y = 729, 431
        
        # Create a purple rectangle as the background of the game area
        self.canvas.create_rectangle(0, 49, 1026, 646, fill='#b4b6fe')

        # Create a grid of squares for the player to move in
        num_squares_x = (end_x - start_x) // square_size
        num_squares_y = (end_y - start_y) // square_size

        for i in range(num_squares_x):
            for j in range(num_squares_y):
                corner_x = start_x + i * square_size
                corner_y = start_y + j * square_size
                color = grey_color if (i + j) % 2 == 0 else white_color
                self.canvas.create_rectangle(corner_x, corner_y, corner_x +
                                             square_size, corner_y +
                                             square_size, fill=color,
                                             outline='')

        self.canvas.create_rectangle(299, 431, 299 + square_size, 431 +
                                     square_size, fill=grey_color, outline='')
        self.canvas.create_rectangle(299 - 43, 431, 299 - 43 + square_size,
                                     431 + square_size, fill=white_color,
                                     outline='')
        self.canvas.create_rectangle(686, 216, 686 + square_size, 216 +
                                     square_size, fill=grey_color, outline='')
        self.canvas.create_rectangle(686 + 43, 216, 686 + 43 + square_size,
                                     216 + square_size, fill=white_color,
                                     outline='')
        
        # Start and end zones
        self.canvas.create_rectangle(132, 216, 256, 474, fill=green_color,
                                     outline='')
        self.canvas.create_rectangle(771, 216, 893, 474, fill=green_color,
                                     outline='')
        
        # Walls surrounding the game area
        wall_coords = [
            (127, 214, 260, 220), (127, 214, 133, 475), (127, 469, 345, 475),
            (255, 214, 261, 433), (255, 427, 302, 433), (296, 257, 302, 433),
            (296, 257, 685, 263), (679, 214, 685, 263), (679, 214, 898, 220),
            (892, 214, 898, 475), (339, 427, 345, 475), (339, 427, 724, 433),
            (724, 257, 730, 433), (724, 257, 771, 263), (765, 263, 771, 475),
            (765, 469, 898, 475)
        ]
        
        # Loop to add walls as a perimeter of the map
        for coords in wall_coords:
            self.canvas.create_rectangle(*coords, fill="black", outline='')
            self.walls.append(coords)  # Store wall coordinates


    # Method to add a moving object (like an obstacle) to the game
    def add_moving_object(self, obj):
        """Adds a moving object to the game.

        Args:
        obj (MovingObject): The moving object to be added.

        Returns:
        None
        """
        self.moving_objects.append(obj)

    # Method to reset the game to its initial state
    def reset_game(self):
        """Resets the game to its initial state.

        Returns:
        None
        """
        self.death_count = 0
        self.initialize_game_elements()
        self.animate()
        
        
    # Main game loop method to handle animation, movement of objects, and game
    # logic checks
    def animate(self):
        """Main animation loop for the game.

        Returns:
        None
        """
        if self.game_over:
            return
        
        for obj in self.moving_objects:
            obj.set_x(obj.get_x() + obj.x_speed)
            obj.set_y(obj.get_y() + obj.y_speed)

            if isinstance(obj, MovingObject) and obj.shape_type == 'oval':
                (leftpos, toppos, rightpos, bottompos) = \
                          self.canvas.coords(obj.shape)
                if leftpos <= 302 or rightpos >= 720:
                    obj.x_speed = -obj.x_speed

            # Check for collision with the player
            if isinstance(obj, MovingObject) and obj.shape_type == 'oval' and \
               self.check_collision(self.player, obj):
                # Reset player to starting position
                self.player.set_x(178)
                self.player.set_y(329)
                self.player.reduce_score()
                self.update_death_counter()  # Update the death counter
            
            # Proximity checking logic for collision debugging
            if isinstance(obj, MovingObject) and obj.shape_type == 'oval':
                player_center_x = self.player.get_x() + self.player.size / 2
                player_center_y = self.player.get_y() + self.player.size / 2
                obj_center_x = obj.get_x() + obj.size / 2
                obj_center_y = obj.get_y() + obj.size / 2

                # Debugging messages in the shell
                if Game.calculate_distance(player_center_x,
                                           player_center_y,
                                           obj_center_x, obj_center_y) < 50:
                    print("Player is close to an oval")

    
        
        self.check_victory()
        self.window.after(30, self.animate)
    
    # Static method to calculate the distance between two points, used in
    # collision detection
    @staticmethod
    def calculate_distance(x1, y1, x2, y2):
        """Calculates the Euclidean distance between two points.

        Args:
        x1 (float): x-coordinate of the first point.
        y1 (float): y-coordinate of the first point.
        x2 (float): x-coordinate of the second point.
        y2 (float): y-coordinate of the second point.

        Returns:
        float: The distance between the two points.
        """
        return ((x2 - x1)**2 + (y2 - y1)**2)**0.5
    
    
    # Method to calculate the distance from the player to the nearest obstacle
    # in the direction of movement
    def distance_to_obstacle(self, player, dx, dy):
        """Calculates the distance from the player to the nearest obstacle in
        the direction of movement.

        Args:
        player (Player): The player object.
        dx (int): The x-axis movement delta.
        dy (int): The y-axis movement delta.

        Returns:
        int: The minimum distance to the nearest obstacle.
        """

        # Start with the maximum possible distance (player's speed)
        min_distance = max(abs(dx), abs(dy))
        try:
            player_coords = self.canvas.coords(player.shape)
            for wall in self.walls:
                if dx > 0:  # Moving right
                    if player_coords[2] <= wall[0] and \
                       player_coords[3] > wall[1] and\
                       player_coords[1] < wall[3]:
                        min_distance = \
                                     min(min_distance,
                                         wall[0] - player_coords[2])
                elif dx < 0:  # Moving left
                    if player_coords[0] >= wall[2] and \
                       player_coords[3] > wall[1] \
                       and player_coords[1] < wall[3]:
                        min_distance = min(min_distance,
                                           player_coords[0] - wall[2])
                if dy > 0:  # Moving down
                    if player_coords[3] <= wall[1] and \
                       player_coords[2] > wall[0] \
                       and player_coords[0] < wall[2]:
                        min_distance = min(min_distance,
                                           wall[1] - player_coords[3])
                elif dy < 0:  # Moving up
                    if player_coords[1] >= wall[3] and \
                       player_coords[2] > wall[0] and \
                       player_coords[0] < wall[2]:
                        min_distance = min(min_distance,
                                           player_coords[1] - wall[3])
        
        except:
            pass
        
        return min_distance
    
    # Method to check for collisions between the player and walls and balls
    def check_collision(self, player, obj):
        """Checks for collisions between the player and other objects like
        walls and obstacles.

        Args:
        player (Player): The player object.
        obj (MovingObject): The object to check collision with.

        Returns:
        bool: True if there is a collision, False otherwise.
        """
        player_coords = self.canvas.coords(player.shape)
        
        # Check collision with walls
        for wall in self.walls:
            if (player_coords[2] > wall[0] and player_coords[0] < wall[2] and
                player_coords[3] > wall[1] and player_coords[1] < wall[3]):
                return True
        
        # Check collision with balls
        obj_coords = self.canvas.coords(obj.shape)
        return (player_coords[2] > obj_coords[0] and
                player_coords[0] < obj_coords[2] and
                player_coords[3] > obj_coords[1] and
                player_coords[1] < obj_coords[3])
    
        return False
    
    # Method to check and update the high score based on the player's
    # performance
    def check_new_high_score(self):
        """Checks and updates the game's high score based on the player's
        performance.

        Returns:
        str: Message indicating whether a new high score was achieved.
        """
        # Debugging messages to make sure score calculations are correct
        print(f"Current Player Score: {self.player.score}")
        print(f"Previous High Score: {Game.high_score}")

        # Check if the player's score is exactly 100
        if self.player.score == 100:
            # If the current high score is 100 or more, increase it by 10
            if Game.high_score >= 100:
                Game.high_score += 10
                self.player.score = Game.high_score
                print(f"High Score increased to: {Game.high_score}")
            else:
                # If the high score is less than 100, set it to the player's
                # score
                Game.high_score = self.player.score
                print("High Score updated to the player's " +
                      "score (less than 100).")
        elif self.player.score > Game.high_score:
            # If the player's score is higher than the high score but not
            # exactly 100
            Game.high_score = self.player.score
            print("High Score updated to a new higher player's score.")

        # Return appropriate message
        if self.player.score == Game.high_score:
            return "New high score!"
        else:
            return "Did not beat the high score."

    
    # Method to update the death counter displayed on the canvas
    def update_death_counter(self):
        """Updates the death counter displayed on the game canvas.

        Returns:
        None
        """
        global death_count
        self.death_count += 1
        self.canvas.itemconfigure(self.death_counter_disp,
                                  text=f"Deaths: {self.death_count}")
      
    # Method to check if the player has reached the victory zone
    def check_victory(self):
        """Checks if the player has reached the victory zone.

        Returns:
        None
        """
        player_coords = self.canvas.coords(self.player.shape)
        if (player_coords[2] > self.victory_zone[0] and
            player_coords[0] < self.victory_zone[2] and
            player_coords[3] > self.victory_zone[1] and
            player_coords[1] < self.victory_zone[3]):
            self.game_over = True
            self.display_victory_screen()

    # Method to animate the victory message on the victory screen
    def animate_victory_message(self):
        """Animates the victory message on the victory screen.

        Returns:
        None
        """
        speed_increment = 20
        letter_spacing = 65
        try:
            # Uses a sine wave to determine the positions of each letter
            for i, (letter_id, phase) in enumerate(self.letters):
                y_offset = 10 * math.sin(math.radians(phase))
                self.canvas.coords(letter_id,
                                   (550 - (letter_spacing *
                                           len("You Win!") // 2) + i *
                                    letter_spacing, 160 + y_offset))
                self.letters[i] = (letter_id, phase + speed_increment)

            if self.game_over:
                self.window.after(50, self.animate_victory_message)
        except:
            pass
     
    # Method to display the victory screen upon game completion 
    def display_victory_screen(self):
        """Displays the victory screen upon game completion.

        Returns:
        None
        """
        self.game_over = True
        self.canvas.delete("all")  # Clear the canvas
        
        # Display a background
        self.canvas.create_rectangle(0, 0, 1026, 646, fill='#b4b6fe')
        # Display victory messages
        self.canvas.create_text(1024/2, 330, text="Now try it with your " +
                                "eyes closed.", fill="black",
                                font=("Arial", 18))
        # Display death counter
        self.canvas.create_text(350, 400, text="Fails:", fill="black",
                                font=("Arial", 18))
        self.canvas.create_text(680, 400, text=f"{self.death_count}",
                                fill="black", font=("Arial", 18))
        
        # Check for a new high score and display the result
        high_score_message = self.check_new_high_score()
        self.canvas.create_text(1024/2, 275, text=high_score_message,
                                fill="black", font=("Arial", 18))        

        message = "You Win!"
        letter_spacing = 65  
        x_start = 550 - (letter_spacing * len(message) // 2)  

        # Used to animate the You Win message
        self.letters = []
        for i, letter in enumerate(message):
            letter_id = self.canvas.create_text(x_start + i * letter_spacing,
                                                160, text=letter,
                                                fill="#000066",
                                                font=("Arial", 50))
            initial_phase = i * 10  # Different initial phase for each letter
            self.letters.append((letter_id, initial_phase))

        # Play again button
        play_again_button = Button(self.canvas, text="Play Again",
                                   command=self.reset_game,
                                   font=("Arial", 16), padx=20, pady=10)
        play_again_but_win = self.canvas.create_window(512, 500,
                                                       window=play_again_button)
        
        self.animate_victory_message()
      
    # Method to run the game, starting with the start screen and entering the
    # main event loop
    def run(self):
        """Starts the game by showing the start screen and entering the main
        event loop.

        Returns:
        None
        """
        self.show_start_screen()
        self.window.mainloop()

def main():
    global game
    """Main function to initialize and run the game.

    Returns:
    None
    """
    game = Game.create_default_game()
    game.run()

# This ensures that the main function is called only when the script is
# executed directly
if __name__ == "__main__":
    main()